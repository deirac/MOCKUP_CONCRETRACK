from fastapi import APIRouter
from app.api.endpoints.home.router import router as home_router


def setup_routers(app) -> None:
    """Register all application routers"""
    
    # Main API Router
    api_router = APIRouter(prefix="/api/v1")
    
    
    # Include routers in app
    app.include_router(home_router, tags=["home"])
    app.include_router(api_router)