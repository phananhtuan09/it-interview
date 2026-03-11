# Redux Saga vs Redux Thunk

## Thông Tin File

- **Chủ đề:** Redux Saga vs Redux Thunk
- **Ngôn ngữ / Framework:** React / Redux
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

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

## Tài Liệu Tham Khảo

- [Redux Saga Docs](https://redux-saga.js.org/)
- [MDN - Generator Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*)
- [Redux Toolkit Docs](https://redux-toolkit.js.org/)
