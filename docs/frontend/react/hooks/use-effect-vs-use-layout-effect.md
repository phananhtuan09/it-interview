# useEffect vs useLayoutEffect

## Thông Tin File

- **Chủ đề:** useEffect vs useLayoutEffect
- **Ngôn ngữ / Framework:** React
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi So Sánh: useEffect vs useLayoutEffect

**Mức độ:** Trung cấp

### Câu hỏi

Sự khác nhau giữa `useEffect` và `useLayoutEffect` là gì? Trong trường hợp thực tế nào bạn sẽ chọn `useLayoutEffect` thay vì `useEffect`?

### Bảng So Sánh

| Tiêu chí              | `useEffect`                        | `useLayoutEffect`                    |
|-----------------------|------------------------------------|--------------------------------------|
| Thời điểm chạy        | Sau khi browser paint UI           | Sau khi DOM update, trước khi paint  |
| Blocking render       | Không                              | Có (synchronous)                     |
| Ảnh hưởng performance | Nhẹ hơn, không block UI            | Nặng hơn nếu dùng nhiều              |
| Use case chính        | API call, logging, event listener  | Đọc/chỉnh layout DOM, tránh flicker |
| SSR                   | An toàn                            | Cần cẩn thận (chạy client-only)      |

### Câu trả lời ngắn gọn

`useEffect` chạy **sau khi browser đã vẽ UI** — phù hợp cho side effects không ảnh hưởng giao diện như gọi API, gắn event listener, logging. `useLayoutEffect` chạy **sau khi React cập nhật DOM nhưng trước khi browser paint** — dùng khi cần đọc kích thước element hoặc thay đổi layout để tránh UI bị nhấp nháy (flicker).

### Giải thích chi tiết

**Thứ tự thực thi trong React:**

```
React render → DOM update → useLayoutEffect → Browser paint → useEffect
```

**useEffect (phổ biến hơn):**
- Chạy bất đồng bộ sau khi browser paint
- Không block quá trình vẽ giao diện
- Phù hợp cho mọi side effect không cần đọc/ghi DOM ngay lập tức

**useLayoutEffect (dùng khi thực sự cần):**
- Chạy đồng bộ (synchronous) — block browser paint cho đến khi callback chạy xong
- Nếu thực hiện DOM mutation trong đây, user sẽ không thấy trạng thái trung gian → tránh flicker
- Hành vi giống `componentDidMount` / `componentDidUpdate` trong class component

### Khi nào dùng cái nào?

- Dùng **`useEffect`** khi: gọi API, subscribe event, logging, set timer — bất cứ thứ gì không cần đọc/sửa DOM layout ngay
- Dùng **`useLayoutEffect`** khi:
  - Đo kích thước element (`getBoundingClientRect`)
  - Tính toán position tooltip / modal / popover
  - Sync scroll position
  - Bất kỳ animation cần đồng bộ với DOM

### Ví dụ minh họa

```jsx
// ✅ useEffect — gọi API, không cần đọc DOM
useEffect(() => {
  fetchUserData(userId).then(setUser);
}, [userId]);

// ✅ useLayoutEffect — đo kích thước element để tính position tooltip
function Tooltip({ targetRef, content }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const tooltipRef = useRef(null);

  useLayoutEffect(() => {
    if (!targetRef.current || !tooltipRef.current) return;

    // Đọc kích thước trước khi browser vẽ → không bị flicker
    const targetRect = targetRef.current.getBoundingClientRect();
    const tooltipRect = tooltipRef.current.getBoundingClientRect();

    setPosition({
      top: targetRect.bottom + 8,
      left: targetRect.left - tooltipRect.width / 2,
    });
  }, [targetRef]);

  return (
    <div ref={tooltipRef} style={{ position: 'fixed', ...position }}>
      {content}
    </div>
  );
}
```

```jsx
// ❌ Sai — dùng useEffect để đo DOM gây flicker
useEffect(() => {
  // User có thể thấy tooltip ở vị trí sai trong 1 frame trước khi correction
  const rect = targetRef.current.getBoundingClientRect();
  setPosition(calculatePosition(rect));
}, []);

// ✅ Đúng — dùng useLayoutEffect
useLayoutEffect(() => {
  const rect = targetRef.current.getBoundingClientRect();
  setPosition(calculatePosition(rect));
}, []);
```

### Lưu ý / Bẫy thường gặp

- `useLayoutEffect` là **synchronous** → nếu có tác vụ nặng sẽ block render, làm app bị lag
- Không nên dùng `useLayoutEffect` cho API call — dùng `useEffect` thay thế
- Trên server-side rendering (SSR), `useLayoutEffect` sẽ gây warning vì không có DOM. Dùng `useEffect` hoặc check `typeof window !== 'undefined'`
- Mặc định luôn dùng `useEffect`, chỉ chuyển sang `useLayoutEffect` khi thực sự gặp vấn đề flicker

---

## Tài Liệu Tham Khảo

- [React Docs - useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)
- [React Docs - useEffect](https://react.dev/reference/react/useEffect)
