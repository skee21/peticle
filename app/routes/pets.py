from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
from app.database import get_database
from app.schemas.pet import PetCreate, PetUpdate, PetResponse  # ADD THIS LINE
from app.services.storage import save_image
from bson import ObjectId
import os

router = APIRouter()

@router.post("/", response_model=dict)
def create_pet(pet: PetCreate, db=Depends(get_database)):
    """Create a new pet profile"""
    pet_dict = pet.dict()
    pet_dict["videos_analyzed"] = 0
    pet_dict["appointments"] = 0
    pet_dict["health_score"] = 90
    
    result = db.pets.insert_one(pet_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Pet created successfully"
    }

@router.get("/", response_model=List[dict])
def get_all_pets(db=Depends(get_database)):
    """Get all pets"""
    pets = []
    for pet in db.pets.find():
        pet["id"] = str(pet.pop("_id"))
        pets.append(pet)
    return pets

@router.get("/{pet_id}", response_model=dict)
def get_pet(pet_id: str, db=Depends(get_database)):
    """Get a specific pet by ID"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    pet = db.pets.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    pet["id"] = str(pet.pop("_id"))
    return pet

@router.put("/{pet_id}", response_model=dict)
def update_pet(
    pet_id: str,
    pet_update: PetUpdate,
    db=Depends(get_database)
):
    """Update pet information"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    update_data = {k: v for k, v in pet_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = db.pets.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return {"message": "Pet updated successfully"}

@router.delete("/{pet_id}")
def delete_pet(pet_id: str, db=Depends(get_database)):
    """Delete a pet"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    result = db.pets.delete_one({"_id": ObjectId(pet_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return {"message": "Pet deleted successfully"}

@router.post("/{pet_id}/image")
async def upload_pet_image(
    pet_id: str,
    file: UploadFile = File(...),
    db=Depends(get_database)
):
    """Upload pet profile image"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save image
    image_path = await save_image(file, "images")
    
    # Update pet record
    db.pets.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": {"image": image_path}}
    )
    
    return {
        "message": "Image uploaded successfully",
        "image_path": image_path
    }
