# LeetCode Roadmap for a Firmware Engineer

- **Audience:** a firmware engineer with about 3 years of experience, targeting Junior/Middle roles.
- **Duration:** about 15–17 weeks at 1 hour per day.
- **Approach:** C first → compare with C++ → shift to C++ once the C/DSA foundation is solid.

Progress: [progress.md](progress.md) · Rules for AI in this repo: [AGENTS.md](AGENTS.md) · Per-problem notes template: [templates/notes.md](templates/notes.md) · Manual testing guide: [docs/manual-testing.md](docs/manual-testing.md)

## 1. Goals

- Strengthen C, pointers, memory and the basic data structures.
- Recognize patterns, explain why an algorithm is correct, and analyze time/space complexity.
- Solve representative Easy and Medium problems independently; present the reasoning as in an interview.
- Use C++/STL to solve DSA problems faster after understanding how to implement them in C.

This covers coding/DSA practice only. Firmware knowledge such as interrupts, concurrency, RTOS and debugging should be reviewed separately according to the target position.

## 2. C-first → C++ strategy

- **Solve in C first.** For arrays, strings, linked lists, stacks/queues, hash tables and heaps, implement a small version yourself to understand the operations and memory. There is no need to build a general-purpose library.
- **Use C++ for comparison.** After understanding the C solution, see how the same algorithm looks with the STL, which structures are replaced, and whether the complexity changes.
- **Shift focus when the checkpoint in section 7 is met.** Keep using C for pointer, memory, bit-manipulation and embedded-style problems.

In C, use a frequency array instead of a hash map only when the value range allows it. For hash tables, understand collisions and the O(1) average / O(n) worst-case lookup.

## 3. Topics in order

| Order | Topic | What to master | Starter problems on LeetCode |
| --- | --- | --- | --- |
| 1 | Big-O | O(1), O(log n), O(n), O(n log n), O(n²); time/memory trade-offs | Analyze the solutions of the following problems |
| 2 | Array / String | Traversal, in-place edits, frequency counting, prefix sums; `sizeof`, array decay, `\0`, buffer limits | #121 Best Time to Buy and Sell Stock; #242 Valid Anagram |
| 3 | Pointer | Array vs pointer, pointer arithmetic, pointer-to-pointer, `const`, ownership; basic function pointers | Write swap and reverse-buffer yourself; trace pointer operations |
| 4 | Hash Map / Set | Key/value, hash function, collisions; implement a small hash table | #1 Two Sum; #217 Contains Duplicate |
| 5 | Two Pointers | Opposite ends, same direction, in-place edits; fast/slow pointers with linked lists | #125 Valid Palindrome; #167 Two Sum II |
| 6 | Binary Search | Search space, invariants, boundaries, first/last occurrence; computing mid without overflow | #704 Binary Search; #35 Search Insert Position |
| 7 | Sliding Window | Fixed and variable windows; substrings and subarrays | #643 Maximum Average Subarray I; #3 Longest Substring Without Repeating Characters |
| 8 | Linked List | Insert/delete, reverse, merge, middle, cycle; keeping the next pointer correct | #206 Reverse Linked List; #21 Merge Two Sorted Lists; #141 Linked List Cycle |
| 9 | Stack / Queue / Ring Buffer | LIFO/FIFO, push/pop, enqueue/dequeue, full/empty handling and wrap-around | #20 Valid Parentheses; #232 Implement Queue using Stacks; implement a ring buffer |
| 10 | Recursion | Base case, recursive case, call stack, depth and stack-overflow risk | Trace calls before starting trees |
| 11 | Tree / BFS / DFS | Binary tree, BST, preorder/inorder/postorder; DFS with recursion/stack, BFS with a queue | #104 Maximum Depth of Binary Tree; #226 Invert Binary Tree; #102 Binary Tree Level Order Traversal |
| 12 | Heap / Priority Queue | Min/max heap, array representation, heapify, push/pop; implement once | #703 Kth Largest Element in a Stream |
| 13 | Basic Graph | Vertices/edges, directed/undirected, adjacency list/matrix, visited, BFS/DFS | #200 Number of Islands; #1971 Find if Path Exists in Graph |
| 14 | Sorting | Know when sorting simplifies a problem; understand insertion, merge, quick sort and `qsort` | Try sorting for Contains Duplicate; compare with hashing |

Bit manipulation and memory are high priority for firmware and are studied throughout, from the start:

- **Bits:** AND/OR/XOR/NOT, shifts, masks, set/clear/toggle/test a bit; #136 Single Number, #191 Number of 1 Bits, #231 Power of Two. Watch `unsigned` types and valid shift counts.
- **Memory:** stack/heap/static storage; text/data/BSS; `malloc`/`calloc`/`realloc`/`free`, ownership, leaks, dangling pointers, buffer overflows, alignment and struct padding.

Basic sorting can be learned early when a problem needs sorted data; set aside time at the end of the roadmap to consolidate it.

## 4. How to study each topic with LeetCode

Short concept study → implement the core in C → solve LeetCode problems right away → review.

1. Read the statement and constraints; make your own examples and edge cases.
2. State the brute force first, compute its complexity, then look for improvements.
3. Write it in C; check small/empty input if valid, duplicates, boundary errors and memory.
4. Use Run/Submit on LeetCode, fix errors, and be able to explain their cause. AC means Accepted.
5. Once understood, compare with C++ and note the pattern, complexity and memorable mistakes.
6. Solve it again a few days later without looking at the answer; try one more problem with the same pattern.

Start each topic with a few Easy problems, then pick representative Mediums. Add problems where you are still weak; do not set a target of finishing all 150 problems in 15–17 weeks. The problems in the table are starting points and may belong to several patterns.

**A 60-minute session:** 15 minutes study/review → 35 minutes solving → 10 minutes review. A hard problem may take several sessions. If there is no progress after about 20–30 minutes, take a small hint and continue on your own.

Each week, spend at least one session on old or mixed-topic problems. Measure progress by the ability to solve and explain independently, not just by the AC count.

## 5. How to use AI

- **When starting:** ask it to explain terms or the problem statement; do not ask for the algorithm yet.
- **When stuck:** ask for one hint at a time, pointing at what to observe; keep the code and reasoning your own.
- **After writing your code:** ask for a review of the logic, pointers/buffers, ownership and complexity, and for counterexample test cases.
- **After understanding:** ask it to compare C with C++, or to act as an interviewer asking why the solution is correct and what the trade-offs are.
- **When reviewing:** ask for similar problems and solve them again without AI. If you need to see a full solution, mark the problem as “with help” until you can solve it on your own.

Sample prompt:

> I am practicing in C. Ask me questions or give one hint at a time; do not give the full algorithm or code yet. After I solve it myself, review correctness, memory and complexity.

Check AI hints and code yourself by tracing small inputs and running them; ask it to state its assumptions about the constraints.

## 6. Timeline of about 15–17 weeks

The milestones below are a standard 16-week plan, about 112 hours. Drop a week if the foundation is already strong, or add one to reinforce weak areas.

| Standard milestone | Focus | Expected outcome |
| --- | --- | --- |
| Weeks 1–2 | Big-O, arrays/strings, pointers | Solve Easy problems in C, control boundaries and explain complexity |
| Weeks 3–6 | Hash map/set, two pointers, binary search, sliding window | Choose the right pattern and solve the corresponding basic Mediums |
| Weeks 7–9 | Linked list, stack, queue/circular buffer | Implement the basic structures; handle pointers and full/empty states correctly |
| Weeks 10–12 | Recursion, trees, BFS/DFS | Trace traversals; choose stack vs queue and analyze memory |
| Weeks 13–14 | Heap, basic graphs | Implement a small heap; traverse graphs/grids with visited |
| Weeks 15–16 | Consolidate sorting, bits, memory; mixed review, mock interviews | Identify weak spots, explain solutions on your own and assess the C++ checkpoint |

Bit manipulation, memory and review of old problems run through the whole roadmap. The timeline is a projected schedule; a topic that is not yet solid may need more time before increasing difficulty.

## 7. Checkpoint for moving to C++

Shift focus when you can do the following:

- [ ] Write C for arrays/strings, linked lists, stacks/queues, a small hash table and a basic heap.
- [ ] Write binary search, tree traversals and BFS/DFS; explain the chosen data structure.
- [ ] Handle pointers, null terminators, buffer boundaries and allocation/freeing without frequent help.
- [ ] Analyze time/space complexity, including the recursion call stack.
- [ ] Re-solve a Medium with a familiar pattern in about 20–30 minutes without looking at the solution. This is a self-assessment milestone, not a promise for every new problem.

After the checkpoint, re-solve some representative problems in C++ using this mapping:

| C | C++ for DSA practice |
| --- | --- |
| Array / character buffer | `vector`, `string` |
| Hand-written hash table / set | `unordered_map`, `unordered_set` |
| Stack / queue | `stack`, `queue` |
| Heap | `priority_queue` |
| `qsort` | `sort` |

Also learn references, `const`, iterators, comparators and how to pass containers without accidental copies. This phase starts based on ability, not automatically at the end of week 16.

## 8. Later topics and what not to go deep on yet

After the core, add basic backtracking → basic greedy → 1D DP when broader coverage is needed.

Not a priority yet: advanced graphs (Dijkstra, Bellman–Ford, Floyd–Warshall, MST), Trie, 2D/hard DP, advanced backtracking/greedy, segment trees, Fenwick trees and competitive-programming math. Adjust if the target position clearly requires them.

## 9. Repository layout

```text
leetcode-practice/
├── README.md                    # This roadmap
├── AGENTS.md                    # Rules for AI working in this repo
├── progress.md                  # Topics, problems, level of help, LeetCode result and review dates
├── templates/notes.md           # Per-problem notes template
├── tools/                       # new_problem.py, build_test.py, selftest.py, lc.h (test helpers)
├── c/<topic>/<id_slug>/         # solution.c (paste-ready for LeetCode), test.c (local tests), notes.md
└── cpp/<topic>/<id_slug>/       # Same with .cpp: C++ comparison after understanding the C solution
```

Topic names used under `c/` and `cpp/`: `big-o`, `array-string`, `pointer`, `hash`, `two-pointers`, `binary-search`, `sliding-window`, `linked-list`, `stack-queue`, `recursion`, `tree`, `heap`, `graph`, `sorting`, `bit`, `memory`. Problem directories are named `<id>_<slug>`, for example `c/hash/0001_two-sum/`.

Notes for each problem only need: problem link · pattern · why it is correct · time/space · edge cases/mistakes · date re-solved. Distinguish “AC with help” from “re-solved independently”.

### Tooling and workflow

Needs Python 3 and GCC or Clang. Everything runs offline except the optional `--fetch`.

For Windows installation, compiler configuration and troubleshooting, see [SETUP.md](SETUP.md).

For a NeoMind flow that reviews an existing solution and produces a per-problem report, see [LeetCode Review](neomind/LEETCODE_REVIEW.md).

1. **Create:** `python tools/new_problem.py hash 1 two-sum` (add `--lang cpp` for C++, `--title "Two Sum"` to set the title). This creates `c/hash/0001_two-sum/` with `notes.md`, `solution.c` (only a TODO stub) and `test.c` (a `main` for your own checks). Unknown topics are refused and an existing problem directory is never overwritten.
   With `--fetch`, the title, the empty LeetCode signature and the examples are read from LeetCode's public API (network, no login). The signature becomes `solution.c` and the examples become comments in `test.c`; if the request fails, the offline skeleton is used.
2. **Solve:** write your solution in `solution.c`. Keep it paste-ready: only what LeetCode accepts, no `main` and no tests.
3. **Test:** add checks to `test.c`, e.g. `LC_CHECK(myFunction(...) == expected);`. `tools/lc.h` defines `ListNode`/`TreeNode` as LeetCode does, plus `lc_list_from_array`, `lc_list_equals_array`, `lc_list_free`, `lc_tree_from_level` (`LC_NULL` = missing node), `lc_tree_free` and `lc_int_array_equals`.
4. **Build and run:** `python tools/build_test.py` (all problems) or `python tools/build_test.py c/hash/0001_two-sum` (one problem or topic). Add `--sanitize` for AddressSanitizer/UBSan and `--strict` to also fail on `TODO`/`NO TESTS`.
5. **Submit:** paste `solution.c` into the LeetCode editor and submit there yourself, then fill in the LeetCode column of `progress.md`. Nothing is submitted automatically and no LeetCode credentials are stored.

Statuses: `PASS`; `NO TESTS` (zero checks ran); `TODO` (the solution still has its `TODO: write your solution` marker and does not compile yet); `BUILD FAIL`, `TEST FAIL`, `TIMEOUT`, `SANITIZER` (these make the exit code non-zero).

Compilers: `CC`/`CXX` if set, otherwise `clang` on PATH, then MSYS2 CLANG64 (`C:\msys64\clang64\bin`), then `gcc`/`g++`; the chosen ones are printed first. Flags: C `-std=c11`; C++ `-std=c++20` when supported, otherwise `-std=c++17` (`-std=c++1z` on GCC 6); always `-Wall -Wextra -Werror`. Binaries go to `build/` (`build/asan/` with `--sanitize`).

`python tools/selftest.py` checks the tooling offline on throwaway samples in a temporary directory and writes a full log to `build/selftest.log`.

#### MSYS2 CLANG64 (sanitizers)

LeetCode runs C/C++ with AddressSanitizer, so out-of-bounds access, use-after-free and similar bugs that often “work” locally fail there. MinGW GCC 6.3 has no sanitizers; to use `--sanitize` on Windows:

1. Install MSYS2 from https://www.msys2.org/ (default location `C:\msys64`).
2. In the MSYS2 shell, run `pacman -S mingw-w64-clang-x86_64-clang`.
3. Optionally add `C:\msys64\clang64\bin` to PATH; `build_test.py` also finds the default location by itself.

On Linux the system GCC or Clang usually supports `--sanitize` already; LeakSanitizer also reports leaks there, so free what your tests allocate. GCC 6.3 keeps working for everything except `--sanitize`.

## 10. Main references

| Source | How to use it |
| --- | --- |
| LeetCode Top Interview 150 | Main problem set; pick by topic and suitable difficulty |
| NeetCode Roadmap / Algorithms & Data Structures for Beginners | See how topics relate; learn concepts and patterns |
| HackerRank Interview Preparation Kit | Extra problems and practice by topic group |
| MIT 6.006 — Introduction to Algorithms | Selective reference on algorithms, correctness and complexity analysis |
| VisuAlgo | Watch linked lists, hash tables, heaps, trees and graph traversals step by step |

This roadmap is a personal plan built from discussions about Firmware Junior/Middle goals; the order and timeline are study suggestions. Use LeetCode for practice, NeetCode for additional explanations, and MIT/VisuAlgo to clarify what is still unclear.
