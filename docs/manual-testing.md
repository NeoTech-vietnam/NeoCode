# Hướng dẫn chạy test thủ công cho các bài LeetCode

Tài liệu này mô tả cách test một bài giải locally trước khi submit lên LeetCode. Yêu cầu: Python 3 và GCC hoặc Clang trên PATH.

## Các bước

### 1. Viết check vào `test.c`

Mở `test.c` của bài (ví dụ `c/array-string/2235_add-two-integers/test.c`) và thêm check bằng macro `LC_CHECK` (định nghĩa trong `tools/lc.h`, đã được include sẵn):

```c
LC_CHECK(sum(12, 5) == 17);
LC_CHECK(sum(-10, 4) == -6);
```

`LC_CHECK` đếm số check; nếu biểu thức sai, nó in ra file:dòng và biểu thức bị lỗi. Cuối `main` phải `return lc_finish();` — dòng kết quả `LC-RESULT checks=... failed=...` mà `build_test.py` đọc chính là từ hàm này.

`tools/lc.h` cũng cung cấp helper cho dữ liệu LeetCode:

- `ListNode` / `TreeNode` định nghĩa giống hệt LeetCode.
- `lc_list_from_array`, `lc_list_equals_array`, `lc_list_free` — dựng/xác So sánh/giải phóng linked list.
- `lc_tree_from_level` (`LC_NULL` = node thiếu, tương ứng `null` trong `[1,null,2]`), `lc_tree_free` — dựng/giải phóng tree từ mảng level-order.
- `lc_int_array_equals` — so sánh hai mảng int.

Lưu ý: **không paste `lc.h` vào LeetCode** — LeetCode đã tự định nghĩa `ListNode`/`TreeNode`.

### 2. Chạy build & test

```bash
# Tất cả các bài trong repo
python tools/build_test.py

# Chỉ một bài (hoặc cả một topic / một ngôn ngữ)
python tools/build_test.py c/array-string/2235_add-two-integers
python tools/build_test.py c/hash
```

Mỗi bài in một dòng trạng thái, sau đó là dòng summary. Exit code: `1` nếu có bài fail, `2` nếu lỗi usage/toolchain.

Cờ tùy chọn:

- `--sanitize`: build với AddressSanitizer + UBSan để bắt out-of-bounds, use-after-free, leak... Binary đặt tại `build/asan/`. Trên Windows cần MSYS2 CLANG64 (cài từ https://www.msys2.org/, rồi `pacman -S mingw-w64-clang-x86_64-clang` trong shell MSYS2); script tự tìm `C:\msys64\clang64\bin`. Trên Linux GCC/Clang thường có sẵn.
- `--strict`: ngoài fail, còn fail cả khi bài ở trạng thái `TODO` hoặc `NO TESTS` — hữu ích khi muốn bảo đảm không bỏ sót bài nào.
- `--timeout S`: giây cho mỗi lần chạy test (mặc định 10).

Compiler được chọn tự động: `$CC`/`$CXX` nếu đặt, sau đó `clang` trên PATH, rồi MSYS2 CLANG64 (Windows), rồi `gcc`/`g++`. Compiler được chọn in ra đầu tiên ở đầu output. Cờ biên dịch: C `-std=c11`; C++ `-std=c++20` (hoặc `-std=c++17` nếu không hỗ trợ); luôn kèm `-Wall -Wextra -Werror`. Binary đặt trong `build/`.

### 3. Đọc trạng thái kết quả

| Trạng thái | Ý nghĩa |
| --- | --- |
| `PASS` | Tất cả check đều pass (số check in kèm theo) |
| `NO TESTS` | Chưa có `test.c`, hoặc chạy 0 check |
| `TODO` | `solution.c` vẫn còn marker `TODO: write your solution` (build lỗi là bình thường) |
| `BUILD FAIL` | Biên dịch lỗi — không phải do TODO; xem output lỗi bên dưới dòng trạng thái |
| `TEST FAIL` | Check fail, hoặc `main` không `return lc_finish()` (không tìm thấy dòng `LC-RESULT`), hoặc crash |
| `TIMEOUT` | Test chạy quá `--timeout` giây |
| `SANITIZER` | Sanitizer phát hiện lỗi (out-of-bounds, UB, leak...) khi chạy với `--sanitize` |

Các trạng thái `BUILD FAIL`, `TEST FAIL`, `TIMEOUT`, `SANITIZER` làm exit code khác 0.

Lưu ý: LeetCode chạy C/C++ với AddressSanitizer, nên bug out-of-bounds/use-after-free có thể "chạy được" locally nhưng fail trên LeetCode — chạy `--sanitize` trước khi submit giúp bắt nhóm bug này.

### 4. Submit lên LeetCode

Khi test local pass: mở `solution.c`, copy toàn bộ nội dung dán vào editor của LeetCode và submit ở đó. Repo không submit tự động và không lưu credential LeetCode nào. Sau đó điền cột LeetCode trong `progress.md`.

## Kiểm tra tooling

`python tools/selftest.py` chạy tự kiểm tra toàn bộ tooling offline (trên sample tạm trong thư mục temp), ghi log đầy đủ vào `build/selftest.log`.
