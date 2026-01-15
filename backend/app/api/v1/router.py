"""
API v1 Router - Combine all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1 import auth, user, wallet, orders


# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(wallet.router)
api_router.include_router(orders.router)