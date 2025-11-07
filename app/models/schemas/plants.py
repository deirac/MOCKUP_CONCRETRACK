from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# ... (schemas existentes se mantienen)

class ConcretePlant(BaseModel):
    id: int
    name: str
    location: str
    capacity: float  # m³ per day
    status: str  # active, maintenance, inactive
    manager: str
    phone: str
    email: str
    mixes_available: List[str]
    trucks_available: int
    last_maintenance: datetime
    notes: Optional[str] = None

class PlantProduction(BaseModel):
    plant_id: int
    date: date
    total_production: float  # m³
    mixes_produced: Dict[str, float]  # mix_type: volume
    trucks_dispatched: int
    efficiency: Optional[float] = None

class PlantSummary(BaseModel):
    total_plants: int
    active_plants: int
    total_capacity: float
    available_trucks: int
    maintenance_plants: int