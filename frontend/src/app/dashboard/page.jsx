'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Plus, Activity } from 'lucide-react';
import { petAPI } from '@/lib/api';
import PetCard from '@/components/PetCard';

export default function Dashboard() {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPets();
  }, []);

  const loadPets = async () => {
    try {
      setLoading(true);
      const data = await petAPI.getAll();
      setPets(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load pets:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePetDelete = (petId) => {
    setPets(pets.filter(p => p.id !== petId));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage all your pets in one place</p>
        </div>
        <Link href="/pets/new">
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Add New Pet
          </button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <p className="text-gray-500 text-sm font-medium">Total Pets</p>
          <p className="text-3xl font-bold mt-2">{pets.length}</p>
        </div>
        {/* Add more stats as needed */}
      </div>

      {/* Pets List */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-6">Your Pets</h2>
        
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Loading pets...</p>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : pets.length === 0 ? (
          <div className="bg-white p-12 rounded-xl shadow-md text-center">
            <Activity className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No pets added yet
            </h3>
            <p className="text-gray-500 mb-6">
              Add your first pet to start tracking their health
            </p>
            <Link href="/pets/new">
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
                Add Your First Pet
              </button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pets.map((pet) => (
              <PetCard 
                key={pet.id} 
                pet={pet}
                onDelete={handlePetDelete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
