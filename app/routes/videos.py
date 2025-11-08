from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Depends
from typing import List
from app.database import get_database
from app.schemas.video import VideoAnalysisResponse, VideoUploadResponse
from app.services.video_processor import process_video
from app.services.ai_analysis import analyze_video
from app.services.storage import save_video
from bson import ObjectId
import os

router = APIRouter()

@router.post("/upload/{pet_id}")
async def upload_video(
    pet_id: str,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db=Depends(get_database)
):
    """Upload video for AI analysis"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    # Check if pet exists
    pet = await db.pets.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Validate file type
    if file.content_type not in ["video/mp4", "video/avi", "video/mov"]:
        raise HTTPException(status_code=400, detail="Invalid video format")
    
    # Save video
    video_path = await save_video(file)
    
    # Create video record
    video_record = {
        "pet_id": pet_id,
        "video_path": video_path,
        "file_size": file.size,
        "analysis_status": "pending",
        "insights": [],
        "recommendations": []
    }
    
    result = await db.videos.insert_one(video_record)
    video_id = str(result.inserted_id)
    
    # Add background task for video analysis
    if background_tasks:
        background_tasks.add_task(
            analyze_video_background,
            video_id,
            video_path,
            pet_id,
            db
        )
    
    return {
        "video_id": video_id,
        "message": "Video uploaded successfully. Analysis in progress.",
        "status": "processing"
    }

async def analyze_video_background(video_id: str, video_path: str, pet_id: str, db):
    """Background task to analyze video"""
    try:
        # Update status to processing
        await db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"analysis_status": "processing"}}
        )
        
        # Analyze video using AI
        analysis_result = await analyze_video(video_path)
        
        # Update video record with analysis
        await db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "analysis_status": "completed",
                "insights": analysis_result["insights"],
                "recommendations": analysis_result["recommendations"],
                "confidence_score": analysis_result["confidence"],
                "detected_behaviors": analysis_result.get("behaviors", []),
                "health_concerns": analysis_result.get("concerns", [])
            }}
        )
        
        # Update pet's video count
        await db.pets.update_one(
            {"_id": ObjectId(pet_id)},
            {"$inc": {"videos_analyzed": 1}}
        )
        
    except Exception as e:
        # Mark as failed
        await db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"analysis_status": "failed"}}
        )
        print(f"Error analyzing video: {str(e)}")

@router.get("/{video_id}")
async def get_video_analysis(video_id: str, db=Depends(get_database)):
    """Get video analysis results"""
    if not ObjectId.is_valid(video_id):
        raise HTTPException(status_code=400, detail="Invalid video ID")
    
    video = await db.videos.find_one({"_id": ObjectId(video_id)})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video["id"] = str(video.pop("_id"))
    return video

@router.get("/pet/{pet_id}/videos")
async def get_pet_videos(pet_id: str, db=Depends(get_database)):
    """Get all videos for a specific pet"""
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="Invalid pet ID")
    
    videos = []
    async for video in db.videos.find({"pet_id": pet_id}):
        video["id"] = str(video.pop("_id"))
        videos.append(video)
    
    return videos
