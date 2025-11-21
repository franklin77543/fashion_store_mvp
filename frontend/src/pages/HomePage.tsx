import React, { useEffect } from "react";
import SearchInput from "../components/SearchInput";
import FilterPanel from "../components/FilterPanel";
import ProductList from "../components/ProductList";
import { useStore } from "../store";
import { productApi } from "../services/api";

const HomePage: React.FC = () => {
  const products = useStore((s) => s.products);
  const setProducts = useStore((s) => s.setProducts);
  const query = useStore((s) => s.query);
  const setLoading = useStore((s) => s.setLoading);
  const setError = useStore((s) => s.setError);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        let data;
        if (query) {
          data = await productApi.search(query);
        } else {
          data = await productApi.getList();
        }
        setProducts(data.products || data);
      } catch (err: any) {
        setError(err.message || "載入失敗");
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [query, setProducts, setLoading, setError]);

  return (
    <div className="max-w-5xl mx-auto p-4">
      <SearchInput />
      <FilterPanel />
      <ProductList products={products} />
    </div>
  );
};

export default HomePage;