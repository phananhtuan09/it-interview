# Tối Ưu Performance AG Grid với Large Dataset

## Thông Tin File

- **Chủ đề:** AG Grid Performance Optimization
- **Ngôn ngữ / Framework:** React / AG Grid
- **Mức độ:** Trung cấp / Nâng cao
- **Cập nhật lần cuối:** 2026-03-11

---

## Câu Hỏi 1: Tối ưu AG Grid khi có hàng nghìn rows

**Mức độ:** Trung cấp / Nâng cao

### Câu hỏi

Bạn đã tối ưu performance của AG Grid như thế nào khi bảng có rất nhiều dữ liệu? (scroll mượt, filter/sort nhanh, tránh re-render grid)

### Câu trả lời ngắn gọn

Dùng row virtualization của AG Grid để chỉ render DOM trong viewport. Debounce search/filter để giảm số lần tính toán. Không lưu data trong React state — dùng AG Grid API để update data trực tiếp. Lưu data dạng object map (`{ [id]: row }`) thay vì array để tìm kiếm O(1) thay vì O(n). Dùng `useMemo`/`useCallback`/`React.memo` để tránh re-render component wrapper.

### Giải thích chi tiết

**Nguyên nhân AG Grid bị chậm:**
1. React state chứa grid data → mỗi update trigger React re-render toàn grid
2. Filter/search không debounce → tính toán liên tục khi user typing
3. Tìm kiếm row trong array O(n) khi cần update/select single row
4. Render quá nhiều DOM element khi không dùng virtualization
5. Cell renderer là React component nặng → render hàng nghìn component

**Các kỹ thuật đã áp dụng:**

1. **Row Virtualization** — AG Grid built-in, chỉ render rows trong viewport
2. **Debounce filter** — delay 300ms trước khi apply filter
3. **AG Grid API thay vì React state** — `gridRef.current.api.setRowData()` nhanh hơn setState
4. **Object map thay vì array** — lookup O(1) vs O(n)
5. **Memoization** — useMemo, useCallback, React.memo cho wrapper components

### Ví dụ minh họa

```javascript
import { useRef, useMemo, useCallback, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { debounce } from 'lodash';

// ✅ Lưu data dạng object map — O(1) lookup thay vì O(n) array.find()
function useGridData(rawData) {
  // { "row-id-1": { id: "row-id-1", name: "...", ... }, "row-id-2": {...} }
  const dataMap = useMemo(() => {
    return rawData.reduce((acc, row) => {
      acc[row.id] = row;
      return acc;
    }, {});
  }, [rawData]);

  // Convert sang array chỉ khi cần truyền vào Grid
  const rowData = useMemo(() => Object.values(dataMap), [dataMap]);

  // ✅ Cập nhật 1 row: O(1)
  const updateRow = useCallback((id, changes) => {
    dataMap[id] = { ...dataMap[id], ...changes };
    // Không setState toàn bộ array — cập nhật qua AG Grid API
  }, [dataMap]);

  return { rowData, dataMap, updateRow };
}
```

```javascript
function DataGrid({ rawData }) {
  const gridRef = useRef(null);
  const { rowData, dataMap } = useGridData(rawData);

  // ✅ Debounce filter — không filter liên tục khi user typing
  const onFilterChanged = useCallback(
    debounce((filterText) => {
      if (!gridRef.current?.api) return;

      // Dùng AG Grid API thay vì filter trong React state
      gridRef.current.api.setQuickFilter(filterText);
    }, 300),
    []
  );

  // ✅ Update single row qua AG Grid API — không trigger React re-render
  const updateSingleRow = useCallback((id, changes) => {
    if (!gridRef.current?.api) return;

    // Tìm row node qua AG Grid API — O(1)
    const rowNode = gridRef.current.api.getRowNode(id);
    if (rowNode) {
      rowNode.setData({ ...rowNode.data, ...changes });
      // Chỉ refresh row đó, không re-render toàn grid
      gridRef.current.api.refreshCells({ rowNodes: [rowNode] });
    }
  }, []);

  // ✅ Column definitions dùng useMemo — không tạo mới mỗi render
  const columnDefs = useMemo(() => [
    {
      field: 'name',
      sortable: true,
      filter: true,
      // Không dùng cellRendererFramework với React component nặng
      // Dùng cellRenderer function đơn giản thay thế
      cellRenderer: (params) => `<span>${params.value}</span>`,
    },
    { field: 'status', sortable: true },
    { field: 'quantity', type: 'numericColumn', sortable: true },
  ], []);

  // ✅ Default column config
  const defaultColDef = useMemo(() => ({
    resizable: true,
    sortable: true,
    filter: true,
  }), []);

  return (
    <div>
      <input
        placeholder="Tìm kiếm..."
        onChange={(e) => onFilterChanged(e.target.value)}
      />
      <div style={{ height: '600px' }} className="ag-theme-alpine">
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          // ✅ Row virtualization — AG Grid built-in, chỉ render rows trong viewport
          rowBuffer={10}
          // ✅ getRowId — AG Grid dùng để identify row cho delta updates
          getRowId={(params) => params.data.id}
          // ✅ Tắt animation nếu không cần — giảm overhead
          animateRows={false}
          // ✅ Server-side pagination nếu data quá lớn
          // pagination={true}
          // paginationPageSize={100}
        />
      </div>
    </div>
  );
}
```

```javascript
// ✅ Server-side row model — load data theo trang từ server
// Dùng khi có > 100,000 rows, không thể load toàn bộ về client

const ServerSideGrid = () => {
  const datasource = useMemo(() => ({
    getRows: async (params) => {
      const { startRow, endRow, sortModel, filterModel } = params.request;

      try {
        const response = await fetch('/api/grid-data', {
          method: 'POST',
          body: JSON.stringify({ startRow, endRow, sortModel, filterModel }),
        });
        const { rows, lastRow } = await response.json();

        params.success({ rowData: rows, rowCount: lastRow });
      } catch (error) {
        params.fail();
      }
    },
  }), []);

  return (
    <AgGridReact
      rowModelType="serverSide"
      serverSideDatasource={datasource}
      cacheBlockSize={100}
    />
  );
};
```

### Lưu ý / Bẫy thường gặp

- **Không lưu grid data trong React useState** — mỗi setState gây React re-render, AG Grid sẽ re-render theo
- Dùng **`getRowId`** để AG Grid track row identity — cần thiết cho delta update và animation
- **Object map** cho data lookup nhanh, nhưng cần convert sang array khi truyền vào `rowData` prop
- `React.memo` và `useCallback` quan trọng cho **cell renderer** nếu dùng React component
- **Column virtualization** mặc định bật — tắt `suppressColumnVirtualisation` nếu cần export
- Với > 100k rows, dùng **Server-Side Row Model** thay vì load toàn bộ về client

---

## Tài Liệu Tham Khảo

- [AG Grid - Row Virtualization](https://www.ag-grid.com/react-data-grid/dom-virtualisation/)
- [AG Grid - Server-Side Row Model](https://www.ag-grid.com/react-data-grid/server-side-model/)
- [AG Grid - Performance](https://www.ag-grid.com/react-data-grid/performance/)
