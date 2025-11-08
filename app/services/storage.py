import aiofiles
import os
import uuid
from fastapi import UploadFile

async def save_video(file: UploadFile) -> str:
    """Save uploaded video to disk"""
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("uploads/videos", unique_filename)
    
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    
    return file_path

async def save_image(file: UploadFile, folder: str = "images") -> str:
    """Save uploaded image to disk"""
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(f"uploads/{folder}", unique_filename)
    
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    
    return file_path
