'use client';
import { useState } from 'react';
import { ShoppingCart, Search, Filter, Star } from 'lucide-react';

export default function ShopPage() {
  const [category, setCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = ['All', 'Food', 'Toys', 'Accessories', 'Health', 'Grooming'];
  
  const products = [
    {
      id: 1,
      name: 'Premium Dog Food',
      price: 2499,
      rating: 4.5,
      image: '/products/dog-food.jpg',
      category: 'Food',
      inStock: true
    },
    {
      id: 2,
      name: 'Interactive Ball Toy',
      price: 799,
      rating: 4.8,
      image: '/products/toy.jpg',
      category: 'Toys',
      inStock: true
    },
    {
      id: 3,
      name: 'Pet Grooming Kit',
      price: 1499,
      rating: 4.3,
      image: '/products/grooming.jpg',
      category: 'Grooming',
      inStock: true
    },
    {
      id: 4,
      name: 'Orthopedic Pet Bed',
      price: 3499,
      rating: 4.7,
      image: '/products/bed.jpg',
      category: 'Accessories',
      inStock: true
    },
    {
      id: 5,
      name: 'Multivitamin Supplements',
      price: 899,
      rating: 4.6,
      image: '/products/vitamins.jpg',
      category: 'Health',
      inStock: true
    },
    {
      id: 6,
      name: 'Cat Scratching Post',
      price: 1899,
      rating: 4.4,
      image: '/products/scratch.jpg',
      category: 'Accessories',
      inStock: false
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Pet Shop</h1>
        <p className="text-gray-600">Everything your pet needs, delivered to your door</p>
      </div>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="bg-gray-100 px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition flex items-center gap-2">
            <Filter className="w-5 h-5" />
            Filters
          </button>
        </div>

        {/* Categories */}
        <div className="flex gap-3 mt-6 overflow-x-auto pb-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat.toLowerCase())}
              className={`px-6 py-2 rounded-full font-semibold whitespace-nowrap transition ${
                category === cat.toLowerCase()
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <div key={product.id} className="bg-white rounded-xl shadow-md hover:shadow-xl transition overflow-hidden group">
            <div className="relative h-48 bg-gray-200 overflow-hidden">
              <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center text-gray-500">
                <ShoppingCart className="w-16 h-16" />
              </div>
              {!product.inStock && (
                <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <span className="bg-red-500 text-white px-4 py-2 rounded-lg font-semibold">
                    Out of Stock
                  </span>
                </div>
              )}
            </div>

            <div className="p-4">
              <h3 className="font-semibold text-lg mb-2 line-clamp-2">
                {product.name}
              </h3>
              
              <div className="flex items-center gap-2 mb-3">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-4 h-4 ${
                        i < Math.floor(product.rating)
                          ? 'text-yellow-400 fill-yellow-400'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600">({product.rating})</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-blue-600">
                  ₹{product.price}
                </span>
                <button
                  disabled={!product.inStock}
                  className={`px-4 py-2 rounded-lg font-semibold transition ${
                    product.inStock
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
