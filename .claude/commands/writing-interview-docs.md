Tạo file tài liệu phỏng vấn frontend theo đúng cấu trúc và format quy định.

## Hướng dẫn sử dụng

Cung cấp thông tin sau để tôi tạo file:
1. **Chủ đề** (topic): ví dụ "closures", "useEffect", "flexbox vs grid"
2. **Ngôn ngữ / Framework**: javascript | typescript | css | html | react | vue | nextjs | nuxtjs | general
3. **Mức độ**: cơ bản | trung cấp | nâng cao | hỗn hợp
4. **Danh sách câu hỏi** (nếu có sẵn, nếu không tôi sẽ tự đề xuất)

## Quy trình thực hiện

### Bước 1 — Xác định đường dẫn file
Dựa vào thông tin người dùng cung cấp, xác định:
- **Thư mục cấp 1**: ngôn ngữ hoặc framework (ví dụ: `docs/frontend/react/`)
- **Thư mục cấp 2**: topic (ví dụ: `docs/frontend/react/hooks/`)
- **Tên file**: kebab-case từ tên topic (ví dụ: `use-effect.md`)

Đường dẫn cuối cùng: `docs/frontend/{ngôn-ngữ}/{topic}/{tên-file}.md`

### Bước 2 — Tạo thư mục nếu chưa tồn tại
Tạo đủ các thư mục theo cấu trúc đã xác định.

### Bước 3 — Tạo nội dung file theo template
Tuân thủ format trong `docs/frontend/TEMPLATE.md`:

```
## Thông Tin File
- Chủ đề, Ngôn ngữ/Framework, Mức độ, Ngày tạo

## Câu Hỏi N: [Tiêu đề]
- Mức độ
- Câu hỏi
- Câu trả lời ngắn gọn
- Giải thích chi tiết
- Ví dụ minh họa (code block)
- Lưu ý / Bẫy thường gặp

## Câu Hỏi So Sánh (nếu là câu so sánh)
- Bảng so sánh
- Khi nào dùng cái nào

## Tài Liệu Tham Khảo
```

### Bước 4 — Kiểm tra và xác nhận
Sau khi tạo file, thông báo:
- Đường dẫn file đã tạo
- Số lượng câu hỏi đã có
- Gợi ý câu hỏi có thể bổ sung thêm

## Quy tắc bắt buộc

- Toàn bộ nội dung viết bằng **tiếng Việt**
- Tên thư mục và file dùng **kebab-case**, chữ thường
- Mỗi câu hỏi phải có đủ 5 phần: câu hỏi, trả lời ngắn, giải thích chi tiết, ví dụ code, lưu ý
- Code example phải có comment giải thích bằng tiếng Việt
- Câu trả lời ngắn gọn tối đa 4 câu — phù hợp trả lời nhanh khi phỏng vấn
- Không tạo nội dung chung chung, phải cụ thể và thực tế

## Ví dụ

**Input của người dùng:**
> Tạo file về closures trong JavaScript, mức trung cấp

**Output mong đợi:**
- Tạo thư mục `docs/frontend/javascript/closures/` nếu chưa có
- Tạo file `docs/frontend/javascript/closures/closures.md`
- Nội dung gồm 3-5 câu hỏi phỏng vấn thực tế về closures
- Mỗi câu hỏi đầy đủ theo template
