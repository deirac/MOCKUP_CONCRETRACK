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
            name="Planta 1",
            location="VITTRIO",
            capacity=17.0,
            status="active",
            manager="Ing. KJDABJSKDA",
            phone="+1-555-0101",
            email="PLANTA1@concreto.com",
            mixes_available=["C-20", "C-25", "C-30", "C-35"],
            transport="Bombeo",
            last_maintenance=datetime.now() - timedelta(days=15)
        ),
        ConcretePlant(
            id=2,
            name="Planta 2",
            location="VITTRIO",
            capacity=24.0,
            status="active",
            manager="Ing. MANUELA ",
            phone="+1-555-0102",
            email="PLANTA2@concreto.com",
            mixes_available=["C-20", "C-25"],
            transport="Torregrúa",
            last_maintenance=datetime.now() - timedelta(days=30)
        ),
        ConcretePlant(
            id=3,
            name="Planta 3",
            location="VIVALTA",
            capacity=17.0,
            status="maintenance",
            manager="Ing. JUAN PULGARIN",
            phone="+1-555-0103",
            email="PLANTA3@concreto.com",
            mixes_available=["C-20", "C-30"],
            transport="Placing boom",
            last_maintenance=datetime.now() - timedelta(days=5)
        ),
        ConcretePlant(
            id=4,
            name="Planta 4",
            location="N/A",
            capacity=30.0,
            status="inactive",
            manager="SIN REGENTE",
            phone="+1-555-0104",
            email="PLANTA4@concreto.com",
            mixes_available=["C-25", "C-30", "C-35"],
            transport="N/A",
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