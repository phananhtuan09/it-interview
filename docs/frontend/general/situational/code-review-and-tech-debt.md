# Xử Lý Code Review và Tech Debt trong Team

## Thông Tin File

- **Chủ đề:** Code Review, Tech Debt Management, Team Communication
- **Ngôn ngữ / Framework:** General (Kỹ năng mềm + kỹ thuật)
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Xử lý code review khi deadline gấp và code quality thấp

**Mức độ:** Trung cấp

### Câu hỏi

Bạn review code của một junior developer và thấy code đó chạy đúng nhưng rất khó maintain (logic lặp lại nhiều, component quá lớn, naming không rõ). Tuy nhiên deadline đang rất gấp. Bạn sẽ xử lý situation này như thế nào?

### Câu trả lời ngắn gọn

Khi code chạy đúng và không gây risk production, tôi sẽ không block PR để đảm bảo tiến độ. Trong code review, tôi comment mang tính xây dựng — chỉ ra vấn đề và gợi ý cách refactor cụ thể. Sau khi release, tôi tạo tech debt task để refactor và pair với junior để giải thích, giúp họ cải thiện cho lần sau. Ngoài ra, đề xuất team xây dựng coding guideline chung để tránh vấn đề tương tự trong tương lai.

### Giải thích chi tiết

**Framework quyết định: Đánh giá mức độ ảnh hưởng**

Câu hỏi cần trả lời trước khi quyết định:
1. Code có gây **risk production** không? (bug tiềm ẩn, security issue)
2. Code có ảnh hưởng **performance** đáng kể không?
3. Code có block **team khác** làm việc không?
4. Tech debt này có **dễ refactor sau** không?

Nếu chỉ là code quality (naming, structure) → không block PR khi deadline gấp.

**Cách tiếp cận:**

**1. Approve với comment mang tính xây dựng**
- Không chỉ nói "code này sai" — gợi ý cách viết tốt hơn cụ thể
- Phân biệt: comment nào là **blocker** (phải sửa), comment nào là **suggestion** (nên sửa sau)
- Giải thích **tại sao** — giúp junior học, không chỉ làm theo

**2. Quản lý tech debt**
- Tạo Jira/GitHub issue ghi rõ: vấn đề là gì, tại sao cần refactor, estimate effort
- Link issue vào PR để có context
- Prioritize tech debt trong sprint tiếp theo

**3. Pair programming / 1-on-1**
- Sau release, ngồi cùng junior để walk through cách refactor
- Cho họ tự refactor dưới sự hướng dẫn — học qua làm
- Không làm thay — tạo cơ hội để junior phát triển

**4. Prevent recurrence**
- Đề xuất coding guideline, style guide cho team
- Tạo shared components/utilities để tránh code duplication
- Set up ESLint rules để enforce coding standard tự động

### Ví dụ minh họa

```javascript
// ❌ Code junior viết — logic lặp lại, naming không rõ
function Comp1({ d }) {
  return (
    <div>
      <p>{d.nm}</p>
      <p>{d.em}</p>
      <button onClick={() => {
        fetch('/api/users/' + d.id, { method: 'DELETE' })
          .then(r => r.json())
          .then(res => {
            if (res.ok) {
              window.location.reload();
            }
          });
      }}>Delete</button>
    </div>
  );
}

function Comp2({ d }) {
  return (
    <div>
      <p>{d.nm}</p>
      <p>{d.em}</p>
      <button onClick={() => {
        fetch('/api/admins/' + d.id, { method: 'DELETE' })
          .then(r => r.json())
          .then(res => {
            if (res.ok) {
              window.location.reload();
            }
          });
      }}>Delete</button>
    </div>
  );
}
```

```javascript
// ✅ Cách comment trong code review — cụ thể và mang tính xây dựng

// [Suggestion] Naming: `d` không rõ ý nghĩa, nên đặt tên rõ ràng hơn.
// Đề xuất: đổi prop `d` thành `user` hoặc `entity`

// [Suggestion] Code duplication: Comp1 và Comp2 có logic gần giống nhau.
// Có thể extract thành 1 component với prop `apiEndpoint`:
// <EntityCard entity={user} onDelete={() => deleteUser(user.id)} />

// [Suggestion] Side effect trong event handler:
// Nên tách logic delete ra custom hook hoặc service function,
// không inline fetch trong JSX. Ví dụ:
// const { deleteUser, loading } = useDeleteUser();
```

```javascript
// ✅ Refactored version — gợi ý cho junior sau sprint

// Shared component — tránh duplication
function EntityCard({ entity, onDelete, loading }) {
  return (
    <div>
      <p>{entity.name}</p>
      <p>{entity.email}</p>
      <button onClick={onDelete} disabled={loading}>
        {loading ? 'Deleting...' : 'Delete'}
      </button>
    </div>
  );
}

// Custom hook — tách logic ra khỏi UI
function useDeleteEntity(endpoint) {
  const [loading, setLoading] = useState(false);

  const deleteEntity = async (id) => {
    setLoading(true);
    try {
      await fetch(`${endpoint}/${id}`, { method: 'DELETE' });
      // Không reload page — dùng state/cache invalidation
    } finally {
      setLoading(false);
    }
  };

  return { deleteEntity, loading };
}

// Usage
function UserList({ users }) {
  const { deleteEntity: deleteUser, loading } = useDeleteEntity('/api/users');

  return users.map(user => (
    <EntityCard
      key={user.id}
      entity={user}
      onDelete={() => deleteUser(user.id)}
      loading={loading}
    />
  ));
}
```

### Lưu ý / Bẫy thường gặp

- **Không block PR** vì code quality khi deadline gấp — delivery quan trọng hơn perfect code
- **Phân biệt blocker vs suggestion** trong code review comment — tránh làm junior bị overwhelm
- **Tech debt phải được track** — không track → sẽ không bao giờ được fix
- Pair programming hiệu quả hơn chỉ comment — junior học nhanh hơn khi được giải thích trực tiếp
- **Đề xuất automation** (ESLint, Prettier, Husky pre-commit hook) để enforce style tự động, giảm review burden

---

## Tài Liệu Tham Khảo

- [Google Engineering Practices - Code Review](https://google.github.io/eng-practices/review/)
- [Conventional Comments](https://conventionalcomments.org/)
