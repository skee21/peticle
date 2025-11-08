import { create } from 'zustand';
import { petAPI } from './api';

export const usePetStore = create((set, get) => ({
  pets: [],
  currentPet: null,
  loading: false,
  
  loadPets: async () => {
    set({ loading: true });
    try {
      const pets = await petAPI.getAll();
      set({ pets, loading: false });
      return pets;
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },
  
  addPet: (pet) => set((state) => ({ pets: [...state.pets, pet] })),
  
  selectPet: async (petId) => {
    const state = get();
    // First check local state
    let pet = state.pets.find(p => p.id === petId);
    
    // If not found, try to fetch from API
    if (!pet) {
      try {
        pet = await petAPI.getOne(petId);
      } catch (error) {
        console.error('Failed to fetch pet:', error);
        set({ currentPet: null });
        return;
      }
    }
    
    set({ currentPet: pet });
  },
}));
