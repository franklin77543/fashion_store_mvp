import React from "react";
import type { Product } from "../../types";
import ProductCard from "../ProductCard";

interface Props {
  products: Product[];
  onProductClick?: (product: Product) => void;
}

const ProductList: React.FC<Props> = ({ products, onProductClick }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} onClick={() => onProductClick?.(product)} />
      ))}
    </div>
  );
};

export default ProductList;