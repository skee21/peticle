import { create } from 'zustand';

export const usePetStore = create((set) => ({
  pets: [],
  currentPet: null,
  addPet: (pet) => set((state) => ({ pets: [...state.pets, pet] })),
  selectPet: (petId) => set((state) => ({ 
    currentPet: state.pets.find(p => p.id === petId) 
  })),
}));
