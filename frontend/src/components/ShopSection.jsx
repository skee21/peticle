'use client';
import { ShoppingCart } from 'lucide-react';

export default function ShopSection({ petType }) {
  const categories = ['Food', 'Toys', 'Accessories', 'Health'];
  
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Shop for {petType}</h2>
      
      <div className="flex gap-3 mb-6">
        {categories.map(cat => (
          <button key={cat} 
                  className="px-4 py-2 rounded-full bg-gray-100 hover:bg-blue-500 hover:text-white">
            {cat}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Product cards */}
      </div>
    </div>
  );
}
