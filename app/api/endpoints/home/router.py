from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.endpoints.home.handlers import read_root, about_page

router = APIRouter()

# Register routes
router.get("/", response_class=HTMLResponse, summary="Home Page")(read_root)
router.get("/about", response_class=HTMLResponse, summary="About Page")(about_page)