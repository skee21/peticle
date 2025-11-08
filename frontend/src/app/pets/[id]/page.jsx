'use client';
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { usePetStore } from '@/lib/store';
import { petAPI } from '@/lib/api';
import { 
  Calendar, Scale, Heart, Activity, Edit2, 
  Video, ShoppingBag, MapPin, Clock, Loader 
} from 'lucide-react';
import VideoUploader from '@/components/VideoUploader';
import ShopSection from '@/components/ShopSection';
import VetLocator from '@/components/VetLocator';

export default function PetProfile() {
  const params = useParams();
  const { pets, selectPet, currentPet, setCurrentPet } = usePetStore();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPet = async () => {
      try {
        setLoading(true);
        // First try to find in store
        const petInStore = pets.find(p => p.id === params.id);
        if (petInStore) {
          selectPet(params.id);
        } else {
          // If not in store, fetch from API
          const petData = await petAPI.getOne(params.id);
          // Normalize the pet data to match expected format
          const normalizedPet = {
            id: petData.id || petData._id,
            name: petData.name,
            species: petData.species,
            breed: petData.breed,
            age: petData.age,
            weight: petData.weight,
            gender: petData.gender,
            dob: petData.dob,
            color: petData.color,
            description: petData.description,
            image: petData.image,
            healthScore: petData.health_score || petData.healthScore || 90,
            videosAnalyzed: petData.videos_analyzed || petData.videosAnalyzed || 0,
            appointments: petData.appointments || 0,
            createdAt: petData.created_at || petData.createdAt,
            status: 'active'
          };
          setCurrentPet(normalizedPet);
        }
      } catch (err) {
        console.error('Error fetching pet:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchPet();
    }
  }, [params.id, pets, selectPet, setCurrentPet]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
        <p className="text-xl text-gray-600">Loading pet...</p>
      </div>
    );
  }

  if (error || !currentPet) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <p className="text-xl text-gray-600">Pet not found</p>
        {error && <p className="text-sm text-gray-500 mt-2">{error}</p>}
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: <Activity className="w-4 h-4" /> },
    { id: 'health', label: 'Health Records', icon: <Heart className="w-4 h-4" /> },
    { id: 'videos', label: 'Video Analysis', icon: <Video className="w-4 h-4" /> },
    { id: 'shopping', label: 'Shopping', icon: <ShoppingBag className="w-4 h-4" /> },
    { id: 'vets', label: 'Find Vets', icon: <MapPin className="w-4 h-4" /> }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      {/* Profile Header */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
        <div className="relative h-48 bg-gradient-to-r from-blue-500 to-purple-600">
          {currentPet.coverImage && (
            <img 
              src={currentPet.coverImage} 
              alt="Cover"
              className="w-full h-full object-cover"
            />
          )}
        </div>

        <div className="relative px-8 pb-8">
          <div className="flex flex-col md:flex-row items-start md:items-end gap-6 -mt-20">
            <div className="relative">
              <img 
                src={currentPet.image || '/default-pet.png'} 
                alt={currentPet.name}
                className="w-40 h-40 rounded-full border-4 border-white object-cover shadow-xl"
              />
              <div className={`absolute bottom-2 right-2 w-6 h-6 rounded-full border-4 border-white ${
                currentPet.status === 'active' ? 'bg-green-500' : 'bg-gray-400'
              }`} />
            </div>

            <div className="flex-1">
              <div className="flex items-start justify-between">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900">{currentPet.name}</h1>
                  <p className="text-lg text-gray-600 mt-1">
                    {currentPet.breed} • {currentPet.species}
                  </p>
                </div>
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2">
                  <Edit2 className="w-4 h-4" />
                  Edit Profile
                </button>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <Calendar className="w-5 h-5 text-blue-600 mb-2" />
                  <p className="text-sm text-gray-600">Age</p>
                  <p className="text-xl font-bold">{currentPet.age ? `${currentPet.age} years` : 'Not specified'}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <Scale className="w-5 h-5 text-green-600 mb-2" />
                  <p className="text-sm text-gray-600">Weight</p>
                  <p className="text-xl font-bold">{currentPet.weight ? `${currentPet.weight} kg` : 'Not specified'}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <Heart className="w-5 h-5 text-red-600 mb-2" />
                  <p className="text-sm text-gray-600">Health Score</p>
                  <p className="text-xl font-bold">{currentPet.healthScore || 90}%</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <Clock className="w-5 h-5 text-purple-600 mb-2" />
                  <p className="text-sm text-gray-600">Member Since</p>
                  <p className="text-xl font-bold">
                    {new Date(currentPet.createdAt || Date.now()).getFullYear()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <div className="flex overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-4 font-semibold whitespace-nowrap transition ${
                  activeTab === tab.id
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-8">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-bold mb-3">About {currentPet.name}</h3>
                <p className="text-gray-700 leading-relaxed">
                  {currentPet.description || `${currentPet.name} is a lovely ${currentPet.breed} who loves to play and explore.`}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="font-semibold mb-4">Basic Information</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Date of Birth</span>
                      <span className="font-semibold">{currentPet.dob || 'Not specified'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Gender</span>
                      <span className="font-semibold">{currentPet.gender || 'Not specified'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Color</span>
                      <span className="font-semibold">{currentPet.color || 'Not specified'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Microchip ID</span>
                      <span className="font-semibold">{currentPet.microchipId || 'Not registered'}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="font-semibold mb-4">Recent Activity</h4>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                      <span className="text-sm">Last checkup: 2 weeks ago</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full" />
                      <span className="text-sm">Video analyzed: 5 days ago</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-purple-500 rounded-full" />
                      <span className="text-sm">Weight updated: 1 week ago</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Health Records Tab */}
          {activeTab === 'health' && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold">Health Records</h3>
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <p className="text-yellow-800">
                  <strong>Note:</strong> Health records feature will be connected to backend
                </p>
              </div>
            </div>
          )}

          {/* Video Analysis Tab */}
          {activeTab === 'videos' && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold">AI Video Analysis</h3>
              <VideoUploader 
                onUpload={async (file) => {
                  console.log('Uploading video:', file);
                  // Backend integration here
                }}
              />
            </div>
          )}

          {/* Shopping Tab */}
          {activeTab === 'shopping' && (
            <ShopSection petType={currentPet.species} />
          )}

          {/* Vets Tab */}
          {activeTab === 'vets' && (
            <VetLocator />
          )}
        </div>
      </div>
    </div>
  );
}
