'use client';
import { useState } from 'react';
import { Camera, Calendar, Weight } from 'lucide-react';

export default function PetProfile({ pet, onUpdate }) {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        {/* Header */}
        <div className="flex items-start gap-6 mb-6">
          <img src={pet.image} alt={pet.name} 
               className="w-32 h-32 rounded-full object-cover" />
          <div className="flex-1">
            <h1 className="text-3xl font-bold">{pet.name}</h1>
            <p className="text-gray-600">{pet.breed} • {pet.age} years old</p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <Weight className="text-blue-600 mb-2" />
            <p className="text-sm text-gray-600">Weight</p>
            <p className="text-xl font-semibold">{pet.weight} kg</p>
          </div>
          {/* Add more stats */}
        </div>

        {/* Tabs: Health, Shopping, Vets */}
        <Tabs pet={pet} />
      </div>
    </div>
  );
}
