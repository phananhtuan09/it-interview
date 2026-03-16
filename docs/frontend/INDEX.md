# Index Tài Liệu Frontend

> File này được generate bởi `scripts/generate_frontend_index.py`. Không nên sửa tay trừ khi bạn cũng cập nhật script.

File này dùng để tra nhanh thư mục `docs/frontend/` hiện có những topic nào và những khoảng trống nào nên ưu tiên bổ sung tiếp.

---

## Cách Dùng

- Khi cần thêm tài liệu mới, kiểm tra file này trước để tránh tạo trùng topic.
- Nếu topic đã tồn tại, ưu tiên mở rộng file cũ thay vì tạo file mới.
- Nếu topic chưa có, chọn đúng folder cấp 1 và nhóm con gần nhất rồi thêm file mới.
- Sau khi thêm file mới, chạy `python3 scripts/generate_frontend_index.py` để cập nhật lại index.

---

## Tổng Quan Hiện Tại

| Nhóm | Số file |
|------|---------|
| `javascript/` | 2 |
| `typescript/` | 2 |
| `css/` | 1 |
| `html/` | 1 |
| `react/` | 6 |
| `nextjs/` | 3 |
| `general/` | 6 |
| `vue/` | 0 |
| `nuxtjs/` | 0 |

Tổng số file nội dung hiện tại: **21**

---

## Topic Hiện Có

### JavaScript

| Nhóm con | Topic | File |
|----------|-------|------|
| `closures/` | Closure trong JavaScript | `javascript/closures/closures.md` |
| `event-loop/` | JavaScript Event Loop và Async Flow | `javascript/event-loop/event-loop.md` |

### TypeScript

| Nhóm con | Topic | File |
|----------|-------|------|
| `type-vs-interface/` | Type vs Interface trong TypeScript | `typescript/type-vs-interface/type-vs-interface.md` |
| `utility-types/` | TypeScript Utility Types cho API Response phức tạp | `typescript/utility-types/utility-types.md` |

### CSS

| Nhóm con | Topic | File |
|----------|-------|------|
| `layout/` | Flexbox vs Grid trong CSS Layout | `css/layout/flexbox-vs-grid.md` |

### HTML

| Nhóm con | Topic | File |
|----------|-------|------|
| `accessibility/` | Accessibility cho Frontend | `html/accessibility/accessibility.md` |

### React

| Nhóm con | Topic | File |
|----------|-------|------|
| `hooks/` | Custom Hooks trong React | `react/hooks/custom-hooks.md` |
| `hooks/` | useEffect vs useLayoutEffect | `react/hooks/use-effect-vs-use-layout-effect.md` |
| `performance/` | Tối Ưu Re-render trong React | `react/performance/re-render-optimization.md` |
| `rendering/` | React Reconciliation, Key và State Preservation | `react/rendering/reconciliation-and-key.md` |
| `state-management/` | Context API vs Redux Toolkit | `react/state-management/context-vs-redux.md` |
| `state-management/` | Redux Saga vs Redux Thunk | `react/state-management/redux-saga-vs-thunk.md` |

### Next.js

| Nhóm con | Topic | File |
|----------|-------|------|
| `app-router/` | Server Component vs Client Component trong Next.js App Router | `nextjs/app-router/server-vs-client-component.md` |
| `performance/` | Tối Ưu LCP (Largest Contentful Paint) trong Next.js | `nextjs/performance/lcp-optimization.md` |
| `rendering/` | SSR vs SSG vs CSR vs ISR trong Next.js | `nextjs/rendering/ssr-ssg-csr-isr.md` |

### General

| Nhóm con | Topic | File |
|----------|-------|------|
| `project/` | Thách Thức Khi Migrate React SPA sang Next.js | `general/project/migration-spa-to-nextjs.md` |
| `project/` | Tối Ưu Performance AG Grid với Large Dataset | `general/project/ag-grid-performance.md` |
| `project/` | Tối Ưu Performance Graph Visualization (React Force Graph) | `general/project/graph-visualization-performance.md` |
| `situational/` | Debug Performance Issue trong Production (React/Next.js) | `general/situational/production-performance-debug.md` |
| `situational/` | Xử Lý Code Review và Tech Debt trong Team | `general/situational/code-review-and-tech-debt.md` |
| `situational/` | Xử Lý Production Incident / Bug Nghiêm Trọng | `general/situational/production-incident-handling.md` |

### Vue

| Nhóm con | Topic | File |
|----------|-------|------|
| - | Chưa có nội dung | - |

### Nuxt.js

| Nhóm con | Topic | File |
|----------|-------|------|
| - | Chưa có nội dung | - |

---

## Khoảng Trống Dễ Thấy

Đây là backlog gợi ý để bổ sung dần. Mục tiêu là phủ các topic middle frontend hay gặp trước khi mở rộng sang niche topic.

### Ưu tiên cao

- `javascript/`
  - `this`, `bind/call/apply`
  - `prototype` và prototype chain
  - `hoisting`, `var/let/const`
  - `debounce` vs `throttle`
- `typescript/`
  - `generics`
  - `unknown` vs `any` vs `never`
  - `discriminated union`
  - `satisfies` và narrowing
- `react/`
  - controlled vs uncontrolled form
  - `useMemo` vs `useCallback`
  - state lifting vs composition
  - React Query / server state
  - error boundary
- `nextjs/`
  - caching và revalidation
  - route handler vs server action
  - hydration mismatch

### Ưu tiên trung bình

- `css/`
  - `position`, stacking context, `z-index`
  - responsive design và media/container query
  - BEM, CSS Modules, CSS-in-JS
- `html/`
  - SEO cơ bản
  - semantic HTML ngoài accessibility
  - form semantics
- `general/`
  - browser rendering pipeline
  - HTTP caching
  - authentication vs authorization
  - web security cơ bản

### Chưa có nội dung

- `vue/`
- `nuxtjs/`

---

## Quy Ước Cập Nhật Index

- Sau khi thêm file mới, chạy lại script generate index.
- Nếu một topic còn cùng chủ đề nhưng sâu hơn, ưu tiên thêm vào file cũ trước khi tạo file mới.
- Nếu tạo nhóm con mới, giữ tên thư mục ở dạng `kebab-case`.
