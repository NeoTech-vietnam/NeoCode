# Reviews: 217. Contains Duplicate

## Review 2026-11-12 – 217. Contains Duplicate

### Tóm tắt
- Kết luận: SAI
- Build & test local: không chạy được: phiên review này không có công cụ shell nên không chạy được `python tools/build_test.py c/hash/0217_contains-duplicate` (kết quả build và `--sanitize` là UNVERIFIED). Dự đoán từ hand trace, chưa phải kết quả chạy: các dòng `LC_CHECK` ở `test.c:20`, `test.c:22`, `test.c:23` sẽ fail (3/5).
- Độ phức tạp hiện tại (giả định `1 ≤ n ≤ 10^5` theo `notes.md:11`): hiện tại hàm thoát ngay ở lần so sánh đầu nên Time O(1), Space O(1) (call stack: O(1)); tốc độ này đến từ lỗi, không phải từ thuật toán hiệu quả. Đếm theo cấu trúc hai vòng lặp lồng nhau thì tiềm năng là Time O(n²).

### Vấn đề (theo mức độ)
**[BUG] Correctness – solution.c:7-16**
- Vấn đề: hàm trả `true` cho mọi mảng có ít nhất một phần tử, kể cả khi các phần tử đều khác nhau.
- Tại sao: input `[7]` (`test.c:22`), expected `false`, actual `true`. Tương tự `[1,2,3,4]` (`test.c:20`) và `distinct_negative` (`test.c:23`) đều trả `true` thay vì `false`. Các test expect `true` (`test.c:19`, `test.c:21`) vẫn qua nên lỗi không lộ ra ở đó.

| bước | i | j | nums[i] | nums[j] | kết quả |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 7 | 7 | điều kiện đúng → `return true` (expected `false`) |

- Gợi ý: thử chạy tay với input nhỏ nhất `[7]` và ghi ra hai chỉ số được so sánh ở lần lặp đầu tiên.

**[TLE – tiềm ẩn] Complexity – solution.c:7-16**
- Vấn đề: cách tiếp cận so sánh từng cặp có số lần so sánh tăng theo bình phương của n; hiện chưa bị lộ vì lỗi ở trên làm hàm thoát sớm.
- Tại sao: với input toàn phần tử khác nhau, số lần so sánh cỡ `n(n−1)/2`; với `n = 10^5` (ràng buộc trong `notes.md:11`) khoảng 5·10^9, nhiều khả năng TLE trên LeetCode (chưa chạy để xác nhận).
- Gợi ý: bài này có thể dùng một cấu trúc tra cứu gần O(1) cho các giá trị đã gặp – bạn nghĩ tới cấu trúc nào?

**[RISK] Pointer, buffer – test.c:23**
- Vấn đề: mảng `distinct_negative` có 4 phần tử nhưng lời gọi truyền kích thước `5`.
- Tại sao: nếu hàm duyệt hết phạm vi kích thước được truyền, sẽ đọc `distinct_negative[4]`, ngoài mảng. Hiện lỗi ở trên làm hàm thoát trước khi đọc tới đó. Việc `--sanitize` có báo hay không là UNVERIFIED.
- Gợi ý: so sánh số phần tử khai báo của `distinct_negative` với đối số kích thước ở dòng này.

### Checklist firmware
| Mục | Kết quả | Bằng chứng |
| --- | --- | --- |
| Correctness | BUG | trace `[7]`: trả `true`, expected `false` |
| Pointer, buffer, \0 | RISK | `solution.c` chỉ dùng chỉ số trong `[0, numsSize)`; riêng `test.c:23` truyền sai kích thước; không có chuỗi, không có `returnSize` |
| Ownership, free | OK | `solution.c` không `malloc`/`free`; `test.c` chỉ dùng mảng trên stack |
| unsigned, overflow, shift | OK | chỉ có `i++`, `j++` trên `int` và phép so sánh `==`; không có unsigned hay shift |
| Complexity (kể cả call stack) | TLE tiềm ẩn | đếm số vòng lặp lồng nhau với `n = 10^5`; call stack O(1), không đệ quy |

### Test case nên thêm vào test.c
- `LC_CHECK(containsDuplicate(dup_ends, 4) == true);`  // với `int dup_ends[] = {5, 1, 2, 5};` – trùng ở hai đầu mảng
- `LC_CHECK(containsDuplicate(extremes, 2) == false);`  // với `int extremes[] = {INT_MIN, INT_MAX};` – giá trị biên

### Ghi chú cho notes.md (gợi ý, người dùng tự quyết)
- Bạn có thể ghi lại pattern và complexity của cách làm cuối cùng, cùng các edge case: một phần tử, mảng toàn phần tử khác nhau, trùng ở hai đầu.
- Các mục "Why it is correct" và "Complexity" đang trống; bạn có thể tự điền sau khi giải xong.
- `Status:` vẫn là văn bản mẫu; bạn tự quyết định khi bài đã qua test.
