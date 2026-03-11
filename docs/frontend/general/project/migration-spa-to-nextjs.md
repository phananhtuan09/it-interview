# Thách Thức Khi Migrate React SPA sang Next.js

## Thông Tin File

- **Chủ đề:** Migration React SPA to Next.js
- **Ngôn ngữ / Framework:** React / Next.js
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Thách thức khi migrate từ React SPA sang Next.js

**Mức độ:** Trung cấp

### Câu hỏi

Thách thức lớn nhất khi migrate từ React SPA sang Next.js là gì? Và bạn đã xử lý như thế nào trong project thực tế?

### Câu trả lời ngắn gọn

Khi migrate React SPA sang Next.js, các thách thức chính là: routing khác nhau (React Router → Next.js file-based routing), SSR compatibility (code phụ thuộc `window`/`document`), state hydration mismatch, và query logic khi đổi ORM. Trong project thực tế, thách thức lớn nhất là đảm bảo câu query khi migrate từ raw SQL sang Prisma không làm thay đổi kết quả trả về — cần hiểu rõ behavior của cả hai để mapping đúng.

### Giải thích chi tiết

**Các thách thức phổ biến khi migrate:**

**1. Routing khác nhau**
- React: `react-router-dom` với component-based routing (`<Route path="/products">`)
- Next.js: File-system based routing (`app/products/page.tsx`)
- Phải mapping lại toàn bộ routes, đặc biệt với dynamic routes và nested routes

**2. SSR Compatibility**
- React SPA code thường gọi `window`, `document`, `localStorage` ở top-level
- Next.js render trên server — những API này không tồn tại ở server
- Phải wrap trong `useEffect` hoặc check `typeof window !== 'undefined'`

**3. State Hydration**
- Server render HTML với một state, client hydrate với state khác → mismatch warning
- Đặc biệt với timestamp, random value, hoặc data từ localStorage

**4. API / ORM Migration**
- Thay đổi ORM (raw SQL → Prisma) có thể gây ra behavior khác trong edge cases
- Cần test kỹ lưỡng, đặc biệt với JOIN phức tạp, NULL handling, date formatting

**5. Third-party libraries**
- Một số library không support SSR — cần dynamic import với `ssr: false`

### Ví dụ minh họa

```javascript
// ❌ React SPA code — không chạy được trên server
const token = localStorage.getItem('auth_token'); // ReferenceError: localStorage is not defined

// ✅ Fix cho Next.js
const getToken = () => {
  if (typeof window === 'undefined') return null; // Guard SSR
  return localStorage.getItem('auth_token');
};

// Hoặc dùng trong useEffect (chỉ chạy ở client)
useEffect(() => {
  const token = localStorage.getItem('auth_token');
  setToken(token);
}, []);
```

```javascript
// ❌ React SPA routing với React Router
import { BrowserRouter, Route, Switch } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/products/:id" component={ProductDetail} />
        <Route path="/products" component={ProductList} />
      </Switch>
    </BrowserRouter>
  );
}

// ✅ Next.js App Router — file-based routing
// File: app/products/page.tsx → /products
// File: app/products/[id]/page.tsx → /products/:id

// app/products/[id]/page.tsx
export default function ProductDetail({ params }: { params: { id: string } }) {
  return <div>Product {params.id}</div>;
}
```

```javascript
// ❌ Hydration mismatch — server và client render khác nhau
function TimestampComponent() {
  // Server render lúc 10:00:00, client mount lúc 10:00:01 → mismatch!
  return <div>{new Date().toLocaleTimeString()}</div>;
}

// ✅ Fix — chỉ hiển thị ở client
function TimestampComponent() {
  const [time, setTime] = useState<string>('');

  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
  }, []);

  return <div>{time || 'Loading...'}</div>;
}
```

```javascript
// ❌ Third-party library không support SSR
import Chart from 'chart.js'; // Lỗi nếu import static

// ✅ Dynamic import với ssr: false
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('./Chart'), {
  ssr: false, // Chỉ render ở client
  loading: () => <p>Loading chart...</p>,
});
```

```sql
-- Thách thức migrate raw SQL sang Prisma
-- Raw SQL — explicit về NULL handling
SELECT * FROM orders
WHERE user_id = 1
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 10;

-- Prisma tương đương — cần verify output giống nhau
const orders = await prisma.order.findMany({
  where: {
    userId: 1,
    deletedAt: null, // Prisma hiểu IS NULL
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
});

-- Cần test kỹ với edge cases:
-- NULL vs undefined trong Prisma
-- JOIN behavior (INNER vs LEFT JOIN)
-- Date timezone handling
-- Aggregate functions (SUM, COUNT)
```

### Lưu ý / Bẫy thường gặp

- **SSR check** — luôn guard các browser API trong useEffect hoặc `typeof window !== 'undefined'`
- **Hydration mismatch** — tránh render giá trị dynamic (timestamp, random) trong initial render
- **React Router → Next.js routing** — kiểm tra kỹ redirect logic, 404 handling, và middleware
- **Prisma vs raw SQL** — viết integration test để verify output của từng query sau migrate
- **Third-party SEO** — meta tags, Open Graph cần chuyển sang Next.js Head hoặc Metadata API

---

## Tài Liệu Tham Khảo

- [Next.js Docs - App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading)
- [Next.js Docs - Dynamic Imports](https://nextjs.org/docs/pages/building-your-application/optimizing/lazy-loading)
- [Prisma Docs](https://www.prisma.io/docs)
