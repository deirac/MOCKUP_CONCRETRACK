from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from app.services.home import HomeService

async def read_root(request: Request) -> HTMLResponse:
    """
    Serve the main home page with dashboard data
    """
    try:
        dashboard_data = HomeService.get_dashboard_data()
        
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "dashboard": dashboard_data,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading home page: {str(e)}"
        )

async def about_page(request: Request) -> HTMLResponse:
    """
    Serve the about page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "about.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading about page: {str(e)}"
        )