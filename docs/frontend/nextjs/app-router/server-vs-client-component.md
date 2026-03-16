# Server Component vs Client Component trong Next.js App Router

## Thông Tin File

- **Chủ đề:** Server Component vs Client Component
- **Ngôn ngữ / Framework:** Next.js (App Router)
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-15

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

## Câu Hỏi 1: Khi nào bắt buộc phải chuyển sang Client Component trong dự án thực tế?

**Mức độ:** Trung cấp

### Câu hỏi

Trong dự án SAGAS, bạn có sử dụng Next.js App Router và Server Components. Bạn có thể phân biệt rõ sự khác biệt về cơ chế render giữa Server Components và Client Components không? Trong trường hợp nào thì bạn bắt buộc phải chuyển một component sang Client Component?

### Câu trả lời ngắn gọn

Server Component render hoàn toàn trên server — không gửi JS xuống browser, có thể truy cập DB trực tiếp, tốt cho SEO. Client Component render ở browser sau khi hydrate — cần thiết khi có state, event handler, hoặc browser API. Trong SAGAS, tôi bắt buộc dùng Client Component cho: search bar có debounce (`useState` + `useEffect`), filter dropdown có interaction, và document preview panel cần `useRef` để control scroll position.

### Giải thích chi tiết

**Cơ chế render khác nhau:**
- **Server Component**: Next.js render thành HTML trên server, gửi HTML xuống browser kèm **RSC Payload** (serialized component tree). Không có JS bundle cho component này ở phía client.
- **Client Component**: Vẫn có thể pre-render HTML trên server (SSR), nhưng React sẽ **hydrate** component đó ở browser — tức là gắn event listener và khởi tạo state.

**Bắt buộc dùng Client Component khi:**

1. **Cần state hoặc lifecycle** — `useState`, `useReducer`, `useEffect`
   - Ví dụ SAGAS: search input cần `useState` cho query, `useEffect` cho debounce
2. **Cần event handler** — `onClick`, `onChange`, `onSubmit`, drag/drop
   - Ví dụ SAGAS: filter buttons, document upload zone
3. **Cần browser API** — `localStorage`, `sessionStorage`, `window`, `navigator`, `document`
   - Ví dụ SAGAS: lưu filter preference vào localStorage
4. **Dùng third-party library chỉ chạy ở browser** — chart libraries, rich text editor, PDF viewer
   - Ví dụ SAGAS: PDF preview component dùng library không hỗ trợ SSR
5. **Dùng React Context** — context provider phải là Client Component

**Chiến lược trong SAGAS:**
- `page.tsx` → Server Component: fetch danh sách document từ DB, truyền xuống
- `SearchBar` → Client Component: có debounce state
- `DocumentList` → Server Component: render danh sách tĩnh
- `FilterPanel` → Client Component: có toggle state cho từng filter
- `DocumentPreview` → Client Component: cần `useRef`, keyboard event

### Ví dụ minh họa

```tsx
// === SAGAS: Document Search Page ===
// app/documents/page.tsx — Server Component
// Fetch data trực tiếp, không expose DB logic ra client

import { SearchBar } from '@/components/SearchBar';    // Client Component
import { DocumentList } from '@/components/DocumentList'; // Server Component
import { FilterPanel } from '@/components/FilterPanel'; // Client Component

// searchParams đến từ URL — không cần state ở đây
export default async function DocumentSearchPage({
  searchParams,
}: {
  searchParams: { q?: string; type?: string };
}) {
  // Fetch trực tiếp trên server — không qua API route
  const documents = await fetchDocuments({
    query: searchParams.q,
    type: searchParams.type,
  });

  return (
    <div>
      <SearchBar defaultValue={searchParams.q} />
      <FilterPanel />
      <DocumentList documents={documents} />
    </div>
  );
}
```

```tsx
// SearchBar.tsx — Client Component (bắt buộc vì có state + debounce)
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function SearchBar({ defaultValue }: { defaultValue?: string }) {
  const [query, setQuery] = useState(defaultValue ?? '');
  const router = useRouter();

  // Debounce: chỉ navigate sau 300ms user ngừng gõ
  useEffect(() => {
    const timeout = setTimeout(() => {
      router.push(`/documents?q=${encodeURIComponent(query)}`);
    }, 300);
    return () => clearTimeout(timeout);
  }, [query, router]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Tìm kiếm tài liệu..."
    />
  );
}
```

### Lưu ý / Bẫy thường gặp

- `'use client'` là **ranh giới (boundary)** — tất cả component được import trong file đó đều trở thành Client Component
- Đặt `'use client'` càng **thấp trong cây component** càng tốt để tối ưu bundle size
- Server Component **không thể** `import` Client Component có state — nhưng có thể nhận nó qua `children` prop
- Nếu dùng Context, provider phải là Client Component — nhưng children bên trong vẫn có thể là Server Component nếu được truyền qua `children`

---

## Câu Hỏi 2: Serialization Rules — Truyền dữ liệu từ Server Component xuống Client Component

**Mức độ:** Nâng cao

### Câu hỏi

Khi bạn truyền dữ liệu từ một Server Component xuống một Client Component (con), bạn cần lưu ý điều gì về kiểu dữ liệu của Props để tránh gặp lỗi "Serialization"? Bạn đã bao giờ gặp khó khăn khi truyền các object phức tạp (như Date hoặc Function) qua ranh giới này chưa?

### Câu trả lời ngắn gọn

Props truyền từ Server Component xuống Client Component phải **serializable** — tức là có thể chuyển thành JSON để gửi qua mạng. Các kiểu dữ liệu được phép: string, number, boolean, array, plain object, null/undefined. Không được truyền: `Function`, `Date` object, `class instance`, `Map`, `Set`, `Symbol`, hoặc bất kỳ thứ gì không JSON-serializable. Trong SAGAS tôi đã gặp lỗi khi cố truyền `Date` object — phải convert sang ISO string trước khi truyền.

### Giải thích chi tiết

**Tại sao cần serializable?**

Khi Next.js render Server Component, nó tạo ra **RSC Payload** — một định dạng đặc biệt của React để mô tả component tree. Payload này được gửi từ server xuống browser qua HTTP. Vì đi qua network, dữ liệu phải có thể serialize (chuyển thành chuỗi) và deserialize (parse lại) ở browser.

**Dữ liệu CÓ THỂ vượt biên (serializable):**
- Primitives: `string`, `number`, `boolean`, `null`, `undefined`
- Arrays của các kiểu trên
- Plain objects (key-value, không có method)
- `BigInt` (có hỗ trợ riêng)

**Dữ liệu KHÔNG THỂ vượt biên (non-serializable):**
- `Function` / arrow function — không thể JSON.stringify
- `Date` object — JSON.stringify sẽ thành string nhưng mất prototype
- `Map`, `Set` — không serialize được
- `class instance` — mất method sau serialize
- `Symbol` — không thể serialize
- `undefined` trong nested object — bị bỏ qua

**Cách xử lý trong thực tế:**
- `Date` → truyền `.toISOString()` (string), parse lại ở Client Component
- `Function` → không truyền; thay vào đó define function trong Client Component
- `class instance` → serialize thành plain object trước khi truyền

### Ví dụ minh họa

```tsx
// === SAGAS: Document metadata từ Server xuống Client ===

// ❌ Sai — Date object không serializable
// Server Component
async function DocumentPage({ id }: { id: string }) {
  const doc = await db.document.findById(id);
  // doc.createdAt là Date object

  return (
    // Lỗi: "Error: Date cannot be serialized as JSON"
    <DocumentPreview createdAt={doc.createdAt} />
  );
}
```

```tsx
// ✅ Đúng — convert sang string trước khi truyền
// Server Component
async function DocumentPage({ id }: { id: string }) {
  const doc = await db.document.findById(id);

  return (
    <DocumentPreview
      // Convert Date → ISO string để vượt biên server/client
      createdAt={doc.createdAt.toISOString()}
      title={doc.title}
      fileSize={doc.fileSize} // number — OK
    />
  );
}

// Client Component — nhận string, parse lại nếu cần
'use client';
function DocumentPreview({
  createdAt,
  title,
  fileSize,
}: {
  createdAt: string; // Nhận string, không phải Date
  title: string;
  fileSize: number;
}) {
  // Parse lại thành Date ở client nếu cần format
  const date = new Date(createdAt);

  return (
    <div>
      <h2>{title}</h2>
      <p>Ngày tạo: {date.toLocaleDateString('vi-VN')}</p>
      <p>Kích thước: {(fileSize / 1024).toFixed(1)} KB</p>
    </div>
  );
}
```

```tsx
// ❌ Sai — truyền Function qua ranh giới server/client
// Server Component
function ParentServer() {
  const handleClick = () => console.log('clicked'); // Function!

  return (
    // Lỗi: Functions cannot be passed directly to Client Components
    <ClientButton onClick={handleClick} />
  );
}

// ✅ Đúng — define function trong Client Component
'use client';
function ClientButton({ label }: { label: string }) {
  // Function được define trong Client Component, không cần truyền từ server
  const handleClick = () => console.log('clicked');

  return <button onClick={handleClick}>{label}</button>;
}
```

```tsx
// ❌ Sai — truyền class instance
class Document {
  constructor(public id: string, public title: string) {}
  getDisplayName() { return `[${this.id}] ${this.title}`; }
}

// Server Component
async function Page() {
  const doc = new Document('123', 'Report'); // class instance
  return <Preview doc={doc} />; // ❌ method mất sau serialize
}

// ✅ Đúng — truyền plain object
async function Page() {
  const doc = new Document('123', 'Report');
  return (
    <Preview
      // Serialize thành plain object — chỉ data, không có method
      doc={{ id: doc.id, title: doc.title }}
    />
  );
}
```

### Lưu ý / Bẫy thường gặp

- **`Date` là bẫy phổ biến nhất** — `JSON.stringify(new Date())` ra string nhưng mất prototype. Luôn truyền `.toISOString()` và parse lại ở client
- **Function** không bao giờ truyền được — kể cả callback. Tách logic vào Client Component
- **Prisma model** trả về object thường chứa `Date` field — cần transform toàn bộ trước khi pass xuống
- Dùng TypeScript để type-check prop có `Date` — compiler sẽ warn nếu bạn truyền sai kiểu
- `undefined` trong object bị JSON.stringify bỏ qua — dùng `null` thay thế nếu cần giữ field

---

## Tài Liệu Tham Khảo

- [Next.js Docs - Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Next.js Docs - Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [React Docs - Server Components](https://react.dev/reference/rsc/server-components)
