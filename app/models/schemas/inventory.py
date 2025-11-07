from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

# ... (otros schemas existentes)

class MaterialStatus(str, Enum):
    CRITICAL = "critical"
    LOW = "low"
    OPTIMAL = "optimal"
    HIGH = "high"

class Material(BaseModel):
    id: int
    name: str
    description: str
    current_stock: float
    min_stock: float
    max_stock: float
    unit: str
    cost_per_unit: float
    supplier: str
    last_restock: datetime
    status: str
    notes: Optional[str] = None

class MaterialUsage(BaseModel):
    material_id: int
    date: date
    quantity_used: float
    project: str
    mix_type: str

class InventorySummary(BaseModel):
    total_materials: int
    critical_materials: int
    low_materials: int
    optimal_materials: int
    total_inventory_value: float
    needs_restock: int

class MaterialRequirements(BaseModel):
    mix_type: str
    volume: float
    requirements: Dict[str, float]

class AvailabilityCheck(BaseModel):
    available: bool
    missing_materials: List[Dict[str, Any]]
    available_materials: List[Dict[str, Any]]