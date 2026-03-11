# SSR vs SSG vs CSR vs ISR trong Next.js

## Thông Tin File

- **Chủ đề:** Rendering Strategies (SSR, SSG, CSR, ISR)
- **Ngôn ngữ / Framework:** Next.js
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi So Sánh: SSR vs SSG vs CSR vs ISR

**Mức độ:** Trung cấp

### Câu hỏi

Sự khác nhau giữa SSR, SSG, CSR và ISR trong Next.js là gì? Trong trường hợp thực tế nào bạn sẽ chọn từng cách?

### Bảng So Sánh

| Mode    | Render khi nào               | HTML sẵn | SEO   | Performance       | Use case                              |
|---------|------------------------------|----------|-------|-------------------|---------------------------------------|
| **CSR** | Browser render sau khi JS load | Không   | Kém   | Load đầu chậm     | Dashboard, admin, app realtime        |
| **SSR** | Server render mỗi request    | Có       | Tốt   | TTFB chậm hơn SSG | SEO page, dynamic content per user    |
| **SSG** | Build time generate HTML     | Có       | Tốt   | Rất nhanh (CDN)   | Blog, docs, marketing page            |
| **ISR** | Rebuild sau khoảng thời gian | Có       | Tốt   | Nhanh (CDN + revalidate) | Data thay đổi nhưng không realtime |

### Câu trả lời ngắn gọn

CSR render ở browser — phù hợp cho app không cần SEO. SSR render trên server mỗi request — phù hợp cho page cần SEO và data động theo user. SSG generate HTML tại build time — cực nhanh vì serve static file từ CDN, phù hợp cho nội dung ít thay đổi. ISR là kết hợp SSG + auto revalidate — page được rebuild sau một khoảng thời gian, phù hợp cho data thay đổi nhưng không cần realtime.

### Giải thích chi tiết

**CSR (Client-Side Rendering):**
- Browser nhận HTML rỗng, sau đó tải JS và render
- Load đầu tiên chậm (phải download và parse JS)
- Sau khi load xong → navigation nhanh (SPA behavior)
- Googlebot có thể index nhưng không đảm bảo bằng SSR/SSG
- Lưu ý: SSR vẫn có thể có `onClick`, interaction — CSR và interaction là hai khái niệm khác nhau

**SSR (Server-Side Rendering):**
- Server render HTML đầy đủ cho mỗi request
- User thấy content ngay (FCP nhanh)
- TTFB (Time to First Byte) phụ thuộc tốc độ server và data fetching
- Phù hợp khi data phụ thuộc vào request (cookie, user session)

**SSG (Static Site Generation):**
- HTML được generate tại `build time` (`next build`)
- Serve từ CDN — cực nhanh, không cần server processing mỗi request
- Không phù hợp cho data thay đổi thường xuyên

**ISR (Incremental Static Regeneration):**
- Kết hợp SSG + background regeneration
- Page được serve từ CDN (nhanh)
- Sau `revalidate` giây, Next.js sẽ regenerate page ở background
- User luôn nhận page từ cache — không bao giờ chờ rebuild

### Khi nào dùng cái nào?

- Dùng **CSR** khi: dashboard, admin panel, app cần authentication, data realtime, không cần SEO
- Dùng **SSR** khi: e-commerce product page (price/stock thay đổi), user-specific content, cần SEO tốt
- Dùng **SSG** khi: blog, documentation, landing page, marketing site — nội dung ít thay đổi
- Dùng **ISR** khi: news site, product catalog — cần SEO nhưng data cập nhật định kỳ (không realtime)

### Ví dụ minh họa

```typescript
// === CSR — dùng 'use client' và fetch trong component ===
'use client';

import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch ở client side
    fetch('/api/dashboard-data').then(r => r.json()).then(setData);
  }, []);

  return <div>{data ? <DataTable data={data} /> : 'Loading...'}</div>;
}
```

```typescript
// === SSR — Next.js App Router (fetch không cache) ===
// Mỗi request gọi server function này
export default async function ProductPage({ params }) {
  // cache: 'no-store' → không cache → SSR behavior
  const product = await fetch(`/api/products/${params.id}`, {
    cache: 'no-store',
  }).then(r => r.json());

  return <ProductDetail product={product} />;
}
```

```typescript
// === SSG — Next.js App Router (default behavior) ===
// fetch mặc định được cache → generate tại build time
export default async function BlogPost({ params }) {
  // Không set cache option → Next.js cache mặc định → SSG
  const post = await fetch(`https://api.example.com/posts/${params.slug}`)
    .then(r => r.json());

  return <Article post={post} />;
}

// Generate paths tại build time
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());
  return posts.map(post => ({ slug: post.slug }));
}
```

```typescript
// === ISR — revalidate sau N giây ===
export default async function NewsPage() {
  const news = await fetch('https://api.example.com/news', {
    next: { revalidate: 3600 }, // Revalidate sau 1 giờ
  }).then(r => r.json());

  return <NewsList news={news} />;
}
```

### Lưu ý / Bẫy thường gặp

- Trong Next.js App Router, mặc định tất cả component là **Server Component** (SSG behavior)
- `'use client'` chuyển component thành Client Component nhưng không có nghĩa là CSR hoàn toàn — vẫn có thể SSR
- CSR không phải chỉ dùng khi có `onClick` — SSR vẫn support interaction sau hydration
- ISR với `revalidate: 0` tương đương SSR
- Luôn đo **LCP, TTFB, CLS** để chọn đúng strategy

---

## Tài Liệu Tham Khảo

- [Next.js Docs - Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Next.js Docs - Incremental Static Regeneration](https://nextjs.org/docs/pages/building-your-application/data-fetching/incremental-static-regeneration)
