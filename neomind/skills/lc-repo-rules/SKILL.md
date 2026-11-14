---
name: LeetCode repo rules
description: Guardrails and conventions for any AI work in this LeetCode practice repo. Pin to every agent that reads or reviews a practice problem.
---

# LeetCode practice repo: rules and conventions

This repo exists so the **user** practices DSA by writing C (then C++) themselves. AI is a guide and reviewer, never the solver. The full rules live in `AGENTS.md`; this skill is the reviewer-facing summary.

## Hard rules (never break)

- **R1 – No solutions.** Do not write, edit or paste solution code for the problem under review: no full algorithm, no corrected function, no "fixed version" diff, not even a few lines of the fix. In anything the user reads, do not name the faulty expression together with its correction either (e.g. "start at X instead of Y") – that is the fix in words.
- **R2 – One hint at a time.** When the user's approach is wrong or suboptimal, give one hint or one guiding question per issue, ordered from gentlest to most direct. Never chain hints into the full algorithm. The rest of the report (What / Why / trace) must not reveal more than that hint does: describe the symptom (input → expected vs actual), not the cause-and-fix.
- **R3 – Firmware checklist.** Every review covers: correctness (with a counterexample if wrong), pointers/buffers and `\0`, ownership and `free`, `unsigned` types / overflow / shift counts, time/space complexity including the call stack. See skill `lc-review-checklist`.
- **R4 – Do not change learning status.** Never edit `progress.md`, the README checkpoints, or the `Status:` line of `notes.md`. You may *suggest* a status.
- **R5 – Verify before asserting.** Every claim about correctness or complexity needs a hand trace on a small input or an actual run, and states its constraint assumptions. See skill `lc-trace-verify`.

## The only file AI may write in a problem directory

- `review.md` in the reviewed problem directory (e.g. `c/hash/0217_contains-duplicate/review.md`), written only by the review flow's write step. Format and history rules: skill `lc-hint-ladder`.
- Never touch `solution.c` / `solution.cpp`, `test.c` / `test.cpp`, `notes.md`, `progress.md`, README or anything else.

## Repo layout

- Problem dir: `c/<topic>/<id>_<slug>/` with `solution.c` (paste-ready for LeetCode: no `main`, no tests), `test.c` (local harness, includes `tools/lc.h` and `solution.c`), `notes.md` and optionally `review.md`. C++ mirror under `cpp/` with `.cpp` files.
- `tools/lc.h`: `LC_CHECK(expr)`, `lc_finish()`, `ListNode` / `TreeNode`, `lc_list_from_array`, `lc_list_equals_array`, `lc_list_free`, `lc_tree_from_level` (`LC_NULL` = missing node), `lc_tree_free`, `lc_int_array_equals`.
- Build and test one problem: `python tools/build_test.py c/<topic>/<id>_<slug>`. Exit code 1 = a problem failed, 2 = usage/toolchain error. `--sanitize` uses MSYS2 CLANG64 clang (ASan/UBSan) when available.
- Compiler: MinGW GCC 6.3, `-std=c11 -Wall -Wextra -Werror`, no sanitizers. Code must also be valid for LeetCode's C compiler (C99/C11, `uthash` available on LeetCode but not locally).

## Language

- Write files in English, except `review.md`, which is the user-facing report and is written in **Vietnamese**; keep code identifiers, complexity notation and compiler messages as-is.
