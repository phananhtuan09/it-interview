# Redux Saga vs Redux Thunk

## Thông Tin File

- **Chủ đề:** Redux Saga vs Redux Thunk
- **Ngôn ngữ / Framework:** React / Redux
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-15

---

## Câu Hỏi So Sánh: Redux Saga vs Redux Thunk

**Mức độ:** Trung cấp

### Câu hỏi

Redux Saga hoạt động dựa trên cơ chế gì? Tại sao một project lại chọn Redux Saga thay vì Redux Thunk?

### Bảng So Sánh

| Tiêu chí              | Redux Thunk                          | Redux Saga                              |
|-----------------------|--------------------------------------|-----------------------------------------|
| Cơ chế                | Higher-order function trả về thunk   | Generator function + middleware         |
| Độ phức tạp           | Đơn giản, ít boilerplate             | Phức tạp hơn, nhiều boilerplate hơn     |
| Async flow            | Promise chains                       | yield / generator control               |
| Cancel request        | Khó                                  | Dễ (`takeLatest`, `cancel`)             |
| Retry logic           | Phải tự implement                    | Built-in với `retry`                    |
| Race conditions       | Khó handle                           | Dễ với `race` effect                   |
| Testing               | Khó test side effects                | Dễ test vì yield trả về plain object   |
| Use case              | Logic async đơn giản                 | Workflow phức tạp, nhiều bước           |

### Câu trả lời ngắn gọn

Redux Saga hoạt động dựa trên **Generator Function** của JavaScript — cho phép `pause` và `resume` execution qua từ khóa `yield`. Saga hoạt động như một middleware lắng nghe action (watcher) và thực thi logic async (worker). Chọn Saga thay Thunk khi cần xử lý workflow phức tạp như cancel request, retry, race condition, hoặc orchestrate nhiều API call theo thứ tự.

### Giải thích chi tiết

**Cơ chế hoạt động của Redux Saga:**

Saga dùng **Generator Function** (`function*`) — một tính năng của JavaScript cho phép:
- `yield` để tạm dừng function tại một điểm
- Generator object có thể được resume từ bên ngoài
- Saga middleware điều khiển vòng đời của generator

**Watcher + Worker pattern:**
- **Watcher saga**: lắng nghe action dispatch (`takeEvery`, `takeLatest`, `take`)
- **Worker saga**: thực hiện logic async (gọi API, delay, dispatch action)

**Flow tổng quát:**

```
User action dispatch
      ↓
Redux middleware nhận action
      ↓
Saga watcher (takeLatest / takeEvery)
      ↓
Worker saga thực thi (call API, delay...)
      ↓
dispatch success / failure action
      ↓
Reducer update state
```

### Khi nào dùng cái nào?

- Dùng **Redux Thunk** khi:
  - Logic async đơn giản (gọi 1 API, submit form)
  - Team nhỏ, muốn ít boilerplate
  - Project không cần cancel / retry / race condition

- Dùng **Redux Saga** khi:
  - Cần cancel request khi user navigate away (`takeLatest` tự cancel request cũ)
  - Cần retry khi API fail
  - Cần orchestrate nhiều API theo thứ tự hoặc song song
  - Cần xử lý race condition
  - Cần polling (gọi API theo chu kỳ)

### Ví dụ minh họa

```javascript
// === Redux Thunk (đơn giản) ===
// Action creator trả về function thay vì object
const fetchUser = (userId) => async (dispatch) => {
  dispatch({ type: 'FETCH_USER_REQUEST' });
  try {
    const user = await api.getUser(userId);
    dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });
  } catch (error) {
    dispatch({ type: 'FETCH_USER_FAILURE', error });
  }
};
```

```javascript
// === Redux Saga (phức tạp hơn, mạnh hơn) ===
import { call, put, takeLatest, retry, race, take } from 'redux-saga/effects';

// Worker saga — thực hiện logic async
function* fetchUserSaga(action) {
  try {
    // call: gọi async function, yield pause execution cho đến khi resolve
    const user = yield call(api.getUser, action.payload.userId);

    // put: dispatch action
    yield put({ type: 'FETCH_USER_SUCCESS', payload: user });
  } catch (error) {
    yield put({ type: 'FETCH_USER_FAILURE', error });
  }
}

// Watcher saga — lắng nghe action
// takeLatest: nếu action dispatch 2 lần, cancel request cũ, chỉ giữ lần mới nhất
function* watchFetchUser() {
  yield takeLatest('FETCH_USER_REQUEST', fetchUserSaga);
}

// === Retry example ===
function* fetchWithRetry(action) {
  try {
    // Thử tối đa 3 lần, delay 1s giữa mỗi lần
    const user = yield retry(3, 1000, api.getUser, action.payload.userId);
    yield put({ type: 'FETCH_USER_SUCCESS', payload: user });
  } catch (error) {
    yield put({ type: 'FETCH_USER_FAILURE', error });
  }
}

// === Race condition example ===
function* loginWithTimeout() {
  const { response, timeout } = yield race({
    response: call(api.login, credentials),
    timeout: delay(30000), // timeout sau 30 giây
  });

  if (timeout) {
    yield put({ type: 'LOGIN_TIMEOUT' });
  } else {
    yield put({ type: 'LOGIN_SUCCESS', payload: response });
  }
}
```

```javascript
// === Testing Saga dễ hơn Thunk ===
// Generator yield trả về plain object — dễ assert mà không cần mock

test('fetchUserSaga gọi đúng API', () => {
  const gen = fetchUserSaga({ payload: { userId: '123' } });

  // Assert lần yield đầu tiên — không cần mock, chỉ so sánh object
  expect(gen.next().value).toEqual(call(api.getUser, '123'));
});
```

### Lưu ý / Bẫy thường gặp

- `takeEvery` cho phép nhiều instance saga chạy song song — dùng khi muốn xử lý mọi action
- `takeLatest` cancel saga cũ khi action mới đến — dùng cho search/filter để tránh race condition
- Generator function không phải async/await — cú pháp khác nhau, cần học riêng
- Saga có learning curve cao hơn Thunk — cân nhắc kỹ trước khi chọn cho project đơn giản
- Redux Toolkit Query (RTK Query) là lựa chọn hiện đại thay thế Saga cho data fetching

---

## Câu Hỏi: Khi nào vẫn cần Redux Toolkit trong dự án Next.js hiện đại?

**Mức độ:** Trung cấp

### Câu hỏi

Với sự phát triển của React Query (TanStack Query) hay chính cơ chế Data Fetching trong Next.js (Server Components) hiện nay, theo bạn, khi nào chúng ta vẫn thực sự cần đến một Global State Management như Redux Toolkit trong một dự án Next.js hiện đại?

### Câu trả lời ngắn gọn

Server Components và React Query giải quyết **Server State** (data từ API/DB) rất tốt — không cần Redux cho việc này. Redux Toolkit vẫn cần khi có **Client State thực sự global**: UI state dùng chung nhiều nơi không liên quan (sidebar open/close, theme, notification queue), workflow phức tạp nhiều bước, hoặc state cần persist và sync giữa nhiều tab. Trong dự án Next.js hiện tại, tôi chỉ dùng Redux cho client-side UI state, còn server data để Server Components hoặc React Query xử lý.

### Giải thích chi tiết

**Phân loại State trong Next.js hiện đại:**

| Loại State | Giải pháp tốt nhất | Redux cần không? |
|---|---|---|
| Server data (API response) | Server Components, React Query | Không |
| URL/search state | `useSearchParams`, `nuqs` | Không |
| Form state | `react-hook-form`, local `useState` | Không |
| Component-local state | `useState` | Không |
| Global UI state (sidebar, modal, theme) | Redux Toolkit / Zustand | Có thể cần |
| Cross-tab sync state | Redux + `redux-persist` | Có |
| Complex client workflow | Redux Toolkit | Có |

**Khi Server Components thay thế Redux hoàn toàn:**
- Data fetch và truyền xuống component tree qua props
- Không cần store trung gian vì component có thể fetch trực tiếp
- Caching được Next.js xử lý tự động

**Khi React Query thay thế Redux:**
- Quản lý loading/error/success state của API call
- Caching, refetching, invalidation
- Optimistic updates

**Khi vẫn cần Redux Toolkit:**
1. **Global UI state dùng chung nhiều nơi không liên quan** — ví dụ: notification toast có thể trigger từ bất kỳ component nào
2. **State cần persist qua session** — dùng `redux-persist`
3. **Complex client-side workflow** — multi-step form wizard, undo/redo
4. **Realtime state** — WebSocket data cần broadcast toàn app
5. **Team quen với Redux** — migration cost không đáng

**Quan điểm cá nhân từ kinh nghiệm thực tế:**
Trong SAGAS, tôi đã giảm Redux store từ quản lý cả API data lẫn UI state xuống chỉ còn UI state. Server Components xử lý document data, React Query xử lý paginated search. Redux chỉ còn quản lý: `selectedDocuments` (multi-select state), `sidebarCollapsed`, và `notificationQueue`. Bundle size giảm đáng kể, code đơn giản hơn nhiều.

### Ví dụ minh họa

```tsx
// === Trước: Redux quản lý cả Server State ===
// ❌ Không cần thiết trong Next.js App Router

// documentSlice.ts
const documentSlice = createSlice({
  name: 'documents',
  initialState: { list: [], loading: false, error: null },
  reducers: { /* ... */ },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDocuments.pending, (state) => { state.loading = true; })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.list = action.payload;
        state.loading = false;
      });
  },
});

// Component phải dispatch action để lấy data
function DocumentsPage() {
  const dispatch = useDispatch();
  const documents = useSelector(state => state.documents.list);

  useEffect(() => {
    dispatch(fetchDocuments()); // ❌ Phải dispatch để fetch
  }, [dispatch]);
}
```

```tsx
// === Sau: Server Component xử lý server state ===
// ✅ Đơn giản hơn nhiều

// app/documents/page.tsx — Server Component
export default async function DocumentsPage() {
  // Fetch trực tiếp, không qua Redux store
  const documents = await db.document.findMany({ where: { active: true } });

  return <DocumentList documents={documents} />;
}
```

```tsx
// === Redux chỉ còn cho Global UI State ===
// ✅ Đây là use case thực sự cần Redux

// store/uiSlice.ts
const uiSlice = createSlice({
  name: 'ui',
  initialState: {
    sidebarCollapsed: false,
    selectedDocumentIds: [] as string[], // Multi-select state
    notifications: [] as Notification[], // Toast queue
  },
  reducers: {
    toggleSidebar: (state) => { state.sidebarCollapsed = !state.sidebarCollapsed; },
    selectDocument: (state, action) => {
      state.selectedDocumentIds.push(action.payload);
    },
    addNotification: (state, action) => {
      state.notifications.push(action.payload);
    },
    removeNotification: (state, action) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
  },
});

// Notification có thể được trigger từ bất kỳ component nào trong app
// → Đây là lý do cần Global State, không thể dùng local useState
function DocumentUploader() {
  const dispatch = useDispatch();

  const handleUpload = async (file: File) => {
    try {
      await uploadDocument(file);
      // Trigger notification từ component này
      dispatch(addNotification({ id: uuid(), type: 'success', message: 'Upload thành công' }));
    } catch {
      dispatch(addNotification({ id: uuid(), type: 'error', message: 'Upload thất bại' }));
    }
  };
  // ...
}
```

```tsx
// === React Query cho Client-side API calls cần caching ===
// ✅ Dùng khi cần search/filter trên client

function DocumentSearch() {
  const [query, setQuery] = useState('');

  // React Query: caching, deduplication, refetch on window focus
  const { data, isLoading } = useQuery({
    queryKey: ['documents', query],
    queryFn: () => fetchDocuments({ q: query }),
    enabled: query.length > 2, // Chỉ fetch khi gõ đủ ký tự
    staleTime: 30_000, // Cache 30 giây
  });

  return (/* ... */);
}
```

### Lưu ý / Bẫy thường gặp

- **Đừng dùng Redux cho server state** trong Next.js App Router — đó là việc của Server Components và React Query
- Redux vẫn có giá trị cho **global client state** — đặc biệt notification system, multi-select, cross-component UI sync
- **Zustand** là lựa chọn nhẹ hơn Redux cho global client state nếu không cần Redux DevTools hay middleware phức tạp
- Nếu state chỉ dùng trong một sub-tree của component, dùng **React Context** thay vì Redux
- RTK Query (Redux Toolkit Query) có thể thay React Query nếu đã dùng Redux — không cần cả hai

---

## Tài Liệu Tham Khảo

- [Redux Saga Docs](https://redux-saga.js.org/)
- [MDN - Generator Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*)
- [Redux Toolkit Docs](https://redux-toolkit.js.org/)
