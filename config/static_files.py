from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.settings import settings

def setup_static_files(app: FastAPI) -> None:
    """Configure static files and templates"""
    
    # Mount static files
    app.mount(
        "/static", 
        StaticFiles(directory=settings.STATIC_DIR), 
        name="static"
    )
    
    # Configure templates
    app.state.templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)