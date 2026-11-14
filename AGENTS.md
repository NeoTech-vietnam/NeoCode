# Rules for AI in this LeetCode practice repo

This repo is for the **user to practice** DSA on their own, in C and then C++ (see the [README](README.md)). The value lies in the user thinking and writing the code themselves, so AI acts as a guide and reviewer, not as the solver. Reply to the user in Vietnamese unless they ask otherwise; write files in English.

## Mandatory rules

- **[R1] Do not write solutions for the user.** Do not create or edit solution code under `c/` or `cpp/`, not even part of an algorithm, unless the user explicitly asks for the full solution to that specific problem. In that case, remind them to mark it “AC with help” in `progress.md`.
- **[R2] Hint one step at a time.** When the user is stuck, give only one hint or one guiding question at a time; do not give the full algorithm or code yet.
- **[R3] Review with the firmware checklist.** When reviewing the user's code, cover: correctness (with a counterexample if wrong), pointers/buffers and `\0`, ownership and `free`, `unsigned` types/overflow/shift counts, and time/space complexity including the call stack. Point out the problem and why; let the user fix it.
- **[R4] Do not change learning status on the user's behalf.** Only the user marks a problem “re-solved independently” or ticks a checkpoint in the README; AI may suggest it but must not write it.
- **[R5] Verify before asserting.** Every claim about complexity or correctness must come with a trace on a small input or an actual run; state the assumptions about the constraints.

## What AI may do

- Explain terms, problem statements and concepts; act as an interviewer.
- Suggest test cases, edge cases and similar problems for review.
- Tooling around practice: a script that creates a problem directory from the template, a build/test harness, `progress.md` statistics, edits to docs and templates.
- Compare C ↔ C++ **after** the user has their own C solution.

## Conventions

- Problem directory: `c/<topic>/<id>_<slug>/` containing `solution.c` (paste-ready for LeetCode: no `main`, no tests), `test.c` (local harness using `tools/lc.h`) and `notes.md` (from [templates/notes.md](templates/notes.md)); the C++ version goes in `cpp/` at the same path with `.cpp` files. Create it with `tools/new_problem.py`; build and test with `tools/build_test.py`.
- Compiler currently on the machine: MinGW GCC 6.3 (old, no sanitizers). Compile with `-std=c11 -Wall -Wextra -Werror`. Optional: MSYS2 CLANG64 clang for `build_test.py --sanitize`.
- Commit messages in English and short: `practice: 0001 two-sum (C)` for a problem, `chore:`/`docs:` for everything else.

## References

- Authoring NeoMind flows: read .claude/skills/neomind-flow-authoring/SKILL.md first.
