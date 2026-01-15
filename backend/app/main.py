"""
FastAPI Application - Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import os
from app.core.config import settings
from app.db.session import connect_to_mongo, close_mongo_connection
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    print("[START] Starting application...")
    await connect_to_mongo()
    
    # Ensure upload directory exists
    upload_dir = Path("uploads")
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
    description=settings.DESCRIPTION,
    docs_url="/docs",           # Standard FastAPI Swagger UI
    redoc_url="/redoc",         # ReDoc alternative UI
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,     # Remember auth token
        "displayRequestDuration": True,   # Show request time
        "filter": True,                   # Enable search filter
        "deepLinking": True,              # Enable deep linking
        "displayOperationId": False,      # Hide operation IDs
        "defaultModelsExpandDepth": 1,    # Expand models by default
        "defaultModelExpandDepth": 1,
        "docExpansion": "list",           # Show list of endpoints
        "syntaxHighlight.theme": "monokai"  # Syntax highlighting theme
    },
    lifespan=lifespan
)

# Add alternative Swagger UI at /apidocs/ (for compatibility with old Flask app)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import Request

@app.get("/apidocs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    """
    Alternative Swagger UI at /apidocs/ (compatible with old Flask/Flasgger URL)
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files for uploads
upload_dir = Path("uploads")
if upload_dir.exists():
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Mount frontend static files (using absolute path)
# Get the project root directory (parent of backend)
current_dir = Path(__file__).resolve().parent.parent  # backend/app/main.py -> backend/
project_root = current_dir.parent  # backend/ -> project root
frontend_dir = project_root / "frontend"

print(f"[DEBUG] Current file: {__file__}")
print(f"[DEBUG] Backend dir: {current_dir}")
print(f"[DEBUG] Project root: {project_root}")
print(f"[DEBUG] Frontend dir: {frontend_dir}")
print(f"[DEBUG] Frontend exists: {frontend_dir.exists()}")

if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
    print(f"[OK] Mounted frontend at /frontend -> {frontend_dir}")
else:
    print(f"[WARNING] Frontend directory not found at {frontend_dir}")


# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Welcome message and API info"
)
async def root():
    """
    Root endpoint - API info and documentation links
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "environment": settings.NODE_ENV,
        "documentation": {
            "swagger_ui": "/docs",
            "swagger_ui_alternative": "/apidocs",  # Compatible with Flask/Flasgger
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "health": "/health",
        "api_base": "/api/v1"
    }


@app.get(
    "/health",
    tags=["Root"],
    summary="Health check",
    description="Check if API is running"
)
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }


# Run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
