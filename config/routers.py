from fastapi import APIRouter
from app.api.endpoints.home.router import router as home_router
from app.api.endpoints.auth.router import router as auth_router
from app.api.endpoints.plants.router import router as plants_router

def setup_routers(app) -> None:
    """Register all application routers"""
    
    # Main API Router
    api_router = APIRouter(prefix="/api/v1")
    
    
    # Include routers in app
    app.include_router(home_router, tags=["home"])
    app.include_router(auth_router, tags=["auth"])
    api_router.include_router(plants_router, tags=["plants"])
    
     # Include the main API router
    app.include_router(api_router)