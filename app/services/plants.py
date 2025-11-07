from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.schemas.plants import ConcretePlant, PlantProduction

class PlantsService:
    """
    Service class for concrete plants management
    """
    
    # Mock database for concrete plants
    _plants_db = [
        ConcretePlant(
            id=1,
            name="Planta Central",
            location="Zona Industrial Norte",
            capacity=120.0,
            status="active",
            manager="Ing. Carlos Rodríguez",
            phone="+1-555-0101",
            email="central@concreto.com",
            mixes_available=["C-20", "C-25", "C-30", "C-35"],
            trucks_available=8,
            last_maintenance=datetime.now() - timedelta(days=15)
        ),
        ConcretePlant(
            id=2,
            name="Planta Sur",
            location="Av. Constructores 456",
            capacity=80.0,
            status="active",
            manager="Ing. María González",
            phone="+1-555-0102",
            email="sur@concreto.com",
            mixes_available=["C-20", "C-25"],
            trucks_available=5,
            last_maintenance=datetime.now() - timedelta(days=30)
        ),
        ConcretePlant(
            id=3,
            name="Planta Este",
            location="Polígono Industrial Este",
            capacity=60.0,
            status="maintenance",
            manager="Ing. Roberto Silva",
            phone="+1-555-0103",
            email="este@concreto.com",
            mixes_available=["C-20", "C-30"],
            trucks_available=3,
            last_maintenance=datetime.now() - timedelta(days=5)
        ),
        ConcretePlant(
            id=4,
            name="Planta Oeste",
            location="Carretera Nacional Km 12",
            capacity=100.0,
            status="active",
            manager="Ing. Laura Mendoza",
            phone="+1-555-0104",
            email="oeste@concreto.com",
            mixes_available=["C-25", "C-30", "C-35"],
            trucks_available=6,
            last_maintenance=datetime.now() - timedelta(days=45)
        )
    ]
    
    # Production data
    _production_data = [
        PlantProduction(
            plant_id=1,
            date=datetime.now().date(),
            total_production=450.5,
            mixes_produced={
                "C-20": 120.0,
                "C-25": 180.5,
                "C-30": 100.0,
                "C-35": 50.0
            },
            trucks_dispatched=22
        ),
        PlantProduction(
            plant_id=2,
            date=datetime.now().date(),
            total_production=320.0,
            mixes_produced={
                "C-20": 200.0,
                "C-25": 120.0
            },
            trucks_dispatched=18
        )
    ]
    
    @staticmethod
    def get_all_plants() -> List[ConcretePlant]:
        """
        Get all concrete plants
        """
        return PlantsService._plants_db
    
    @staticmethod
    def get_plant_by_id(plant_id: int) -> Optional[ConcretePlant]:
        """
        Get plant by ID
        """
        return next((plant for plant in PlantsService._plants_db 
                    if plant.id == plant_id), None)
    
    @staticmethod
    def get_active_plants() -> List[ConcretePlant]:
        """
        Get only active plants
        """
        return [plant for plant in PlantsService._plants_db 
                if plant.status == "active"]
    
    @staticmethod
    def get_plants_by_status(status: str) -> List[ConcretePlant]:
        """
        Get plants by status
        """
        return [plant for plant in PlantsService._plants_db 
                if plant.status == status]
    
    @staticmethod
    def get_production_data(plant_id: int) -> Optional[PlantProduction]:
        """
        Get production data for a plant
        """
        return next((prod for prod in PlantsService._production_data 
                    if prod.plant_id == plant_id), None)
    
    @staticmethod
    def get_plants_summary() -> Dict[str, Any]:
        """
        Get plants summary statistics
        """
        active_plants = PlantsService.get_active_plants()
        total_capacity = sum(plant.capacity for plant in PlantsService._plants_db)
        available_trucks = sum(plant.trucks_available for plant in active_plants)
        
        return {
            "total_plants": len(PlantsService._plants_db),
            "active_plants": len(active_plants),
            "total_capacity": total_capacity,
            "available_trucks": available_trucks,
            "maintenance_plants": len(PlantsService.get_plants_by_status("maintenance"))
        }
    
    @staticmethod
    def update_plant_status(plant_id: int, status: str) -> bool:
        """
        Update plant status
        """
        plant = PlantsService.get_plant_by_id(plant_id)
        if plant:
            plant.status = status
            return True
        return False