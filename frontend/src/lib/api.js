const API_BASE_URL = 'http://localhost:8000/api';

// Pet endpoints
export const petAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/pets/`);
    if (!response.ok) throw new Error('Failed to fetch pets');
    return response.json();
  },
  
  getOne: async (id) => {
    const response = await fetch(`${API_BASE_URL}/pets/${id}`);
    if (!response.ok) throw new Error('Pet not found');
    return response.json();
  },
  
  create: async (data) => {
    const response = await fetch(`${API_BASE_URL}/pets/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to create pet');
    return response.json();
  },
  
  update: async (id, data) => {
    const response = await fetch(`${API_BASE_URL}/pets/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update pet');
    return response.json();
  },
  
  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/pets/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete pet');
    return response.json();
  },

  uploadImage: async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/pets/${id}/image`, {
      method: 'POST',
      body: formData
    });
    if (!response.ok) throw new Error('Failed to upload image');
    return response.json();
  }
};

// Video endpoints
export const videoAPI = {
  upload: async (petId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/videos/upload/${petId}`, {
      method: 'POST',
      body: formData
    });
    if (!response.ok) throw new Error('Failed to upload video');
    return response.json();
  },
  
  getAnalysis: async (videoId) => {
    const response = await fetch(`${API_BASE_URL}/videos/${videoId}`);
    if (!response.ok) throw new Error('Failed to get analysis');
    return response.json();
  },
  
  getPetVideos: async (petId) => {
    const response = await fetch(`${API_BASE_URL}/videos/pet/${petId}/videos`);
    if (!response.ok) throw new Error('Failed to fetch videos');
    return response.json();
  }
};

// Shop endpoints
export const shopAPI = {
  getProducts: async (category = null, species = null) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (species) params.append('species', species);
    
    const response = await fetch(
      `${API_BASE_URL}/shop/products?${params}`
    );
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  },
  
  getCategories: async () => {
    const response = await fetch(`${API_BASE_URL}/shop/categories`);
    if (!response.ok) throw new Error('Failed to fetch categories');
    return response.json();
  }
};

// Vet endpoints
export const vetAPI = {
  findNearby: async (lat, lng, radius = 5000) => {
    const response = await fetch(
      `${API_BASE_URL}/vets/nearby?lat=${lat}&lng=${lng}&radius=${radius}`
    );
    if (!response.ok) throw new Error('Failed to fetch vets');
    return response.json();
  },
  
  getDetails: async (placeId) => {
    const response = await fetch(`${API_BASE_URL}/vets/${placeId}/details`);
    if (!response.ok) throw new Error('Failed to fetch vet details');
    return response.json();
  }
};
