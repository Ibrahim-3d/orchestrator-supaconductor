#!/usr/bin/env python3
"""
Initialize message bus for a track.

Usage:
    python init-bus.py <track_path>
    python init-bus.py conductor/tracks/feature-xyz_20260201

Creates the message bus directory structure for inter-agent coordination.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def init_message_bus(track_path: str) -> str:
    """Initialize message bus directory structure for a track."""

    bus_path = os.path.join(track_path, ".message-bus")

    # Create directories
    os.makedirs(bus_path, exist_ok=True)
    os.makedirs(os.path.join(bus_path, "events"), exist_ok=True)
    os.makedirs(os.path.join(bus_path, "board"), exist_ok=True)

    # Initialize queue.jsonl (append-only message log)
    queue_file = os.path.join(bus_path, "queue.jsonl")
    if not os.path.exists(queue_file):
        Path(queue_file).touch()
        # Write initialization message
        init_msg = {
            "id": "msg-init",
            "type": "BUS_INIT",
            "source": "init-bus.py",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "track_path": track_path,
                "version": "1.0"
            }
        }
        with open(queue_file, "w") as f:
            f.write(json.dumps(init_msg) + "\n")

    # Initialize locks.json
    locks_file = os.path.join(bus_path, "locks.json")
    if not os.path.exists(locks_file):
        with open(locks_file, "w") as f:
            json.dump({}, f, indent=2)

    # Initialize worker-status.json
    status_file = os.path.join(bus_path, "worker-status.json")
    if not os.path.exists(status_file):
        with open(status_file, "w") as f:
            json.dump({}, f, indent=2)

    # Initialize board files
    board_path = os.path.join(bus_path, "board")

    assessments_file = os.path.join(board_path, "assessments.json")
    if not os.path.exists(assessments_file):
        with open(assessments_file, "w") as f:
            json.dump({}, f, indent=2)

    votes_file = os.path.join(board_path, "votes.json")
    if not os.path.exists(votes_file):
        with open(votes_file, "w") as f:
            json.dump({}, f, indent=2)

    discussion_file = os.path.join(board_path, "discussion.jsonl")
    if not os.path.exists(discussion_file):
        Path(discussion_file).touch()

    return bus_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python init-bus.py <track_path>")
        print("Example: python init-bus.py conductor/tracks/feature-xyz_20260201")
        sys.exit(1)

    track_path = sys.argv[1]

    if not os.path.exists(track_path):
        print(f"Error: Track path does not exist: {track_path}")
        sys.exit(1)

    bus_path = init_message_bus(track_path)

    print(f"Message bus initialized at: {bus_path}")
    print("\nCreated structure:")
    print(f"  {bus_path}/")
    print("  ├── queue.jsonl")
    print("  ├── locks.json")
    print("  ├── worker-status.json")
    print("  ├── events/")
    print("  └── board/")
    print("      ├── assessments.json")
    print("      ├── votes.json")
    print("      └── discussion.jsonl")


if __name__ == "__main__":
    main()
