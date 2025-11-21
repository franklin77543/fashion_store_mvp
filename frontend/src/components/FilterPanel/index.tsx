import React from "react";

const FilterPanel: React.FC = () => {
  // 可根據 props 或 store 狀態顯示篩選選項
  return (
    <div className="p-4 border rounded mb-4">
      <div className="font-bold mb-2">篩選條件</div>
      {/* 篩選 UI 可擴充：類別、顏色、價格等 */}
      <div className="flex gap-2">
        <input type="checkbox" id="color-white" />
        <label htmlFor="color-white">白色</label>
        {/* ...更多篩選選項 */}
      </div>
    </div>
  );
};

export default FilterPanel;