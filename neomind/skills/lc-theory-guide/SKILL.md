---
name: LeetCode theory guide
description: "How to write a Vietnamese theory/background guide (theory.md) for an existing LeetCode practice problem: concepts to learn, C knowledge, a collapsed hint ladder and verified reference links, without revealing the solution. Pin to every step of the lc-theory flow."
---

# LeetCode theory guide (theory.md)

This repo exists so the **user** practices DSA by writing C (then C++) themselves. AI is a guide, never the solver (full rules in `AGENTS.md`). The lc-theory flow writes ONE file, `<problem-dir>/theory.md`, that tells the user what theory to learn before or while solving an existing problem. It points the way; it never walks it.

## 1. Resolve the problem directory

- The task names an existing problem: an id (`217`, `0217`), a slug (`contains-duplicate`), a title (`Contains Duplicate`) or a path (`c/hash/0217_contains-duplicate`).
- Problem dirs are `c/<topic>/<id4>_<slug>/` (C++ mirror `cpp/<topic>/<id4>_<slug>/`). List `c/*/` and `cpp/*/` and match the id (zero-padded to 4 digits) or the slug. Prefer the `c/` directory when both exist.
- Exactly one match is required. If none or several match, say so plainly in the plan and write nothing.
- Read `notes.md` (statement, constraints, examples, edge cases) and `test.c`. Do not review or comment on `solution.c`; the guide must not depend on the user's current code.

## 2. Hard rules (never break)

- **R1 - No solution.** No code that solves or partly solves the problem, no pseudo-code, no numbered algorithm steps, no "first do X, then Y" recipe, no sentence that says which approach solves this problem AND how to apply it. No code blocks at all except a C library function prototype copied from cppreference (e.g. the `qsort` prototype). Explain each concept in general terms (what it is, its operations and their cost), not applied to this problem.
- **R2 - Hints one at a time.** The hint ladder has at most 3 rungs, each in its own collapsed `<details>` block, ordered gentlest first: (1) an observation question about the input/output, (2) a question pointing at the property or area to think about, (3) at most the name of a concept family (e.g. "hash set", "two pointers", "sort first"). Nothing elsewhere in the file may reveal more than rung 3.
- **R4 - No learning status.** Never edit `progress.md`, the README, `notes.md`, `solution.c`, `test.c` or `review.md`. The only file this flow may create or change is `<problem-dir>/theory.md`. If it already exists, replace its whole content (it is generated).
- **R5 - No wrong claims.** Every complexity or fact must be standard and correct; constraint numbers must be copied from `notes.md`. If unsure, leave it out.
- **Links:** use ONLY URLs from section 4, plus LeetCode problem pages `https://leetcode.com/problems/<slug>/` for problems whose exact slug you are sure of. Never invent or guess any other URL (guessed URLs on these same sites were verified to return 404).
- Keep Vietnamese diacritics intact (UTF-8). Keep code identifiers, complexity notation and English technical terms as-is (you may add the English term in parentheses).
- **Math formatting:** write every number, power and complexity as inline code: `10^5`, `-10^9`, `O(n log n)`, `O(n^2)`. Never use LaTeX (`$...$`, `\(...\)`, `^{...}`) and never wrap math in bare parentheses such as (10^5) or (O(n)).

## 3. theory.md format (Vietnamese)

```
# Lý thuyết nền: <id>. <title>

> Tài liệu định hướng do AI tạo ngày <YYYY-MM-DD>. Không chứa lời giải. Mỗi gợi ý ở mục 4 chỉ mở khi đã tự thử mà vẫn kẹt.

- Đề bài: https://leetcode.com/problems/<slug>/
- Thư mục: `<problem-dir>`

## 1. Đọc đề và ngân sách độ phức tạp
- Ràng buộc chính (copy from notes.md) và ý nghĩa: rough rule ~10^8 simple operations per second, so which complexity classes fit and which would be too slow (state it as a budget, not as the answer).
- 2-3 câu hỏi tự kiểm tra đã hiểu đề chưa.

## 2. Kiến thức nền cần nắm
2-4 concepts that are relevant, including at least one that is a plausible alternative, without saying which one is the intended solution. For each:
### <Tên khái niệm (English term)>
- Là gì: general definition.
- Thao tác chính và độ phức tạp: e.g. insert / lookup / delete, average and worst case, extra memory.
- Câu hỏi tự kiểm tra: one question.
- Đọc thêm: 1-3 links from section 4.

## 3. Kiến thức C cần cho bài này
C-specific knowledge the user will need. Cover the C pitfalls of EVERY concept named in section 2, checked against the constraint ranges in notes.md, not just generic C facts. Mandatory when they apply:
- Sorting named: `qsort` and its comparator contract (negative / zero / positive); a comparator that returns `a - b` overflows `int` when values can be near `INT_MIN`/`INT_MAX` (e.g. `-10^9` and `10^9` differ by `2*10^9`, more than `INT_MAX`); `qsort` sorts the caller's array in place.
- Hashing named: the C standard library has no hash set; LeetCode provides uthash (not available locally); every added element must be freed; or a direct-address array when the value range is small.
- Returned arrays or strings: `malloc`/`free`, who owns the result, `returnSize`, and the `\0` terminator.
- Characters: `<ctype.h>` functions take an `unsigned char` value or `EOF`.
- Integer ranges: `<limits.h>`, and intermediate sums or products that can exceed `int`.
Explain in words and link cppreference; no code except prototypes.

## 4. Gợi ý theo bậc (mở dần)
<details><summary>Gợi ý 1 - quan sát</summary>

question

</details>
(rung 2 and rung 3 in the same way)

## 5. Bẫy thường gặp và edge cases
Phrased as questions about inputs (empty/minimum size, duplicates, negative values, extremes of the constraints, overflow), never as fixes.

## 6. Bài tương tự để luyện
2-4 LeetCode problems that train the same concepts: `[<id>. <title>](https://leetcode.com/problems/<slug>/)` with one line on which concept they practise.

## 7. Tài liệu tổng quát
2-3 general links from section 4 (complexity cheat sheet, visualisations, roadmap).
```

The user should be able to read it in about five minutes; prefer short bullet points.

## 4. Verified reference links (HTTP 200, checked 2026-11-12)

General and complexity:
- https://www.bigocheatsheet.com/
- https://en.wikipedia.org/wiki/Big_O_notation
- https://usaco.guide/
- https://usaco.guide/bronze/time-comp
- https://neetcode.io/roadmap
- https://www.programiz.com/dsa
- https://cp-algorithms.com/
- https://visualgo.net/en

Hashing:
- https://en.wikipedia.org/wiki/Hash_table
- https://visualgo.net/en/hashtable
- https://www.geeksforgeeks.org/hashing-data-structure/
- https://cp-algorithms.com/string/string-hashing.html
- https://troydhanson.github.io/uthash/
- https://troydhanson.github.io/uthash/userguide.html
- https://en.cppreference.com/w/cpp/container/unordered_set

Sorting, merging, in-place, searching:
- https://en.wikipedia.org/wiki/Sorting_algorithm
- https://visualgo.net/en/sorting
- https://usaco.guide/bronze/intro-sorting
- https://usaco.guide/silver/greedy-sorting
- https://en.wikipedia.org/wiki/Merge_algorithm
- https://en.wikipedia.org/wiki/In-place_algorithm
- https://en.wikipedia.org/wiki/Binary_search
- https://cp-algorithms.com/num_methods/binary_search.html
- https://usaco.guide/silver/binary-search

Two pointers, sliding window, prefix sums:
- https://www.geeksforgeeks.org/two-pointers-technique/
- https://usaco.guide/silver/two-pointers
- https://www.geeksforgeeks.org/window-sliding-technique/
- https://en.wikipedia.org/wiki/Prefix_sum
- https://usaco.guide/silver/prefix-sums
- https://www.geeksforgeeks.org/prefix-sum-array-implementation-applications-competitive-programming/

Linear structures:
- https://en.wikipedia.org/wiki/Linked_list
- https://visualgo.net/en/list
- https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29
- https://en.wikipedia.org/wiki/Queue_%28abstract_data_type%29

Trees, heaps, tries:
- https://en.wikipedia.org/wiki/Tree_traversal
- https://visualgo.net/en/bst
- https://en.wikipedia.org/wiki/Binary_heap
- https://visualgo.net/en/heap
- https://en.wikipedia.org/wiki/Trie
- https://visualgo.net/en/suffixtree
- https://cp-algorithms.com/data_structures/segment_tree.html
- https://cp-algorithms.com/data_structures/fenwick.html

Graphs:
- https://visualgo.net/en/graphds
- https://visualgo.net/en/dfsbfs
- https://usaco.guide/silver/graph-traversal
- https://cp-algorithms.com/graph/breadth-first-search.html
- https://cp-algorithms.com/graph/depth-first-search.html
- https://cp-algorithms.com/graph/topological-sort.html
- https://cp-algorithms.com/graph/dijkstra.html
- https://visualgo.net/en/sssp
- https://cp-algorithms.com/data_structures/disjoint_set_union.html
- https://visualgo.net/en/ufds

Recursion, backtracking, DP, greedy:
- https://en.wikipedia.org/wiki/Recursion_%28computer_science%29
- https://visualgo.net/en/recursion
- https://en.wikipedia.org/wiki/Backtracking
- https://en.wikipedia.org/wiki/Dynamic_programming
- https://cp-algorithms.com/dynamic_programming/intro-to-dp.html
- https://usaco.guide/gold/intro-dp
- https://en.wikipedia.org/wiki/Greedy_algorithm

Bits, math, strings:
- https://en.wikipedia.org/wiki/Bit_manipulation
- https://cp-algorithms.com/algebra/bit-manipulation.html
- https://visualgo.net/en/bitmask
- https://cp-algorithms.com/algebra/binary-exp.html
- https://en.wikipedia.org/wiki/Two%27s_complement
- https://en.wikipedia.org/wiki/Integer_overflow
- https://en.wikipedia.org/wiki/Pigeonhole_principle
- https://cp-algorithms.com/string/prefix-function.html

C language and library (cppreference):
- https://en.cppreference.com/w/c
- https://en.cppreference.com/w/c/algorithm/qsort
- https://en.cppreference.com/w/c/memory/malloc
- https://en.cppreference.com/w/c/string/byte
- https://en.cppreference.com/w/c/string/byte/isalnum
- https://en.cppreference.com/w/c/string/byte/tolower
- https://en.cppreference.com/w/c/string/byte/memset
- https://en.cppreference.com/w/c/language/operator_arithmetic
- https://en.cppreference.com/w/c/language/conversion
- https://en.cppreference.com/w/c/types/integer
- https://en.cppreference.com/w/c/types/limits

If no listed link fits a concept, give no link for it rather than inventing one.
