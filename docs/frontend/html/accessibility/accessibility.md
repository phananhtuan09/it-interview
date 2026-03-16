# Accessibility cho Frontend

## Thông Tin File

- **Chủ đề:** Accessibility, Semantic HTML, Keyboard Navigation và ARIA
- **Ngôn ngữ / Framework:** HTML
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Bạn kiểm tra accessibility của một form như thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Nếu interviewer hỏi bạn cách làm một form accessible, bạn sẽ kiểm tra những điểm nào đầu tiên?

### Câu trả lời ngắn gọn

Tôi kiểm tra label có gắn đúng với input, thông báo lỗi có được screen reader đọc, keyboard có thao tác được đầy đủ và color contrast có đủ không. Ngoài ra cần dùng semantic HTML đúng như `button`, `label`, `fieldset`, `legend`. Một form accessible không chỉ "dùng được bằng chuột", mà phải dùng được bằng bàn phím và công cụ hỗ trợ.

### Giải thích chi tiết

Checklist thực tế cho form:

- Mỗi input có label rõ ràng
- Field bắt buộc được biểu đạt bằng text, không chỉ bằng màu
- Error message liên kết với input qua `aria-describedby`
- Thứ tự focus hợp lý
- Submit bằng Enter hoạt động đúng

### Ví dụ minh họa

```html
<form>
  <div>
    <label for="email">Email</label>
    <input
      id="email"
      name="email"
      type="email"
      aria-describedby="email-error"
      aria-invalid="true"
    />
    <p id="email-error">Email không đúng định dạng.</p>
  </div>

  <button type="submit">Gửi</button>
</form>
```

### Lưu ý / Bẫy thường gặp

- Placeholder không thay thế cho label
- Chỉ đổi viền sang màu đỏ là chưa đủ nếu không có text hoặc state cho screen reader
- `div` click được không tự động có keyboard behavior như `button`

---

## Câu Hỏi 2: Làm modal accessible cần chú ý gì?

**Mức độ:** Trung cấp

### Câu hỏi

Bạn xây modal như thế nào để hỗ trợ keyboard và screen reader đúng chuẩn cơ bản?

### Câu trả lời ngắn gọn

Modal cần có role phù hợp, tiêu đề rõ ràng, focus được đưa vào modal khi mở và trả về phần tử cũ khi đóng. Người dùng phải đóng được bằng keyboard, thường là `Escape`, và tab focus không được thoát ra ngoài modal khi nó đang mở. Đồng thời phần nội dung nền phía sau nên bị vô hiệu hóa tương tác.

### Giải thích chi tiết

Những điểm interviewer hay chờ bạn nhắc tới:

- `role="dialog"` hoặc dùng phần tử/dialog pattern phù hợp
- `aria-modal="true"`
- Focus trap trong modal
- Restore focus khi đóng
- Ẩn hoặc inert phần nền phía sau

### Ví dụ minh họa

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  class="modal"
>
  <h2 id="modal-title">Xác nhận xóa</h2>
  <p>Hành động này không thể hoàn tác.</p>

  <button type="button">Hủy</button>
  <button type="button">Xóa</button>
</div>
```

```javascript
// Pseudo code cho focus management
function openModal(triggerButton, modalElement) {
  const previousActiveElement = triggerButton;
  const firstFocusable = modalElement.querySelector('button, [href], input');

  firstFocusable?.focus(); // Đưa focus vào modal khi mở

  return () => {
    previousActiveElement.focus(); // Trả focus về phần tử cũ khi đóng
  };
}
```

### Lưu ý / Bẫy thường gặp

- Chỉ render modal đẹp chưa đủ, keyboard flow mới là phần hay bị bỏ sót
- `role="dialog"` không tự sinh ra focus trap, bạn vẫn phải xử lý behavior
- Nhiều thư viện UI hỗ trợ a11y sẵn, nhưng team vẫn cần hiểu nguyên lý để dùng đúng

---

## Câu Hỏi 3: Semantic HTML và ARIA khác nhau thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Phân biệt semantic HTML và ARIA. Tại sao nguyên tắc "native first" lại quan trọng khi làm accessibility?

### Câu trả lời ngắn gọn

Semantic HTML dùng đúng phần tử có sẵn như `button`, `nav`, `main`, `label`, còn ARIA dùng để bổ sung ngữ nghĩa khi native HTML chưa đủ. Nguyên tắc "native first" quan trọng vì phần tử native đã có sẵn keyboard behavior, focus behavior và semantics tốt hơn. ARIA chỉ nên bổ sung, không nên thay thế bừa bãi cho HTML chuẩn.

### Giải thích chi tiết

Ví dụ:

- Dùng `<button>` tốt hơn `<div role="button">`
- Dùng `<input type="checkbox">` tốt hơn tự dựng checkbox bằng `div`
- Chỉ thêm `aria-*` khi thật sự cần diễn đạt trạng thái hoặc mối quan hệ mà HTML thuần chưa thể hiện

ARIA sai còn nguy hiểm hơn không dùng ARIA, vì nó có thể làm screen reader hiểu lệch.

### Ví dụ minh họa

```html
<!-- ❌ Không ưu tiên native -->
<div role="button" tabindex="0">Lưu</div>

<!-- ✅ Đúng: dùng phần tử semantic -->
<button type="button">Lưu</button>
```

```html
<!-- ✅ ARIA bổ sung khi cần mô tả trạng thái -->
<button
  type="button"
  aria-expanded="false"
  aria-controls="faq-answer-1"
>
  Xem câu trả lời
</button>
<div id="faq-answer-1" hidden>
  Nội dung câu trả lời
</div>
```

### Lưu ý / Bẫy thường gặp

- `role="button"` không tự hỗ trợ phím Space/Enter như button native
- Đừng thêm ARIA nếu semantic HTML đã mô tả đủ
- Accessibility tốt bắt đầu từ cấu trúc HTML, không phải từ việc thêm hàng loạt `aria-*`

---

## Câu Hỏi So Sánh: Semantic HTML vs `div` + ARIA

**Mức độ:** Trung cấp

### Câu hỏi

So sánh cách dùng semantic HTML với cách dựng UI bằng `div` rồi thêm `role`/`aria-*`. Khi nào thực sự cần đến ARIA?

### Bảng So Sánh

| Tiêu chí | Semantic HTML | `div` + ARIA |
|----------|---------------|--------------|
| Semantics mặc định | Có | Phải tự thêm |
| Keyboard behavior mặc định | Có ở nhiều phần tử | Phải tự xử lý |
| Độ ổn định | Cao | Dễ sai hơn |
| Use case phù hợp | Hầu hết form, button, nav, table | Widget custom phức tạp |

### Câu trả lời ngắn gọn

Semantic HTML nên là lựa chọn mặc định vì nó đơn giản, đúng chuẩn và ít lỗi hơn. `div` + ARIA chỉ nên dùng khi bạn xây custom widget mà native element không đáp ứng đủ. Ngay cả khi dùng ARIA, bạn vẫn phải tự lo keyboard interaction và focus management.

### Giải thích chi tiết

Interviewer thường muốn nghe bạn nhắc rằng ARIA không phải "bùa thần" để biến mọi `div` thành accessible. Khi có thể dùng phần tử native thì nên dùng native trước. ARIA phát huy giá trị nhất ở các widget như combobox, tree view, tabs tùy biến hoặc trạng thái động cần mô tả rõ hơn.

### Khi nào dùng cái nào?

- Dùng **semantic HTML** khi: form, link, button, heading, table, list, nav
- Dùng **ARIA** khi: cần mô tả trạng thái mở/đóng, active descendant, relationship giữa các vùng, hoặc custom widget không có native equivalent tốt

### Ví dụ

```html
<nav aria-label="Điều hướng chính">
  <ul>
    <li><a href="/home">Trang chủ</a></li>
  </ul>
</nav>
```

```html
<button
  type="button"
  aria-expanded="true"
  aria-controls="menu-1"
>
  Mở menu
</button>
```

### Lưu ý / Bẫy thường gặp

- `aria-label` không thay thế hoàn toàn visible label trong nhiều form control
- Nếu custom widget quá phức tạp, dùng thư viện đã xử lý a11y tốt thường an toàn hơn
- Test bằng keyboard và screen reader cơ bản sẽ thực tế hơn chỉ đọc checklist

---

## Tài Liệu Tham Khảo

- [MDN - Accessibility](https://developer.mozilla.org/en-US/docs/Learn/Accessibility)
- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
