#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "frontend"
INDEX_PATH = DOCS_DIR / "INDEX.md"
EXCLUDED_FILES = {"README.md", "TEMPLATE.md", "INDEX.md"}
GROUP_ORDER = [
    "javascript",
    "typescript",
    "css",
    "html",
    "react",
    "nextjs",
    "general",
    "vue",
    "nuxtjs",
]
GROUP_LABELS = {
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "css": "CSS",
    "html": "HTML",
    "react": "React",
    "nextjs": "Next.js",
    "general": "General",
    "vue": "Vue",
    "nuxtjs": "Nuxt.js",
}
SUGGESTED_GAPS = {
    "Ưu tiên cao": {
        "javascript": [
            "`this`, `bind/call/apply`",
            "`prototype` và prototype chain",
            "`hoisting`, `var/let/const`",
            "`debounce` vs `throttle`",
        ],
        "typescript": [
            "`generics`",
            "`unknown` vs `any` vs `never`",
            "`discriminated union`",
            "`satisfies` và narrowing",
        ],
        "react": [
            "controlled vs uncontrolled form",
            "`useMemo` vs `useCallback`",
            "state lifting vs composition",
            "React Query / server state",
            "error boundary",
        ],
        "nextjs": [
            "caching và revalidation",
            "route handler vs server action",
            "hydration mismatch",
        ],
    },
    "Ưu tiên trung bình": {
        "css": [
            "`position`, stacking context, `z-index`",
            "responsive design và media/container query",
            "BEM, CSS Modules, CSS-in-JS",
        ],
        "html": [
            "SEO cơ bản",
            "semantic HTML ngoài accessibility",
            "form semantics",
        ],
        "general": [
            "browser rendering pipeline",
            "HTTP caching",
            "authentication vs authorization",
            "web security cơ bản",
        ],
    },
    "Chưa có nội dung": {
        "vue": [],
        "nuxtjs": [],
    },
}


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def collect_topics() -> dict[str, list[dict[str, str]]]:
    topics: dict[str, list[dict[str, str]]] = defaultdict(list)

    for path in sorted(DOCS_DIR.rglob("*.md")):
        if path.name in EXCLUDED_FILES:
            continue

        relative_path = path.relative_to(DOCS_DIR)
        parts = relative_path.parts
        if not parts:
            continue

        group = parts[0]
        subgroup = parts[1] if len(parts) > 2 else "-"

        topics[group].append(
            {
                "subgroup": subgroup,
                "title": read_title(path),
                "path": relative_path.as_posix(),
            }
        )

    for group_topics in topics.values():
        group_topics.sort(key=lambda item: (item["subgroup"], item["title"], item["path"]))

    return topics


def render_group_overview(topics: dict[str, list[dict[str, str]]]) -> list[str]:
    lines = [
        "## Tổng Quan Hiện Tại",
        "",
        "| Nhóm | Số file |",
        "|------|---------|",
    ]

    total = 0
    for group in GROUP_ORDER:
        count = len(topics.get(group, []))
        total += count
        lines.append(f"| `{group}/` | {count} |")

    lines.extend(
        [
            "",
            f"Tổng số file nội dung hiện tại: **{total}**",
        ]
    )
    return lines


def render_topic_tables(topics: dict[str, list[dict[str, str]]]) -> list[str]:
    lines = ["## Topic Hiện Có", ""]

    for group in GROUP_ORDER:
        lines.append(f"### {GROUP_LABELS[group]}")
        lines.append("")
        lines.append("| Nhóm con | Topic | File |")
        lines.append("|----------|-------|------|")

        group_topics = topics.get(group, [])
        if not group_topics:
            lines.append("| - | Chưa có nội dung | - |")
        else:
            for item in group_topics:
                lines.append(
                    f"| `{item['subgroup']}/` | {item['title']} | `{item['path']}` |"
                )
        lines.append("")

    if lines[-1] == "":
        lines.pop()
    return lines


def render_suggested_gaps(topics: dict[str, list[dict[str, str]]]) -> list[str]:
    lines = [
        "## Khoảng Trống Dễ Thấy",
        "",
        "Đây là backlog gợi ý để bổ sung dần. Mục tiêu là phủ các topic middle frontend hay gặp trước khi mở rộng sang niche topic.",
        "",
    ]

    for section_name, groups in SUGGESTED_GAPS.items():
        lines.append(f"### {section_name}")
        lines.append("")

        for group, items in groups.items():
            if section_name == "Chưa có nội dung":
                if topics.get(group):
                    continue
                lines.append(f"- `{group}/`")
                continue

            lines.append(f"- `{group}/`")
            for item in items:
                lines.append(f"  - {item}")

        lines.append("")

    if lines[-1] == "":
        lines.pop()
    return lines


def build_index() -> str:
    topics = collect_topics()

    sections = [
        "# Index Tài Liệu Frontend",
        "",
        "> File này được generate bởi `scripts/generate_frontend_index.py`. Không nên sửa tay trừ khi bạn cũng cập nhật script.",
        "",
        "File này dùng để tra nhanh thư mục `docs/frontend/` hiện có những topic nào và những khoảng trống nào nên ưu tiên bổ sung tiếp.",
        "",
        "---",
        "",
        "## Cách Dùng",
        "",
        "- Khi cần thêm tài liệu mới, kiểm tra file này trước để tránh tạo trùng topic.",
        "- Nếu topic đã tồn tại, ưu tiên mở rộng file cũ thay vì tạo file mới.",
        "- Nếu topic chưa có, chọn đúng folder cấp 1 và nhóm con gần nhất rồi thêm file mới.",
        "- Sau khi thêm file mới, chạy `python3 scripts/generate_frontend_index.py` để cập nhật lại index.",
        "",
        "---",
        "",
    ]

    sections.extend(render_group_overview(topics))
    sections.extend(["", "---", ""])
    sections.extend(render_topic_tables(topics))
    sections.extend(["", "---", ""])
    sections.extend(render_suggested_gaps(topics))
    sections.extend(
        [
            "",
            "---",
            "",
            "## Quy Ước Cập Nhật Index",
            "",
            "- Sau khi thêm file mới, chạy lại script generate index.",
            "- Nếu một topic còn cùng chủ đề nhưng sâu hơn, ưu tiên thêm vào file cũ trước khi tạo file mới.",
            "- Nếu tạo nhóm con mới, giữ tên thư mục ở dạng `kebab-case`.",
        ]
    )

    return "\n".join(sections) + "\n"


def main() -> None:
    INDEX_PATH.write_text(build_index(), encoding="utf-8")


if __name__ == "__main__":
    main()
