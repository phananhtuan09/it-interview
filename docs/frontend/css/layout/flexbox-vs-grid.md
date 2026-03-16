# Flexbox vs Grid trong CSS Layout

## Thông Tin File

- **Chủ đề:** Flexbox, CSS Grid, Responsive Layout và Overflow
- **Ngôn ngữ / Framework:** CSS
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Khi nào dùng Flexbox, khi nào dùng Grid?

**Mức độ:** Trung cấp

### Câu hỏi

Trong thực tế, bạn quyết định dùng Flexbox hay CSS Grid dựa trên tiêu chí nào? Hãy cho ví dụ tình huống cụ thể thay vì nêu định nghĩa một chiều.

### Câu trả lời ngắn gọn

Tôi dùng Flexbox khi layout chủ yếu theo một chiều, ví dụ căn hàng nút, navbar, card row hoặc phân bố item trong một trục. Tôi dùng Grid khi cần kiểm soát cả hàng lẫn cột, ví dụ dashboard, gallery, form layout nhiều vùng hoặc responsive layout phức tạp. Nói ngắn gọn: một chiều ưu tiên Flexbox, hai chiều ưu tiên Grid.

### Giải thích chi tiết

**Flexbox mạnh ở:**
- Căn chỉnh theo trục chính và trục phụ
- Phân phối khoảng trống linh hoạt
- Layout nội dung phụ thuộc kích thước phần tử

**Grid mạnh ở:**
- Chia vùng theo cả row và column
- Đặt item vào ô hoặc area rõ ràng
- Dễ diễn tả layout khung trang hơn

### Ví dụ minh họa

```css
/* Flexbox phù hợp cho thanh action */
.actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  align-items: center;
}
```

```css
/* Grid phù hợp cho dashboard */
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar content";
  min-height: 100vh;
}
```

### Lưu ý / Bẫy thường gặp

- Flexbox không "thay thế hoàn toàn" Grid, và Grid cũng không làm mọi thứ tốt hơn Flexbox
- Nhiều layout thực tế dùng kết hợp cả hai: Grid cho khung lớn, Flexbox cho item bên trong
- Chọn sai công cụ thường làm CSS dài và khó responsive hơn mức cần thiết

---

## Câu Hỏi 2: Làm sao xử lý layout card responsive mà không bị vỡ hàng?

**Mức độ:** Trung cấp

### Câu hỏi

Bạn cần hiển thị danh sách card responsive: desktop 4 cột, tablet 2 cột, mobile 1 cột. Bạn sẽ làm bằng Flexbox hay Grid, và xử lý spacing thế nào cho gọn?

### Câu trả lời ngắn gọn

Với bài toán card list nhiều cột rõ ràng, tôi ưu tiên Grid vì nó diễn tả số cột và khoảng cách gọn hơn. Có thể dùng `repeat(auto-fit, minmax(...))` để responsive mềm mà không cần quá nhiều media query. Nếu từng row cần chiều cao đều và gap nhất quán, Grid càng phù hợp.

### Giải thích chi tiết

Grid cho phép định nghĩa số cột theo không gian còn lại thay vì phải tính phần trăm width từng card. Điều này giảm nhu cầu hack `calc(...)` hoặc margin âm. Với Flexbox vẫn làm được, nhưng thường phải xử lý `flex-basis`, `wrap` và width cẩn thận hơn.

### Ví dụ minh họa

```css
.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.card {
  padding: 16px;
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  background: #fff;
}
```

```html
<!-- Card tự xuống hàng theo không gian khả dụng -->
<section class="card-list">
  <article class="card">Card 1</article>
  <article class="card">Card 2</article>
  <article class="card">Card 3</article>
</section>
```

### Lưu ý / Bẫy thường gặp

- `auto-fit` và `auto-fill` khác nhau; trả lời phỏng vấn nên nêu được ý chính
- Đừng trộn `width` cứng với Grid nếu muốn layout thật sự co giãn
- Gap trong Grid/Flex hiện đại thường tốt hơn giải pháp dùng margin thủ công

---

## Câu Hỏi 3: Vì sao item Flex/Grid hay bị tràn ngang dù đã đặt `overflow: hidden`?

**Mức độ:** Trung cấp

### Câu hỏi

Trong layout thực tế, vì sao một item bên trong Flexbox hoặc Grid có thể bị tràn ngang dù container đã cố gắng co giãn? Bạn sửa thế nào?

### Câu trả lời ngắn gọn

Nguyên nhân rất hay gặp là `min-width: auto` mặc định khiến item không chịu co nhỏ hơn intrinsic size của nội dung. Với Flexbox hoặc Grid, chỉ thêm `overflow: hidden` ở container chưa chắc đủ. Cách sửa thường là đặt `min-width: 0` hoặc `minmax(0, 1fr)` để item thực sự được phép co lại.

### Giải thích chi tiết

Trong Flexbox, flex item mặc định không phải lúc nào cũng co như bạn nghĩ. Nếu bên trong có chuỗi dài, table hoặc code block, item có thể giữ kích thước tối thiểu lớn hơn container. Tương tự với Grid, cột `1fr` đôi khi vẫn tràn nếu nội dung có min-content size lớn.

### Ví dụ minh họa

```css
/* ❌ Layout dễ tràn do item không được phép co đủ nhỏ */
.wrapper {
  display: flex;
}

.sidebar {
  width: 240px;
}

.content {
  flex: 1;
  /* Thiếu min-width: 0 */
}
```

```css
/* ✅ Cho phép content co nhỏ */
.wrapper {
  display: flex;
}

.sidebar {
  width: 240px;
  flex-shrink: 0;
}

.content {
  flex: 1;
  min-width: 0; /* Quan trọng để text dài không phá layout */
  overflow: hidden;
}
```

```css
/* ✅ Với Grid, dùng minmax(0, 1fr) để tránh tràn */
.layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
}
```

### Lưu ý / Bẫy thường gặp

- `text-overflow: ellipsis` không hoạt động nếu phần tử chưa được phép co
- Đây là bug layout rất phổ biến nhưng nhiều ứng viên không nhắc tới `min-width: 0`
- Với grid column, `1fr` không phải lúc nào cũng đủ nếu nội dung có min-content lớn

---

## Câu Hỏi So Sánh: Flexbox vs Grid

**Mức độ:** Trung cấp

### Câu hỏi

So sánh Flexbox và Grid về cách tư duy layout, khả năng responsive và maintainability.

### Bảng So Sánh

| Tiêu chí | Flexbox | Grid |
|----------|---------|------|
| Trục layout chính | Một chiều | Hai chiều |
| Căn chỉnh item | Rất mạnh | Tốt |
| Mô tả khung trang | Hạn chế hơn | Rất tốt |
| Responsive card layout | Làm được | Thường gọn hơn |
| Use case điển hình | Navbar, actions, row/column nhỏ | Dashboard, gallery, page layout |

### Câu trả lời ngắn gọn

Flexbox mạnh khi bạn cần phân phối item theo một trục và nội dung quyết định layout. Grid mạnh khi bạn muốn mô hình hóa cấu trúc hai chiều ngay từ đầu. Trong nhiều UI hiện đại, hai công cụ này bổ sung nhau thay vì cạnh tranh trực tiếp.

### Giải thích chi tiết

Nếu layout có khái niệm cột và hàng rõ ràng, Grid thường đọc code dễ hơn. Nếu mục tiêu chỉ là căn hàng hoặc dàn item theo một chiều, Flexbox gọn hơn và ít khai báo. Trả lời tốt trong phỏng vấn nên nhấn mạnh lựa chọn theo bài toán chứ không theo sở thích.

### Khi nào dùng cái nào?

- Dùng **Flexbox** khi: căn nút, thanh menu, media object, list theo trục
- Dùng **Grid** khi: layout khung trang, dashboard, form nhiều cột, card gallery responsive

### Ví dụ

```css
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}
```

### Lưu ý / Bẫy thường gặp

- Không cần ép toàn bộ hệ thống dùng một loại layout duy nhất
- Trả lời phỏng vấn nên nêu bài toán thật như dashboard hoặc button group
- Nên nhớ thêm các bẫy `min-width: 0`, `auto-fit`, `auto-fill` để câu trả lời sâu hơn mức cơ bản

---

## Tài Liệu Tham Khảo

- [MDN - Basic concepts of flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- [MDN - Basic concepts of grid layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout)
