---
name: Trace and verify claims
description: How to back every correctness or complexity claim with a hand trace or an actual run (rule R5) before putting it in a review.
---

# Trace and verify before asserting (R5)

A review claim without evidence is not allowed. For every claim, attach one of:

## A. Actual run (preferred when possible)
1. Run the local harness: `python tools/build_test.py c/<topic>/<id>_<slug>` and quote the status line and any `LC_CHECK` failure output (use repo-relative paths, not absolute workspace paths).
2. If available, also try `--sanitize` and quote any ASan/UBSan report. If the toolchain is missing, say so – do not pretend it ran.
3. If a counterexample is not covered by `test.c`, do **not** edit `test.c` or `solution.c`. Instead report the exact `LC_CHECK(...)` line the user could add, and back the claim with a hand trace (B).

## B. Hand trace on a small input
Use a table of the relevant variables per iteration. Generic example (finding the maximum of an array, `best` initialised before the loop):

| step | i | a[i] | best | action |
| --- | --- | --- | --- | --- |
| 0 | – | – | 0 | init |
| 1 | 0 | -3 | 0 | -3 > 0? no |
| 2 | 1 | -1 | 0 | -1 > 0? no → returns 0, expected -1 |

Keep inputs tiny (size 1–4) and pick them to hit the suspected bug.

## C. Complexity evidence
- Count iterations as a function of n (e.g. a loop nested in another over the same range → Σ ≈ n²/2 → O(n²)).
- For recursion, write the recurrence and the maximum depth.
- State the constraints used ("assuming 1 ≤ n ≤ 10^5 from the problem statement").

## Rules
- Mark anything you could not verify as **UNVERIFIED** with the reason.
- Never claim "tests pass" without the run output in hand.
- In user-facing text, a trace shows *what happens* (values per step and the wrong result); it must not point at the fix.
