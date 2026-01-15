"""
Main server file - Serves both API and Frontend
Run this file from project root: python serve.py
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Load .env file from backend directory
env_file = backend_path / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"[OK] Loaded .env from {env_file}", flush=True)
else:
    print(f"[WARNING] .env not found at {env_file}", flush=True)
    print(f"[INFO] Please copy backend/.env.example to backend/.env", flush=True)

from app.core.config import settings
from app.db.session import connect_to_mongo, close_mongo_connection
from app.api.v1.router import api_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("[START] Starting application...")
    await connect_to_mongo()
    
    # Ensure upload directory exists
    upload_dir = Path("backend/uploads")
    upload_dir.mkdir(exist_ok=True)
    (upload_dir / "orders").mkdir(exist_ok=True)
    
    yield
    
    # Shutdown
    print("[SHUTDOWN] Shutting down application...")
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Shipway API with Frontend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files FIRST (html=True enables index.html auto-serving)
frontend_dir = Path("frontend")
if frontend_dir.exists():
    try:
        app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
        print("[OK] Mounted frontend at /frontend", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to mount frontend: {e}", flush=True)
else:
    print(f"[WARNING] Frontend directory not found at {frontend_dir.absolute()}", flush=True)

# Mount static files for uploads
upload_dir = Path("backend/uploads")
if upload_dir.exists():
    app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")
    print(f"[OK] Mounted uploads at /uploads", flush=True)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API info"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "frontend": "/frontend/index.html",
        "api_base": "/api/v1"
    }

# Health check
@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("Starting Shipway Server")
    print("=" * 60)
    print(f"Frontend: http://localhost:8000/frontend/")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"API Base: http://localhost:8000/api/v1/")
    print("=" * 60)
    
    uvicorn.run(
        "serve:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
