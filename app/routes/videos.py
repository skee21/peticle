from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Depends
from typing import List
from app.database import get_database
from app.schemas.video import VideoAnalysisResponse, VideoUploadResponse
from app.services.video_processor import process_video
from app.services.ai_analysis import analyze_video
from app.services.storage import save_video
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
    try:
        # Check if pet exists
        pet = await db.pets.find_one({"_id": pet_id})
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
        video_id = str(result["inserted_id"])
        
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload video: {str(e)}")

async def analyze_video_background(video_id: str, video_path: str, pet_id: str, db):
    """Background task to analyze video"""
    try:
        # Update status to processing
        await db.videos.update_one(
            {"_id": video_id},
            {"$set": {"analysis_status": "processing"}}
        )
        
        # Analyze video using AI
        analysis_result = await analyze_video(video_path)
        
        # Update video record with analysis
        await db.videos.update_one(
            {"_id": video_id},
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
        pet = await db.pets.find_one({"_id": pet_id})
        if pet:
            current_count = pet.get("videos_analyzed", 0)
            await db.pets.update_one(
                {"_id": pet_id},
                {"$set": {"videos_analyzed": current_count + 1}}
            )
        
    except Exception as e:
        # Mark as failed
        await db.videos.update_one(
            {"_id": video_id},
            {"$set": {"analysis_status": "failed"}}
        )
        print(f"Error analyzing video: {str(e)}")

@router.get("/{video_id}")
async def get_video_analysis(video_id: str, db=Depends(get_database)):
    """Get video analysis results"""
    try:
        video = await db.videos.find_one({"_id": video_id})
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_id_value = video.pop("_id", None)
        video["id"] = str(video_id_value) if video_id_value else video_id
        return video
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video: {str(e)}")

@router.get("/pet/{pet_id}/videos")
async def get_pet_videos(pet_id: str, db=Depends(get_database)):
    """Get all videos for a specific pet"""
    try:
        videos_data = await db.videos.find({"pet_id": pet_id})
        videos = []
        for video in videos_data:
            video_id_value = video.pop("_id", None)
            video["id"] = str(video_id_value) if video_id_value else None
            videos.append(video)
        
        return videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch videos: {str(e)}")
