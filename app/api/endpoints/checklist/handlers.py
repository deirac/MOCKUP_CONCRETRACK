from fastapi import Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from app.services.checklist import ChecklistService
from app.models.schemas.checklist import CreateChecklistRequest

async def checklist_page(request: Request) -> HTMLResponse:
    """
    Serve the checklist management page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "checklist.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading checklist page: {str(e)}"
        )

async def get_checklists_data():
    """
    Get all checklists data
    """
    try:
        checklists = ChecklistService.get_all_checklists()
        return {
            "success": True,
            "data": checklists,
            "total": len(checklists)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading checklists data: {str(e)}"
        )

async def get_checklist_details(checklist_id: int):
    """
    Get specific checklist details
    """
    try:
        checklist = ChecklistService.get_checklist_by_id(checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")
        
        return {
            "success": True,
            "data": checklist
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading checklist details: {str(e)}"
        )

async def create_checklist(checklist_data: CreateChecklistRequest):
    """
    Create a new checklist
    """
    try:
        checklist = ChecklistService.create_checklist(checklist_data)
        return {
            "success": True,
            "message": "Checklist created successfully",
            "data": checklist
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating checklist: {str(e)}"
        )

async def update_checklist_item(checklist_id: int, item_id: int, completed: bool = Form(...)):
    """
    Update checklist item status
    """
    try:
        success = ChecklistService.update_checklist_item(checklist_id, item_id, completed)
        if not success:
            raise HTTPException(status_code=404, detail="Checklist or item not found")
        
        return {
            "success": True,
            "message": "Checklist item updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating checklist item: {str(e)}"
        )

async def complete_checklist(checklist_id: int):
    """
    Complete a checklist
    """
    try:
        success = ChecklistService.complete_checklist(checklist_id)
        if not success:
            raise HTTPException(status_code=404, detail="Checklist not found")
        
        return {
            "success": True,
            "message": "Checklist completed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error completing checklist: {str(e)}"
        )