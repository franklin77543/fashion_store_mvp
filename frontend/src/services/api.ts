// API 客戶端 (Axios)
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
});

// 商品 API
export const productApi = {
  // 商品列表 (分頁)
  async getList(params?: { page?: number; limit?: number }) {
    const res = await api.get("/products", { params });
    return res.data;
  },
  // 商品詳情
  async getDetail(id: number) {
    const res = await api.get(`/products/${id}`);
    return res.data;
  },
  // 商品搜尋
  async search(query: string) {
    const res = await api.get("/products/search", { params: { q: query } });
    return res.data;
  },
};

// 推薦 API
export const recommendApi = {
  async recommend(query: string, limit: number = 10) {
    const res = await api.post("/recommend", { query, limit });
    return res.data;
  },
};

export default api;