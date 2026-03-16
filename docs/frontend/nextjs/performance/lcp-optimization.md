# Tối Ưu LCP (Largest Contentful Paint) trong Next.js

## Thông Tin File

- **Chủ đề:** LCP Optimization — Core Web Vitals trong Next.js
- **Ngôn ngữ / Framework:** Next.js
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-15

---

## Câu Hỏi 1: Kỹ thuật tối ưu LCP với Next.js Image component

**Mức độ:** Trung cấp

### Câu hỏi

Trong CV, bạn có đề cập đến việc tối ưu hóa Core Web Vitals khi migration sang Next.js. Một trong những chỉ số quan trọng là LCP (Largest Contentful Paint). Giả sử trong trang SAGAS (Document Search) của bạn có một Banner lớn hoặc một hình ảnh Preview tài liệu nằm ngay đầu trang. Bạn đã áp dụng những kỹ thuật cụ thể nào trong Next.js (ví dụ với component `<Image />`) để đảm bảo chỉ số LCP này đạt kết quả tốt nhất?

### Câu trả lời ngắn gọn

Để tối ưu LCP cho image đầu trang trong SAGAS, tôi dùng: (1) `priority` prop để preload ảnh LCP ngay lập tức, không lazy-load; (2) khai báo đúng `width` và `height` để tránh layout shift (CLS); (3) `sizes` prop để serve đúng kích thước ảnh theo viewport, tránh download ảnh quá lớn; (4) chọn format `WebP/AVIF` tự động qua Next.js Image optimization; (5) dùng `placeholder="blur"` với `blurDataURL` để hiển thị preview trong khi ảnh thật đang load.

### Giải thích chi tiết

**LCP là gì?**
LCP đo thời gian từ khi user navigate đến khi element lớn nhất trong viewport được render xong. Target: **< 2.5 giây** (Good), 2.5–4s (Needs Improvement), > 4s (Poor). Element LCP thường là: hero image, banner, hoặc large text block.

**Tại sao Next.js `<Image />` tốt hơn `<img />` thuần?**
- Tự động convert sang **WebP/AVIF** — nhỏ hơn 25-50% so với JPEG/PNG
- Built-in **lazy loading** mặc định (nhưng cần tắt cho LCP element)
- **Responsive images** với `srcset` tự động
- Tránh **layout shift** (CLS) vì biết trước kích thước
- Server-side **image optimization** theo on-demand

**5 kỹ thuật chính đã áp dụng trong SAGAS:**

1. **`priority`** — preload ảnh LCP, không lazy load
2. **`width` + `height`** — tránh layout shift, browser biết trước không gian cần dành
3. **`sizes`** — chỉ download kích thước phù hợp với viewport hiện tại
4. **`placeholder="blur"`** — UX tốt hơn khi ảnh đang load
5. **`quality`** — balance giữa file size và visual quality

### Ví dụ minh họa

```tsx
// === SAGAS: Document Search Banner ===
// app/documents/page.tsx

import Image from 'next/image';

export default function DocumentSearchPage() {
  return (
    <div>
      {/* ✅ Kỹ thuật 1: priority — QUAN TRỌNG NHẤT cho LCP */}
      {/* priority=true: Next.js thêm <link rel="preload"> vào <head>
          Browser bắt đầu download ảnh ngay, không chờ đến khi render */}
      <Image
        src="/images/document-search-banner.jpg"
        alt="SAGAS Document Search"
        width={1200}
        height={400}

        // ✅ priority: bắt buộc cho ảnh LCP — tắt lazy loading
        priority

        // ✅ sizes: chỉ download ảnh đúng kích thước viewport
        // Nếu không có sizes, Next.js download ảnh full width cho mọi device
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 1200px"

        // ✅ quality: 85 là sweet spot — ít mất chất nhưng file nhỏ hơn ~30%
        quality={85}

        // ✅ placeholder: hiện blur preview trong khi ảnh thật đang load
        // Cải thiện CLS và UX
        placeholder="blur"
        blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..." // base64 ảnh nhỏ

        // ✅ style thay vì className cho critical images — tránh FOUC
        style={{ objectFit: 'cover', width: '100%', height: 'auto' }}
      />

      {/* Document Preview thumbnail — KHÔNG dùng priority (không phải LCP element) */}
      <Image
        src={previewUrl}
        alt="Document preview"
        width={300}
        height={400}
        // Không có priority → lazy load bình thường ✅
        placeholder="blur"
        blurDataURL={doc.thumbnailBlur}
      />
    </div>
  );
}
```

```tsx
// === Tạo blurDataURL cho placeholder ===
// Có thể generate lúc build time hoặc lưu vào DB

// Option 1: Dùng plaiceholder library
import { getPlaiceholder } from 'plaiceholder';

async function getImageWithBlur(src: string) {
  const { base64, metadata } = await getPlaiceholder(src);
  return { blurDataURL: base64, width: metadata.width, height: metadata.height };
}

// Option 2: Inline base64 của ảnh 1x1 pixel (đơn giản nhất)
const BLUR_DATA_URL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';

// Option 3: Server-side generate blur
// app/documents/page.tsx — Server Component
export default async function DocumentSearchPage() {
  const banner = await fetchBannerImage();

  // Generate blur hash trên server
  const { base64 } = await getPlaiceholder(banner.url);

  return (
    <Image
      src={banner.url}
      alt={banner.alt}
      width={1200}
      height={400}
      priority
      placeholder="blur"
      blurDataURL={base64} // Server-generated blur
    />
  );
}
```

```tsx
// === sizes prop chi tiết ===
// sizes giúp browser chọn đúng ảnh từ srcset Next.js tự generate

<Image
  src="/banner.jpg"
  alt="Banner"
  width={1200}
  height={400}
  priority
  // Giải thích sizes:
  // - Mobile (< 768px): ảnh full width (100vw) → download ảnh ~768px
  // - Tablet (768px - 1200px): ảnh 80% width → download ảnh ~960px
  // - Desktop (> 1200px): ảnh 1200px cố định → download ảnh 1200px
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 1200px"

  // Nếu không có sizes:
  // Next.js mặc định download ảnh full width (100vw) cho mọi device
  // Mobile user phải download ảnh 1200px → lãng phí bandwidth → LCP chậm
/>
```

```tsx
// === next.config.js — cấu hình Image Optimization ===
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    // Format ưu tiên: AVIF nhỏ hơn WebP ~20%, nhưng encode chậm hơn
    formats: ['image/avif', 'image/webp'],

    // Định nghĩa các breakpoint để generate srcset
    // Match với Tailwind breakpoints để nhất quán
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

    // Cache optimized images bao lâu (giây)
    minimumCacheTTL: 60 * 60 * 24 * 7, // 7 ngày
  },
};
```

```tsx
// === Kỹ thuật bổ sung: preload bằng Link header ===
// Cho trường hợp dynamic image URL — Next.js không thể preload tự động

// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        {/* Preload critical LCP image khi URL cố định */}
        <link
          rel="preload"
          as="image"
          href="/images/banner.webp"
          // Khai báo sizes để browser biết preload ảnh nào
          imageSrcSet="/images/banner-640w.webp 640w, /images/banner-1200w.webp 1200w"
          imageSizes="(max-width: 768px) 100vw, 1200px"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Lưu ý / Bẫy thường gặp

- **`priority` là kỹ thuật quan trọng nhất** — quên `priority` cho LCP image là lỗi phổ biến nhất; lazy loading mặc định sẽ delay LCP đáng kể
- **Không dùng `fill` mode** cho LCP image nếu có thể — `width`+`height` cho browser biết trước layout, tránh layout shift (CLS)
- **`sizes` prop bắt buộc khi dùng `fill` mode** hoặc khi image responsive — thiếu `sizes` khiến browser download ảnh quá lớn
- **AVIF vs WebP** — AVIF nhỏ hơn ~20% nhưng encode chậm, có thể ảnh hưởng TTFB trên server yếu; WebP là lựa chọn an toàn hơn
- **Không overuse `priority`** — chỉ dùng cho 1-2 ảnh quan trọng nhất above-the-fold; quá nhiều `priority` gây contention trong browser
- `placeholder="blur"` yêu cầu `blurDataURL` hoặc ảnh static (local) — nếu thiếu, Next.js sẽ throw error lúc build

---

## Tài Liệu Tham Khảo

- [Next.js Docs - Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [Web.dev - LCP](https://web.dev/articles/lcp)
- [web.dev - Optimize LCP](https://web.dev/articles/optimize-lcp)
- [Next.js Image API Reference](https://nextjs.org/docs/app/api-reference/components/image)
