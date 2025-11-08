from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings

router = APIRouter()

@router.get("/nearby")
async def find_nearby_vets(lat: float, lng: float, radius: int = 5000):
    """Find nearby veterinarians using Google Places API"""
    
    if not settings.google_maps_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API key not configured"
        )
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "veterinary_care",
        "key": settings.google_maps_api_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch veterinarians"
            )
        
        data = response.json()
        
        # Transform results
        vets = []
        for place in data.get("results", []):
            vet = {
                "id": place.get("place_id"),
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating"),
                "location": place.get("geometry", {}).get("location"),
                "open_now": place.get("opening_hours", {}).get("open_now", False)
            }
            vets.append(vet)
        
        return {"vets": vets}

@router.get("/{place_id}/details")
async def get_vet_details(place_id: str):
    """Get detailed information about a specific vet"""
    
    if not settings.google_maps_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API key not configured"
        )
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,rating,opening_hours,website,photos",
        "key": settings.google_maps_api_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch vet details"
            )
        
        return response.json()
