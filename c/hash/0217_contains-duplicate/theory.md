# Lý thuyết nền: 217. Contains Duplicate

> Tài liệu định hướng do AI tạo ngày 2026-11-12. Không chứa lời giải. Mỗi gợi ý ở mục 4 chỉ mở khi đã tự thử mà vẫn kẹt.

- Đề bài: https://leetcode.com/problems/contains-duplicate/
- Thư mục: `c/hash/0217_contains-duplicate`

## 1. Đọc đề và ngân sách độ phức tạp

- Ràng buộc: `1 <= nums.length <= 10^5`, `-10^9 <= nums[i] <= 10^9`. Với tối đa `10^5` phần tử, ngân sách gần đúng `10^8` phép tính đơn giản mỗi giây thường đủ cho cách làm tuyến tính hoặc `O(n log n)`. Cách làm `O(n^2)` có thể cần tới khoảng `10^10` lượt so sánh ở kích thước lớn nhất, vượt xa ngân sách đó.
- Tự kiểm tra: Đầu ra cần thể hiện điều gì về các giá trị trong mảng?
- Tự kiểm tra: Mảng một phần tử có thể thỏa điều kiện nào của đề?
- Tự kiểm tra: Giá trị âm và dương nằm trong khoảng nào?

## 2. Kiến thức nền cần nắm

### Bảng băm (hash table)

- Là gì: Cấu trúc dữ liệu dùng hàm băm để ánh xạ khóa vào các vị trí lưu trữ, giúp tìm kiếm theo khóa nhanh trong trường hợp thông thường.
- Thao tác chính và độ phức tạp: Thêm, tra cứu và xóa thường có thời gian trung bình `O(1)`; trường hợp xấu nhất có thể là `O(n)` do va chạm. Bộ nhớ phụ thường là `O(n)` cho `n` khóa.
- Câu hỏi tự kiểm tra: Vì sao hai khóa khác nhau vẫn có thể được ánh xạ đến cùng một vị trí?
- Đọc thêm: [Hash table](https://en.wikipedia.org/wiki/Hash_table), [Visualgo: hash table](https://visualgo.net/en/hashtable), [uthash user guide](https://troydhanson.github.io/uthash/userguide.html).

### Sắp xếp (sorting)

- Là gì: Sắp xếp tổ chức các phần tử theo một thứ tự xác định. Với dữ liệu so sánh tổng quát, các thuật toán phổ biến thường cần `O(n log n)` thời gian; bộ nhớ phụ tùy thuật toán.
- Thao tác chính và độ phức tạp: So sánh và đổi vị trí các phần tử; nhiều thuật toán phổ biến chạy trong `O(n log n)`, còn một số cách đơn giản có thể cần `O(n^2)`. Có thuật toán dùng bộ nhớ phụ `O(1)`, có thuật toán cần `O(n)`.
- Câu hỏi tự kiểm tra: Khi dữ liệu đã có thứ tự, quan hệ giữa hai phần tử kề nhau có thể giúp ta nhận ra điều gì?
- Đọc thêm: [Sorting algorithms](https://en.wikipedia.org/wiki/Sorting_algorithm), [Visualgo: sorting](https://visualgo.net/en/sorting), [USACO: sorting](https://usaco.guide/bronze/intro-sorting).

## 3. Kiến thức C cần cho bài này

- Bảng băm: Thư viện chuẩn C không có hash set. LeetCode cung cấp uthash, nhưng môi trường luyện tập cục bộ không có sẵn thư viện đó. Nếu tự quản lý các nút được cấp phát động, cần giải phóng từng nút đã thêm bằng `free`. Mảng đánh địa chỉ trực tiếp chỉ hợp lý khi miền giá trị nhỏ; ở đây miền từ `-10^9` đến `10^9` có `2*10^9+1` giá trị, quá lớn để dùng làm mảng theo giá trị. Xem [`malloc` và quản lý bộ nhớ trong C](https://en.cppreference.com/w/c/memory/malloc).
- Sắp xếp: `qsort` sắp xếp trực tiếp mảng được truyền vào. Hàm so sánh phải trả về số âm, `0` hoặc số dương để biểu thị thứ tự. Không nên trả về hiệu `a - b`: hai giá trị `-10^9` và `10^9` có độ chênh `2*10^9`, lớn hơn `INT_MAX`, nên phép trừ kiểu `int` có thể tràn. Xem [`qsort`](https://en.cppreference.com/w/c/algorithm/qsort), [giới hạn kiểu số nguyên](https://en.cppreference.com/w/c/types/limits) và [tràn số nguyên](https://en.wikipedia.org/wiki/Integer_overflow).

## 4. Gợi ý theo bậc (mở dần)

<details><summary>Gợi ý 1 - quan sát</summary>

Nếu mọi phần tử đều khác nhau, mối quan hệ nào giữa số lần xuất hiện của mỗi giá trị và đầu ra?

</details>

<details><summary>Gợi ý 2 - suy nghĩ thêm</summary>

Có đặc điểm nào của thứ tự các giá trị hoặc cách ghi nhớ giá trị đã gặp giúp việc phát hiện lặp lại hiệu quả hơn?

</details>

<details><summary>Gợi ý 3 - nhóm khái niệm</summary>

Bảng băm hoặc sắp xếp.

</details>

## 5. Bẫy thường gặp và edge cases

- Nếu mảng có kích thước nhỏ nhất theo ràng buộc, điều gì có thể kết luận về các lần xuất hiện?
- Nếu giá trị lặp nằm ở hai đầu mảng, câu trả lời có phụ thuộc vào vị trí của chúng không?
- Nếu mọi giá trị đều âm, điều kiện về trùng lặp có thay đổi không?
- Nếu các giá trị ở sát `-10^9` và `10^9`, phép tính trung gian nào có thể vượt giới hạn kiểu `int`?
- Nếu một giá trị xuất hiện nhiều hơn hai lần, đầu ra cần phản ánh điều kiện nào?

## 6. Bài tương tự để luyện

- [1. Two Sum](https://leetcode.com/problems/two-sum/) — luyện tra cứu khóa và phân tích thời gian trung bình của bảng băm.
- [349. Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) — luyện tư duy tập hợp và cách xử lý giá trị trùng.
- [350. Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/) — luyện so sánh cách tổ chức dữ liệu khi số lần xuất hiện có ý nghĩa.

## 7. Tài liệu tổng quát

- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [USACO Guide: time complexity](https://usaco.guide/bronze/time-comp)
- [NeetCode roadmap](https://neetcode.io/roadmap)
