# JavaScript Event Loop và Async Flow

## Thông Tin File

- **Chủ đề:** Event Loop, Call Stack, Task Queue, Microtask Queue
- **Ngôn ngữ / Framework:** JavaScript
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Event Loop trong JavaScript hoạt động như thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Hãy giải thích `call stack`, `Web APIs`, `task queue`, `microtask queue` và `event loop` trong JavaScript. Tại sao JavaScript là single-threaded nhưng vẫn xử lý được nhiều tác vụ bất đồng bộ?

### Câu trả lời ngắn gọn

JavaScript chạy code đồng bộ trên một `call stack`, nhưng browser hoặc Node.js cung cấp `Web APIs` để xử lý các tác vụ bất đồng bộ như timer, network, DOM events. Khi tác vụ hoàn tất, callback sẽ được đẩy vào `task queue` hoặc `microtask queue`. `Event loop` liên tục kiểm tra stack có trống không để đưa callback phù hợp vào chạy. Vì vậy JS vẫn là single-threaded ở phần execute code, nhưng runtime hỗ trợ concurrency cho async work.

### Giải thích chi tiết

**1. Call Stack**
- Nơi JavaScript thực thi function theo cơ chế LIFO
- Mỗi lần gọi function sẽ push một frame mới vào stack

**2. Web APIs / Runtime APIs**
- `setTimeout`, `fetch`, DOM event listener không chạy trực tiếp trong engine JS
- Runtime sẽ xử lý chúng ở bên ngoài `call stack`

**3. Queue**
- `task queue` chứa callback từ `setTimeout`, `setInterval`, DOM events
- `microtask queue` chứa callback từ `Promise.then`, `catch`, `finally`, `queueMicrotask`, phần tiếp theo của `async/await`

**4. Event Loop**
- Chỉ khi `call stack` trống, event loop mới lấy task tiếp theo để chạy
- `microtask queue` luôn được ưu tiên flush hết trước khi xử lý `task queue`

### Ví dụ minh họa

```javascript
console.log('1. Bắt đầu');

setTimeout(() => {
  console.log('4. Task queue từ setTimeout');
}, 0);

Promise.resolve().then(() => {
  console.log('3. Microtask từ Promise');
});

console.log('2. Kết thúc synchronous code');

// Kết quả:
// 1. Bắt đầu
// 2. Kết thúc synchronous code
// 3. Microtask từ Promise
// 4. Task queue từ setTimeout
```

### Lưu ý / Bẫy thường gặp

- `setTimeout(fn, 0)` không có nghĩa là chạy ngay lập tức, mà chỉ được đưa vào `task queue`
- `Promise.then` không chạy song song với code hiện tại, nó chỉ được ưu tiên hơn `task queue`
- Single-threaded không đồng nghĩa với không xử lý được bất đồng bộ

---

## Câu Hỏi 2: Dự đoán output của đoạn code async/await sau

**Mức độ:** Trung cấp

### Câu hỏi

Cho đoạn code sau, hãy giải thích thứ tự output và vì sao:

### Câu trả lời ngắn gọn

`async/await` thực chất vẫn dựa trên `Promise`, nên phần code sau `await` sẽ được đưa vào `microtask queue`. Toàn bộ synchronous code chạy trước, sau đó flush `microtask`, cuối cùng mới đến `task queue`. Muốn trả lời tốt dạng câu hỏi này, cần tách rõ từng bước: synchronous, microtask, rồi macrotask.

### Giải thích chi tiết

Khi gặp `await`, function `async` sẽ tạm dừng tại đó. Phần còn lại của function không bị mất, nó được lên lịch như một `microtask`. Vì `microtask` chạy trước `setTimeout`, nên các log sau `await` thường xuất hiện sớm hơn callback timer.

### Ví dụ minh họa

```javascript
async function run() {
  console.log('A');

  setTimeout(() => {
    console.log('D');
  }, 0);

  await Promise.resolve();
  console.log('C');
}

console.log('Start');
run();
console.log('B');

// Thứ tự:
// Start
// A
// B
// C
// D
```

```javascript
// Cách phân tích nên trình bày khi phỏng vấn:
// 1. 'Start' là synchronous
// 2. Gọi run() -> log 'A'
// 3. setTimeout đăng ký callback vào runtime
// 4. await Promise.resolve() -> phần sau await thành microtask
// 5. log 'B' vẫn là synchronous ở ngoài
// 6. flush microtask -> log 'C'
// 7. xử lý task queue -> log 'D'
```

### Lưu ý / Bẫy thường gặp

- `await Promise.resolve()` vẫn tạo ra điểm yield, không chạy tiếp ngay trong cùng call stack
- Đừng gom `async/await` vào `task queue`; phần sau `await` thuộc `microtask queue`
- Nhiều ứng viên chỉ nhớ output nhưng không giải thích được runtime behavior

---

## Câu Hỏi 3: Nếu một đoạn JavaScript nặng làm treo UI, bạn xử lý thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Bạn có một tác vụ tính toán nặng trên client làm UI bị đơ vài giây. Bạn sẽ xử lý như thế nào để tránh block main thread?

### Câu trả lời ngắn gọn

Tôi ưu tiên giảm lượng công việc chạy trên main thread: chia nhỏ tác vụ thành nhiều chunk, dùng `requestIdleCallback` hoặc `setTimeout` để nhường event loop, hoặc chuyển sang `Web Worker` nếu tính toán thực sự nặng. Với bài toán render list lớn, tôi kết hợp virtualization và debounce input. Quan trọng là đo bằng Performance tab trước khi tối ưu.

### Giải thích chi tiết

**Các hướng xử lý chính:**

**1. Chia nhỏ tác vụ**
- Sau mỗi chunk, trả quyền điều khiển lại cho browser để paint UI
- Phù hợp khi logic vẫn cần chạy trên main thread

**2. Dùng Web Worker**
- Chuyển việc tính toán nặng sang thread riêng
- Main thread chỉ nhận kết quả để render

**3. Giảm số lần kích hoạt**
- Debounce search, throttle scroll, memoize kết quả nếu dữ liệu không đổi

### Ví dụ minh họa

```javascript
// ❌ Chạy một mạch 1 triệu item trên main thread
function processBigList(items) {
  return items.map((item) => heavyTransform(item));
}
```

```javascript
// ✅ Chia nhỏ tác vụ để không block UI quá lâu
function processInChunks(items, chunkSize = 500) {
  let index = 0;

  function nextChunk() {
    const end = Math.min(index + chunkSize, items.length);

    for (let i = index; i < end; i += 1) {
      heavyTransform(items[i]);
    }

    index = end;

    if (index < items.length) {
      setTimeout(nextChunk, 0); // Nhường event loop để browser kịp paint
    }
  }

  nextChunk();
}
```

```javascript
// ✅ Web Worker phù hợp khi tính toán nặng kéo dài
// main.js
const worker = new Worker(new URL('./worker.js', import.meta.url));

worker.postMessage(largeData);
worker.onmessage = (event) => {
  // Nhận kết quả từ worker và cập nhật UI
  renderResult(event.data);
};
```

### Lưu ý / Bẫy thường gặp

- Tối ưu mà không đo trước thường dẫn đến sửa sai chỗ
- `setTimeout` chỉ giúp chia nhỏ công việc, không làm tổng CPU cost biến mất
- `Web Worker` không truy cập trực tiếp DOM, nên phải thiết kế message passing rõ ràng

---

## Câu Hỏi So Sánh: Microtask vs Macrotask

**Mức độ:** Trung cấp

### Câu hỏi

`Microtask` và `macrotask` khác nhau ở điểm nào? Vì sao hiểu sai thứ tự này dễ dẫn đến bug async khó debug?

### Bảng So Sánh

| Tiêu chí | Microtask | Macrotask |
|----------|-----------|-----------|
| Ví dụ | `Promise.then`, `await`, `queueMicrotask` | `setTimeout`, `setInterval`, DOM events |
| Thời điểm chạy | Sau khi stack trống, trước khi paint/task tiếp theo | Sau khi microtask đã flush xong |
| Mức ưu tiên | Cao hơn | Thấp hơn |
| Rủi ro | Flush quá nhiều có thể làm UI bị đói thời gian paint | Delay lâu hơn mong đợi khi queue dài |

### Câu trả lời ngắn gọn

`Microtask` luôn được xử lý trước `macrotask` mỗi khi `call stack` trống. Vì vậy callback từ `Promise` hoặc phần sau `await` thường chạy trước `setTimeout`. Nếu không hiểu điều này, ứng viên dễ đoán sai thứ tự state update, render và cleanup.

### Giải thích chi tiết

Runtime sẽ flush toàn bộ `microtask queue` trước khi chuyển sang `macrotask` tiếp theo. Điều này giúp `Promise` chain có tính nhất quán, nhưng cũng có thể làm browser chưa kịp paint nếu bạn tạo quá nhiều `microtask` liên tiếp. Trong UI code, đây là lý do một số log hoặc state transition xảy ra sớm hơn trực giác.

### Khi nào dùng cái nào?

- Dùng **microtask** khi: cần lên lịch công việc nhỏ ngay sau synchronous code hiện tại, ví dụ finalize Promise chain
- Dùng **macrotask** khi: muốn trì hoãn sang vòng lặp kế tiếp, hoặc chủ động nhường browser xử lý UI/events

### Ví dụ

```javascript
console.log('start');

setTimeout(() => {
  console.log('macrotask');
}, 0);

queueMicrotask(() => {
  console.log('microtask');
});

console.log('end');

// start
// end
// microtask
// macrotask
```

### Lưu ý / Bẫy thường gặp

- `requestAnimationFrame` không phải microtask, nó có timing riêng gắn với frame render
- Tạo vòng lặp Promise vô hạn có thể làm app lag dù không có `setTimeout`
- Khi giải thích trong phỏng vấn, nên dùng đúng thuật ngữ `microtask` và `task/macrotask`

---

## Tài Liệu Tham Khảo

- [MDN - Event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)
- [MDN - Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)

