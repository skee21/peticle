'use client';
import VetLocator from '@/components/VetLocator';
import { MapPin, Phone, Clock, Star, ExternalLink } from 'lucide-react';

export default function VetsPage() {
  // Sample vet data - will be replaced with Google Places API results
  const sampleVets = [
    {
      id: 1,
      name: 'City Animal Hospital',
      address: '123 Main Street, Mumbai',
      phone: '+91 98765 43210',
      rating: 4.7,
      distance: '1.2 km',
      open: true,
      hours: 'Open until 8:00 PM'
    },
    {
      id: 2,
      name: 'Pet Care Clinic',
      address: '456 Park Avenue, Mumbai',
      phone: '+91 98765 43211',
      rating: 4.5,
      distance: '2.5 km',
      open: true,
      hours: 'Open 24 hours'
    },
    {
      id: 3,
      name: 'Veterinary Wellness Center',
      address: '789 Lake Road, Mumbai',
      phone: '+91 98765 43212',
      rating: 4.8,
      distance: '3.1 km',
      open: false,
      hours: 'Opens tomorrow at 9:00 AM'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Find Veterinarians Nearby</h1>
        <p className="text-gray-600">Locate trusted vets with ratings, hours, and directions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Map Section */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <VetLocator />
        </div>

        {/* Vet List Section */}
        <div className="space-y-4">
          {sampleVets.map((vet) => (
            <div key={vet.id} className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold mb-2">{vet.name}</h3>
                  <div className="flex items-center gap-2 text-yellow-500 mb-2">
                    <Star className="w-5 h-5 fill-yellow-500" />
                    <span className="font-semibold">{vet.rating}</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-gray-600">{vet.distance} away</span>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  vet.open 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-red-100 text-red-700'
                }`}>
                  {vet.open ? 'Open' : 'Closed'}
                </div>
              </div>

              <div className="space-y-3 mb-4">
                <div className="flex items-start gap-3 text-gray-700">
                  <MapPin className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <span>{vet.address}</span>
                </div>
                <div className="flex items-center gap-3 text-gray-700">
                  <Phone className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span>{vet.phone}</span>
                </div>
                <div className="flex items-center gap-3 text-gray-700">
                  <Clock className="w-5 h-5 text-purple-600 flex-shrink-0" />
                  <span>{vet.hours}</span>
                </div>
              </div>

              <div className="flex gap-3">
                <a 
                  href={`tel:${vet.phone}`}
                  className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition text-center"
                >
                  Call Now
                </a>
                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(vet.address)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 bg-gray-100 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-200 transition text-center flex items-center justify-center gap-2"
                >
                  Directions
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
