---
name: writing-interview-docs
description: Create or update Vietnamese frontend interview Markdown documents under `docs/frontend/` in this repository. Use when asked to write interview docs by topic, language/framework, and difficulty; when converting a rough request into a structured file; when expanding an existing interview doc to match `docs/frontend/TEMPLATE.md`; or when a request references `.claude/commands/writing-interview-docs.md`.
---

# Writing Interview Docs

## Workflow

1. Read `docs/frontend/TEMPLATE.md` before writing.
2. Inspect nearby files under `docs/frontend/` to reuse the repository's existing folder taxonomy and writing style.
3. Extract or infer the required inputs:
   - `topic`
   - `language/framework`
   - `level`
   - optional question list
4. Create or update the target Markdown file.
5. Verify the final structure and report the result.

## Path Rules

- Normalize `language/framework` to a repo folder such as `javascript`, `typescript`, `css`, `html`, `react`, `vue`, `nextjs`, `nuxtjs`, or `general`.
- Convert new directory names and filenames to lowercase kebab-case.
- If the user explicitly gives a target path, use it.
- Otherwise, prefer an existing second-level folder that already matches the topic family. Reuse patterns already present in the repo, such as `hooks`, `performance`, `state-management`, `rendering`, `project`, or `situational`.
- If no existing category is a good match, create `docs/frontend/<framework>/<topic-slug>/<topic-slug>.md`.
- Default filename to `<topic-slug>.md`.

## Content Rules

- Write all prose in Vietnamese.
- Follow the section order from `docs/frontend/TEMPLATE.md`.
- Fill the metadata block with topic, language/framework, level, and the current date in `YYYY-MM-DD`.
- Keep each short answer within 4 sentences.
- Make every question concrete and interview-oriented. Avoid generic filler.
- Include a code block for every question. Use the most relevant fence language, and write code comments in Vietnamese.
- Include a `Lưu ý / Bẫy thường gặp` section for every question.
- For comparison topics, include a comparison section with a table and `Khi nào dùng cái nào?`. Add a short answer and detailed explanation as well when it improves consistency with existing docs.

## Question Generation

- If the user already supplies questions, keep them and improve wording only when needed.
- If the user does not supply questions, generate 3-5 practical questions that match the requested topic and level.
- Prefer a mix of conceptual understanding, real-world usage, common mistakes, and follow-up depth.
- Add at least one comparison question when the topic naturally invites comparison.

## Editing Existing Docs

- Preserve the file's existing title and style if the target file already exists.
- Expand incomplete sections until they satisfy the template.
- Do not remove useful repository-specific examples just to make the file look more uniform.

## Final Checks

- Ensure the target directories exist before writing.
- Re-open the finished file and verify that the metadata and question sections are complete.
- Count the number of `## Câu Hỏi` sections before reporting completion.
- Report:
  - the file path
  - the number of question sections written
  - optional follow-up topics or questions worth adding next
