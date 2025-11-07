from fastapi import Request, Form, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.auth import AuthService

async def login_page(request: Request) -> HTMLResponse:
    """
    Serve the login page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "auth/login.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading login page: {str(e)}"
        )

async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Handle login form submission
    """
    try:
        user = AuthService.authenticate_user(email, password)
        
        if user:
            # En una aplicación real, aquí crearías una sesión o JWT token
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            # response.set_cookie(key="session_token", value="fake_session_token")
            return response
        else:
            templates = request.app.state.templates
            return templates.TemplateResponse(
                "auth/login.html",
                {
                    "request": request,
                    "project_name": request.app.title,
                    "version": request.app.version,
                    "error": "Credenciales inválidas"
                },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error during login: {str(e)}"
        )

async def logout_user(request: Request):
    """
    Handle user logout
    """
    try:
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        # response.delete_cookie(key="session_token")
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error during logout: {str(e)}"
        )

async def register_page(request: Request) -> HTMLResponse:
    """
    Serve the register page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "auth/register.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading register page: {str(e)}"
        )

async def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    company: str = Form(None),
    phone: str = Form(...)
):
    """
    Handle register form submission
    """
    try:
        if password != confirm_password:
            templates = request.app.state.templates
            return templates.TemplateResponse(
                "auth/register.html",
                {
                    "request": request,
                    "project_name": request.app.title,
                    "version": request.app.version,
                    "error": "Las contraseñas no coinciden"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        user = AuthService.register_user(name, email, password, company, phone)
        
        if user:
            response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
            return response
        else:
            templates = request.app.state.templates
            return templates.TemplateResponse(
                "auth/register.html",
                {
                    "request": request,
                    "project_name": request.app.title,
                    "version": request.app.version,
                    "error": "El usuario ya existe"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error during registration: {str(e)}"
        )