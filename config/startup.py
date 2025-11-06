from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.application import create_app
from config.middleware import setup_middleware
from config.static_files import setup_static_files
from config.routers import setup_routers
from config.settings import settings
import asyncio

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup/shutdown events
    """
    # Startup logic
    startup_success = await startup_handler(app)
    
    if not startup_success:
        raise RuntimeError("Application startup failed")
    
    yield  # App is running here
    
    # Shutdown logic
    await shutdown_handler(app)

async def startup_handler(app: FastAPI) -> bool:
    """Handle application startup"""
    try:
        print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
        print(f"📊 Debug mode: {settings.DEBUG}")
        print(f"🌐 API prefix: {settings.API_PREFIX}")
        print(f"📁 Static files: {settings.STATIC_DIR}")
        print(f"🎨 Templates: {settings.TEMPLATES_DIR}")
        
        # Here you can add database connections, cache initialization, etc.
        # await database.connect()
        # await cache.initialize()
        
        print("✅ Startup completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

async def shutdown_handler(app: FastAPI) -> None:
    """Handle application shutdown"""
    try:
        print(f"🛑 Shutting down {settings.PROJECT_NAME}...")
        
        # Here you can add cleanup logic
        # await database.disconnect()
        # await cache.close()
        
        print("✅ Shutdown completed successfully")
        
    except Exception as e:
        print(f"⚠️  Shutdown warnings: {e}")

def create_application() -> FastAPI:
    """Application factory - orchestrates all configuration"""
    
    # Create base application with lifespan
    app = create_app(lifespan=app_lifespan)
    
    # Setup all components
    setup_middleware(app)
    setup_static_files(app)
    setup_routers(app)
    
    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "project": settings.PROJECT_NAME
        }
    
    return app