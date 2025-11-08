from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
from app.database import get_database
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.services.storage import save_image
import os

router = APIRouter()

@router.post("", response_model=dict)
async def create_pet(pet: PetCreate, db=Depends(get_database)):
    """Create a new pet profile"""
    print(f"POST /api/pets - Received request to create pet: {pet.name}")
    try:
        # Use model_dump() for Pydantic v2, fallback to dict() for v1
        if hasattr(pet, 'model_dump'):
            pet_dict = pet.model_dump()
        else:
            pet_dict = pet.dict()
        
        print(f"Pet dict created: {list(pet_dict.keys())}")
        
        pet_dict["videos_analyzed"] = 0
        pet_dict["appointments"] = 0
        pet_dict["health_score"] = 90
        
        print("Calling insert_one...")
        result = await db.pets.insert_one(pet_dict)
        print(f"Insert result: {result}")
        
        return {
            "id": str(result["inserted_id"]),
            "message": "Pet created successfully"
        }
    except Exception as e:
        import traceback
        print(f"Error creating pet: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create pet: {str(e)}")

@router.get("", response_model=List[dict])
async def get_all_pets(db=Depends(get_database)):
    """Get all pets"""
    pets_data = await db.pets.find()
    pets = []
    for pet in pets_data:
        pet["id"] = str(pet.pop("_id"))
        pets.append(pet)
    return pets

@router.get("/{pet_id}", response_model=dict)
async def get_pet(pet_id: str, db=Depends(get_database)):
    """Get a specific pet by ID"""
    pet = await db.pets.find_one({"_id": pet_id})
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    pet["id"] = str(pet.pop("_id"))
    return pet

@router.put("/{pet_id}", response_model=dict)
async def update_pet(
    pet_id: str,
    pet_update: PetUpdate,
    db=Depends(get_database)
):
    """Update pet information"""
    try:
        # Use model_dump() for Pydantic v2, fallback to dict() for v1
        if hasattr(pet_update, 'model_dump'):
            update_dict = pet_update.model_dump(exclude_unset=True)
        else:
            update_dict = pet_update.dict(exclude_unset=True)
        
        update_data = {k: v for k, v in update_dict.items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.pets.update_one(
            {"_id": pet_id},
            {"$set": update_data}
        )
        
        if result["matched_count"] == 0:
            raise HTTPException(status_code=404, detail="Pet not found")
        
        return {"message": "Pet updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error updating pet: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update pet: {str(e)}")

@router.delete("/{pet_id}")
async def delete_pet(pet_id: str, db=Depends(get_database)):
    """Delete a pet"""
    result = await db.pets.delete_one({"_id": pet_id})
    
    if result["deleted_count"] == 0:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return {"message": "Pet deleted successfully"}

@router.post("/{pet_id}/image")
async def upload_pet_image(
    pet_id: str,
    file: UploadFile = File(...),
    db=Depends(get_database)
):
    """Upload pet profile image"""
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save image
    image_path = await save_image(file, "images")
    
    # Update pet record
    await db.pets.update_one(
        {"_id": pet_id},
        {"$set": {"image": image_path}}
    )
    
    return {
        "message": "Image uploaded successfully",
        "image_path": image_path
    }
