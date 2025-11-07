from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.endpoints.inventory.handlers import (
    inventory_page,
    get_inventory_data,
    get_material_details,
    update_material_stock,
    get_material_usage
)

router = APIRouter()

# Register routes
router.get("/inventory", response_class=HTMLResponse, summary="Inventory Page")(inventory_page)
router.get("/api/inventory", summary="Get inventory data")(get_inventory_data)
router.get("/api/inventory/{material_id}", summary="Get material details")(get_material_details)
router.put("/api/inventory/{material_id}/stock", summary="Update material stock")(update_material_stock)
router.get("/api/inventory/{material_id}/usage", summary="Get material usage")(get_material_usage)