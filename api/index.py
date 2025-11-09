"""
Vercel serverless function handler for FastAPI app
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Export the FastAPI app for Vercel
handler = app

