from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.schemas.orders import ConcreteOrder, CreateOrderRequest

class OrdersService:
    """
    Service class for concrete orders management
    """
    
    # Mock database for orders
    _orders_db = [
        ConcreteOrder(
            id=1,
            project_id=101,
            project_name="VITTRIO",
            client="Ing. UnIngenieroCivil",  # Cambiado aquí
            mix_type="C-30",
            volume=45.5,
            status="scheduled",
            scheduled_time=datetime.now() + timedelta(hours=3),
            address="ZAPATA A-1 TORRE 1",
            priority="high",
            assigned_plant="PLANTA 1",
            estimated_duration=4.5,
            created_at=datetime.now() - timedelta(days=1),
            notes="Requiere bomba de 43.5 metros"
        ),
        ConcreteOrder(
            id=2,
            project_id=102,
            project_name="VITTRIO",
            client="Ing. Manuela Jimenez",
            mix_type="C-25",
            volume=35.0,
            status="in_progress",
            scheduled_time=datetime.now(),
            address="ZAPATA H-12 TORRE 4",
            priority="medium",
            assigned_plant="PLANTA 2",
            estimated_duration=3.0,
            created_at=datetime.now() - timedelta(hours=6),
            notes="Coordinación con jefe de obra necesaria"
        ),
        ConcreteOrder(
            id=3,
            project_id=103,
            project_name="CRISTALI",
            client="Ing. Manuela Jimenez",
            mix_type="C-20",
            volume=5.0,
            status="completed",
            scheduled_time=datetime.now() - timedelta(hours=8),
            address="PROVICIONALES",
            priority="low",
            assigned_plant="PLANTA 1",
            estimated_duration=1.0,
            created_at=datetime.now() - timedelta(days=1),
            notes="Vaciado completado satisfactoriamente"
        ),
        ConcreteOrder(
            id=4,
            project_id=104,
            project_name="VITTRIO",
            client="Ing. Juan Pulgarín",
            mix_type="C-35",
            volume=35.0,
            status="cancelled",
            scheduled_time=datetime.now() + timedelta(days=1),
            address="Pedestales eje 9 (H-I-J)",
            priority="high",
            assigned_plant="PLANTA 1",
            estimated_duration=6.0,
            created_at=datetime.now() - timedelta(hours=2),
            notes="Concreto especial para cimientos de pedestales"
        ),
        ConcreteOrder(
            id=5,
            project_id=105,
            project_name="CRISTALI",
            client="Ing. UnIngenieroCivil",  # Cambiado aquí
            mix_type="C-30",
            volume=25.0,
            status="cancelled",
            scheduled_time=datetime.now() + timedelta(days=2),
            address="Plancha sotano nivel -3",
            priority="medium",
            assigned_plant="PLANTA 2",
            estimated_duration=4.0,
            created_at=datetime.now() - timedelta(days=3),
            notes="Cancelado por condiciones climáticas"
        )
    ]
    
    # Projects database - ACTUALIZADO con el nombre correcto
    _projects_db = [
        {"id": 101, "name": "VITTRIO", "client": "Ing. UnIngenieroCivil", "location": "ZAPATA A-1 TORRE 1", "start_date": datetime.now() - timedelta(days=30), "status": "active"},
        {"id": 102, "name": "VITTRIO", "client": "Ing. Manuela Jimenez", "location": "ZAPATA H-12 TORRE 4", "start_date": datetime.now() - timedelta(days=15), "status": "active"},
        {"id": 103, "name": "CRISTALI", "client": "Ing. Manuela Jimenez", "location": "PROVICIONALES", "start_date": datetime.now() - timedelta(days=7), "status": "active"},
        {"id": 104, "name": "VITTRIO", "client": "Ing. Juan Pulgarín", "location": "Pedestales eje 9 (H-I-J)", "start_date": datetime.now() - timedelta(days=45), "status": "active"},
        {"id": 105, "name": "CRISTALI", "client": "Ing. UnIngenieroCivil", "location": "Plancha sotano nivel -3", "start_date": datetime.now() - timedelta(days=10), "status": "on_hold"},
    ]
    
    # ... (el resto de los métodos se mantiene igual)
    @staticmethod
    def get_all_orders() -> List[ConcreteOrder]:
        """
        Get all concrete orders
        """
        return OrdersService._orders_db
    
    @staticmethod
    def get_order_by_id(order_id: int) -> Optional[ConcreteOrder]:
        """
        Get order by ID
        """
        return next((order for order in OrdersService._orders_db 
                    if order.id == order_id), None)
    
    @staticmethod
    def get_orders_by_status(status: str) -> List[ConcreteOrder]:
        """
        Get orders by status
        """
        return [order for order in OrdersService._orders_db 
                if order.status == status]
    
    @staticmethod
    def get_todays_orders() -> List[ConcreteOrder]:
        """
        Get today's orders
        """
        today = datetime.now().date()
        return [order for order in OrdersService._orders_db 
                if order.scheduled_time.date() == today]
    
    @staticmethod
    def create_order(order_data: CreateOrderRequest) -> ConcreteOrder:
        """
        Create a new order
        """
        # Find project
        project = next((p for p in OrdersService._projects_db 
                       if p["id"] == order_data.project_id), None)
        
        if not project:
            raise ValueError("Project not found")
        
        # Create new order
        new_order = ConcreteOrder(
            id=len(OrdersService._orders_db) + 1,
            project_id=order_data.project_id,
            project_name=project["name"],
            client=project["client"],
            mix_type=order_data.mix_type,
            volume=order_data.volume,
            status="scheduled",
            scheduled_time=order_data.scheduled_time,
            address=order_data.address,
            priority=order_data.priority,
            assigned_plant=order_data.assigned_plant,
            estimated_duration=order_data.estimated_duration,
            created_at=datetime.now(),
            notes=order_data.notes
        )
        
        OrdersService._orders_db.append(new_order)
        return new_order
    
    @staticmethod
    def update_order_status(order_id: int, status: str) -> bool:
        """
        Update order status
        """
        order = OrdersService.get_order_by_id(order_id)
        if order:
            order.status = status
            if status == "completed":
                order.completed_at = datetime.now()
            return True
        return False
    
    @staticmethod
    def get_orders_summary() -> Dict[str, Any]:
        """
        Get orders summary statistics
        """
        todays_orders = OrdersService.get_todays_orders()
        active_orders = [order for order in OrdersService._orders_db 
                        if order.status in ["scheduled", "preparing", "in_progress"]]
        
        total_volume_today = sum(order.volume for order in todays_orders)
        total_volume_active = sum(order.volume for order in active_orders)
        
        return {
            "total_orders": len(OrdersService._orders_db),
            "active_orders": len(active_orders),
            "todays_orders": len(todays_orders),
            "total_volume_today": total_volume_today,
            "total_volume_active": total_volume_active,
            "completed_today": len(OrdersService.get_orders_by_status("completed")),
            "urgent_orders": len([order for order in active_orders 
                                if order.priority == "high"])
        }
    
    @staticmethod
    def get_available_projects() -> List[Dict[str, Any]]:
        """
        Get available projects for new orders
        """
        return [project for project in OrdersService._projects_db 
                if project["status"] == "active"]