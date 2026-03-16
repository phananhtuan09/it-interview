# TypeScript Utility Types cho API Response phức tạp

## Thông Tin File

- **Chủ đề:** Utility Types — Pick, Omit, Partial và xử lý Nested API Response
- **Ngôn ngữ / Framework:** TypeScript
- **Mức độ:** Trung cấp
- **Cập nhật lần cuối:** 2026-03-15

---

## Câu Hỏi 1: Xử lý Type Safety cho API response lớn và nested

**Mức độ:** Trung cấp

### Câu hỏi

Giả sử bạn nhận được một API trả về một Object rất lớn và lồng ghép nhiều lớp (nested object), nhưng bạn chỉ cần dùng một vài field trong đó. Bạn sẽ xử lý như thế nào để đảm bảo Type Safety mà vẫn giữ cho Codebase sạch sẽ, dễ bảo trì? Bạn có ưu tiên dùng Interface, Type hay các Utility Types (như Pick, Omit, Partial) trong trường hợp này không?

### Câu trả lời ngắn gọn

Tôi định nghĩa `ApiResponse` type đầy đủ cho toàn bộ response, sau đó dùng `Pick` hoặc tạo sub-type nhỏ hơn cho từng use case cụ thể. Ưu tiên `type` với Utility Types cho derived types, `interface` cho base model. Không định nghĩa lại type thủ công từng field — gây drift khi API thay đổi. Tổ chức theo layer: `types/api/` cho raw response, `types/domain/` cho transformed data dùng trong UI.

### Giải thích chi tiết

**Quy tắc chọn `interface` vs `type`:**
- `interface` — cho **base model/contract**, có thể extend/implement, hỗ trợ declaration merging
- `type` — cho **derived types** dùng Utility Types, union types, intersection types

**Các Utility Types thường dùng nhất:**

| Utility Type | Dùng khi | Ví dụ |
|---|---|---|
| `Pick<T, K>` | Chỉ cần một số field từ type lớn | `Pick<User, 'id' \| 'name'>` |
| `Omit<T, K>` | Muốn tất cả field trừ một vài field nhạy cảm | `Omit<User, 'password' \| 'secret'>` |
| `Partial<T>` | Tất cả field đều optional (form, patch API) | `Partial<UserProfile>` |
| `Required<T>` | Tất cả field đều required | `Required<Config>` |
| `Readonly<T>` | Không cho phép mutation | `Readonly<Config>` |
| `Record<K, V>` | Map/Dictionary type | `Record<string, Permission>` |

**Chiến lược tổ chức type trong dự án MODAT:**

```
types/
├── api/          # Raw response từ API — shape đúng với backend
│   ├── network.ts
│   ├── security.ts
│   └── common.ts
├── domain/       # Transformed type dùng trong UI components
│   ├── graph.ts
│   └── alert.ts
└── index.ts      # Re-export
```

**Nguyên tắc:**
1. Luôn có **single source of truth** — define base type một lần
2. Dùng Utility Types để derive từ base type — không copy-paste field
3. Transform data ở một chỗ (service layer) — component nhận domain type, không nhận raw API type
4. Dùng `satisfies` operator để validate type mà không mất inference

### Ví dụ minh họa

```typescript
// === MODAT: Raw API Response từ Security API ===
// types/api/network.ts

// Base interface — định nghĩa đầy đủ shape của API response
interface NetworkDeviceApiResponse {
  id: string;
  hostname: string;
  ip_address: string;
  mac_address: string;
  device_type: 'router' | 'switch' | 'firewall' | 'endpoint';
  vendor: string;
  firmware_version: string;
  location: {
    building: string;
    floor: number;
    rack_position: string;
    coordinates: { lat: number; lng: number };
  };
  security: {
    risk_score: number;
    last_scan: string;
    vulnerabilities: Array<{
      cve_id: string;
      severity: 'critical' | 'high' | 'medium' | 'low';
      description: string;
      patch_available: boolean;
    }>;
    open_ports: number[];
    compliance_status: Record<string, boolean>;
  };
  network: {
    vlan_id: number;
    subnet: string;
    gateway: string;
    dns_servers: string[];
    bandwidth_mbps: number;
  };
  metadata: {
    created_at: string;
    updated_at: string;
    created_by: string;
    tags: string[];
  };
}
```

```typescript
// === Dùng Utility Types để tạo sub-types theo use case ===
// types/domain/graph.ts

// Chỉ cần các field để render node trong graph visualization
// Pick chỉ lấy những field cần — không để type thừa
type GraphNodeDevice = Pick<
  NetworkDeviceApiResponse,
  'id' | 'hostname' | 'ip_address' | 'device_type' | 'vendor'
> & {
  // Flatten nested field ra ngoài cho dễ dùng
  riskScore: number;           // từ security.risk_score
  vulnerabilityCount: number;  // đếm từ security.vulnerabilities
};

// Cho security alert list — không cần location hay network detail
type SecurityAlertDevice = Pick<
  NetworkDeviceApiResponse,
  'id' | 'hostname' | 'ip_address'
> & {
  criticalVulnerabilities: NetworkDeviceApiResponse['security']['vulnerabilities'];
};

// Cho form edit device — tất cả optional vì PATCH API
type UpdateDevicePayload = Partial<
  Pick<NetworkDeviceApiResponse, 'hostname' | 'vendor' | 'firmware_version'>
> & {
  tags?: string[]; // Thêm field không có trong base type
};

// Omit — loại bỏ sensitive fields khi log/display
type DeviceDisplayInfo = Omit<
  NetworkDeviceApiResponse,
  'security' | 'metadata' // Không hiển thị security detail và audit metadata
>;
```

```typescript
// === Transform function — convert raw API type sang domain type ===
// services/networkService.ts

function transformToGraphNode(raw: NetworkDeviceApiResponse): GraphNodeDevice {
  return {
    id: raw.id,
    hostname: raw.hostname,
    ip_address: raw.ip_address,
    device_type: raw.device_type,
    vendor: raw.vendor,
    // Flatten nested fields
    riskScore: raw.security.risk_score,
    vulnerabilityCount: raw.security.vulnerabilities.length,
  };
}

// Component nhận domain type — không quan tâm raw API shape
function GraphNode({ device }: { device: GraphNodeDevice }) {
  return (
    <div style={{ color: device.riskScore > 80 ? 'red' : 'green' }}>
      {device.hostname} — Risk: {device.riskScore}
    </div>
  );
}
```

```typescript
// === Kỹ thuật nâng cao: Nested Pick với helper type ===

// Utility type tự tạo để Pick nested field
type NestedPick<T, K1 extends keyof T, K2 extends keyof T[K1]> = {
  [P in K1]: Pick<T[P], K2 extends keyof T[P] ? K2 : never>;
};

// Lấy chỉ risk_score và vulnerabilities từ security object
type SecuritySummary = Pick<NetworkDeviceApiResponse, 'id' | 'hostname'> & {
  security: Pick<NetworkDeviceApiResponse['security'], 'risk_score' | 'vulnerabilities'>;
};

// satisfies — validate type nhưng giữ nguyên inference
const defaultConfig = {
  maxNodes: 1000,
  renderMode: 'canvas',
  clusterThreshold: 50,
} satisfies Partial<GraphConfig>; // TypeScript check mà không cast

// typeof defaultConfig vẫn là type chính xác, không bị widened thành GraphConfig
```

```typescript
// === Generic API Response wrapper ===
// Dùng cho mọi API endpoint — không viết lại boilerplate

interface ApiResponse<T> {
  data: T;
  total?: number;
  page?: number;
  error?: string;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
}

// Sử dụng
type DeviceListResponse = PaginatedResponse<GraphNodeDevice>;
type DeviceDetailResponse = ApiResponse<NetworkDeviceApiResponse>;

// Fetch function — type-safe từ API đến UI
async function fetchDevices(params: FilterParams): Promise<GraphNodeDevice[]> {
  const response: DeviceListResponse = await api.get('/devices', { params });
  // Transform raw data sang domain type
  return response.data.map(transformToGraphNode);
}
```

### Lưu ý / Bẫy thường gặp

- **Đừng dùng `any`** khi không biết type — dùng `unknown` và narrow dần
- **Đừng copy-paste field** từ type lớn sang type nhỏ — dùng `Pick`/`Omit` để tránh drift khi API thay đổi
- `interface` hỗ trợ **declaration merging** — có thể extend ở nhiều file; `type` thì không
- **Tránh nested Pick quá sâu** — nếu cần nhiều field nested, tốt hơn là flatten qua transform function
- Dùng **`satisfies` operator** (TypeScript 4.9+) thay vì `as` để validate type mà vẫn giữ inference chính xác
- **`Record<string, T>`** tốt hơn `{ [key: string]: T }` — ngắn gọn và readable hơn

---

## Tài Liệu Tham Khảo

- [TypeScript Handbook - Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [TypeScript Handbook - Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
- [TypeScript - satisfies operator](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html)
