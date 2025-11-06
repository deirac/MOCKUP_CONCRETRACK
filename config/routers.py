
from fastapi import APIRouter
#from app.api.endpoints.home.router import router as home_router
#from app.api.endpoints.mock_data.router import router as mock_data_router

def setup_routers(app) -> None:
    """Register all application routers"""
    
    # Main API Router
    api_router = APIRouter(prefix="/api/v1")
    
    # Include all endpoint routers
    #api_router.include_router(mock_data_router, tags=["mock-data"])
    
    # Include routers in app
    #app.include_router(home_router, tags=["home"])
    app.include_router(api_router)

