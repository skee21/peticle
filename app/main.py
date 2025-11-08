from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import pets, videos, shop, vets
import os

app = FastAPI(
    title="PetCare API",
    description="AI-powered pet health and care platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/images", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()  # Initialize JSON database

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()  # Close JSON database

# Routes
app.include_router(pets.router, prefix="/api/pets", tags=["Pets"])
app.include_router(videos.router, prefix="/api/videos", tags=["Videos"])
app.include_router(shop.router, prefix="/api/shop", tags=["Shop"])
app.include_router(vets.router, prefix="/api/vets", tags=["Vets"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to PetCare API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
