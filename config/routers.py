from fastapi import APIRouter
from app.api.endpoints.home.router import router as home_router
from app.api.endpoints.auth.router import router as auth_router
from app.api.endpoints.plants.router import router as plants_router
from app.api.endpoints.orders.router import router as orders_router
from app.api.endpoints.checklist.router import router as checklist_router
from app.api.endpoints.inventory.router import router as inventory_router

def setup_routers(app) -> None:
    """Register all application routers"""
    
    # Main API Router
    api_router = APIRouter(prefix="/api/v1")
   
    # Include routers in app
    app.include_router(home_router, tags=["home"])
    app.include_router(auth_router, tags=["auth"])
    app.include_router(plants_router, tags=["plants"])
    app.include_router(orders_router, tags=["orders"])
    app.include_router(checklist_router, tags=["checklist"])
    app.include_router(api_router)
    app.include_router(inventory_router, tags=["inventory"])

    @app.get("/api/v1/checklists-summary")
    async def get_checklists_summary():
        from app.services.checklist import ChecklistService
        return ChecklistService.get_checklists_summary()

    @app.get("/api/v1/inventory-summary")
    async def get_inventory_summary():
        from app.services.inventory import InventoryService
        return InventoryService.get_inventory_summary()