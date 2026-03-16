# Type vs Interface trong TypeScript

## Thông Tin File

- **Chủ đề:** Type vs Interface, Extends, Intersection và Modeling
- **Ngôn ngữ / Framework:** TypeScript
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-16

---

## Câu Hỏi 1: Khi nào nên dùng `type`, khi nào nên dùng `interface`?

**Mức độ:** Trung cấp

### Câu hỏi

Trong dự án TypeScript thực tế, bạn chọn `type` hay `interface` theo tiêu chí nào? Có rule nào giúp team dùng nhất quán không?

### Câu trả lời ngắn gọn

Tôi thường dùng `interface` cho object contract ổn định như DTO, props, domain model có khả năng mở rộng; dùng `type` cho union, mapped type, utility type hoặc kiểu derived từ type khác. Rule quan trọng nhất là nhất quán và chọn theo mục đích, không theo sở thích cá nhân. Khi cần composition mạnh, `type` linh hoạt hơn; khi muốn API shape rõ ràng, `interface` dễ đọc hơn.

### Giải thích chi tiết

**Ưu tiên `interface` khi:**
- Mô tả shape của object chính trong hệ thống
- Cần `extends` rõ ràng cho nhiều model
- Muốn tận dụng declaration merging ở library typing

**Ưu tiên `type` khi:**
- Cần union như `'idle' | 'loading' | 'error'`
- Dùng `Pick`, `Omit`, `Partial`, conditional types
- Kết hợp nhiều type qua intersection

**Rule gọn cho team:**
- `interface` cho base contract
- `type` cho derived type và advanced typing

### Ví dụ minh họa

```typescript
// Base contract của domain model
interface User {
  id: string;
  name: string;
  email: string;
}

// Derived type cho màn hình edit
type UpdateUserPayload = Partial<Pick<User, 'name' | 'email'>>;

// Union type chỉ có thể dùng type
type RequestStatus = 'idle' | 'loading' | 'success' | 'error';
```

### Lưu ý / Bẫy thường gặp

- Khác biệt runtime giữa `type` và `interface` là không có, đây hoàn toàn là compile-time
- Đừng dùng rule cực đoan kiểu "chỉ dùng interface" hoặc "chỉ dùng type" nếu codebase có nhu cầu khác nhau
- Review tốt nên xét readability và maintainability thay vì tranh luận thuần cú pháp

---

## Câu Hỏi 2: Bạn model API response và UI state thế nào để tránh lặp type?

**Mức độ:** Trung cấp

### Câu hỏi

Backend trả về object lớn nhưng UI chỉ dùng một phần dữ liệu. Bạn sẽ model type thế nào để tránh copy-paste nhiều interface nhỏ và giảm rủi ro type bị lệch?

### Câu trả lời ngắn gọn

Tôi định nghĩa một base model hoặc raw API type, sau đó derive các type nhỏ hơn bằng `Pick`, `Omit`, indexed access type hoặc transform function ở service layer. Component UI nên nhận domain type đã được thu gọn thay vì raw response. Cách này giữ `single source of truth` và giảm drift khi backend thay đổi.

### Giải thích chi tiết

Một lỗi phổ biến là tạo nhiều type thủ công gần giống nhau cho từng màn hình. Về lâu dài, khi backend đổi field, project dễ bị lệch type ở nhiều nơi. Cách tốt hơn là:

1. Có `ApiUser` hoặc `UserResponse` là nguồn gốc
2. Dùng utility types để derive type mới
3. Transform từ API model sang UI model tại service layer

### Ví dụ minh họa

```typescript
interface ApiUser {
  id: string;
  full_name: string;
  email: string;
  avatar_url: string | null;
  role: 'admin' | 'member';
  created_at: string;
  updated_at: string;
}

type UserCard = Pick<ApiUser, 'id' | 'email' | 'avatar_url'> & {
  displayName: string;
};

function toUserCard(user: ApiUser): UserCard {
  return {
    id: user.id,
    email: user.email,
    avatar_url: user.avatar_url,
    displayName: user.full_name,
  };
}
```

```typescript
// Indexed access type giúp tái sử dụng nested type
interface ApiOrder {
  id: string;
  customer: {
    id: string;
    name: string;
    email: string;
  };
}

type CustomerSummary = ApiOrder['customer'];
```

### Lưu ý / Bẫy thường gặp

- Đừng truyền raw API response đi xuyên component tree nếu UI không cần toàn bộ field
- `Pick`/`Omit` giúp tránh lặp, nhưng nếu phải transform nhiều field thì nên tạo function map riêng
- Type an toàn không thay thế validation runtime khi dữ liệu từ server không đáng tin tuyệt đối

---

## Câu Hỏi 3: `extends`, `intersection` và declaration merging ảnh hưởng gì đến maintainability?

**Mức độ:** Trung cấp

### Câu hỏi

Hãy phân biệt `interface extends`, `type intersection (&)` và declaration merging. Trong dự án lớn, dùng sai những kỹ thuật này có thể gây vấn đề gì?

### Câu trả lời ngắn gọn

`extends` và `intersection` đều dùng để composition type, nhưng `extends` thường rõ nghĩa hơn cho object model, còn `&` linh hoạt hơn khi kết hợp nhiều kiểu. Declaration merging chỉ có với `interface` và thường hữu ích ở library typing hoặc module augmentation. Dùng quá tay có thể làm type khó đọc, error message rối và che giấu xung đột field.

### Giải thích chi tiết

**`interface extends`**
- Phù hợp cho quan hệ "is-a" rõ ràng
- Dễ đọc khi model domain

**`type A & B`**
- Kết hợp được object, union helper, mapped type
- Nếu hai field cùng tên nhưng khác kiểu, type có thể trở nên khó hiểu hoặc thành `never`

**Declaration merging**
- Cho phép khai báo nhiều `interface` cùng tên để gộp lại
- Hay dùng khi mở rộng typing của thư viện

### Ví dụ minh họa

```typescript
interface BaseEntity {
  id: string;
  createdAt: string;
}

interface UserEntity extends BaseEntity {
  email: string;
}

type WithTimestamps = {
  createdAt: string;
  updatedAt: string;
};

type ProductEntity = {
  id: string;
  name: string;
} & WithTimestamps;
```

```typescript
// Declaration merging
interface Window {
  analytics: {
    track: (eventName: string) => void;
  };
}

window.analytics.track('page_view');
```

### Lưu ý / Bẫy thường gặp

- `type A = { id: string } & { id: number }` là dấu hiệu mô hình hóa sai
- Declaration merging tiện nhưng có thể làm source of truth bị phân tán nếu team lạm dụng
- Khi error message quá dài, thường là do chain intersection hoặc conditional type quá phức tạp

---

## Câu Hỏi So Sánh: `type` vs `interface`

**Mức độ:** Trung cấp

### Câu hỏi

So sánh `type` và `interface` trong TypeScript. Nếu bạn đang code review một codebase mới, bạn sẽ chọn convention nào cho team?

### Bảng So Sánh

| Tiêu chí | `type` | `interface` |
|----------|--------|-------------|
| Mô tả object | Có | Có |
| Union / tuple / primitive alias | Tốt | Không hỗ trợ |
| Utility / mapped / conditional type | Phù hợp hơn | Hạn chế |
| Declaration merging | Không | Có |
| Readability cho object contract | Tốt | Thường rõ hơn |

### Câu trả lời ngắn gọn

`interface` phù hợp cho object contract ổn định và có khả năng mở rộng, còn `type` phù hợp cho advanced typing và kiểu dẫn xuất. Trong team, tôi chọn convention đơn giản: `interface` cho base object model, `type` cho union và utility-based types. Điều quan trọng là codebase nhất quán và dễ bảo trì.

### Giải thích chi tiết

Nếu team mới bắt đầu với TypeScript, nên chọn quy ước dễ nhớ để giảm tranh luận không cần thiết. Tuy nhiên vẫn nên cho phép ngoại lệ khi bài toán yêu cầu, ví dụ state machine dùng union thì bắt buộc phải dùng `type`. Review tốt là review theo intent của model, không cố ép mọi thứ về một kiểu khai báo.

### Khi nào dùng cái nào?

- Dùng **`interface`** khi: định nghĩa props, entity, API contract, class implement
- Dùng **`type`** khi: cần union, tuple, mapped type, utility type, compose kiểu phức tạp

### Ví dụ

```typescript
interface ButtonProps {
  label: string;
  disabled?: boolean;
}

type ButtonVariant = 'primary' | 'secondary' | 'ghost';

type ButtonState = ButtonProps & {
  variant: ButtonVariant;
};
```

### Lưu ý / Bẫy thường gặp

- Đừng biến guideline thành tranh cãi tôn giáo trong team
- Nếu project đã có convention rõ ràng, ưu tiên theo codebase hiện tại
- Nên để ESLint/biome hoặc review guideline enforce nhất quán thay vì nhớ bằng miệng

---

## Tài Liệu Tham Khảo

- [TypeScript Handbook - Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [TypeScript Handbook - Interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html)

