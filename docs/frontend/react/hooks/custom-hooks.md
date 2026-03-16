# Custom Hooks trong React

## Thông Tin File

- **Chủ đề:** Custom Hooks, Reuse Logic, Side Effects và Dependency Management
- **Ngôn ngữ / Framework:** React
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Khi nào nên tách logic thành custom hook?

**Mức độ:** Trung cấp

### Câu hỏi

Khi nào bạn quyết định tách logic thành custom hook thay vì để nguyên trong component hoặc chuyển sang utility function?

### Câu trả lời ngắn gọn

Tôi tách thành custom hook khi logic gắn với React state, lifecycle hoặc side effects và cần tái sử dụng giữa nhiều component. Nếu chỉ là hàm thuần xử lý dữ liệu, utility function thường phù hợp hơn. Custom hook giúp code rõ ràng hơn khi nó đóng gói một behavior hoàn chỉnh thay vì chỉ gom code cho ngắn.

### Giải thích chi tiết

Custom hook nên được tạo khi logic có các dấu hiệu sau:

- Có `useState`, `useReducer`, `useEffect`, `useRef`
- Có một behavior rõ ràng như fetch data, listen resize, sync query param
- Nhiều component cùng lặp lại một flow giống nhau

Không nên tạo hook chỉ để bọc một hàm thuần hoặc giấu logic đơn giản một cách máy móc, vì điều đó làm code khó trace hơn.

### Ví dụ minh họa

```jsx
// ❌ Logic fetch lặp lại trong nhiều component
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function fetchUsers() {
      setLoading(true);
      const response = await fetch('/api/users');
      const data = await response.json();

      if (!cancelled) {
        setUsers(data);
        setLoading(false);
      }
    }

    fetchUsers();

    return () => {
      cancelled = true;
    };
  }, []);
}
```

```jsx
// ✅ Tách thành custom hook để tái sử dụng
function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function fetchUsers() {
      setLoading(true);
      const response = await fetch('/api/users');
      const data = await response.json();

      if (!cancelled) {
        setUsers(data);
        setLoading(false);
      }
    }

    fetchUsers();

    return () => {
      cancelled = true;
    };
  }, []);

  return { users, loading };
}
```

### Lưu ý / Bẫy thường gặp

- Đừng tạo custom hook chỉ vì "React khuyên dùng hooks"
- Hook tốt nên có API rõ ràng: input nào, output nào, side effect nào
- Nếu logic là pure function không phụ thuộc React, utility function thường đơn giản hơn

---

## Câu Hỏi 2: Thiết kế API của custom hook như thế nào để dễ dùng và dễ test?

**Mức độ:** Trung cấp

### Câu hỏi

Bạn thiết kế API cho một custom hook như thế nào để component dùng dễ hiểu, ít bug và có thể test được?

### Câu trả lời ngắn gọn

Tôi thiết kế hook theo hướng một trách nhiệm rõ ràng, input tối thiểu cần thiết và output ổn định, có tên dễ đoán. Hook nên trả về object nếu có nhiều giá trị để tăng readability, và tách side effect bên trong khỏi phần transform dữ liệu nếu có thể. Với async hook, nên expose trạng thái `loading`, `error`, `data` hoặc action rõ ràng.

### Giải thích chi tiết

Một custom hook dễ dùng thường có:

- Tên bắt đầu bằng `use` và phản ánh đúng behavior
- Input nhỏ gọn, tránh truyền cả object lớn nếu chỉ cần vài field
- Return shape nhất quán giữa các lần render
- Cleanup rõ ràng nếu có subscribe hoặc timer

Khi test, phần logic thuần nên được tách khỏi hook để unit test độc lập; phần hook có thể test bằng React Testing Library hoặc hook testing utilities.

### Ví dụ minh họa

```jsx
function useDebouncedValue(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timerId = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timerId); // Cleanup để không giữ timer cũ
    };
  }, [value, delay]);

  return debouncedValue;
}

function SearchInput() {
  const [keyword, setKeyword] = useState('');
  const debouncedKeyword = useDebouncedValue(keyword, 400);

  useEffect(() => {
    // Chỉ gọi API khi giá trị debounce thay đổi
    fetchSearchResult(debouncedKeyword);
  }, [debouncedKeyword]);

  return <input value={keyword} onChange={(e) => setKeyword(e.target.value)} />;
}
```

### Lưu ý / Bẫy thường gặp

- Trả về array khi hook có nhiều field dễ làm người dùng nhầm vị trí
- Hook async nên xử lý race condition hoặc cleanup cơ bản
- Đừng để hook vừa fetch, vừa map UI text, vừa mở modal; trách nhiệm nên rõ ràng

---

## Câu Hỏi 3: Stale closure trong custom hook là gì và tránh như thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

`Stale closure` trong custom hook là gì? Cho một ví dụ thực tế và cách fix.

### Câu trả lời ngắn gọn

`Stale closure` xảy ra khi callback hoặc effect giữ giá trị cũ của state/props vì dependency không được cập nhật đúng. Kết quả là hook vẫn chạy nhưng dùng dữ liệu lỗi thời. Cách fix phổ biến là khai báo dependency đầy đủ, dùng functional update, hoặc lưu giá trị mới nhất trong `ref` khi cần.

### Giải thích chi tiết

Trong React, mỗi lần render tạo ra closure mới. Nếu effect hoặc callback được tạo ở render cũ và không được cập nhật khi dependency đổi, nó sẽ tiếp tục dùng dữ liệu cũ. Lỗi này hay gặp ở `setInterval`, event listener, debounce, websocket handler và custom hook trừu tượng hóa các logic đó.

### Ví dụ minh họa

```jsx
// ❌ Bug stale closure
function useAutoSave(value) {
  useEffect(() => {
    const timerId = setInterval(() => {
      saveDraft(value); // Có thể dùng giá trị cũ nếu dependency sai
    }, 5000);

    return () => clearInterval(timerId);
  }, []); // Thiếu dependency value
}
```

```jsx
// ✅ Cách đơn giản: khai báo dependency đầy đủ
function useAutoSave(value) {
  useEffect(() => {
    const timerId = setInterval(() => {
      saveDraft(value);
    }, 5000);

    return () => clearInterval(timerId);
  }, [value]);
}
```

```jsx
// ✅ Khi không muốn re-subscribe liên tục: dùng ref giữ giá trị mới nhất
function useAutoSave(value) {
  const latestValueRef = useRef(value);

  useEffect(() => {
    latestValueRef.current = value;
  }, [value]);

  useEffect(() => {
    const timerId = setInterval(() => {
      saveDraft(latestValueRef.current);
    }, 5000);

    return () => clearInterval(timerId);
  }, []);
}
```

### Lưu ý / Bẫy thường gặp

- Tắt ESLint `exhaustive-deps` bừa bãi thường che giấu bug thay vì giải quyết nó
- Dùng `ref` là giải pháp có chủ đích, không phải cách né dependency thiếu hiểu biết
- Functional update như `setCount((prev) => prev + 1)` cũng là cách tránh stale state phổ biến

---

## Câu Hỏi So Sánh: Custom Hook vs Utility Function

**Mức độ:** Trung cấp

### Câu hỏi

Khác nhau giữa custom hook và utility function là gì? Khi nào nên chọn cái nào?

### Bảng So Sánh

| Tiêu chí | Custom Hook | Utility Function |
|----------|-------------|------------------|
| Dùng React hooks bên trong | Có | Không |
| Gắn với lifecycle/state | Có | Không |
| Dễ tái sử dụng logic UI behavior | Tốt | Hạn chế |
| Dùng ngoài React | Không phù hợp | Phù hợp |

### Câu trả lời ngắn gọn

Custom hook dành cho logic gắn với React như state, effect, ref và lifecycle; utility function dành cho logic thuần không phụ thuộc React. Nếu behavior cần subscribe, cleanup hoặc đồng bộ state, nên dùng hook. Nếu chỉ format dữ liệu hoặc tính toán, utility function đơn giản hơn.

### Giải thích chi tiết

Việc chọn sai abstraction làm code kém rõ ràng. Nhiều codebase bọc cả hàm thuần vào hook chỉ để "đồng bộ naming", khiến component khó test hơn và phụ thuộc React không cần thiết. Ngược lại, cố nhét logic side effect vào utility function làm bạn mất lifecycle management.

### Khi nào dùng cái nào?

- Dùng **custom hook** khi: cần `useState`, `useEffect`, `useRef`, subscribe event, sync browser API
- Dùng **utility function** khi: format tiền, sort data, validate input, map response

### Ví dụ

```jsx
function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
    }

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return width;
}
```

```javascript
function formatCurrency(value) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
  }).format(value);
}
```

### Lưu ý / Bẫy thường gặp

- Utility function không được gọi hook bên trong
- Custom hook vẫn phải tuân thủ Rules of Hooks như component
- Tên `useSomething` chỉ nên dùng khi nó thực sự là hook

---

## Tài Liệu Tham Khảo

- [React Docs - Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [React Docs - Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)

