# Tối Ưu Performance Graph Visualization (React Force Graph)

## Thông Tin File

- **Chủ đề:** Graph Visualization Performance Optimization
- **Ngôn ngữ / Framework:** React / Canvas / WebGL
- **Mức độ:** Nâng cao
- **Cập nhật lần cuối:** 2026-03-15

---

## Câu Hỏi 1: Tối ưu performance khi render graph với hàng nghìn node

**Mức độ:** Nâng cao

### Câu hỏi

Trong dự án MODAT, bạn có nhắc đến việc sử dụng React Force Graph và React Flow để visualize các dữ liệu bảo mật mạng phức tạp. Khi làm việc với các biểu đồ dạng Graph có số lượng node (nút) và edge (cạnh) lớn, bạn đã gặp phải vấn đề gì về hiệu suất (performance) của trình duyệt không? Và bạn đã áp dụng những kỹ thuật gì để đảm bảo thao tác kéo thả, zoom của người dùng vẫn mượt mà?

### Câu trả lời ngắn gọn

Vấn đề chính khi render hàng nghìn node là browser bị nghẽn ở cả render pipeline (quá nhiều DOM element) lẫn computation (simulation vật lý tính liên tục). Tôi giải quyết bằng 7 kỹ thuật: (1) dùng thư viện render Canvas/WebGL thay vì DOM; (2) custom node rendering bằng Canvas API trực tiếp thay vì React component; (3) `useMemo` cho data transform nặng; (4) Icon/texture caching để tránh re-load mỗi frame; (5) `ResizeObserver` thay vì `window.resize`; (6) LOD — đơn giản hóa node khi zoom out; (7) Node clustering — nhóm node lại khi có quá nhiều.

### Giải thích chi tiết

**Vấn đề gặp phải:**
- **FPS drop** khi kéo thả hoặc zoom với > 500 node — DOM layout/paint quá tốn kém
- **Main thread bị block** bởi force simulation tính toán liên tục
- **Memory leak** do icon/texture bị tạo mới mỗi frame render
- **Janky resize** vì `window.resize` fire quá nhiều lần không cần thiết
- **Overcrowded graph** — khi zoom out, hàng nghìn node chồng chéo, vô nghĩa

**7 kỹ thuật đã áp dụng:**

1. **Canvas/WebGL rendering** — tránh bottleneck DOM khi render nhiều node
2. **Canvas API cho custom node** — không tạo React component cho mỗi node
3. **`useMemo`** cho data transform (nodes/edges/filter processing)
4. **Icon/texture caching** — cache canvas texture, không load lại mỗi update
5. **`ResizeObserver`** — chính xác và hiệu quả hơn `window.resize`
6. **LOD (Level of Detail)** — khi zoom out, render node đơn giản hơn
7. **Node Clustering** — nhóm node lại khi có quá nhiều

### Ví dụ minh họa

```javascript
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';

// ✅ Kỹ thuật 4: Icon/Texture caching
// Tránh TextureLoader.load() gọi lại mỗi frame render
const iconCache = new Map();

function getIconTexture(iconUrl) {
  if (iconCache.has(iconUrl)) {
    return iconCache.get(iconUrl); // Trả về từ cache
  }

  const texture = new THREE.TextureLoader().load(iconUrl);
  iconCache.set(iconUrl, texture);
  return texture;
}
```

```javascript
// ✅ Kỹ thuật 2 + 4: Custom node bằng Three.js object — không tạo React component
function renderCustomNode(node) {
  // Three.js mesh thay vì React element — GPU accelerated
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
// ✅ Kỹ thuật 3: useMemo cho data transform nặng
function GraphComponent({ rawData, activeFilters }) {
  // Chỉ transform lại khi rawData hoặc filters thay đổi — không tính lại mỗi render
  const graphData = useMemo(() => {
    const filteredNodes = rawData.nodes.filter(node =>
      activeFilters.includes(node.type)
    );

    return {
      nodes: filteredNodes.map(node => ({
        id: node.id,
        label: node.name,
        color: getNodeColor(node.type),
        iconUrl: getNodeIcon(node.type),
        // ... transform khác
      })),
      links: rawData.edges
        .filter(edge =>
          filteredNodes.some(n => n.id === edge.from) &&
          filteredNodes.some(n => n.id === edge.to)
        )
        .map(edge => ({
          source: edge.from,
          target: edge.to,
        })),
    };
  }, [rawData, activeFilters]); // Dependency array chính xác

  return (
    <ForceGraph3D
      graphData={graphData}
      cooldownTicks={100}         // Giới hạn simulation ticks
      nodeThreeObject={renderCustomNode}
    />
  );
}
```

```javascript
// ✅ Kỹ thuật 5: ResizeObserver thay vì window.resize
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

    return () => observer.disconnect(); // Cleanup quan trọng

    // ❌ window.resize: fire cho MỌI resize trên trang, không chỉ container này
    // Không chính xác khi container bị resize do layout thay đổi (sidebar collapse)
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
// ✅ Kỹ thuật 6: LOD (Level of Detail) — đơn giản hóa node khi zoom out
// Khi zoom out xa, render node đơn giản → tăng FPS đáng kể

function renderNodeWithLOD(node, { camera }) {
  const distance = camera.position.distanceTo(
    new THREE.Vector3(node.x, node.y, node.z)
  );

  if (distance > 800) {
    // Zoom out rất xa — chỉ render dot nhỏ, không label, không icon
    return new THREE.Mesh(
      new THREE.SphereGeometry(2),
      new THREE.MeshBasicMaterial({ color: node.color })
    );
  }

  if (distance > 400) {
    // Zoom out vừa — sphere với màu, không có texture/icon
    return new THREE.Mesh(
      new THREE.SphereGeometry(4),
      new THREE.MeshLambertMaterial({ color: node.color })
    );
  }

  // Zoom gần — render đầy đủ với icon và label
  return renderFullNode(node);
}
```

```javascript
// ✅ Kỹ thuật 7: Node Clustering — nhóm node lại khi quá nhiều
// Khi zoom out, thay vì render 1000 node riêng lẻ, gom thành ~50 cluster

function clusterNodes(nodes, zoomLevel) {
  // Chỉ cluster khi zoom out (zoomLevel nhỏ)
  if (zoomLevel > 0.5) return { nodes, links: [] }; // Zoom gần → show all

  // Gom node theo subnet/type (MODAT: gom theo network segment)
  const clusters = new Map();

  nodes.forEach(node => {
    const clusterKey = node.subnet || node.type; // Key để gom nhóm
    if (!clusters.has(clusterKey)) {
      clusters.set(clusterKey, {
        id: `cluster-${clusterKey}`,
        label: clusterKey,
        nodeCount: 0,
        children: [],
        color: getClusterColor(clusterKey),
      });
    }
    const cluster = clusters.get(clusterKey);
    cluster.nodeCount++;
    cluster.children.push(node.id);
  });

  return {
    nodes: Array.from(clusters.values()),
    // Links giữa cluster thay vì giữa individual nodes
    links: computeClusterLinks(nodes, clusters),
  };
}

// Sử dụng trong component
function GraphComponent({ rawData }) {
  const [zoomLevel, setZoomLevel] = useState(1);

  const graphData = useMemo(() => {
    const processed = transformNodes(rawData);

    // Cluster khi zoom out — giảm từ 5000 nodes xuống còn ~50 clusters
    if (zoomLevel < 0.3) {
      return clusterNodes(processed.nodes, zoomLevel);
    }

    return processed;
  }, [rawData, zoomLevel]);

  return (
    <ForceGraph3D
      graphData={graphData}
      onZoom={({ k }) => setZoomLevel(k)} // Track zoom level
      nodeThreeObject={renderNodeWithLOD}
    />
  );
}
```

### Lưu ý / Bẫy thường gặp

- **Canvas/WebGL tốt hơn DOM** cho large-scale rendering — chọn thư viện render bằng canvas ngay từ đầu (react-force-graph-3d dùng Three.js/WebGL)
- **Icon caching cực kỳ quan trọng** — `TextureLoader.load()` là async operation, gọi lại mỗi frame gây memory leak và lag
- **LOD cần calibrate threshold** theo dữ liệu thực tế — ngưỡng zoom distance phụ thuộc vào kích thước graph
- **Clustering làm mất detail** — cần UI cho phép user click vào cluster để drill down
- `cooldownTicks` quá thấp → simulation chưa ổn định, node vẫn dịch chuyển; quá cao → tốn CPU lúc đầu
- **`useMemo` dependency array** phải chính xác — thiếu dependency gây stale data; thừa dependency gây re-compute không cần thiết

---

## Tài Liệu Tham Khảo

- [React Force Graph Docs](https://github.com/vasturiano/react-force-graph)
- [Three.js Docs](https://threejs.org/docs/)
- [MDN - ResizeObserver](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver)
