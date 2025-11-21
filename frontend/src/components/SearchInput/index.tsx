import React, { useState } from "react";
import { useStore } from "../../store";

const SearchInput: React.FC = () => {
  const query = useStore((s) => s.query);
  const setQuery = useStore((s) => s.setQuery);
  const [input, setInput] = useState(query);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSearch = () => {
    setQuery(input);
    // 可在此觸發 API 搜尋
  };

  return (
    <div className="w-full flex gap-2">
      <input
        type="text"
        className="border rounded px-3 py-2 w-full"
        placeholder="請輸入商品或自然語言..."
        value={input}
        onChange={handleChange}
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSearch}>
        搜尋
      </button>
    </div>
  );
};

export default SearchInput;