# Tài Liệu Phỏng Vấn Frontend

Thư mục này chứa các câu hỏi phỏng vấn và câu trả lời mẫu dành cho lập trình viên frontend.

Xem danh sách topic hiện có và backlog gợi ý tại `INDEX.md`.

---

## Cấu Trúc Thư Mục

```
docs/frontend/
├── README.md               ← Tài liệu này (quy tắc & hướng dẫn)
├── TEMPLATE.md             ← Template mẫu cho mỗi file
│
├── javascript/             ← Ngôn ngữ: JavaScript
│   ├── closures/
│   ├── prototype/
│   ├── event-loop/
│   └── ...
│
├── typescript/             ← Ngôn ngữ: TypeScript
│   ├── generics/
│   ├── type-vs-interface/
│   └── ...
│
├── css/                    ← Ngôn ngữ/Công nghệ: CSS
│   ├── flexbox/
│   ├── grid/
│   └── ...
│
├── react/                  ← Framework: React
│   ├── hooks/
│   ├── lifecycle/
│   ├── state-management/
│   └── ...
│
├── vue/                    ← Framework: Vue
│   ├── reactivity/
│   ├── composition-api/
│   └── ...
│
├── nextjs/                 ← Framework: Next.js
│   ├── ssr-vs-ssg/
│   ├── app-router/
│   └── ...
│
└── general/                ← Kiến thức chung (không phụ thuộc ngôn ngữ)
    ├── web-performance/
    ├── security/
    └── ...
```

---

## Quy Tắc Đặt Tên

### Thư Mục (folder)
- Dùng **kebab-case** (chữ thường, ngăn cách bằng dấu gạch ngang)
- Tên mô tả ngắn gọn, rõ ràng
- Ví dụ: `event-loop`, `state-management`, `type-vs-interface`

### File
- Dùng **kebab-case**
- Đặt tên theo **topic chính** của nội dung
- Luôn có phần mở rộng `.md`
- Ví dụ: `closures.md`, `use-effect.md`, `virtual-dom.md`

---

## Phân Loại Thư Mục Cấp 1

| Thư mục       | Dùng cho                                      |
|---------------|-----------------------------------------------|
| `javascript/` | Câu hỏi về JS thuần (ES5, ES6+, runtime...)   |
| `typescript/` | Câu hỏi về TypeScript                         |
| `css/`        | CSS, SCSS, styling, layout                    |
| `html/`       | HTML semantics, accessibility, SEO            |
| `react/`      | React, React ecosystem                        |
| `vue/`        | Vue 2, Vue 3, Pinia, Vue Router               |
| `nextjs/`     | Next.js (App Router, Pages Router, SSR...)    |
| `nuxtjs/`     | Nuxt.js                                       |
| `general/`    | Performance, Security, Browser, HTTP...       |

---

## Quy Tắc Nội Dung

- Tất cả nội dung viết bằng **tiếng Việt**
- Câu trả lời phải **ngắn gọn, súc tích** — phù hợp để trả lời trong buổi phỏng vấn
- Luôn có **ví dụ code** minh họa khi cần thiết
- Ghi rõ **mức độ câu hỏi**: Cơ bản / Trung cấp / Nâng cao
- Tham khảo `TEMPLATE.md` để biết format chi tiết

---

## Điều Hướng Nhanh

- `INDEX.md` — danh sách topic hiện có theo folder và gợi ý phần còn thiếu
- `TEMPLATE.md` — mẫu chuẩn để tạo file mới
- `python3 scripts/generate_frontend_index.py` — regenerate `INDEX.md` từ filesystem
