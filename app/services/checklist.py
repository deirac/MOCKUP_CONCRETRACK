from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.schemas.checklist import ConcreteChecklist, CreateChecklistRequest, ChecklistItem

class ChecklistService:
    """
    Service class for concrete pouring checklists management
    """
    
    # Mock database for checklists
    _checklists_db = [
        ConcreteChecklist(
            id=1,
            order_id=2,
            project_name="Centro Comercial Plaza",
            supervisor="Ing. Roberto Jiménez",
            scheduled_time=datetime.now(),
            status="in_progress",
            created_at=datetime.now() - timedelta(hours=2),
            completed_at=None,
            items=[
                ChecklistItem(
                    id=1,
                    category="pre_vaciado",
                    description="Verificar limpieza y preparación del área de vaciado",
                    completed=True,
                    notes="Área limpia y preparada correctamente"
                ),
                ChecklistItem(
                    id=2,
                    category="pre_vaciado",
                    description="Confirmar disponibilidad de mezcla C-25",
                    completed=True,
                    notes="Mezcla confirmada en Planta Sur"
                ),
                ChecklistItem(
                    id=3,
                    category="pre_vaciado",
                    description="Verificar equipo de bombeo y mangueras",
                    completed=True,
                    notes="Equipo en óptimas condiciones"
                ),
                ChecklistItem(
                    id=4,
                    category="seguridad",
                    description="Verificar EPP del personal (casco, chaleco, botas)",
                    completed=True,
                    notes="Todo el personal cuenta con EPP completo"
                ),
                ChecklistItem(
                    id=5,
                    category="seguridad",
                    description="Delimitación y señalización del área de trabajo",
                    completed=False,
                    notes="Pendiente colocar conos de seguridad"
                ),
                ChecklistItem(
                    id=6,
                    category="calidad",
                    description="Toma de muestra para cilindros de prueba",
                    completed=False,
                    notes="Programado para inicio del vaciado"
                )
            ]
        ),
        ConcreteChecklist(
            id=2,
            order_id=1,
            project_name="Torre Norte",
            supervisor="Ing. Carlos Mendoza",
            scheduled_time=datetime.now() + timedelta(hours=2),
            status="pending",
            created_at=datetime.now() - timedelta(days=1),
            completed_at=None,
            items=[
                ChecklistItem(
                    id=1,
                    category="pre_vaciado",
                    description="Verificar limpieza y preparación del área de vaciado",
                    completed=False,
                    notes=None
                ),
                ChecklistItem(
                    id=2,
                    category="pre_vaciado",
                    description="Confirmar disponibilidad de mezcla C-30",
                    completed=True,
                    notes="Mezcla confirmada en Planta Central"
                ),
                ChecklistItem(
                    id=3,
                    category="pre_vaciado",
                    description="Verificar equipo de bombeo de 42 metros",
                    completed=True,
                    notes="Bomba confirmada y en ruta"
                )
            ]
        ),
        ConcreteChecklist(
            id=3,
            order_id=3,
            project_name="Residencial Jardines",
            supervisor="Téc. Ana López",
            scheduled_time=datetime.now() - timedelta(hours=8),
            status="completed",
            created_at=datetime.now() - timedelta(days=1),
            completed_at=datetime.now() - timedelta(hours=6),
            items=[
                ChecklistItem(
                    id=1,
                    category="pre_vaciado",
                    description="Verificar limpieza y preparación del área de vaciado",
                    completed=True,
                    notes="Área preparada según especificaciones"
                ),
                ChecklistItem(
                    id=2,
                    category="pre_vaciado",
                    description="Confirmar disponibilidad de mezcla C-20",
                    completed=True,
                    notes="Mezcla entregada según programación"
                ),
                ChecklistItem(
                    id=3,
                    category="seguridad",
                    description="Verificar EPP del personal",
                    completed=True,
                    notes="Todo el personal con EPP adecuado"
                ),
                ChecklistItem(
                    id=4,
                    category="calidad",
                    description="Toma de muestra para cilindros de prueba",
                    completed=True,
                    notes="3 cilindros tomados correctamente"
                ),
                ChecklistItem(
                    id=5,
                    category="post_vaciado",
                    description="Limpieza final del área",
                    completed=True,
                    notes="Área limpiada y equipos guardados"
                )
            ]
        )
    ]
    
    # Template items for new checklists
    _template_items = [
        # Pre-vaciado
        ChecklistItem(id=1, category="pre_vaciado", description="Verificar limpieza y preparación del área de vaciado", completed=False),
        ChecklistItem(id=2, category="pre_vaciado", description="Confirmar disponibilidad de mezcla especificada", completed=False),
        ChecklistItem(id=3, category="pre_vaciado", description="Verificar equipo de bombeo y mangueras", completed=False),
        ChecklistItem(id=4, category="pre_vaciado", description="Confirmar acceso para camiones mixer", completed=False),
        
        # Seguridad
        ChecklistItem(id=5, category="seguridad", description="Verificar EPP del personal (casco, chaleco, botas)", completed=False),
        ChecklistItem(id=6, category="seguridad", description="Delimitación y señalización del área de trabajo", completed=False),
        ChecklistItem(id=7, category="seguridad", description="Verificar extintores y kit de primeros auxilios", completed=False),
        
        # Calidad
        ChecklistItem(id=8, category="calidad", description="Toma de muestra para cilindros de prueba", completed=False),
        ChecklistItem(id=9, category="calidad", description="Verificar temperatura del concreto", completed=False),
        ChecklistItem(id=10, category="calidad", description="Control de asentamiento (slump test)", completed=False),
        
        # Post-vaciado
        ChecklistItem(id=11, category="post_vaciado", description="Limpieza final del área", completed=False),
        ChecklistItem(id=12, category="post_vaciado", description="Curado inicial aplicado", completed=False),
        ChecklistItem(id=13, category="post_vaciado", description="Documentación y reportes completados", completed=False)
    ]
    
    @staticmethod
    def get_all_checklists() -> List[ConcreteChecklist]:
        """
        Get all concrete checklists
        """
        return ChecklistService._checklists_db
    
    @staticmethod
    def get_checklist_by_id(checklist_id: int) -> Optional[ConcreteChecklist]:
        """
        Get checklist by ID
        """
        return next((checklist for checklist in ChecklistService._checklists_db 
                    if checklist.id == checklist_id), None)
    
    @staticmethod
    def get_checklists_by_status(status: str) -> List[ConcreteChecklist]:
        """
        Get checklists by status
        """
        return [checklist for checklist in ChecklistService._checklists_db 
                if checklist.status == status]
    
    @staticmethod
    def get_todays_checklists() -> List[ConcreteChecklist]:
        """
        Get today's checklists
        """
        today = datetime.now().date()
        return [checklist for checklist in ChecklistService._checklists_db 
                if checklist.scheduled_time.date() == today]
    
    @staticmethod
    def create_checklist(checklist_data: CreateChecklistRequest) -> ConcreteChecklist:
        """
        Create a new checklist
        """
        # Create items from template
        items = []
        for template_item in ChecklistService._template_items:
            if template_item.category in checklist_data.categories:
                items.append(ChecklistItem(
                    id=len(items) + 1,
                    category=template_item.category,
                    description=template_item.description,
                    completed=False
                ))
        
        # Create new checklist
        new_checklist = ConcreteChecklist(
            id=len(ChecklistService._checklists_db) + 1,
            order_id=checklist_data.order_id,
            project_name=checklist_data.project_name,
            supervisor=checklist_data.supervisor,
            scheduled_time=checklist_data.scheduled_time,
            status="pending",
            created_at=datetime.now(),
            completed_at=None,
            items=items
        )
        
        ChecklistService._checklists_db.append(new_checklist)
        return new_checklist
    
    @staticmethod
    def update_checklist_item(checklist_id: int, item_id: int, completed: bool) -> bool:
        """
        Update checklist item status
        """
        checklist = ChecklistService.get_checklist_by_id(checklist_id)
        if checklist:
            item = next((item for item in checklist.items 
                        if item.id == item_id), None)
            if item:
                item.completed = completed
                return True
        return False
    
    @staticmethod
    def complete_checklist(checklist_id: int) -> bool:
        """
        Complete a checklist
        """
        checklist = ChecklistService.get_checklist_by_id(checklist_id)
        if checklist:
            checklist.status = "completed"
            checklist.completed_at = datetime.now()
            return True
        return False
    
    @staticmethod
    def get_checklists_summary() -> Dict[str, Any]:
        """
        Get checklists summary statistics
        """
        todays_checklists = ChecklistService.get_todays_checklists()
        completed_today = len([checklist for checklist in todays_checklists 
                             if checklist.status == "completed"])
        in_progress = len(ChecklistService.get_checklists_by_status("in_progress"))
        
        # Calculate completion rates
        total_items = 0
        completed_items = 0
        for checklist in ChecklistService._checklists_db:
            total_items += len(checklist.items)
            completed_items += len([item for item in checklist.items 
                                  if item.completed])
        
        completion_rate = (completed_items / total_items * 100) if total_items > 0 else 0
        
        return {
            "total_checklists": len(ChecklistService._checklists_db),
            "todays_checklists": len(todays_checklists),
            "completed_today": completed_today,
            "in_progress": in_progress,
            "pending": len(ChecklistService.get_checklists_by_status("pending")),
            "completion_rate": round(completion_rate, 1),
            "total_items": total_items,
            "completed_items": completed_items
        }
    
    @staticmethod
    def get_available_categories() -> List[str]:
        """
        Get available checklist categories
        """
        return ["pre_vaciado", "seguridad", "calidad", "post_vaciado"]