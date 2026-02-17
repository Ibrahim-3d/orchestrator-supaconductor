#!/usr/bin/env python3
"""
Monitor message bus for a track.

Usage:
    python monitor-bus.py <track_path> [--watch]
    python monitor-bus.py conductor/tracks/feature-xyz_20260201 --watch

Shows current state and optionally watches for new messages.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


def read_jsonl(filepath: str) -> list:
    """Read JSONL file and return list of objects."""
    if not os.path.exists(filepath):
        return []

    messages = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                messages.append(json.loads(line))
    return messages


def read_json(filepath: str) -> dict:
    """Read JSON file and return dict."""
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r") as f:
        return json.load(f)


def check_stale_workers(statuses: dict, threshold_minutes: int = 10) -> list:
    """Find workers with no heartbeat for threshold_minutes."""
    stale = []
    now = datetime.utcnow()

    for worker_id, status in statuses.items():
        if status.get("status") == "RUNNING":
            last_heartbeat = status.get("last_heartbeat")
            if last_heartbeat:
                hb_time = datetime.fromisoformat(last_heartbeat.replace("Z", ""))
                if now - hb_time > timedelta(minutes=threshold_minutes):
                    stale.append({
                        "worker_id": worker_id,
                        "task_id": status.get("task_id"),
                        "last_heartbeat": last_heartbeat,
                        "minutes_stale": int((now - hb_time).total_seconds() / 60)
                    })

    return stale


def check_expired_locks(locks: dict) -> list:
    """Find expired file locks."""
    expired = []
    now = datetime.utcnow()

    for filepath, lock in locks.items():
        expires_at = lock.get("expires_at")
        if expires_at:
            exp_time = datetime.fromisoformat(expires_at.replace("Z", ""))
            if exp_time < now:
                expired.append({
                    "filepath": filepath,
                    "worker_id": lock.get("worker_id"),
                    "expired_at": expires_at,
                    "minutes_expired": int((now - exp_time).total_seconds() / 60)
                })

    return expired


def detect_deadlocks(statuses: dict, messages: list) -> list:
    """Detect circular wait patterns."""
    # Build wait-for graph from BLOCKED messages
    wait_for = {}

    for msg in messages:
        if msg.get("type") == "BLOCKED":
            source = msg.get("source")
            waiting_for = msg.get("payload", {}).get("waiting_for")
            if source and waiting_for:
                wait_for[source] = waiting_for

    # Detect cycles
    def find_cycle(start, visited, path):
        if start in path:
            return path[path.index(start):]
        if start in visited:
            return []
        visited.add(start)
        path.append(start)
        if start in wait_for:
            cycle = find_cycle(wait_for[start], visited, path)
            if cycle:
                return cycle
        path.pop()
        return []

    visited = set()
    for worker in wait_for:
        cycle = find_cycle(worker, visited, [])
        if cycle:
            return cycle

    return []


def print_status(bus_path: str):
    """Print current message bus status."""
    queue_file = os.path.join(bus_path, "queue.jsonl")
    locks_file = os.path.join(bus_path, "locks.json")
    status_file = os.path.join(bus_path, "worker-status.json")

    messages = read_jsonl(queue_file)
    locks = read_json(locks_file)
    statuses = read_json(status_file)

    print("\n" + "=" * 60)
    print(f"MESSAGE BUS STATUS - {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    # Message summary
    print(f"\nMESSAGES: {len(messages)} total")
    msg_types = {}
    for msg in messages:
        t = msg.get("type", "UNKNOWN")
        msg_types[t] = msg_types.get(t, 0) + 1

    for msg_type, count in sorted(msg_types.items()):
        print(f"   {msg_type}: {count}")

    # Worker status
    print(f"\nWORKERS: {len(statuses)} registered")
    for worker_id, status in statuses.items():
        state = status.get("status", "?")
        print(f"   [{state}] {worker_id}")
        print(f"      Task: {status.get('task_id')}")
        print(f"      Status: {status.get('status')} ({status.get('progress_pct', 0)}%)")

    # Stale workers
    stale = check_stale_workers(statuses)
    if stale:
        print(f"\nSTALE WORKERS: {len(stale)}")
        for sw in stale:
            print(f"   {sw['worker_id']} - {sw['minutes_stale']} min since heartbeat")

    # File locks
    active_locks = {k: v for k, v in locks.items()
                   if datetime.fromisoformat(v.get("expires_at", "2000-01-01").replace("Z", "")) > datetime.utcnow()}

    print(f"\nACTIVE LOCKS: {len(active_locks)}")
    for filepath, lock in active_locks.items():
        print(f"   {filepath}")
        print(f"      Held by: {lock.get('worker_id')}")
        print(f"      Expires: {lock.get('expires_at')}")

    # Expired locks
    expired = check_expired_locks(locks)
    if expired:
        print(f"\nEXPIRED LOCKS: {len(expired)}")
        for el in expired:
            print(f"   {el['filepath']} - expired {el['minutes_expired']} min ago")

    # Deadlock detection
    deadlock = detect_deadlocks(statuses, messages)
    if deadlock:
        print(f"\nDEADLOCK DETECTED!")
        print(f"   Cycle: {' -> '.join(deadlock)} -> {deadlock[0]}")

    # Recent messages
    print(f"\nRECENT MESSAGES (last 5):")
    for msg in messages[-5:]:
        print(f"   [{msg.get('timestamp', '?')}] {msg.get('type')} from {msg.get('source')}")

    # Board status
    board_path = os.path.join(bus_path, "board")
    if os.path.exists(board_path):
        assessments = read_json(os.path.join(board_path, "assessments.json"))
        votes = read_json(os.path.join(board_path, "votes.json"))

        if assessments or votes:
            print(f"\nBOARD STATUS:")
            print(f"   Assessments: {len(assessments)}/5 directors")
            print(f"   Votes: {len(votes)}/5 directors")

            if votes:
                approve = sum(1 for v in votes.values() if v.get("final_verdict") == "APPROVE")
                reject = len(votes) - approve
                print(f"   Current tally: {approve} APPROVE / {reject} REJECT")


def watch_bus(bus_path: str, interval: int = 5):
    """Watch message bus for changes."""
    print(f"Watching message bus at: {bus_path}")
    print(f"Refresh interval: {interval} seconds")
    print("Press Ctrl+C to stop\n")

    last_msg_count = 0

    try:
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')

            print_status(bus_path)

            # Check for new messages
            queue_file = os.path.join(bus_path, "queue.jsonl")
            messages = read_jsonl(queue_file)

            if len(messages) > last_msg_count:
                new_count = len(messages) - last_msg_count
                print(f"\n{new_count} new message(s) since last check")
                last_msg_count = len(messages)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nStopped watching.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor-bus.py <track_path> [--watch]")
        print("Example: python monitor-bus.py conductor/tracks/feature-xyz_20260201 --watch")
        sys.exit(1)

    track_path = sys.argv[1]
    watch_mode = "--watch" in sys.argv

    bus_path = os.path.join(track_path, ".message-bus")

    if not os.path.exists(bus_path):
        print(f"Error: Message bus not found at: {bus_path}")
        print("Run init-bus.py first to initialize the message bus.")
        sys.exit(1)

    if watch_mode:
        watch_bus(bus_path)
    else:
        print_status(bus_path)


if __name__ == "__main__":
    main()
