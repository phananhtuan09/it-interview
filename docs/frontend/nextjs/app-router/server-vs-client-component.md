# Server Component vs Client Component trong Next.js App Router

## Thông Tin File

- **Chủ đề:** Server Component vs Client Component
- **Ngôn ngữ / Framework:** Next.js (App Router)
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi So Sánh: Server Component vs Client Component

**Mức độ:** Trung cấp

### Câu hỏi

Sự khác nhau giữa Server Component và Client Component trong Next.js App Router là gì? Khi nào nên dùng Server Component thay vì Client Component?

### Bảng So Sánh

| Tiêu chí                  | Server Component (default)         | Client Component (`'use client'`)    |
|---------------------------|------------------------------------|--------------------------------------|
| Render ở đâu              | Server                             | Browser (sau hydration)              |
| JS gửi xuống browser      | Không                              | Có                                   |
| Bundle size               | Không ảnh hưởng                    | Tăng bundle size                     |
| Truy cập database         | Trực tiếp (server-side)            | Không (phải qua API)                 |
| State / hooks             | Không dùng được                    | Dùng được (`useState`, `useEffect`)  |
| Event handlers            | Không dùng được                    | Dùng được (`onClick`, `onChange`)    |
| Browser APIs              | Không dùng được                    | Dùng được (`window`, `document`)     |
| SEO                       | Tốt (HTML render sẵn)              | Phụ thuộc vào hydration              |
| Streaming / Suspense      | Hỗ trợ                             | Hỗ trợ giới hạn                      |

### Câu trả lời ngắn gọn

Server Component render trên server, không gửi JS xuống browser — giảm bundle size, tốt cho SEO, có thể truy cập database trực tiếp. Client Component chạy ở browser — cần thiết khi dùng state, event handler, hoặc browser API. Mặc định mọi component trong App Router là Server Component, thêm `'use client'` để chuyển thành Client Component.

### Giải thích chi tiết

**Server Component:**
- Default trong Next.js App Router
- Chạy hoàn toàn trên server — code không bao giờ xuất hiện ở browser
- Có thể truy cập database, filesystem, secret environment variable an toàn
- Không expose logic nhạy cảm ra client
- Hỗ trợ **React Streaming** — render dần từng phần với `Suspense`
- Không thể dùng state, lifecycle hooks, event handler

**Client Component:**
- Cần thêm `'use client'` ở đầu file
- Vẫn có thể được pre-render trên server (SSR), nhưng sẽ hydrate ở browser
- Cần thiết cho bất kỳ interaction nào với user

**Quy tắc tổ chức component:**
- Đẩy `'use client'` boundary xuống thấp nhất có thể
- Page / Layout → Server Component (fetch data, SEO)
- Button, Form, Modal → Client Component (interaction)
- Có thể lồng Client Component vào Server Component (nhưng không ngược lại)

### Khi nào dùng cái nào?

- Dùng **Server Component** khi:
  - Fetch data từ database hoặc API (không cần truyền xuống client)
  - Hiển thị static content
  - Truy cập server-side resource (file system, secrets)
  - Cần SEO tốt

- Dùng **Client Component** khi:
  - Cần `useState`, `useEffect`, `useReducer`
  - Cần event handler (`onClick`, `onChange`, `onSubmit`)
  - Cần browser API (`localStorage`, `window`, `navigator`)
  - Dùng third-party library chỉ chạy ở browser

### Ví dụ minh họa

```tsx
// === Server Component (default) ===
// app/products/page.tsx
// Không có 'use client' → Server Component

import { db } from '@/lib/database'; // ✅ Truy cập DB trực tiếp

export default async function ProductsPage() {
  // Fetch trực tiếp trên server — không expose API key ra client
  const products = await db.product.findMany({ where: { active: true } });

  return (
    <main>
      <h1>Sản phẩm</h1>
      {/* Truyền data xuống Client Component nếu cần interaction */}
      <ProductList products={products} />
      <AddToCartButton /> {/* Client Component cho interaction */}
    </main>
  );
}
```

```tsx
// === Client Component ===
// components/AddToCartButton.tsx
'use client'; // Bắt buộc khai báo

import { useState } from 'react';

export function AddToCartButton({ productId }: { productId: string }) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    });
    setLoading(false);
  };

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? 'Đang thêm...' : 'Thêm vào giỏ'}
    </button>
  );
}
```

```tsx
// === Streaming với Server Component + Suspense ===
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Stream từng section độc lập — không block toàn trang */}
      <Suspense fallback={<Skeleton />}>
        <RevenueChart />  {/* Server Component fetch chậm */}
      </Suspense>
      <Suspense fallback={<Skeleton />}>
        <RecentOrders /> {/* Server Component fetch nhanh hơn */}
      </Suspense>
    </div>
  );
}
```

```tsx
// ❌ Sai — import Client Component vào Server Component với 'use client' trong Server
// Server Component không thể dùng useState
// app/page.tsx
export default function Page() {
  const [count, setCount] = useState(0); // ❌ Lỗi! Server Component không có state
  return <div>{count}</div>;
}

// ✅ Đúng — tách riêng phần cần state ra Client Component
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Lưu ý / Bẫy thường gặp

- `'use client'` là **boundary** — mọi component import vào file đó đều trở thành Client Component
- Server Component **không thể** dùng context trực tiếp — phải wrap trong Client Component
- Không thể truyền **non-serializable props** (function, Date object) từ Server sang Client Component
- `useState`, `useEffect` chỉ hoạt động trong Client Component
- Đặt `'use client'` càng thấp trong cây component càng tốt để tối ưu bundle size

---

## Tài Liệu Tham Khảo

- [Next.js Docs - Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Next.js Docs - Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [React Docs - Server Components](https://react.dev/reference/rsc/server-components)
