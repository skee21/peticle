'use client';
import Link from 'next/link';
import { Video, Heart, ShoppingBag, MapPin, ArrowRight, Sparkles } from 'lucide-react';

export default function Home() {
  const features = [
    {
      icon: <Video className="w-8 h-8" />,
      title: 'AI Video Analysis',
      description: 'Upload videos to detect behavior patterns and early illness signs',
      color: 'bg-blue-500'
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: 'Pet Profiles',
      description: 'Comprehensive health records and personality tracking',
      color: 'bg-red-500'
    },
    {
      icon: <ShoppingBag className="w-8 h-8" />,
      title: 'Smart Shopping',
      description: 'Personalized recommendations for food, toys, and accessories',
      color: 'bg-green-500'
    },
    {
      icon: <MapPin className="w-8 h-8" />,
      title: 'Find Vets Nearby',
      description: 'Locate trusted veterinarians with ratings and directions',
      color: 'bg-purple-500'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 py-24 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-6">
              <Sparkles className="w-12 h-12 animate-pulse" />
            </div>
            <h1 className="text-5xl md:text-6xl font-extrabold mb-6">
              Understand Your Pet Like Never Before
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
              AI-powered video analysis to detect health issues, track behavior, 
              and provide everything your pet needs in one place
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/dashboard">
                <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition flex items-center justify-center gap-2">
                  Get Started Free
                  <ArrowRight className="w-5 h-5" />
                </button>
              </Link>
              <Link href="/analysis">
                <button className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white/10 transition">
                  Try AI Analysis
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 py-20 sm:px-6 lg:px-8">
        <h2 className="text-4xl font-bold text-center mb-4">
          Everything Your Pet Needs
        </h2>
        <p className="text-gray-600 text-center mb-12 text-lg">
          A comprehensive platform for modern pet care
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, idx) => (
            <div key={idx} 
                 className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition cursor-pointer group">
              <div className={`${feature.color} w-16 h-16 rounded-lg flex items-center justify-center text-white mb-4 group-hover:scale-110 transition`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gray-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-16">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="bg-blue-500 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-bold mb-3">Create Pet Profile</h3>
              <p className="text-gray-600">
                Add your pet's details, photos, and medical history
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-500 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-bold mb-3">Upload Videos</h3>
              <p className="text-gray-600">
                Our AI analyzes behavior and detects potential health concerns
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-500 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-bold mb-3">Get Insights & Care</h3>
              <p className="text-gray-600">
                Receive recommendations, shop, and find vets easily
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Transform Pet Care?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of pet owners using AI to keep their pets healthy
          </p>
          <Link href="/dashboard">
            <button className="bg-white text-blue-600 px-10 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition">
              Start Now - It's Free
            </button>
          </Link>
        </div>
      </section>
    </div>
  );
}
