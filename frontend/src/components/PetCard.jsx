'use client';
import Link from 'next/link';
import { petAPI } from '@/lib/api';
import { Trash2 } from 'lucide-react';

export default function PetCard({ pet, onDelete }) {
  const handleDelete = async () => {
    if (window.confirm(`Delete ${pet.name}?`)) {
      try {
        await petAPI.delete(pet.id);
        onDelete?.(pet.id);
      } catch (err) {
        alert('Failed to delete pet: ' + err.message);
      }
    }
  };

  return (
    <Link href={`/pets/${pet.id}`}>
      <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition cursor-pointer overflow-hidden group relative">
        <div className="relative h-48 bg-gradient-to-br from-blue-400 to-purple-500">
          {pet.image ? (
            <img 
              src={pet.image} 
              alt={pet.name}
              className="w-full h-full object-cover group-hover:scale-110 transition duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white text-6xl font-bold">
              {pet.name?.[0] || '?'}
            </div>
          )}
        </div>
        
        <div className="p-6">
          <h3 className="text-xl font-bold mb-2">{pet.name}</h3>
          <p className="text-gray-600 mb-4">
            {pet.breed} • {pet.age || '?'} years old
          </p>
          
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-1">
              <div className={`w-3 h-3 rounded-full ${
                (pet.health_score || 90) > 80 ? 'bg-green-500' : 
                (pet.health_score || 90) > 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`} />
              <span className="text-gray-600">
                Health: {pet.health_score || 90}%
              </span>
            </div>
          </div>
        </div>

        <button
          onClick={(e) => {
            e.preventDefault();
            handleDelete();
          }}
          className="absolute top-3 right-3 bg-red-500 text-white p-2 rounded-lg hover:bg-red-600 transition opacity-0 group-hover:opacity-100"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </Link>
  );
}
