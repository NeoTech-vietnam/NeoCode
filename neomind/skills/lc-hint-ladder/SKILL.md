---
name: Hint ladder and review report
description: How to turn review findings into a Vietnamese report that teaches through one hint at a time (rules R1, R2, R4) without revealing the solution.
---

# Hint ladder, review report and review.md

## Hint ladder (R2)
For each issue, give only the **first rung** the user has not reached yet:
1. Point at the symptom: "Thử chạy với input nhỏ nhất có thể xem kết quả là gì?"
2. Point at the area: "Xem lại điều kiện khởi đầu của vòng lặp trong."
3. Name the concept: "Bài này có thể dùng một cấu trúc tra cứu O(1) – bạn nghĩ tới cấu trúc nào?"
Never go past rung 3 and never write the fixed code (R1). For a better-complexity approach, name the pattern family at most (e.g. "hash set", "two pointers", "sort trước"), not the algorithm steps.

## No leaks outside the hint
The whole user-facing report counts, not just the `Gợi ý` line:
- `Vấn đề` / `Tại sao` describe the **symptom**: which input, expected vs actual output, which test line fails.
- A trace may show variable values per step, but must not say which expression is wrong or what it should be.
- Never copy the reviewers' internal `Cause` line into the report.
- Line references may point at a range (e.g. `solution.c:6-14`), not at the single faulty token.

## Report format (Vietnamese)

```
## Review <YYYY-MM-DD> – <id>. <title>

### Tóm tắt
- Kết luận: ĐÚNG / SAI / ĐÚNG nhưng TLE / ĐÚNG nhưng có rủi ro
- Build & test local: <status line from build_test.py, or "không chạy được: <lý do>">
- Độ phức tạp hiện tại: Time O(..), Space O(..) (call stack: ..)

### Vấn đề (theo mức độ)
**[BUG|TLE|MLE|RISK|NIT] <mục checklist> – <file>:<line range>**
- Vấn đề: <symptom>
- Tại sao: <counterexample / trace / run, symptom-level>
- Gợi ý: <first rung only>

### Checklist firmware
| Mục | Kết quả | Bằng chứng |
| --- | --- | --- |
| Correctness | ... | trace / run |
| Pointer, buffer, \0 | ... | ... |
| Ownership, free | ... | ... |
| unsigned, overflow, shift | ... | ... |
| Complexity (kể cả call stack) | ... | ... |

### Test case nên thêm vào test.c
- `LC_CHECK(...);`  // lý do (only cases not already in test.c)

### Ghi chú cho notes.md (gợi ý, người dùng tự quyết)
- Pattern, complexity, edge cases worth recording. Suggest – never set – a Status (R4).
```

Keep it short: the user should be able to read it in two minutes.

## Writing review.md (write step only)
- Path: `<problem-dir>/review.md`, where `<problem-dir>` is the directory named in the task.
- If the file does not exist, create it with the first line `# Reviews: <id>. <title>`, a blank line, then the report.
- If it exists, keep everything already there and insert the new report directly below the `# Reviews` heading, so the newest review is on top. Separate reviews with a `---` line.
- Write the audited report **verbatim**; do not rephrase or add content.
- Change no other file.
