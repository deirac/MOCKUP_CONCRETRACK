from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.models.schemas.home import ConcreteOrder, ConcreteMix, Project, Client

class HomeService:
    """
    Service class for concrete pouring system dashboard data and business logic
    """
    
    @staticmethod
    def get_dashboard_data() -> Dict[str, Any]:
        """
        Get dashboard data for the concrete pouring system
        """
        active_orders = HomeService._get_active_orders()
        recent_projects = HomeService._get_recent_projects()
        concrete_mixes = HomeService._get_concrete_mixes()
        
        return {
            "active_orders": len(active_orders),
            "completed_orders_today": HomeService._get_completed_orders_today(),
            "total_projects": len(recent_projects),
            "concrete_volume_today": HomeService._calculate_volume_today(active_orders),
            "pending_deliveries": HomeService._get_pending_deliveries_count(),
            "available_mixes": len(concrete_mixes),
            "revenue_today": HomeService._calculate_revenue_today(active_orders),
            "upcoming_schedules": HomeService._get_upcoming_schedules()
        }
    
    @staticmethod
    def _get_active_orders() -> List[ConcreteOrder]:
        """
        Get active concrete orders
        """
        return [
            ConcreteOrder(
                id=1,
                project_id=101,
                mix_type="C-25",
                volume=15.5,
                status="scheduled",
                scheduled_time=datetime.now() + timedelta(hours=2),
                address="Av. Constructores 123"
            ),
            ConcreteOrder(
                id=2,
                project_id=102,
                mix_type="C-30",
                volume=22.0,
                status="in_progress",
                scheduled_time=datetime.now(),
                address="Calle Obreros 456"
            ),
            ConcreteOrder(
                id=3,
                project_id=103,
                mix_type="C-20",
                volume=8.5,
                status="preparing",
                scheduled_time=datetime.now() + timedelta(hours=1),
                address="Via Cemento 789"
            )
        ]
    
    @staticmethod
    def _get_recent_projects() -> List[Project]:
        """
        Get recent projects
        """
        return [
            Project(
                id=101,
                name="Torre Norte",
                client="Constructora ABC",
                location="Zona Industrial",
                start_date=datetime.now() - timedelta(days=30),
                status="active"
            ),
            Project(
                id=102,
                name="Centro Comercial Plaza",
                client="Desarrolladora XYZ",
                location="Centro Ciudad",
                start_date=datetime.now() - timedelta(days=15),
                status="active"
            ),
            Project(
                id=103,
                name="Residencial Jardines",
                client="Inmobiliaria Sur",
                location="Sector Residencial",
                start_date=datetime.now() - timedelta(days=7),
                status="active"
            )
        ]
    
    @staticmethod
    def _get_concrete_mixes() -> List[ConcreteMix]:
        """
        Get available concrete mixes
        """
        return [
            ConcreteMix(
                code="C-20",
                name="Concreto Normal",
                strength=20,
                price_per_m3=85.00,
                available=True
            ),
            ConcreteMix(
                code="C-25",
                name="Concreto Estructural",
                strength=25,
                price_per_m3=95.00,
                available=True
            ),
            ConcreteMix(
                code="C-30",
                name="Concreto High-Strength",
                strength=30,
                price_per_m3=110.00,
                available=True
            ),
            ConcreteMix(
                code="C-35",
                name="Concreto Premium",
                strength=35,
                price_per_m3=125.00,
                available=False
            )
        ]
    
    @staticmethod
    def _get_completed_orders_today() -> int:
        """
        Get number of completed orders today
        """
        return 12
    
    @staticmethod
    def _calculate_volume_today(orders: List[ConcreteOrder]) -> float:
        """
        Calculate total concrete volume for today's orders
        """
        return sum(order.volume for order in orders)
    
    @staticmethod
    def _get_pending_deliveries_count() -> int:
        """
        Get count of pending deliveries
        """
        return 5
    
    @staticmethod
    def _calculate_revenue_today(orders: List[ConcreteOrder]) -> float:
        """
        Calculate estimated revenue for today
        """
        mix_prices = {
            "C-20": 85.00,
            "C-25": 95.00,
            "C-30": 110.00,
            "C-35": 125.00
        }
        
        return sum(order.volume * mix_prices.get(order.mix_type, 100.00) 
                  for order in orders)
    
    @staticmethod
    def _get_upcoming_schedules() -> int:
        """
        Get number of upcoming schedules for next 24 hours
        """
        return 8
    
    @staticmethod
    def get_todays_schedule() -> List[Dict[str, Any]]:
        """
        Get today's concrete pouring schedule
        """
        active_orders = HomeService._get_active_orders()
        
        schedule = []
        for order in active_orders:
            project = next(
                (p for p in HomeService._get_recent_projects() 
                 if p.id == order.project_id), 
                None
            )
            
            if project:
                schedule.append({
                    "order_id": order.id,
                    "project_name": project.name,
                    "client": project.client,
                    "mix_type": order.mix_type,
                    "volume": order.volume,
                    "scheduled_time": order.scheduled_time.strftime("%H:%M"),
                    "status": order.status,
                    "address": order.address
                })
        
        return sorted(schedule, key=lambda x: x["scheduled_time"])
    
    @staticmethod
    def get_concrete_stats() -> Dict[str, Any]:
        """
        Get concrete production statistics
        """
        return {
            "monthly_volume": 450.5,
            "monthly_revenue": 42500.75,
            "avg_delivery_time": "2.5 horas",
            "completion_rate": 94.5,
            "active_trucks": 8,
            "available_pumps": 3
        }