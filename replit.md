# PetCare - AI-Powered Pet Health & Care Platform

## Overview
PetCare is a full-stack web application that provides AI-powered video analysis to detect pet health issues, track behavior, and offers a complete pet care platform including a shop and veterinary clinic locator.

**Tech Stack:**
- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Next.js 14 with React 18
- **Database**: MongoDB
- **AI**: OpenAI API for video analysis
- **Maps**: Google Maps API for vet locator

## Project Structure

```
├── app/                      # FastAPI backend
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic (AI analysis, storage, video processing)
│   ├── config.py            # Configuration settings
│   ├── database.py          # MongoDB connection
│   └── main.py              # FastAPI app entry point
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities and API clients
│   │   └── styles/        # CSS styles
│   └── package.json
└── uploads/                # File storage directory
```

## Recent Changes (Migration to Replit)

**Date**: November 8, 2024

Successfully migrated the PetCare application from Vercel to Replit with the following changes:

1. **Port Configuration**: Updated Next.js to run on port 5000 (required for Replit webview)
   - Modified `frontend/package.json` scripts to use `-p 5000 -H 0.0.0.0`
   
2. **CORS Configuration**: Updated FastAPI to accept Replit domains
   - Modified `app/main.py` to dynamically read `REPLIT_DOMAINS` environment variable
   - Added localhost:5000 to allowed origins

3. **API URL Configuration**: Changed frontend to use environment variables
   - Updated `frontend/src/lib/api.js` to use `NEXT_PUBLIC_API_URL`
   - Created `frontend/.env.local` with local API URL

4. **Workflows Setup**:
   - Frontend: Runs on port 5000 (webview) - User-facing interface
   - Backend: Runs on port 8000 (console) - API server

5. **Dependencies**: Installed all required packages
   - Python: fastapi, uvicorn, pymongo, openai, opencv-python, pillow, and more
   - Node.js: next, react, axios, zustand, tailwindcss, and more

## Environment Variables

The following secrets are configured in Replit:

- `MONGODB_URL` - MongoDB connection string
- `OPENAI_API_KEY` - OpenAI API key for AI analysis
- `NEXT_PUBLIC_GOOGLE_MAPS_API` - Google Maps API key for vet locator
- `REPLIT_DOMAINS` - Automatically set by Replit

Frontend environment (`.env.local`):
- `NEXT_PUBLIC_API_URL` - Backend API URL (http://localhost:8000/api for local dev)

## Features

1. **Pet Management**: Create and manage pet profiles with images
2. **AI Video Analysis**: Upload pet videos for AI-powered health and behavior analysis
3. **Shop**: Browse pet products by category and species
4. **Vet Locator**: Find nearby veterinary clinics using Google Maps
5. **Dashboard**: View all pets and their health status

## Running the Application

The application runs automatically via configured workflows:

- **Frontend**: Accessible at the Replit webview (port 5000)
- **Backend API**: Runs on port 8000, accessible to frontend via localhost

Both services start automatically when the Repl is opened.

## API Documentation

When the backend is running, visit `/docs` for interactive API documentation (Swagger UI).

## Architecture Decisions

- **Separate Frontend/Backend**: Maintains clear separation of concerns and allows independent scaling
- **Environment-based Configuration**: Uses environment variables for all sensitive data and deployment-specific settings
- **MongoDB**: NoSQL database chosen for flexible schema and easy scalability
- **File Storage**: Local file system for uploads (videos/images) with organized directory structure
- **CORS Strategy**: Dynamic CORS configuration that works in both development and production environments
