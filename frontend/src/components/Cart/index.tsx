import React from "react";
import { useStore } from "../../store";

const Cart: React.FC = () => {
  const cart = useStore((s) => s.cart);
  const removeFromCart = useStore((s) => s.removeFromCart);
  const clearCart = useStore((s) => s.clearCart);

  return (
    <div className="p-4 border rounded">
      <div className="font-bold mb-2">購物車</div>
      {cart.length === 0 ? (
        <div className="text-gray-500">購物車為空</div>
      ) : (
        <ul>
          {cart.map((item) => (
            <li key={item.product.id} className="flex justify-between items-center mb-2">
              <span>{item.product.name} x {item.quantity}</span>
              <button className="text-red-500" onClick={() => removeFromCart(item.product.id)}>
                移除
              </button>
            </li>
          ))}
        </ul>
      )}
      {cart.length > 0 && (
        <button className="bg-gray-300 px-3 py-1 rounded mt-2" onClick={clearCart}>
          清空購物車
        </button>
      )}
    </div>
  );
};

export default Cart;