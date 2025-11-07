from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from app.services.plants import PlantsService

async def plants_page(request: Request) -> HTMLResponse:
    """
    Serve the plants management page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "plants.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading plants page: {str(e)}"
        )

async def get_plants_data():
    """
    Get all plants data
    """
    try:
        plants = PlantsService.get_all_plants()
        return {
            "success": True,
            "data": plants,
            "total": len(plants)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading plants data: {str(e)}"
        )

async def get_plant_details(plant_id: int):
    """
    Get specific plant details
    """
    try:
        plant = PlantsService.get_plant_by_id(plant_id)
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        return {
            "success": True,
            "data": plant
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading plant details: {str(e)}"
        )