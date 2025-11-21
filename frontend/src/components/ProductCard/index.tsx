import React from "react";
import type { Product } from "../../types";

interface Props {
  product: Product;
  onClick?: () => void;
}

const ProductCard: React.FC<Props> = ({ product, onClick }) => {
  return (
    <div className="border rounded shadow p-4 cursor-pointer" onClick={onClick}>
      <div className="h-40 bg-gray-100 mb-2 flex items-center justify-center overflow-hidden">
        {true ? (
          <img
            src={`${import.meta.env.VITE_API_BASE_URL?.replace(/\/$/,"") || "http://localhost:8000"}/images/${product.id}.jpg`}
            alt={product.product_display_name}
            className="object-cover h-full w-full"
          />
        ) : (
          <span className="text-gray-400">圖片</span>
        )}
      </div>
      <div className="font-bold text-lg mb-1">{product.product_display_name}</div>
      <div className="text-blue-600 font-semibold">${product.price}</div>
      {/* 可加標籤等 */}
    </div>
  );
};

export default ProductCard;