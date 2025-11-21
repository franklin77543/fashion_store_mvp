// Zustand store 入口
import { create } from "zustand";
import type { Product } from "../types";

export interface CartItem {
  product: Product;
  quantity: number;
}

interface StoreState {
  products: Product[];
  query: string;
  cart: CartItem[];
  loading: boolean;
  error: string | null;
  setProducts: (products: Product[]) => void;
  setQuery: (query: string) => void;
  addToCart: (product: Product, quantity?: number) => void;
  removeFromCart: (productId: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearCart: () => void;
}

export const useStore = create<StoreState>((set, get) => ({
  products: [],
  query: "",
  cart: [],
  loading: false,
  error: null,
  setProducts: (products) => set({ products }),
  setQuery: (query) => set({ query }),
  addToCart: (product, quantity = 1) => {
    const cart = get().cart;
    const idx = cart.findIndex((item) => item.product.id === product.id);
    if (idx >= 0) {
      // 更新數量
      const updated = [...cart];
      updated[idx].quantity += quantity;
      set({ cart: updated });
    } else {
      set({ cart: [...cart, { product, quantity }] });
    }
  },
  removeFromCart: (productId) => {
    set({ cart: get().cart.filter((item) => item.product.id !== productId) });
  },
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearCart: () => set({ cart: [] }),
}));