from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.endpoints.auth.handlers import (
    login_page, 
    login_submit, 
    logout_user,
    register_page,
    register_submit
)

router = APIRouter()

# Register routes
router.get("/login", response_class=HTMLResponse, summary="Login Page")(login_page)
router.post("/login", summary="Login Submit")(login_submit)
router.get("/logout", summary="Logout")(logout_user)
router.get("/register", response_class=HTMLResponse, summary="Register Page")(register_page)
router.post("/register", summary="Register Submit")(register_submit)