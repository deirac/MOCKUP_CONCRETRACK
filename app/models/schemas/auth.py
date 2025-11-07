from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# ... (los schemas anteriores se mantienen)

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    company: Optional[str] = None
    phone: str
    role: str = "client"  # admin, operator, client
    created_at: datetime
    active: bool = True

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    company: Optional[str] = None
    phone: str