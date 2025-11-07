from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.endpoints.plants.handlers import (
    plants_page,
    get_plants_data,
    get_plant_details
)

router = APIRouter()

# Register routes
router.get("/plants", response_class=HTMLResponse, summary="Plants Page")(plants_page)
router.get("/api/plants", summary="Get plants data")(get_plants_data)
router.get("/api/plants/{plant_id}", summary="Get plant details")(get_plant_details)