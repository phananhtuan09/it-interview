# Tối Ưu Re-render trong React

## Thông Tin File

- **Chủ đề:** Re-render Optimization
- **Ngôn ngữ / Framework:** React
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Các kỹ thuật tối ưu re-render trong React

**Mức độ:** Trung cấp

### Câu hỏi

Khi một component React re-render quá nhiều lần gây performance issue, bạn sẽ dùng những kỹ thuật nào để tối ưu? Hãy nêu ít nhất 3 cách và giải thích ngắn gọn.

### Câu trả lời ngắn gọn

Re-render trong React xảy ra khi state, props hoặc context thay đổi. Các kỹ thuật tối ưu chính: dùng `React.memo` để skip re-render khi props không đổi, `useMemo`/`useCallback` để memoize giá trị và hàm, tách nhỏ component để giảm phạm vi re-render, virtualization cho list lớn, và debounce cho search/filter. Kiểm tra bằng React DevTools Profiler để xác định bottleneck.

### Giải thích chi tiết

**Nguyên nhân re-render:**
1. State thay đổi (`useState`, `useReducer`)
2. Props thay đổi (parent re-render truyền props mới)
3. Context thay đổi (`useContext`)
4. Force update

**Các kỹ thuật tối ưu:**

**1. React.memo — tránh re-render khi props không đổi**
- Wrap component con để so sánh props trước khi re-render
- Chỉ hiệu quả khi props là primitive hoặc stable reference

**2. useMemo — memoize giá trị tính toán nặng**
- Tránh tính toán lại expensive computation mỗi render
- Trả về cached value nếu dependencies không đổi

**3. useCallback — memoize function reference**
- Tránh tạo function mới mỗi render
- Quan trọng khi function được truyền vào component con dùng React.memo

**4. Tách nhỏ component**
- Component nhỏ hơn = phạm vi re-render nhỏ hơn
- Component cha re-render không kéo component con re-render nếu props không đổi

**5. Virtualization cho list lớn**
- Chỉ render DOM element nằm trong viewport
- Thư viện: `react-window`, `react-virtualized`, `@tanstack/react-virtual`

**6. Debounce/throttle input**
- Giảm số lần re-render khi user typing trong search/filter

### Ví dụ minh họa

```jsx
// ❌ Vấn đề: tạo inline object và inline function trong props
// → Component con re-render mỗi lần dù giá trị không đổi
function ParentBad() {
  const [count, setCount] = useState(0);

  return (
    <ChildComponent
      config={{ theme: 'dark' }}        // object mới mỗi render
      onClick={() => console.log('click')} // function mới mỗi render
    />
  );
}

// ✅ Tối ưu với useMemo + useCallback + React.memo
const ChildComponent = React.memo(function Child({ config, onClick }) {
  console.log('Child render'); // chỉ log khi thực sự cần re-render
  return <button onClick={onClick}>{config.theme}</button>;
});

function ParentGood() {
  const [count, setCount] = useState(0);

  // Stable reference — không tạo mới mỗi render
  const config = useMemo(() => ({ theme: 'dark' }), []);
  const handleClick = useCallback(() => console.log('click'), []);

  return <ChildComponent config={config} onClick={handleClick} />;
}
```

```jsx
// ✅ useMemo cho expensive calculation
function ProductList({ products, filterText }) {
  // Chỉ tính lại khi products hoặc filterText thay đổi
  const filteredProducts = useMemo(
    () => products.filter(p => p.name.includes(filterText)),
    [products, filterText]
  );

  return <ul>{filteredProducts.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

```jsx
// ✅ Tách nhỏ component để giảm phạm vi re-render
// Thay vì để counter và heavy list trong cùng component:
function App() {
  return (
    <>
      <Counter />   {/* Re-render độc lập */}
      <HeavyList /> {/* Không bị kéo theo khi Counter re-render */}
    </>
  );
}
```

```jsx
// ✅ Debounce search input
import { useState, useCallback } from 'react';
import { debounce } from 'lodash';

function SearchBox({ onSearch }) {
  // debounce 300ms — không re-trigger search mỗi keystroke
  const debouncedSearch = useCallback(
    debounce((value) => onSearch(value), 300),
    [onSearch]
  );

  return <input onChange={(e) => debouncedSearch(e.target.value)} />;
}
```

### Lưu ý / Bẫy thường gặp

- `React.memo` chỉ so sánh **shallow** — với object/array lồng nhau phải dùng kèm `useMemo`
- Không nên memoize mọi thứ — memoization có overhead, chỉ dùng khi thực sự cần
- Tránh inline object `{}` và inline function `() => {}` trong JSX nếu component con dùng `React.memo`
- Dùng **React DevTools Profiler** để xác định component nào re-render nhiều trước khi tối ưu

---

## Tài Liệu Tham Khảo

- [React Docs - Skipping expensive recalculations](https://react.dev/reference/react/useMemo)
- [React Docs - React.memo](https://react.dev/reference/react/memo)
- [React DevTools Profiler](https://react.dev/learn/react-developer-tools)
