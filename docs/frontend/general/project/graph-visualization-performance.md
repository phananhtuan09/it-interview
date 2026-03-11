# Tối Ưu Performance Graph Visualization (React Force Graph)

## Thông Tin File

- **Chủ đề:** Graph Visualization Performance Optimization
- **Ngôn ngữ / Framework:** React / Canvas / WebGL
- **Mức độ:** Nâng cao
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Tối ưu performance khi render graph với hàng nghìn node

**Mức độ:** Nâng cao

### Câu hỏi

Khi graph có rất nhiều node và edge (ví dụ vài nghìn node), bạn xử lý như thế nào để tránh lag hoặc drop FPS trên trình duyệt? Hãy mô tả các kỹ thuật tối ưu performance bạn đã áp dụng.

### Câu trả lời ngắn gọn

Dùng thư viện render bằng **Canvas/WebGL** thay vì DOM để tránh bottleneck khi render nhiều node. Tùy chỉnh node rendering bằng Canvas API trực tiếp thay vì React component. Cache các asset (icon, texture) để tránh load lại mỗi lần update. Giới hạn simulation tính toán bằng `cooldownTicks`. Dùng `useMemo` cho data transform nặng và `ResizeObserver` thay vì `window.resize` để đo container size.

### Giải thích chi tiết

**Tại sao Canvas/WebGL tốt hơn DOM khi render nhiều node:**
- DOM render mỗi node thành một HTML element → hàng nghìn element = DOM tree nặng
- Canvas/WebGL render trực tiếp lên pixel buffer — không tạo DOM node
- Browser không cần layout + paint cho từng element riêng lẻ
- React Force Graph (3D) dùng Three.js + WebGL → GPU accelerated

**Các kỹ thuật đã áp dụng:**

1. **Canvas API cho custom node** — thay vì React component
2. **useMemo** cho data transform (nodes/edges processing)
3. **cooldownTicks** — giới hạn số lần tính toán simulation vật lý
4. **Icon caching** — cache canvas texture, không load lại mỗi update
5. **ResizeObserver** — hiệu quả hơn `window.resize` event

**Kỹ thuật nâng cao có thể thêm:**
- LOD (Level of Detail) — khi zoom out, render node đơn giản hơn
- Node clustering — nhóm node lại khi có quá nhiều
- Progressive rendering — render theo batch, không block main thread

### Ví dụ minh họa

```javascript
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';

// ✅ Cache icon texture — tránh tạo mới mỗi frame
const iconCache = new Map();

function getIconTexture(iconUrl) {
  if (iconCache.has(iconUrl)) {
    return iconCache.get(iconUrl); // Trả về cache
  }

  // Tạo texture mới và cache lại
  const texture = new THREE.TextureLoader().load(iconUrl);
  iconCache.set(iconUrl, texture);
  return texture;
}
```

```javascript
// ✅ useMemo cho data transform nặng
function GraphComponent({ rawData }) {
  // Chỉ transform lại khi rawData thay đổi — không tính lại mỗi render
  const graphData = useMemo(() => {
    return {
      nodes: rawData.nodes.map(node => ({
        id: node.id,
        label: node.name,
        color: getNodeColor(node.type),
        // ... transform khác
      })),
      links: rawData.edges.map(edge => ({
        source: edge.from,
        target: edge.to,
        // ...
      })),
    };
  }, [rawData]);

  return (
    <ForceGraph3D
      graphData={graphData}
      // Giới hạn simulation ticks để tránh tính toán liên tục
      cooldownTicks={100}
      // Custom node bằng Three.js object thay vì React component
      nodeThreeObject={renderCustomNode}
    />
  );
}
```

```javascript
// ✅ Custom node bằng Three.js — không tạo React component cho mỗi node
function renderCustomNode(node) {
  // Tạo Three.js mesh thay vì React element
  const geometry = new THREE.SphereGeometry(5);
  const material = new THREE.MeshLambertMaterial({
    color: node.color,
    map: getIconTexture(node.iconUrl), // Lấy từ cache
  });

  return new THREE.Mesh(geometry, material);
}

// So sánh: ❌ Cách này tạo React component cho mỗi node → lag với hàng nghìn node
// nodeThreeObject={(node) => <div className="node">{node.label}</div>}
```

```javascript
// ✅ ResizeObserver thay vì window.resize
function GraphContainer() {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setDimensions({ width, height });
      }
    });

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect(); // Cleanup

    // So sánh: ❌ window.resize fire cho mọi resize trên trang, không chỉ container này
    // window.addEventListener('resize', handleResize);
  }, []);

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%' }}>
      <ForceGraph3D
        width={dimensions.width}
        height={dimensions.height}
        graphData={graphData}
      />
    </div>
  );
}
```

```javascript
// ✅ LOD (Level of Detail) — đơn giản hóa node khi zoom out
function renderNodeWithLOD(node, camera) {
  const distance = camera.position.distanceTo(new THREE.Vector3(node.x, node.y, node.z));

  if (distance > 500) {
    // Zoom out xa — render đơn giản hơn (chỉ sphere, không có label)
    return new THREE.Mesh(
      new THREE.SphereGeometry(3),
      new THREE.MeshBasicMaterial({ color: node.color })
    );
  }

  // Zoom gần — render đầy đủ với label và icon
  return renderFullNode(node);
}
```

### Lưu ý / Bẫy thường gặp

- **Canvas/WebGL tốt hơn DOM** cho large-scale rendering — chọn thư viện render bằng canvas ngay từ đầu
- `cooldownTicks` qúa thấp → simulation chưa ổn định, node vẫn dịch chuyển; quá cao → tốn CPU
- **Icon caching** rất quan trọng — `TextureLoader.load()` là async operation, cache tránh re-fetch
- Không dùng `React.createElement` hoặc JSX cho node rendering trong canvas mode — sẽ không hoạt động
- Với 3D graph, giảm `nodeResolution` (độ phân giải sphere) để tăng FPS khi có nhiều node

---

## Tài Liệu Tham Khảo

- [React Force Graph Docs](https://github.com/vasturiano/react-force-graph)
- [Three.js Docs](https://threejs.org/docs/)
- [MDN - ResizeObserver](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver)
