# React Reconciliation, Key và State Preservation

## Thông Tin File

- **Chủ đề:** Reconciliation, Key, Re-render, Remount và State Preservation
- **Ngôn ngữ / Framework:** React
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Reconciliation trong React là gì?

**Mức độ:** Trung cấp

### Câu hỏi

React reconciliation là gì? Khi state hoặc props thay đổi, React quyết định update DOM như thế nào?

### Câu trả lời ngắn gọn

Reconciliation là quá trình React so sánh cây element mới với cây cũ để xác định phần nào cần update. React không diff trực tiếp DOM thật từng lần render, mà diff trên virtual tree rồi áp thay đổi tối thiểu xuống DOM. Quyết định preserve hay reset state phụ thuộc vào type của element và `key`.

### Giải thích chi tiết

Mỗi lần component render, React tạo ra một tree element mới. Thuật toán reconciliation sẽ so sánh node cũ và node mới theo một số heuristic:

- Nếu type khác nhau, React coi đó là node mới và remount
- Nếu type giống nhau, React cập nhật props và giữ state nội bộ
- Với list, `key` giúp React ghép đúng item cũ và mới

Hiểu đúng điểm này giúp giải thích vì sao cùng một JSX nhưng state có lúc được giữ, có lúc bị reset.

### Ví dụ minh họa

```jsx
function App({ isAdmin }) {
  return (
    <div>
      {isAdmin ? <Dashboard /> : <Dashboard />}
    </div>
  );
}

// Cùng type Dashboard ở cùng vị trí
// React sẽ preserve state của Dashboard khi isAdmin đổi
```

```jsx
function App({ isAdmin }) {
  return (
    <div>
      {isAdmin ? <AdminDashboard /> : <UserDashboard />}
    </div>
  );
}

// Khác type component
// React sẽ unmount component cũ và mount component mới
```

### Lưu ý / Bẫy thường gặp

- "Render" không đồng nghĩa với "DOM update"; component có thể render nhưng DOM thay đổi rất ít
- Reconciliation dựa vào type và key, không phải chỉ nhìn nội dung text
- Hiểu sai preserve state vs remount là nguồn gốc của nhiều bug form và animation

---

## Câu Hỏi 2: Vì sao không nên dùng index làm `key` trong list?

**Mức độ:** Trung cấp

### Câu hỏi

Tại sao dùng `index` làm `key` trong list có thể gây bug? Cho một ví dụ thực tế thay vì trả lời lý thuyết chung chung.

### Câu trả lời ngắn gọn

Dùng `index` làm `key` khiến React ghép state theo vị trí thay vì theo identity thực của item. Khi list bị insert, delete hoặc reorder, state của item cũ có thể bị gán nhầm sang item khác. Điều này đặc biệt nguy hiểm với input, animation, checkbox, drag-and-drop và form editing.

### Giải thích chi tiết

`key` không phải để React tối ưu warning, mà là để giữ identity ổn định giữa các lần render. Nếu list chỉ append cuối và không reorder, `index` đôi khi chưa gây lỗi rõ rệt. Nhưng trong UI thực tế, list thường filter, sort, prepend hoặc remove item nên bug sẽ xuất hiện.

### Ví dụ minh họa

```jsx
function TodoList({ todos }) {
  return todos.map((todo, index) => (
    <TodoItem
      key={index} // ❌ Sai khi list có thể reorder hoặc xóa item
      todo={todo}
    />
  ));
}
```

```jsx
// Ví dụ bug: TodoItem có state local cho input edit
function TodoItem({ todo }) {
  const [draft, setDraft] = useState(todo.title);

  return (
    <input
      value={draft}
      onChange={(e) => setDraft(e.target.value)}
    />
  );
}

// Nếu xóa item đầu tiên, draft của item thứ hai có thể bị nhảy sang item khác
```

```jsx
// ✅ Dùng id ổn định từ dữ liệu
function TodoList({ todos }) {
  return todos.map((todo) => (
    <TodoItem
      key={todo.id}
      todo={todo}
    />
  ));
}
```

### Lưu ý / Bẫy thường gặp

- `Math.random()` còn tệ hơn `index` vì key thay đổi mỗi render, gây remount toàn bộ
- Nếu dữ liệu không có id ổn định, nên tạo id khi ingest data thay vì dùng index
- `index` chỉ chấp nhận được với list tĩnh, không reorder, không remove, không có state local phức tạp

---

## Câu Hỏi 3: Làm sao chủ động preserve hoặc reset state của component?

**Mức độ:** Trung cấp

### Câu hỏi

Trong React, làm sao để chủ động giữ lại hoặc reset state của một component khi UI chuyển tab, đổi mode hoặc đổi dữ liệu?

### Câu trả lời ngắn gọn

Muốn preserve state, giữ cùng component type ở cùng vị trí với cùng `key`. Muốn reset state, đổi `key` hoặc render sang component type khác. Đây là kỹ thuật rất hữu ích khi xử lý form nhiều mode như create/edit hoặc wizard nhiều bước.

### Giải thích chi tiết

React gắn state với vị trí trong tree kết hợp với identity của element. Vì vậy:

- Giữ cùng `type` và `key` -> state được preserve
- Đổi `key` -> React remount component -> state reset

Điểm này thường được dùng để reset form khi đổi user hoặc đổi chế độ màn hình.

### Ví dụ minh họa

```jsx
function UserEditor({ userId }) {
  return <UserForm key={userId} userId={userId} />;
}

function UserForm({ userId }) {
  const [draft, setDraft] = useState('');

  // Khi userId đổi, key đổi -> form được remount và draft reset
  return <input value={draft} onChange={(e) => setDraft(e.target.value)} />;
}
```

```jsx
// Muốn giữ state giữa các lần ẩn/hiện
function TabPanel({ activeTab }) {
  return (
    <>
      <section hidden={activeTab !== 'profile'}>
        <ProfileForm />
      </section>
      <section hidden={activeTab !== 'settings'}>
        <SettingsForm />
      </section>
    </>
  );
}

// Component vẫn tồn tại trong tree nên state có thể được giữ
```

### Lưu ý / Bẫy thường gặp

- Reset state bằng cách tự set nhiều `useState` về default thường kém rõ ràng hơn đổi `key`
- Ẩn component bằng CSS hoặc `hidden` không giống unmount
- Giữ state quá lâu có thể dẫn tới dữ liệu cũ nếu business flow yêu cầu reset

---

## Câu Hỏi So Sánh: Re-render vs Remount

**Mức độ:** Trung cấp

### Câu hỏi

`Re-render` và `remount` khác nhau như thế nào trong React? Vì sao phân biệt sai hai khái niệm này làm debug khó hơn?

### Bảng So Sánh

| Tiêu chí | Re-render | Remount |
|----------|-----------|---------|
| Component instance | Giữ nguyên | Tạo instance mới |
| Local state | Thường được giữ | Bị reset |
| Effect cleanup | Không nhất thiết chạy cleanup toàn phần | Cleanup cũ rồi mount lại |
| Nguyên nhân thường gặp | State/props/context đổi | `key` đổi hoặc type đổi |

### Câu trả lời ngắn gọn

Re-render là component chạy lại function render nhưng vẫn là cùng instance; remount là unmount instance cũ và mount instance mới. Khi remount, local state reset và lifecycle/effect chạy lại từ đầu. Phân biệt đúng hai trường hợp này giúp bạn xác định bug nằm ở props update hay identity của component.

### Giải thích chi tiết

Nhiều người nói "component bị rerender nên state mất", nhưng thực ra mất state thường do remount. Nếu chỉ re-render, state local vẫn còn. Trong thực tế, việc đổi `key`, đổi type component hoặc thay đổi cấu trúc tree là nguyên nhân phổ biến của remount ngoài ý muốn.

### Khi nào dùng cái nào?

- Dùng **re-render** như hành vi bình thường khi state/props thay đổi
- Chủ động tạo **remount** khi: cần reset form, reset animation, reset internal cache của component

### Ví dụ

```jsx
function App({ shouldReset, userId }) {
  return (
    <>
      <ProfileCard userId={userId} />
      <ProfileForm key={shouldReset ? userId : 'stable'} userId={userId} />
    </>
  );
}

// ProfileCard thường chỉ re-render khi props đổi
// ProfileForm có thể remount khi key thay đổi
```

### Lưu ý / Bẫy thường gặp

- Log `console.log('render')` không đủ để biết remount hay re-render
- Có thể dùng cleanup trong effect để xác định component có bị unmount hay không
- Debug state mất đột ngột nên kiểm tra `key` trước khi tối ưu performance

---

## Tài Liệu Tham Khảo

- [React Docs - Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)
- [React Docs - Rendering Lists](https://react.dev/learn/rendering-lists)

