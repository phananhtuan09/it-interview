# Context API vs Redux Toolkit

## Thông Tin File

- **Chủ đề:** Context API, Redux Toolkit, Global State và Re-render Strategy
- **Ngôn ngữ / Framework:** React
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Khi nào Context API là đủ, khi nào nên dùng Redux Toolkit?

**Mức độ:** Trung cấp

### Câu hỏi

Trong dự án React thực tế, bạn quyết định dùng Context API hay Redux Toolkit theo tiêu chí nào? Hãy trả lời bằng tình huống cụ thể thay vì nêu định nghĩa chung.

### Câu trả lời ngắn gọn

Tôi dùng Context khi state tương đối nhỏ, thay đổi không quá thường xuyên và consumer ít, ví dụ theme, locale, auth session đơn giản. Tôi chọn Redux Toolkit khi state lớn hơn, nhiều màn hình cùng truy cập, cần trace action, middleware, normalized store hoặc debug tốt hơn. Quyết định nên dựa trên fan-out của state và độ phức tạp luồng cập nhật, không chỉ dựa trên số file.

### Giải thích chi tiết

**Context phù hợp khi:**
- State cấu hình như theme, language, permission snapshot
- Số component đọc state không quá lớn
- Không cần lịch sử action hay middleware phức tạp

**Redux Toolkit phù hợp khi:**
- Nhiều feature cùng đọc/ghi shared state
- Cần selector, devtools, async flow rõ ràng
- Muốn enforce cấu trúc state và side effect thống nhất

### Ví dụ minh họa

```jsx
// Context cho theme là use case phù hợp
const ThemeContext = createContext(null);

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

```typescript
// Redux Toolkit phù hợp cho state nghiệp vụ phức tạp
interface CartState {
  items: Array<{ id: string; quantity: number; price: number }>;
  couponCode: string | null;
  loading: boolean;
}

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    couponCode: null,
    loading: false,
  } satisfies CartState,
  reducers: {
    addItem(state, action) {
      state.items.push(action.payload);
    },
  },
});
```

### Lưu ý / Bẫy thường gặp

- Context không phải "Redux phiên bản nhẹ" cho mọi trường hợp
- Redux cũng không phải luôn overkill nếu app thực sự có state flow phức tạp
- Đừng nhét server state như cache API lớn vào Context nếu nó update thường xuyên

---

## Câu Hỏi 2: Vì sao Context dễ gây re-render lan rộng và giảm nó bằng cách nào?

**Mức độ:** Trung cấp

### Câu hỏi

Context API có nhược điểm gì về performance? Nếu một provider chứa nhiều state, bạn tối ưu re-render thế nào?

### Câu trả lời ngắn gọn

Khi `value` của Context thay đổi, toàn bộ consumer của context đó có thể re-render dù chỉ cần một phần nhỏ dữ liệu. Để giảm vấn đề này, tôi tách context theo domain, memoize value khi hợp lý và tránh nhét state cập nhật liên tục vào một provider lớn. Với case phức tạp hơn, selector-based store như Redux, Zustand hoặc context selector sẽ phù hợp hơn.

### Giải thích chi tiết

Vấn đề lớn nhất của Context không phải syntax mà là granularity. Nếu provider trả về `{ user, theme, notifications, setUser, setTheme, ... }`, chỉ cần một field đổi là toàn bộ consumer phụ thuộc context đó có thể re-render. Một số hướng giảm:

- Tách nhiều provider nhỏ
- Tách state và actions nếu cần
- Memoize object `value`
- Đặt provider sát nơi cần dùng thay vì bọc toàn app

### Ví dụ minh họa

```jsx
// ❌ Provider quá to: mọi consumer đều bị ảnh hưởng
function AppProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);

  const value = {
    theme,
    setTheme,
    user,
    setUser,
    notifications,
    setNotifications,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}
```

```jsx
// ✅ Tách provider theo domain và memoize value
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const value = useMemo(() => ({ theme, setTheme }), [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
```

### Lưu ý / Bẫy thường gặp

- `useMemo` không giải quyết được nếu bản thân dependency vẫn đổi liên tục
- Tối ưu Context bằng cách tách domain thường hiệu quả hơn nhồi nhét thêm memo
- Nếu consumer quá nhiều và update quá thường xuyên, nên cân nhắc store selector-based

---

## Câu Hỏi 3: Bạn chia global state, server state và local UI state như thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Trong một ứng dụng frontend hiện đại, bạn phân biệt và đặt global state, server state và local UI state ở đâu? Vì sao việc phân loại sai làm codebase khó maintain?

### Câu trả lời ngắn gọn

Tôi tách rõ ba nhóm: local UI state ở component, global client state ở Context/Redux/Zustand khi nhiều nơi cùng dùng, và server state ở React Query/SWR hoặc layer fetch riêng. Nếu nhét tất cả vào một store chung, code sẽ dư đồng bộ, invalidation phức tạp và khó debug. Phân loại đúng giúp mỗi loại state dùng đúng công cụ.

### Giải thích chi tiết

**Local UI state**
- Input text, modal open/close, hover, tab active
- Gần component nhất có thể

**Global client state**
- Auth snapshot, theme, feature flags, wizard shared state
- Dùng Context hoặc store tùy độ phức tạp

**Server state**
- Danh sách users, orders, dashboard metrics lấy từ API
- Cần caching, refetch, invalidation, retry

Đưa server state vào Redux/Context theo cách thủ công thường dẫn tới nhiều boilerplate và bug cache.

### Ví dụ minh họa

```jsx
function ProductFilter() {
  const [keyword, setKeyword] = useState(''); // Local UI state

  const { data, isLoading } = useQuery({
    queryKey: ['products', keyword],
    queryFn: () => fetchProducts(keyword),
  }); // Server state

  const theme = useTheme(); // Global client state

  return (
    <div data-theme={theme}>
      <input value={keyword} onChange={(e) => setKeyword(e.target.value)} />
      {isLoading ? 'Loading...' : <ProductList products={data ?? []} />}
    </div>
  );
}
```

### Lưu ý / Bẫy thường gặp

- Đừng đồng bộ cùng một dữ liệu server vào nhiều nơi nếu không có lý do rõ ràng
- Auth token và thông tin session không giống với danh sách API paginated
- Chọn sai loại state thường làm team thêm nhiều code "sync" không cần thiết

---

## Câu Hỏi So Sánh: Context API vs Redux Toolkit

**Mức độ:** Trung cấp

### Câu hỏi

So sánh Context API và Redux Toolkit về khả năng mở rộng, performance và trải nghiệm làm việc trong team.

### Bảng So Sánh

| Tiêu chí | Context API | Redux Toolkit |
|----------|-------------|---------------|
| Thiết lập ban đầu | Nhanh, ít boilerplate | Nhiều setup hơn |
| Scale với state lớn | Hạn chế hơn | Tốt hơn |
| Selector / granularity | Cơ bản | Mạnh |
| Debug action flow | Hạn chế | Tốt với DevTools |
| Middleware / async flow | Tự làm | Có pattern rõ ràng |

### Câu trả lời ngắn gọn

Context API đơn giản và phù hợp cho state nhỏ hoặc ít update, còn Redux Toolkit mạnh hơn khi state flow phức tạp và cần debug tốt. Redux Toolkit trả giá bằng setup và abstraction nhiều hơn. Chọn công cụ nên dựa trên độ phức tạp thực tế và cách team cần làm việc lâu dài.

### Giải thích chi tiết

Một app nhỏ hoàn toàn có thể sống tốt với Context. Nhưng khi business logic tăng, cần tracing action, selector, middleware và chuẩn hóa state, Redux Toolkit thường đem lại lợi ích rõ hơn. Trong team đông người, convention rõ và DevTools tốt thường giúp giảm bug integration.

### Khi nào dùng cái nào?

- Dùng **Context API** khi: theme, locale, auth snapshot đơn giản, feature nhỏ
- Dùng **Redux Toolkit** khi: cart phức tạp, dashboard lớn, workflow nhiều bước, state chia sẻ rộng

### Ví dụ

```jsx
// Context cho theme
const ThemeContext = createContext({ theme: 'light', setTheme: () => {} });
```

```typescript
// Redux Toolkit cho cart workflow
const store = configureStore({
  reducer: {
    cart: cartSlice.reducer,
  },
});
```

### Lưu ý / Bẫy thường gặp

- Không nên so sánh Context với Redux theo kiểu "cái nào nhanh hơn tuyệt đối"
- Nếu dự án đã có React Query, nhiều state "global" thực ra là server state và không nên đưa vào Redux
- Chọn công cụ theo lifecycle dữ liệu và nhu cầu team, không theo trend

---

## Tài Liệu Tham Khảo

- [React Docs - Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)
- [Redux Toolkit Docs](https://redux-toolkit.js.org/)

