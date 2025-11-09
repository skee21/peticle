# Vercel Deployment Guide

## Backend API (FastAPI)

The backend is configured to run as a serverless function on Vercel.

### Configuration Files

- `vercel.json` - Vercel configuration for routing
- `api/index.py` - Serverless function handler
- `requirements.txt` - Python dependencies

### Environment Variables

Set these in your Vercel project settings:

- `FRONTEND_URL` - Your frontend URL (e.g., `https://your-app.vercel.app`)
- `VERCEL_URL` - Automatically set by Vercel
- `OPENAI_API_KEY` - (Optional) For AI features
- `GOOGLE_MAPS_API_KEY` - (Optional) For vet locator

### Data Storage

The app uses JSON file storage in the `data/` directory. On Vercel, this is ephemeral storage that resets on each deployment. For production, consider:

1. Using Vercel's KV storage
2. Using an external database (PostgreSQL, MongoDB, etc.)
3. Using Vercel Blob storage for file uploads

## Frontend (Next.js)

### Configuration

- `next.config.js` - Configured to proxy API calls in development
- Environment variable: `NEXT_PUBLIC_API_URL` - Set to your backend API URL

### Environment Variables

- `NEXT_PUBLIC_API_URL` - Your backend API URL (e.g., `https://your-api.vercel.app`)

### Deployment

1. Connect your repository to Vercel
2. Set the root directory to `frontend/` for the frontend deployment
3. Set environment variables
4. Deploy

## Development

### Backend

```bash
cd app
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Production Notes

- The `data/` directory is ephemeral on Vercel - data will be lost on redeployment
- Consider using external storage for production
- File uploads should use Vercel Blob or external storage
- CORS is configured to allow your frontend domain

