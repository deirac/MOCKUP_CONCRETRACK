from fastapi import Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from app.services.inventory import InventoryService

async def inventory_page(request: Request) -> HTMLResponse:
    """
    Serve the inventory management page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "inventory.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading inventory page: {str(e)}"
        )

async def get_inventory_data():
    """
    Get all inventory data
    """
    try:
        inventory = InventoryService.get_all_materials()
        return {
            "success": True,
            "data": inventory,
            "total": len(inventory)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading inventory data: {str(e)}"
        )

async def get_material_details(material_id: int):
    """
    Get specific material details
    """
    try:
        material = InventoryService.get_material_by_id(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        
        return {
            "success": True,
            "data": material
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading material details: {str(e)}"
        )

async def update_material_stock(material_id: int, new_stock: float = Form(...)):
    """
    Update material stock
    """
    try:
        success = InventoryService.update_material_stock(material_id, new_stock)
        if not success:
            raise HTTPException(status_code=404, detail="Material not found")
        
        return {
            "success": True,
            "message": f"Stock updated to {new_stock}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating material stock: {str(e)}"
        )

async def get_material_usage(material_id: int):
    """
    Get material usage statistics
    """
    try:
        usage = InventoryService.get_material_usage(material_id)
        if not usage:
            raise HTTPException(status_code=404, detail="Material not found")
        
        return {
            "success": True,
            "data": usage
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading material usage: {str(e)}"
        )