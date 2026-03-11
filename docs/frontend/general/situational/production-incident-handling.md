# Xử Lý Production Incident / Bug Nghiêm Trọng

## Thông Tin File

- **Chủ đề:** Production Incident Handling Process
- **Ngôn ngữ / Framework:** General (Quy trình xử lý)
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Quy trình xử lý bug production nghiêm trọng

**Mức độ:** Trung cấp

### Câu hỏi

Production có bug nghiêm trọng: user không thể submit form quan trọng (checkout hoặc submit survey). PM và client đang rất gấp. Bạn sẽ xử lý incident này theo các bước nào?

### Câu trả lời ngắn gọn

Bước 1: Xác nhận và reproduce issue để hiểu mức độ ảnh hưởng. Bước 2: Ưu tiên giảm impact ngay — rollback hoặc hotfix nhanh để unblock user. Bước 3: Sau khi hệ thống ổn định, phân tích root cause qua logs, commit gần nhất và API response. Bước 4: Deploy hotfix và verify trên production. Bước 5: Viết postmortem và cải thiện testing/monitoring để tránh tái diễn.

### Giải thích chi tiết

**Quy trình xử lý incident:**

```
Detect → Triage → Mitigate → Root Cause → Fix → Verify → Postmortem
```

**Phase 1 — Detect & Triage (phút đầu tiên)**
- Confirm bug xảy ra (reproduce được không?)
- Đánh giá scope: bao nhiêu % user bị ảnh hưởng?
- Priority: Critical (mọi user), High (một số user), Medium (edge case)
- Thông báo team ngay nếu là critical

**Phase 2 — Immediate Mitigation (ưu tiên hàng đầu)**
- Option 1: **Rollback** — nhanh nhất, trở về version ổn định trước
- Option 2: **Feature flag** — tắt tính năng bị lỗi
- Option 3: **Hotfix** — nếu fix nhanh được và test được ngay
- Mục tiêu: unblock user ASAP, giảm business impact

**Phase 3 — Root Cause Analysis**
- Kiểm tra **error logs** (Sentry, CloudWatch, Datadog)
- Xem **commit gần nhất** — deploy nào gây ra lỗi?
- Kiểm tra **API response** — 4xx? 5xx? unexpected payload?
- Xem **browser console** của user gặp lỗi
- Reproduce với data cụ thể của user bị ảnh hưởng

**Phase 4 — Fix & Deploy**
- Viết unit test cho bug case trước khi fix
- Fix → review → deploy hotfix
- Verify trên production với real data

**Phase 5 — Postmortem**
- Timeline: bug xuất hiện khi nào, detect khi nào, fix khi nào
- Root cause: tại sao bug xảy ra
- Impact: bao nhiêu user, bao nhiêu doanh thu bị ảnh hưởng
- Action items: cải thiện gì để tránh tái diễn (test coverage, monitoring, alert)

### Ví dụ minh họa

```javascript
// === Scenario: Form submit bị lỗi sau deploy ===

// Bước 1: Reproduce — check console, network tab
// Phát hiện: API /api/checkout trả về 400 Bad Request
// Payload gửi lên thiếu field `currency`

// Root cause: PR #234 thêm field `currency` là required ở backend
// nhưng frontend form chưa cập nhật → validate fail

// ✅ Fix:
function CheckoutForm() {
  const handleSubmit = async (formData) => {
    const payload = {
      ...formData,
      currency: 'VND', // Field mới backend yêu cầu — bị thiếu sau deploy
    };

    const response = await fetch('/api/checkout', {
      method: 'POST',
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      // ✅ Error handling rõ ràng — log đủ thông tin để debug
      const error = await response.json();
      console.error('Checkout failed:', {
        status: response.status,
        error,
        payload, // Log payload để verify
      });
      throw new Error(error.message);
    }
  };
}
```

```javascript
// ✅ Error monitoring setup — detect issue sớm hơn
// Dùng Sentry để capture lỗi với full context

import * as Sentry from '@sentry/nextjs';

async function submitForm(data) {
  try {
    const response = await fetch('/api/submit', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();

      // Capture với context để debug dễ hơn
      Sentry.captureException(new Error('Form submit failed'), {
        extra: {
          statusCode: response.status,
          errorMessage: error.message,
          formData: data, // Cẩn thận với PII data
        },
      });

      throw error;
    }
  } catch (err) {
    Sentry.captureException(err);
    throw err;
  }
}
```

```markdown
## Postmortem Template

### Incident Summary
- **Date:** 2026-03-11
- **Duration:** 45 minutes (14:00 - 14:45)
- **Impact:** 100% user không submit được checkout form
- **Severity:** Critical

### Timeline
- 14:00 — Deploy v2.1.4 lên production
- 14:05 — PM nhận complaint từ user
- 14:08 — Engineer reproduce được bug
- 14:15 — Rollback về v2.1.3
- 14:20 — User có thể checkout trở lại
- 14:45 — Root cause xác định, hotfix đang develop

### Root Cause
Backend PR #234 thêm field `currency` là required
nhưng frontend không được update tương ứng.
Không có integration test cover case này.

### Action Items
- [ ] Thêm integration test cho checkout API contract
- [ ] Setup API schema validation (OpenAPI/Zod)
- [ ] Cải thiện staging testing process trước deploy
- [ ] Alert khi checkout error rate > 5%
```

```yaml
# ✅ Monitoring alert — phát hiện sớm hơn
# Ví dụ với Datadog monitor

monitors:
  checkout_error_rate:
    query: "sum:api.errors{endpoint:/api/checkout}.as_count() / sum:api.requests{endpoint:/api/checkout}.as_count() > 0.05"
    message: "🚨 Checkout error rate > 5% — investigate immediately"
    notify: ["@slack-production-alerts"]
```

### Lưu ý / Bẫy thường gặp

- **Ưu tiên mitigate trước, root cause sau** — mỗi phút user không submit được = doanh thu mất
- **Rollback nhanh hơn hotfix** — nếu có thể rollback, làm ngay, đừng cố fix trước
- **Không fix vội** — sửa sai lại có thể gây thêm vấn đề, reproduce kỹ trước khi fix
- **Communication quan trọng** — cập nhật PM và stakeholder định kỳ trong lúc incident
- **Postmortem không phải blame** — mục tiêu là cải thiện hệ thống, không phải tìm người có lỗi
- **Test sau fix** — verify trên staging với production data trước khi deploy hotfix

---

## Tài Liệu Tham Khảo

- [Google SRE - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [PagerDuty - Incident Response Guide](https://response.pagerduty.com/)
- [Sentry Docs](https://docs.sentry.io/)
