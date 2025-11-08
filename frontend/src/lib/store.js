import { create } from 'zustand';
import { petAPI } from './api';

export const usePetStore = create((set, get) => ({
  pets: [],
  currentPet: null,
  addPet: (pet) => set((state) => ({ pets: [...state.pets, pet] })),
  selectPet: (petId) => set((state) => ({ 
    currentPet: state.pets.find(p => p.id === petId) 
  })),
  setCurrentPet: (pet) => set({ currentPet: pet }),
  loadPets: async () => {
    try {
      const data = await petAPI.getAll();
      const normalizedPets = Array.isArray(data) ? data.map(pet => ({
        id: pet.id || pet._id,
        name: pet.name,
        species: pet.species,
        breed: pet.breed,
        age: pet.age,
        weight: pet.weight,
        gender: pet.gender,
        dob: pet.dob,
        color: pet.color,
        description: pet.description,
        image: pet.image,
        healthScore: pet.health_score || pet.healthScore || 90,
        videosAnalyzed: pet.videos_analyzed || pet.videosAnalyzed || 0,
        appointments: pet.appointments || 0,
        createdAt: pet.created_at || pet.createdAt,
        status: 'active'
      })) : [];
      set({ pets: normalizedPets });
    } catch (error) {
      console.error('Failed to load pets:', error);
    }
  },
}));
