# Debug Performance Issue trong Production (React/Next.js)

## Thông Tin File

- **Chủ đề:** Production Performance Debugging Process
- **Ngôn ngữ / Framework:** React / Next.js
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Quy trình debug page load chậm trên production

**Mức độ:** Trung cấp

### Câu hỏi

Một trang React/Next.js bị chậm nghiêm trọng khi user mở page (load 6–8 giây). PM yêu cầu bạn tìm nguyên nhân và cải thiện performance. Bạn sẽ debug vấn đề này theo các bước nào?

### Câu trả lời ngắn gọn

Bước 1: Reproduce issue và đo performance bằng Chrome DevTools + Lighthouse để xác định bottleneck (network, bundle size, hay rendering). Bước 2: Phân tích nguyên nhân — API chậm, JS bundle quá lớn, data fetching tuần tự, hay React re-render không cần thiết. Bước 3: Áp dụng giải pháp tương ứng (parallel API, code splitting, caching, memoization). Bước 4: Verify lại bằng Lighthouse và Web Vitals để đo kết quả cải thiện.

### Giải thích chi tiết

**Quy trình debug step by step:**

**Step 1 — Reproduce và đo baseline**
- Mở Chrome DevTools → tab Performance và Network
- Chạy Lighthouse (Production mode, throttled network)
- Ghi lại các metrics: LCP, TTFB, TBT, CLS
- Xem Network waterfall để thấy request nào chậm nhất

**Step 2 — Phân loại bottleneck**
- **Network**: API response chậm, large payload, nhiều request tuần tự
- **Bundle size**: JS bundle quá lớn, không code split
- **Rendering**: React re-render nhiều lần, blocking JavaScript

**Step 3 — Deep dive theo loại bottleneck**

*Nếu network chậm:*
- Xem Network tab → tìm request nào TTFB cao
- Kiểm tra API có bị N+1 query không
- Xem có request nào có thể parallel không

*Nếu bundle size lớn:*
- Chạy `next build --analyze` hoặc dùng `@next/bundle-analyzer`
- Tìm thư viện nào quá lớn, có thể lazy load không

*Nếu rendering chậm:*
- React DevTools Profiler → xem component nào render lâu nhất
- Flame chart trong Chrome DevTools → tìm long task

**Step 4 — Apply fix và verify**

**Nguyên nhân → Giải pháp:**
| Nguyên nhân            | Giải pháp                            |
|------------------------|--------------------------------------|
| API tuần tự (waterfall)| `Promise.all()` — parallel requests  |
| JS bundle lớn          | Code splitting, dynamic import       |
| Data không cache       | HTTP cache, React Query, SWR         |
| Re-render nhiều        | useMemo, useCallback, React.memo     |
| Images nặng            | Next.js `<Image>`, WebP format       |
| Font blocking          | `next/font`, `font-display: swap`    |

### Ví dụ minh họa

```javascript
// ❌ Waterfall API calls — tuần tự, tốn thời gian
async function loadDashboardData() {
  const user = await fetchUser();     // 200ms
  const orders = await fetchOrders(); // 300ms
  const stats = await fetchStats();   // 250ms
  // Tổng: 750ms
}

// ✅ Parallel API calls — giảm thời gian xuống còn max(200, 300, 250) = 300ms
async function loadDashboardDataFast() {
  const [user, orders, stats] = await Promise.all([
    fetchUser(),
    fetchOrders(),
    fetchStats(),
  ]);
  // Tổng: ~300ms
}
```

```javascript
// ✅ Code splitting với dynamic import
import dynamic from 'next/dynamic';

// Chart library nặng — chỉ load khi cần
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

// ✅ Lazy load component không critical
const UserModal = dynamic(() => import('./UserModal'));
```

```javascript
// ✅ Next.js App Router — parallel data fetching với Server Component
// Không cần Promise.all — Next.js tự optimize fetch calls
export default async function Dashboard() {
  // Những fetch này chạy parallel nếu không có dependency
  const userPromise = fetch('/api/user', { cache: 'no-store' });
  const ordersPromise = fetch('/api/orders', { cache: 'no-store' });
  const statsPromise = fetch('/api/stats', { cache: 'no-store' });

  const [user, orders, stats] = await Promise.all([
    userPromise.then(r => r.json()),
    ordersPromise.then(r => r.json()),
    statsPromise.then(r => r.json()),
  ]);

  return <DashboardView user={user} orders={orders} stats={stats} />;
}
```

```bash
# ✅ Bundle analyzer — tìm thư viện nào làm bundle lớn
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer({});

# Chạy analysis
ANALYZE=true npm run build
```

```javascript
// ✅ Đo Web Vitals trong production
// next.config.js
export function reportWebVitals(metric) {
  const { name, value } = metric;

  // Gửi về analytics
  if (name === 'LCP') {
    console.log('LCP:', value, 'ms'); // Target < 2500ms
  }
  if (name === 'TTFB') {
    console.log('TTFB:', value, 'ms'); // Target < 800ms
  }
  if (name === 'CLS') {
    console.log('CLS:', value); // Target < 0.1
  }
}
```

### Lưu ý / Bẫy thường gặp

- Luôn **reproduce trong điều kiện giống production** — dùng throttled network, không test trên localhost
- **TTFB cao** thường do server/API chậm, không phải client-side — debug backend trước
- **LCP cao** thường do image không optimize hoặc critical resource bị block
- React DevTools Profiler chỉ hoạt động trong **development mode** — không phản ánh chính xác production
- Sau khi fix, đo lại bằng **Lighthouse** và so sánh với baseline để verify improvement

---

## Tài Liệu Tham Khảo

- [Web Vitals](https://web.dev/vitals/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Next.js - Bundle Analyzer](https://nextjs.org/docs/pages/building-your-application/optimizing/bundle-analyzer)
- [React DevTools Profiler](https://react.dev/learn/react-developer-tools)
