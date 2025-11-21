import React from "react";
import ProductDetail from "../components/ProductDetail";
import { useStore } from "../store";
import { useParams } from "react-router-dom";

const ProductDetailPage: React.FC = () => {
  const { id } = useParams();
  const product = useStore((s) => s.products.find((p) => String(p.id) === id));
  if (!product) return <div className="p-4">找不到商品</div>;
  return (
    <div className="max-w-3xl mx-auto p-4">
      <ProductDetail product={product} />
    </div>
  );
};

export default ProductDetailPage;