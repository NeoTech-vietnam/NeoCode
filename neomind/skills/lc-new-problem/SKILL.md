---
name: LeetCode new-problem scaffold
description: How to pick and scaffold a new LeetCode practice problem in this repo (directory, notes.md statement, edge-case questions, LC_CHECK tests from the examples) without revealing the solution. Pin to every step of the lc-new-problem flow.
---

# Scaffolding a new LeetCode practice problem

This repo exists so the **user** practices DSA by writing the solution themselves. This flow only prepares a problem for them. It never solves it.

## Hard rules

- **No solution (R1).** `solution.c` holds only the LeetCode function signature with an empty body and the marker comment `// TODO: write your solution`. No algorithm, no helper functions, no data structures, no return logic.
- **No hints about the approach (R2).** Do not fill the `Pattern:` line of `notes.md`, do not add a Hints section, do not name a technique (hash set, two pointers, sorting, DP, ...) anywhere the user reads. The topic directory name is the only allowed hint.
- **No learning status (R4).** Never edit `progress.md`, README or the `Status:` line of `notes.md`.
- **Only the new problem directory.** Create exactly `c/<topic>/<id4>_<slug>/` with `solution.c`, `test.c`, `notes.md` (`<id4>` = id zero-padded to 4 digits). Never modify an existing problem directory or any other file. If the directory already exists, stop and report it.
- Files are written in English. Keep non-ASCII characters intact (UTF-8).

## 1. Resolve the task to one problem

The task is either an explicit problem (`125 valid-palindrome`, `#125`, a LeetCode URL, or a title) plus optionally a topic, or only a topic.

- Topics: `big-o`, `array-string`, `pointer`, `hash`, `two-pointers`, `binary-search`, `sliding-window`, `linked-list`, `stack-queue`, `recursion`, `tree`, `heap`, `graph`, `sorting`, `bit`, `memory` (README section 9, also `TOPICS` in `tools/new_problem.py`).
- Explicit problem without a topic: choose the topic from README section 3 where the problem is listed, otherwise the closest topic for its main pattern.
- Topic only: list problems already in the repo (`c/*/*` and `cpp/*/*` directory names) and pick the first starter problem for that topic in README section 3 (or the Bits bullet for `bit`) that is not in the repo yet. If all are done, pick a well-known, free (non-premium) LeetCode problem of the same pattern, Easy before Medium, that is not in the repo. Never pick a premium problem.
- The slug must be the exact LeetCode URL slug and the id its frontend number.

## 2. Create the skeleton

Run from the repo root:

```
python tools/new_problem.py <topic> <id> <slug> --fetch
```

- If it prints `fetched '...' from LeetCode`, the signature and examples came from LeetCode. Keep that signature exactly.
- If it prints `fetch failed ...; using offline skeleton` (for example no network in the sandbox), replace the placeholder `int solution(void)` stub in `solution.c` with the exact LeetCode C signature you know, empty body, keeping the two header comment lines and the `// TODO: write your solution` marker inside the body. Keep the `* Note: The returned array must be malloced...` style comment block LeetCode shows for that problem if it has one. Then record in `notes.md` (see below) that the signature and statement were written without fetching.

## 3. notes.md

Keep the template as generated and insert these sections right after the bullet list (before `## Why it is correct`), the same layout as `c/hash/0217_contains-duplicate/notes.md`:

```
## Problem

<the problem statement in your own concise words, all requirements kept, including what to return and any "in any order" / "exactly one solution" guarantees>

- **Constraints:** <every constraint from LeetCode>

## Examples

- Input: `<...>` → Output: `<...>`

## Edge cases to consider

- <a question about an input the user should test, e.g. "What should happen when the array has one element?">
```

- Examples: every official LeetCode example, exact values.
- Edge cases: 3 to 6 short questions about inputs only (sizes at the constraint limits, empty/single/duplicates/negatives, `INT_MIN`/`INT_MAX`, `'\0'` and buffer length, returned-array size and ownership). A question must not suggest a technique or the answer.
- If the fetch failed, add one line under `## Problem`: `> Written without fetching from LeetCode: compare the signature and statement with the LeetCode editor before you start.`
- Leave `Pattern:` empty and the `Status:` line unchanged.

## 4. test.c

Keep the generated includes and the `return lc_finish();` line. Replace the `// TODO: add your own test cases` comment block with one `LC_CHECK` per official example (keep the original example comments if `--fetch` added them), so the user can add more checks later.

- Use named local arrays for inputs, as in `c/hash/0217_contains-duplicate/test.c`. Pass sizes as literals that match the array.
- Array results: call the function with `int returnSize = 0;`, compare with `lc_int_array_equals(result, returnSize, expected, n)`, then `free(result)`. Linked lists and trees: build with `lc_list_from_array` / `lc_tree_from_level` (`LC_NULL` for a missing node), compare with `lc_list_equals_array`, free with `lc_list_free` / `lc_tree_free`. Strings: pass a modifiable `char s[] = "...";` when the function may modify it; compare with `strcmp`.
- If LeetCode accepts any order, write the check so every valid order passes (for a pair, accept both orders); never assume an order the statement does not guarantee.
- No solution logic in tests: no reference implementation, no brute force, only the example inputs and expected outputs.
- Design classes (e.g. `MyQueue`): write the example as the sequence of `...Create` / method / `...Free` calls with `LC_CHECK` on each returned value.

## 5. Checks

- `gcc -std=c11 -fsyntax-only -I tools c/<topic>/<id4>_<slug>/test.c` must exit 0 (warnings such as a missing return in the empty stub are expected and fine).
- `git diff --check` must be clean.
- Do not use `python tools/build_test.py` as a gate: the empty stub makes it report `TODO` by design.

## 6. Final message

End with: problem id, title, slug, topic, directory, whether the fetch worked, the number of `LC_CHECK`s, and the next command for the user: `python tools/build_test.py c/<topic>/<id4>_<slug>`.
