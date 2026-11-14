---
name: LeetCode firmware review checklist
description: The R3 firmware-style checklist for reviewing a C/C++ LeetCode solution, with what to look for in each item and how to report a finding.
---

# Firmware review checklist for a LeetCode solution

Read `solution.c`, `test.c`, `notes.md` of the problem and the problem statement (LeetCode link in the header comment of `solution.c`). Recall the official constraints of the problem; if unsure, state the assumed constraints explicitly.

## 1. Correctness
- Does the algorithm answer the problem for **all** inputs within the constraints, not just the examples?
- Probe edge cases: empty / size 1 / size 2, all equal, already sorted / reverse sorted, negatives, zero, `INT_MIN` / `INT_MAX`, duplicates, target not present, answer at first / last index, max-size input.
- Off-by-one in loop bounds, loop start indices, inclusive vs exclusive ranges, early `return` placement.
- If wrong: give a **concrete counterexample** (input, expected, actual) and show the trace that produces the wrong output.

## 2. Pointers, buffers and `\0`
- Every array index provably within `[0, size)`; no read past the size, no `arr[-1]`.
- Strings: room for the terminating `\0`, `strlen` not called in a loop condition, no writing into string literals.
- `NULL` checks where LeetCode can pass `NULL` / empty lists / empty trees.
- Returned arrays: `*returnSize` set on **every** path, including early returns.

## 3. Ownership and `free`
- Memory returned to LeetCode must be `malloc`ed (caller frees); never return a pointer to a stack array.
- Every temporary `malloc`/`calloc` freed on every path, including early returns. Check `malloc` size arithmetic (`n * sizeof *p`) for overflow.
- Do not free memory owned by the caller (input lists/trees) unless the problem says so.

## 4. Integer types, overflow, shifts
- Sums / products / differences of two `int`s that can overflow (`a + b`, `mid = (lo + hi) / 2`, `a - b` in comparators, `abs(INT_MIN)`).
- Signed/unsigned mixing in comparisons (`int i < size_t n`), `unsigned` loop counters going below 0.
- Shift count `>= width` or shifting negative values is UB; `1 << 31` on `int` is UB.
- `qsort` comparators must not use `return a - b` when values can overflow.

## 5. Complexity (time and space, including the call stack)
- Derive time complexity from the loop structure / recurrence; state the dominant term.
- Space: extra heap + **recursion depth** (worst-case stack frames, e.g. O(n) for a skewed tree).
- Compare against the constraints: with n = 10^5, O(n^2) = 10^10 operations → TLE. Say whether it would pass.

## 6. Style that matters in interviews (brief)
- Naming, dead code, unnecessary work, `-Wall -Wextra -Werror` cleanliness.

## How to report each finding

Specialist reviewers report to the coach (internal, English) and may name the exact cause:

```
[severity] <checklist item> – <file>:<line>
What: <the problem, one sentence>
Why: <why it is wrong / risky, with counterexample or trace>
Cause (internal only): <exact faulty expression and why it fails>
Hint: <one guiding question or nudge – NOT the fix>
```

The `Cause` line is for the coach and auditor only and must **never** reach the user-facing report (see `lc-hint-ladder`).

Severity: **BUG** (wrong answer / crash / UB), **TLE/MLE** (too slow or too big for the constraints), **RISK** (works on LeetCode tests but fragile), **NIT** (style). If an item has no finding, write "OK" with one line of evidence – do not skip it.
