import React from "react";
import ProductDetail from "../components/ProductDetail";
import { useStore } from "../store";

// 實際專案可用 React Router 取得 id 並 fetch 詳細資料
const ProductDetailPage: React.FC = () => {
  // 這裡僅示範，假設 store.products[0] 為展示商品
  const product = useStore((s) => s.products[0]);
  if (!product) return <div className="p-4">找不到商品</div>;
  return (
    <div className="max-w-3xl mx-auto p-4">
      <ProductDetail product={product} />
    </div>
  );
};

export default ProductDetailPage;