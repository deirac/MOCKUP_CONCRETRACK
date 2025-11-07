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
            client="Constructora ABC",
            mix_type="C-30",
            volume=45.5,
            status="scheduled",
            scheduled_time=datetime.now() + timedelta(hours=3),
            address="Av. Constructores 123, Zona Industrial",
            priority="high",
            assigned_plant="Planta Central",
            estimated_duration=4.5,
            created_at=datetime.now() - timedelta(days=1),
            notes="Requiere bomba de 42 metros"
        ),
        ConcreteOrder(
            id=2,
            project_id=102,
            project_name="Centro Comercial Plaza",
            client="Desarrolladora XYZ",
            mix_type="C-25",
            volume=28.0,
            status="in_progress",
            scheduled_time=datetime.now(),
            address="Centro Ciudad, Calle Principal 456",
            priority="medium",
            assigned_plant="Planta Sur",
            estimated_duration=3.0,
            created_at=datetime.now() - timedelta(hours=6),
            notes="Coordinación con jefe de obra necesaria"
        ),
        ConcreteOrder(
            id=3,
            project_id=103,
            project_name="Residencial Jardines",
            client="Inmobiliaria Sur",
            mix_type="C-20",
            volume=15.0,
            status="completed",
            scheduled_time=datetime.now() - timedelta(hours=8),
            address="Sector Residencial Norte, Manzana 5",
            priority="low",
            assigned_plant="Planta Este",
            estimated_duration=2.0,
            created_at=datetime.now() - timedelta(days=1),
            notes="Vaciado completado satisfactoriamente"
        ),
        ConcreteOrder(
            id=4,
            project_id=104,
            project_name="Hospital Regional",
            client="Gobierno Estatal",
            mix_type="C-35",
            volume=60.0,
            status="preparing",
            scheduled_time=datetime.now() + timedelta(days=1),
            address="Zona Médica, Av. Salud 789",
            priority="high",
            assigned_plant="Planta Central",
            estimated_duration=6.0,
            created_at=datetime.now() - timedelta(hours=2),
            notes="Concreto especial para cimientos hospitalarios"
        ),
        ConcreteOrder(
            id=5,
            project_id=105,
            project_name="Edificio Corporativo",
            client="Empresa Global S.A.",
            mix_type="C-30",
            volume=35.0,
            status="cancelled",
            scheduled_time=datetime.now() + timedelta(days=2),
            address="Distrito Financiero, Torre B",
            priority="medium",
            assigned_plant="Planta Oeste",
            estimated_duration=4.0,
            created_at=datetime.now() - timedelta(days=3),
            notes="Cancelado por condiciones climáticas"
        )
    ]
    
    # Simple projects list (no need for Project class)
    _projects_db = [
        {"id": 101, "name": "Torre Norte", "client": "Constructora ABC", "location": "Zona Industrial", "start_date": datetime.now() - timedelta(days=30), "status": "active"},
        {"id": 102, "name": "Centro Comercial Plaza", "client": "Desarrolladora XYZ", "location": "Centro Ciudad", "start_date": datetime.now() - timedelta(days=15), "status": "active"},
        {"id": 103, "name": "Residencial Jardines", "client": "Inmobiliaria Sur", "location": "Sector Residencial", "start_date": datetime.now() - timedelta(days=7), "status": "active"},
        {"id": 104, "name": "Hospital Regional", "client": "Gobierno Estatal", "location": "Zona Médica", "start_date": datetime.now() - timedelta(days=45), "status": "active"},
        {"id": 105, "name": "Edificio Corporativo", "client": "Empresa Global S.A.", "location": "Distrito Financiero", "start_date": datetime.now() - timedelta(days=10), "status": "on_hold"},
    ]
    
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