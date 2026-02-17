# UI/UX Audit Report Template
**Date:** [YYYY-MM-DD]
**Auditor:** Claude Code (Automated Browser Testing)
**Methodology:** Live browser testing with agent-browser CLI, accessibility tree analysis, DOM measurements

---

## Executive Summary

[Brief summary of audit findings, highlighting strengths and critical issues.]

### Overall Grade: **[A-F] ([0-100]/100)**

**Breakdown:**
- Touch Targets & Sizing: [0-100]/100
- Color Contrast: [0-100]/100
- Cognitive Load: [0-100]/100
- Typography: [0-100]/100
- Responsive Design: [0-100]/100

---

## Critical Issues (Fix Immediately)

### 1. [Issue Title]

**Severity:** P0 - [Category]
**Impact:** [Description of user/business impact]

#### Evidence:

[Measurements, screenshots, and data from live browser testing]

#### Root Cause:

[Code analysis showing the source of the issue]

#### Fix:

[Specific code changes with before/after examples]

**File to fix:** `[path/to/file.tsx]`

---

## Moderate Issues (Should Fix)

### [N]. [Issue Title]

**Severity:** P1
**Impact:** [Description]

#### Evidence:

[Measurements and data]

#### Fix:

[Recommended changes]

---

## Minor Improvements (Nice to Have)

### [N]. [Issue Title]

[Description and recommendations]

---

## Positive Findings (What Works Well)

### [Category]
[List of things done well with evidence]

---

## Design Principle Analysis

### Miller's Law (5-9 items for working memory)

| Element | Count | Status | Notes |
|---------|-------|--------|-------|
| Navigation items | [N] | [Status] | [Notes] |
| Form fields | [N] | [Status] | [Notes] |
| Choice options | [N] | [Status] | [Notes] |
| Pricing tiers | [N] | [Status] | [Notes] |

### Fitts's Law (Touch target sizing)

| Element | Size | Minimum | Status |
|---------|------|---------|--------|
| Header buttons | [W]x[H]px | 44x44px | [Status] |
| CTAs | [W]x[H]px | 44x44px | [Status] |
| Cards | [W]x[H]px | 44x44px | [Status] |

### Jakob's Law (Familiarity)

- [x/missing] Logo in top-left links to home
- [x/missing] Sign In / Sign Up in top-right
- [x/missing] Footer with legal links
- [x/missing] Standard layout patterns
- [x/missing] Step-by-step form follows expected pattern

### Hick's Law (Choice paralysis)

- [Status] [Element]: [N] options ([assessment])
- [Status] [Element]: [N] options ([assessment])

### Usability Check (Non-technical user comprehension)

- [Status] [Label/Copy assessment]
- [Status] [Navigation assessment]
- [Status] [Feature naming assessment]

---

## WCAG 2.1 Level AA Compliance

### Summary:
- **Color Contrast:** [PASS/FAIL] ([details])
- **Touch Targets:** [PASS/FAIL] ([details])
- **Semantic HTML:** [PASS/FAIL] ([details])
- **Keyboard Navigation:** [PASS/FAIL] ([details])

### Contrast Requirements:

| Element Type | Required Ratio | Status |
|-------------|----------------|--------|
| Normal text (< 18pt) | 4.5:1 | [Status with measured ratio] |
| Large text (>= 18pt) | 3:1 | [Status with measured ratio] |
| UI components | 3:1 | [Status with measured ratio] |

---

## Priority Matrix

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| [Issue 1] | [HIGH/MEDIUM/LOW] | [HIGH/MEDIUM/LOW] | **P0** |
| [Issue 2] | [HIGH/MEDIUM/LOW] | [HIGH/MEDIUM/LOW] | **P1** |
| [Issue 3] | [HIGH/MEDIUM/LOW] | [HIGH/MEDIUM/LOW] | **P2** |

---

## Recommended Fixes (Code Snippets)

### Fix 1: [Title] (P0)

**File:** `[path/to/file.tsx]`

```tsx
// BEFORE
[original code]

// AFTER
[fixed code]
```

**Verification:** [How to verify the fix works]

---

## Testing Checklist

Before marking this audit complete, verify:

- [ ] Run automated contrast checker on all buttons
- [ ] Test keyboard navigation through entire flow
- [ ] Verify ARIA labels on all interactive elements
- [ ] Test screen reader compatibility
- [ ] Validate mobile responsiveness at 320px, 375px, 768px, 1024px
- [ ] Run Lighthouse accessibility audit (target: 90+)
- [ ] Verify focus indicators visible on all interactive elements

---

## Screenshots & Evidence

**Stored in:** `[path/to/screenshots/]`

1. `[screenshot-1.png]` - [Description]
2. `[screenshot-2.png]` - [Description]

---

## Next Steps

1. **Immediate (This Week):**
   - [P0 fixes with estimated effort]

2. **Short-term (Next Sprint):**
   - [P1 fixes with estimated effort]

3. **Medium-term (Next Month):**
   - [P2 fixes and improvements]

---

## Conclusion

[Summary of findings, key takeaways, and overall assessment.]

**Priority:** [Key recommendation before launch/release]

**Estimated effort:** [Total hours for all P0 fixes]

---

**Audit completed:** [Date]
**Evidence-based:** Live browser measurements, DOM inspection, accessibility tree analysis
**Tools used:** agent-browser CLI, Chrome DevTools, manual WCAG calculations
