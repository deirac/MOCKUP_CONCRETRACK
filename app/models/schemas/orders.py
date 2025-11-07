from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

# ... (otros schemas existentes)

class ConcreteOrder(BaseModel):
    id: int
    project_id: int
    project_name: str
    client: str
    mix_type: str
    volume: float  # m³
    status: str
    scheduled_time: datetime
    address: str
    priority: str
    assigned_plant: str
    estimated_duration: float  # hours
    created_at: datetime
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None  # Agregado este campo

class CreateOrderRequest(BaseModel):
    project_id: int
    mix_type: str
    volume: float
    scheduled_time: datetime
    address: str
    priority: str = "medium"
    assigned_plant: str
    estimated_duration: float
    notes: Optional[str] = None

class OrdersSummary(BaseModel):
    total_orders: int
    active_orders: int
    todays_orders: int
    total_volume_today: float
    total_volume_active: float
    completed_today: int
    urgent_orders: int