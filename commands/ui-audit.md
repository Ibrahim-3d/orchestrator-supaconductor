---
name: ui-audit
description: "Run comprehensive UI/UX design validation against design principles, accessibility standards, and usability laws"
arguments:
  - name: target
    description: "Component path, page URL, or --browser flag for live testing"
    required: false
user_invocable: true
---

# /ui-audit

Run comprehensive UI/UX design validation against established design principles, usability laws, accessibility standards, and cognitive psychology principles.

## When to Use

Run this command:
- After completing UI component implementation
- Before marking a UI-related track complete
- When you need to validate designs against design laws
- To check WCAG accessibility compliance
- To audit cognitive load and usability issues
- For automated browser-based visual testing

## What It Does

The command launches the **ui-design-tester** agent which:

1. **Validates Design Principles**
   - Miller's Law (cognitive load, 7+/-2 items)
   - Fitts's Law (button sizes, touch targets)
   - Jakob's Law (familiar conventions)
   - Hick's Law (choice overload)
   - Usability check (representativeness heuristic)

2. **Checks Accessibility**
   - WCAG 2.1 contrast ratios (4.5:1, 3:1, 7:1)
   - Semantic HTML and ARIA labels
   - Keyboard navigation
   - Screen reader support

3. **Audits Visual Design**
   - Typography (sizes, hierarchy, readability)
   - Color theory (palette, semantic colors)
   - Spacing and layout consistency
   - Visual hierarchy

4. **Live Browser Testing** (ALWAYS)
   - agent-browser CLI integration for live testing
   - Screenshot capture and analysis
   - Real DOM measurements (button sizes, spacing)
   - Contrast ratio extraction from rendered elements

## Usage

### Basic Usage (Live Browser Testing)
```bash
/ui-audit
```
Launches agent-browser to test your live application for UI/UX issues.

### Specific Component
```bash
/ui-audit src/components/feature/my-card.tsx
```
Audits a specific component file.

### Automated Browser Testing
```bash
/ui-audit --browser /create
```
Launches browser automation to test a specific page visually.

### Multiple Pages
```bash
/ui-audit --browser / /create /dashboard
```
Tests multiple pages in sequence.

## Evaluation Criteria

The agent checks against these standards:

### Critical Issues
- WCAG AA failures (contrast < 4.5:1)
- Inaccessible interactive elements
- Major usability blockers
- Missing semantic HTML

### Moderate Issues
- Design principle violations
- Inconsistent patterns
- Usability friction
- Minor accessibility issues

### Minor Improvements
- Polish opportunities
- Micro-interaction improvements
- Nice-to-have enhancements

## Output Format

The agent generates a structured audit report:

```markdown
# UI Design Audit Report

## Component: [Name]
**File**: [path:line]
**Overall Score**: [0-100]

## Critical Issues (Fix Immediately)
### 1. Button Too Small - Fitts's Law Violation
**Severity**: Critical
**Location**: src/components/ui/button.tsx:24
**Problem**: Button is 28x28px, below minimum 32x32px (desktop)
**Impact**: Users will struggle to click, especially on mobile
**Fix**:
\`\`\`tsx
// Before
<Button className="h-7 w-7">

// After
<Button className="h-8 w-8"> {/* 32x32px minimum */}
\`\`\`

## Positive Findings
- Clear visual hierarchy
- Consistent spacing scale
- Good color contrast on primary CTAs

## Summary & Priority Matrix
| Priority | Issue | Impact | Effort |
|----------|-------|--------|--------|
| 1 | Button sizing | High | Low |
| 2 | Menu item count | Medium | Medium |
```

## Browser Testing Workflow

The agent ALWAYS uses live browser testing with agent-browser:

1. **Checks dev server** - Verifies `npm run dev` is running
2. **Launches agent-browser** - Opens Chromium and navigates to your app
3. **Captures page state** - Accessibility tree snapshots and screenshots
4. **Measures elements** - Real DOM measurements for button sizes, spacing, colors
5. **Extracts data** - Gets computed styles, contrast ratios, element counts
6. **Analyzes visually** - Screenshot-based principle validation
7. **Generates report** - Evidence-based findings with real measurements

## Integration with Evaluate-Loop

This command is automatically used by:
- **loop-execution-evaluator** → Dispatches to **eval-ui-ux** → Uses this command
- **eval-ui-ux** → Specialized UI evaluator that validates design system consistency

You can also run it manually during development.

## Design Principles Reference

### Miller's Law
- Navigation: 5-9 items max
- Forms: 5-9 fields per section
- Lists: Chunk appropriately

### Fitts's Law
- Mobile buttons: 44x44px minimum
- Desktop buttons: 32x32px minimum
- Touch spacing: 8px between targets

### Jakob's Law
- Logo top-left → homepage
- Navigation in header
- Search top-right
- Primary button on right

### Usability Check
- Icons represent functions intuitively
- Labels match user mental models
- Categories follow user thinking, not system architecture

### WCAG Contrast
- Normal text: 4.5:1 (AA), 7:1 (AAA)
- Large text: 3:1 (AA), 4.5:1 (AAA)
- UI components: 3:1 minimum

## Examples

### Example 1: Audit After Component Work
```bash
# After finishing button component
/ui-audit src/components/ui/button.tsx
```

### Example 2: Pre-Launch Check
```bash
# Before shipping new feature
/ui-audit --browser /create /results
```

### Example 3: Full App Audit
```bash
# Audit entire component library
/ui-audit src/components/
```

## Related

- **Agent**: `.claude/plugin/ui-design-validator/agents/ui-design-tester.md`
- **Design Principles**: `.claude/plugin/ui-design-validator/DESIGN_PRINCIPLES.md`
- **Examples**: `.claude/plugin/ui-design-validator/EXAMPLES.md`
- **Evaluate-Loop**: `conductor/workflow.md`
- **eval-ui-ux**: `.claude/skills/eval-ui-ux/SKILL.md`

## Tips

1. **Run early and often** - Catch issues during development
2. **Use browser testing for critical pages** - Visual validation catches more
3. **Focus on top 3-5 issues** - Don't get overwhelmed
4. **Check mobile and desktop** - Responsive design needs both
5. **Apply usability check** - Would a non-technical user understand this?
6. **Celebrate good patterns** - Note what works well to reinforce it
