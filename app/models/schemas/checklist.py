from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

# ... (otros schemas existentes)

class ChecklistStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ChecklistItem(BaseModel):
    id: int
    category: str
    description: str
    completed: bool = False
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None

class ConcreteChecklist(BaseModel):
    id: int
    order_id: int
    project_name: str
    supervisor: str
    scheduled_time: datetime
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    items: List[ChecklistItem]

class CreateChecklistRequest(BaseModel):
    order_id: int
    project_name: str
    supervisor: str
    scheduled_time: datetime
    categories: List[str]

class ChecklistSummary(BaseModel):
    total_checklists: int
    todays_checklists: int
    completed_today: int
    in_progress: int
    pending: int
    completion_rate: float
    total_items: int
    completed_items: int