import React from "react";
import type { Product } from "../../types";

interface Props {
  product: Product;
}

const ProductDetail: React.FC<Props> = ({ product }) => {
  return (
    <div className="p-4">
      <div className="h-60 bg-gray-100 mb-4 flex items-center justify-center overflow-hidden">
        {product.image ? (
          <img
            src={`${import.meta.env.VITE_API_BASE_URL?.replace(/\/$/,"") || "http://localhost:8000/api/v1"}/../images/${product.image}`}
            alt={product.product_display_name}
            className="object-cover h-full w-full"
          />
        ) : (
          <span className="text-gray-400">圖片</span>
        )}
      </div>
      <div className="font-bold text-2xl mb-2">{product.product_display_name}</div>
      <div className="text-blue-600 font-semibold text-xl mb-2">${product.price}</div>
      {/* 其他商品資訊顯示 */}
      <div className="text-gray-700">商品詳細資訊...</div>
    </div>
  );
};

export default ProductDetail;