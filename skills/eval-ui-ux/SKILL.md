---
name: eval-ui-ux
description: "Specialized UI/UX evaluator for the Evaluate-Loop. Use this for evaluating UI shell tracks, design system tracks, screen implementation tracks, or any track where the primary deliverable is visual/interactive UI. Checks design system adherence, visual consistency, layout structure, responsive behavior, component states, animations, accessibility baseline, and usability check (copy quality). Dispatched by loop-execution-evaluator when track type is 'ui', 'design-system', or 'screens'. Triggered by: 'evaluate UI', 'UI review', 'design review', 'visual audit'."
---

# UI/UX Evaluator Agent

Specialized evaluator for tracks whose deliverables are visual UI — screens, components, design systems, layouts.

## When This Evaluator Is Used

Dispatched by `loop-execution-evaluator` when the track is one of:
- Screen implementation
- Design system work
- Component library
- UI polish or UX audit

## Inputs Required

1. Track's `spec.md` — what was supposed to be built
2. Track's `plan.md` — tasks that should be complete
3. Design system reference — your project's global CSS or token file (e.g., `src/app/globals.css`)
4. Components to evaluate — all files in `src/components/` and `src/app/`
5. Data files — content JSON files used for copy (if applicable)

## Evaluation Passes (8 checks)

### Pass 1: Design System Adherence

Read your project's CSS/token file to extract the token system, then check components:

| Check | What to Look For |
|-------|-----------------|
| Colors | CSS custom properties (`--color-*`, `--brand-*`) used, no raw hex/rgb in components |
| Spacing | Tailwind spacing classes follow consistent grid, no arbitrary `px` values |
| Typography | Font families from your design system fonts, sizes from scale |
| Radius | Uses token-defined radius values, no random `rounded-*` overrides |
| Shadows | Shadow classes from token system, consistent elevation levels |
| Glass-morphism | Backdrop-blur, bg-opacity patterns on cards/modals/overlays (if applicable) |

```markdown
### Design System Adherence: PASS / FAIL
- Hardcoded colors found: [count] — [list files:lines]
- Hardcoded spacing found: [count] — [list files:lines]
- Typography violations: [count] — [list]
- Token coverage: [X]% of visual properties use design tokens
```

### Pass 2: Visual Consistency

Compare styling patterns across screens:

| Check | What to Look For |
|-------|-----------------|
| Spacing rhythm | Same gap/padding patterns across sections |
| Color usage | Brand palette applied consistently (not random grays) |
| Component styling | Same component (Card, Button) looks identical on all pages |
| Icon sizing | Icons use consistent size props |
| Page structure | Similar content types have similar visual treatment |

```markdown
### Visual Consistency: PASS / FAIL
- Inconsistencies found: [count]
- Affected screens: [list]
- Specific issues: [describe each]
```

### Pass 3: Layout & Structure

| Check | What to Look For |
|-------|-----------------|
| Header presence | Header component rendered on every page (or layout group) |
| Footer presence | Footer component rendered on every page |
| Container usage | Max-width Container wraps content on all pages |
| Section usage | Vertical spacing via Section component |
| Visual hierarchy | h1 → h2 → body → actions ordering clear |
| Content width | No full-bleed text blocks (constrained width) |

```markdown
### Layout & Structure: PASS / FAIL
- Pages missing Header: [list]
- Pages missing Footer: [list]
- Pages missing Container: [list]
- Hierarchy issues: [describe]
```

### Pass 4: Responsive Behavior

Check component classes and layout patterns:

| Breakpoint | What to Check |
|-----------|---------------|
| 375px (mobile) | Single column, stacked layout, touch-friendly |
| 768px (tablet) | 2-column grids, adjusted spacing |
| 1024px+ (desktop) | Full layout, 3-4 column grids |

| Check | What to Look For |
|-------|-----------------|
| Grid collapse | `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` patterns |
| Horizontal scroll | No `overflow-x` issues, no fixed-width elements |
| Touch targets | Buttons/links >= 44px on mobile (`min-h-11`, `p-3`, etc.) |
| Mobile menu | Header collapses to hamburger/sheet on mobile |
| Text truncation | Long text doesn't break layout |

```markdown
### Responsive: PASS / FAIL
- Breakpoints covered: [375/768/1024]
- Pages with issues: [list]
- Touch target violations: [list components]
```

### Pass 5: Component States & Conditional Rendering

Check interactive components for complete state coverage and safe rendering logic:

| Component Type | Required States |
|---------------|----------------|
| Button | default, hover, active, focus, disabled, loading |
| Input | default, focus, error, disabled, placeholder |
| Card | default, hover (if interactive) |
| Modal | open/close animation, backdrop, focus trap, escape-to-close |
| Toast | success, error, info variants |
| Loading | spinner or skeleton for every async operation |

**Conditional Rendering Patterns to Check:**

| Anti-Pattern | What to Flag | Fix |
|--------------|--------------|-----|
| Magic string comparison | `status === 'ready' && <Image />` | Use explicit arrays: `['ready', 'locked'].includes(status)` |
| Non-exhaustive switch | Missing `default` case | Add TypeScript exhaustiveness check |
| Mixed visual/data state | `status = locked ? 'locked' : 'ready'` | Separate: `const isLocked = item.locked; const hasContent = !!imageUrl;` |
| Status explosion | 7+ status codes | Split into orthogonal states |

**Example Brittle Pattern:**

```typescript
// BAD: Image disappears when status changes
{imageUrl && status === 'ready' && <Image />}
// When item is locked, status becomes 'locked' → image hidden!

// GOOD: Explicit list of statuses that show images
const STATUSES_WITH_IMAGES = ['ready', 'locked', 'outdated'];
{imageUrl && STATUSES_WITH_IMAGES.includes(status) && <Image />}

// BETTER: Separate concerns
const shouldShowImage = imageUrl && !['generating', 'error'].includes(status);
{shouldShowImage && <Image />}
```

```markdown
### Component States & Rendering: PASS / FAIL
- Missing states: [component: missing state]
- Components audited: [count]
- Coverage: [X]% have all required states
- **Brittle conditionals found: [count] — [list files:lines]**
- **Non-exhaustive switches: [count] — [list]**
- **Status explosion (>7 codes): [list components]**
```

### Pass 6: Animation & Transitions

| Check | What to Look For |
|-------|-----------------|
| Page transitions | Page transition wrapper or framer-motion layout |
| Hover effects | Subtle scale/shadow/opacity changes on interactive elements |
| Loading animations | Spinner/skeleton with smooth animation |
| Modal transitions | Fade/scale on open/close |
| State transitions | No sudden jumps between states |

```markdown
### Animations: PASS / FAIL
- Pages missing transitions: [list]
- Components missing hover effects: [list]
- Jarring state changes: [describe]
```

### Pass 7: Accessibility Baseline

| Check | WCAG Level | What to Look For |
|-------|-----------|-----------------|
| Labels | A | All `<input>` elements have associated `<label>` |
| Button text | A | All buttons have visible text or `aria-label` |
| Alt text | A | All `<img>` elements have meaningful `alt` |
| Color contrast | AA | Text/background contrast >= 4.5:1 (body), >= 3:1 (large) |
| Focus visible | AA | Focus ring visible on all interactive elements |
| Focus order | A | Tab order follows visual reading order |
| Modal focus | A | Modal traps focus when open |

```markdown
### Accessibility: PASS / FAIL
- Missing labels: [list inputs]
- Missing alt text: [list images]
- Contrast issues: [list]
- Focus order issues: [describe]
```

### Pass 8: Usability Check (Copy Quality)

Read all user-facing text in components and data files:

| Check | What to Look For |
|-------|-----------------|
| Headings | Simple, friendly, no jargon |
| CTAs | Action verbs that clearly describe the outcome |
| Errors | Tell user what to do, not technical details |
| Labels | Everyday language (e.g., "Your name", not "Name identifier") |
| Jargon | No: "auth", "render", "deps", "schema", "API", "submit" |
| Tone | Reassuring, not pushy (especially paywall, error states) |

Verify against your target personas — would they understand every piece of text without explanation?

```markdown
### Usability Check: PASS / FAIL
- Jargon found: [word: file:line]
- Unfriendly copy: [text: file:line]
- Suggested rewrites: [original → suggested]
```

## Verdict Template

```markdown
## UI/UX Evaluation Report

**Track**: [track-id]
**Evaluator**: eval-ui-ux
**Date**: [YYYY-MM-DD]
**Screens Evaluated**: [count]

### Results
| Pass | Status | Issues |
|------|--------|--------|
| 1. Design System | PASS/FAIL | [count] issues |
| 2. Visual Consistency | PASS/FAIL | [count] issues |
| 3. Layout & Structure | PASS/FAIL | [count] issues |
| 4. Responsive | PASS/FAIL | [count] issues |
| 5. Component States | PASS/FAIL | [count] issues |
| 6. Animations | PASS/FAIL | [count] issues |
| 7. Accessibility | PASS/FAIL | [count] issues |
| 8. Usability Check | PASS/FAIL | [count] issues |

### Verdict: PASS / FAIL
[If FAIL, list specific fix actions for loop-fixer]
```

## Handoff

- **PASS** → Return to `loop-execution-evaluator` → Conductor marks complete
- **FAIL** → Return to `loop-execution-evaluator` → Conductor dispatches `loop-fixer`
