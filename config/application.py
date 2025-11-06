from fastapi import FastAPI
from typing import Optional, Callable, AsyncContextManager, Any
from contextlib import asynccontextmanager
from config.settings import settings

def create_app(lifespan: Optional[Callable[[FastAPI], AsyncContextManager[Any]]] = None) -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    return app