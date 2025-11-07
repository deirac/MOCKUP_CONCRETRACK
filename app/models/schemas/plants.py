from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class ConcretePlant(BaseModel):
    id: int
    name: str
    location: str
    capacity: float  # m³ per hour
    status: str  # active, maintenance, inactive
    manager: str
    phone: str
    email: str
    mixes_available: List[str]
    transport : Optional[str] = None
    last_maintenance: datetime
    notes: Optional[str] = None

class PlantProduction(BaseModel):
    plant_id: int
    date: date
    total_production: float  # m³
    mixes_produced: Dict[str, float]  # mix_type: volume
    transport : Optional[str] = None
    efficiency: Optional[float] = None

class PlantSummary(BaseModel):
    total_plants: int
    active_plants: int
    total_capacity: float
    available_trucks: int
    maintenance_plants: int