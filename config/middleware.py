from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

def setup_middleware(app: FastAPI) -> None:
    """Configure application middleware"""
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # You can add more middleware here
    # Example: Security headers, logging, etc.