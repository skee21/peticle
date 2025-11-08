'use client';
import { useEffect, useRef } from 'react';
import { Loader } from '@googlemaps/js-api-loader';

export default function VetLocator() {
  const mapRef = useRef(null);

  useEffect(() => {
    const loader = new Loader({
      apiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API,
      version: 'weekly',
    });

    loader.load().then(() => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          const map = new google.maps.Map(mapRef.current, {
            center: { 
              lat: position.coords.latitude, 
              lng: position.coords.longitude 
            },
            zoom: 13,
          });

          // Search nearby vets
          const service = new google.maps.places.PlacesService(map);
          service.nearbySearch({
            location: map.getCenter(),
            radius: 5000,
            type: 'veterinary_care'
          }, (results, status) => {
            if (status === 'OK') {
              results.forEach(place => {
                new google.maps.Marker({
                  position: place.geometry.location,
                  map: map,
                  title: place.name
                });
              });
            }
          });
        });
      }
    });
  }, []);

  return (
    <div>
      <div ref={mapRef} className="w-full h-96 rounded-lg" />
      <div className="mt-4">
        {/* Vet list with "Open in Maps" buttons */}
      </div>
    </div>
  );
}
