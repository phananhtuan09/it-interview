# Closure trong JavaScript

## Thông Tin File

- **Chủ đề:** Closure, Lexical Scope, Memory và Use Case thực tế
- **Ngôn ngữ / Framework:** JavaScript
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Closure là gì và vì sao nó quan trọng?

**Mức độ:** Trung cấp

### Câu hỏi

Closure là gì? Hãy giải thích theo cách dễ hiểu và nêu ít nhất 2 use case thực tế của closure trong frontend.

### Câu trả lời ngắn gọn

Closure là khả năng một function nhớ được biến ở lexical scope bên ngoài kể cả khi outer function đã chạy xong. Nó quan trọng vì nhiều pattern trong JavaScript như factory function, memoization, event handler và custom hook đều dựa trên cơ chế này. Khi hiểu closure tốt, bạn sẽ debug async callback và stale data dễ hơn.

### Giải thích chi tiết

Khi function được tạo ra, nó giữ tham chiếu tới môi trường lexical nơi nó được định nghĩa. Điều này có nghĩa là callback vẫn truy cập được biến của outer scope dù outer function không còn nằm trên call stack. Ứng dụng thực tế của closure:

- Đóng gói state private trong factory function
- Tạo callback nhớ context tại thời điểm đăng ký
- Memoization để cache kết quả
- Debounce/throttle giữ timer giữa nhiều lần gọi

### Ví dụ minh họa

```javascript
function createCounter() {
  let count = 0;

  return function increment() {
    count += 1; // Biến count vẫn được nhớ nhờ closure
    return count;
  };
}

const counter = createCounter();

console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

```javascript
// Use case thực tế: tạo hàm format theo locale
function createPriceFormatter(locale, currency) {
  return function formatPrice(value) {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency,
    }).format(value);
  };
}

const formatVND = createPriceFormatter('vi-VN', 'VND');
console.log(formatVND(250000));
```

### Lưu ý / Bẫy thường gặp

- Closure không phải là copy giá trị, mà là giữ tham chiếu tới lexical environment
- Không phải mọi nested function đều gây vấn đề memory; chỉ khi tham chiếu bị giữ lại quá lâu
- Nhiều bug React về stale state cũng liên quan tới cách closure giữ giá trị cũ

---

## Câu Hỏi 2: Vì sao `var` trong loop dễ gây bug với closure?

**Mức độ:** Trung cấp

### Câu hỏi

Giải thích vì sao đoạn code dùng `var` trong vòng lặp với `setTimeout` thường in ra kết quả sai. Bạn sửa nó như thế nào?

### Câu trả lời ngắn gọn

`var` có function scope nên tất cả callback trong loop sẽ cùng giữ tham chiếu tới một biến `i`. Khi callback chạy, vòng lặp đã kết thúc nên `i` có cùng giá trị cuối. Có thể sửa bằng `let`, IIFE hoặc tạo scope mới cho từng iteration.

### Giải thích chi tiết

Vấn đề không nằm ở `setTimeout`, mà nằm ở việc closure của từng callback cùng nhìn vào một biến `i` duy nhất. `let` tạo block scope cho mỗi vòng lặp, nên mỗi callback nhận được một binding riêng. Đây là câu hỏi rất hay gặp để kiểm tra bạn hiểu scope thật hay chỉ nhớ syntax.

### Ví dụ minh họa

```javascript
// ❌ Sai: mọi callback cùng dùng một biến i
for (var i = 0; i < 3; i += 1) {
  setTimeout(() => {
    console.log(i); // 3, 3, 3
  }, 0);
}
```

```javascript
// ✅ Đúng: let tạo binding riêng cho từng iteration
for (let i = 0; i < 3; i += 1) {
  setTimeout(() => {
    console.log(i); // 0, 1, 2
  }, 0);
}
```

```javascript
// ✅ Cũng đúng: dùng IIFE để tạo scope mới
for (var i = 0; i < 3; i += 1) {
  ((currentIndex) => {
    setTimeout(() => {
      console.log(currentIndex);
    }, 0);
  })(i);
}
```

### Lưu ý / Bẫy thường gặp

- Nhiều người trả lời "vì setTimeout async" là chưa đủ, gốc vấn đề là `scope` và `closure`
- `const` không dùng được nếu biến cần tăng trong loop
- `let` giải quyết cả readability lẫn correctness, nên thường là cách ưu tiên

---

## Câu Hỏi 3: Closure có thể gây memory leak hoặc bug thực tế như thế nào?

**Mức độ:** Trung cấp

### Câu hỏi

Closure có thể gây memory leak hoặc giữ dữ liệu cũ ngoài ý muốn trong frontend như thế nào? Cho ví dụ và cách phòng tránh.

### Câu trả lời ngắn gọn

Closure gây vấn đề khi một callback giữ tham chiếu tới object lớn hoặc state cũ quá lâu, làm GC không dọn được hoặc logic dùng dữ liệu stale. Ví dụ phổ biến là event listener không cleanup, timer không clear, hoặc callback trong React đọc state cũ. Cách xử lý là cleanup đúng lifecycle, chỉ giữ dữ liệu cần thiết và cập nhật closure khi dependencies đổi.

### Giải thích chi tiết

Closure bản thân không phải memory leak, nhưng nó có thể giữ object sống lâu hơn dự định. Nếu bạn đăng ký listener lên `window` hoặc lưu callback vào singleton mà không remove, toàn bộ dữ liệu outer scope có thể bị giữ lại. Trong React, stale closure hay xuất hiện khi effect hoặc callback không khai báo dependency đúng.

### Ví dụ minh họa

```javascript
function attachResizeLogger(largeConfig) {
  function handleResize() {
    // Closure đang giữ cả largeConfig trong bộ nhớ
    console.log(largeConfig.theme);
  }

  window.addEventListener('resize', handleResize);

  return () => {
    // Cleanup để GC có thể thu hồi dữ liệu khi không còn dùng
    window.removeEventListener('resize', handleResize);
  };
}
```

```javascript
// Ví dụ stale closure trong callback
function createLogger() {
  let message = 'Phiên bản cũ';

  return {
    update(newMessage) {
      message = newMessage;
    },
    logLater() {
      setTimeout(() => {
        console.log(message); // Sẽ in giá trị hiện tại của message tại thời điểm callback chạy
      }, 1000);
    },
  };
}
```

### Lưu ý / Bẫy thường gặp

- Đừng gọi mọi vấn đề giữ memory là "memory leak" nếu object vẫn còn được tham chiếu hợp lệ
- Event listener, interval và cache custom là nơi closure dễ gây rủi ro nhất
- Khi nói về stale closure, nên phân biệt dữ liệu cũ do dependency sai với bug do race condition

---

## Tài Liệu Tham Khảo

- [MDN - Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
- [You Don't Know JS Yet - Scope & Closures](https://github.com/getify/You-Dont-Know-JS)

