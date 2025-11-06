from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class ConcreteOrder(BaseModel):
    id: int
    project_id: int
    mix_type: str
    volume: float  # in m3
    status: str  # scheduled, preparing, in_progress, completed, cancelled
    scheduled_time: datetime
    address: str
    notes: Optional[str] = None

class ConcreteMix(BaseModel):
    code: str
    name: str
    strength: int  # MPa
    price_per_m3: float
    available: bool = True
    description: Optional[str] = None

class Project(BaseModel):
    id: int
    name: str
    client: str
    location: str
    start_date: datetime
    status: str  # active, completed, on_hold
    total_volume: Optional[float] = 0.0

class Client(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    address: str

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class DashboardStats(BaseModel):
    active_orders: int
    completed_orders_today: int
    total_projects: int
    concrete_volume_today: float
    pending_deliveries: int
    available_mixes: int
    revenue_today: float
    upcoming_schedules: int

class ConcreteStats(BaseModel):
    monthly_volume: float
    monthly_revenue: float
    avg_delivery_time: str
    completion_rate: float
    active_trucks: int
    available_pumps: int