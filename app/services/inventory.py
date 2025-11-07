from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.schemas.inventory import Material, MaterialUsage

class InventoryService:
    """
    Service class for materials inventory management
    """
    
    # Mock database for materials
    _materials_db = [
        Material(
            id=1,
            name="ARENA",
            description="Arena de río para concreto",
            current_stock=1250.5,  # m³
            min_stock=200.0,
            max_stock=1500.0,
            unit="m³",
            cost_per_unit=45.50,
            supplier="Arenera del Norte S.A.",
            last_restock=datetime.now() - timedelta(days=5),
            status="optimal"
        ),
        Material(
            id=2,
            name="AGUA",
            description="Agua potable para mezcla",
            current_stock=800.0,  # m³
            min_stock=100.0,
            max_stock=1000.0,
            unit="m³",
            cost_per_unit=2.50,
            supplier="Municipalidad Local",
            last_restock=datetime.now() - timedelta(days=1),
            status="optimal"
        ),
        Material(
            id=3,
            name="ADT1",
            description="Aditivo 1 - Acelerante de fraguado",
            current_stock=850.0,  # kg
            min_stock=200.0,
            max_stock=1000.0,
            unit="kg",
            cost_per_unit=15.75,
            supplier="Químicos Constructores",
            last_restock=datetime.now() - timedelta(days=15),
            status="optimal"
        ),
        Material(
            id=4,
            name="ADT2",
            description="Aditivo 2 - Plastificante",
            current_stock=420.5,  # kg
            min_stock=150.0,
            max_stock=800.0,
            unit="kg",
            cost_per_unit=22.30,
            supplier="Químicos Constructores",
            last_restock=datetime.now() - timedelta(days=20),
            status="low"
        ),
        Material(
            id=5,
            name="CMTO",
            description="Cemento Portland Tipo I",
            current_stock=3200.0,  # kg
            min_stock=1000.0,
            max_stock=5000.0,
            unit="kg",
            cost_per_unit=0.35,
            supplier="Cementos Nacionales",
            last_restock=datetime.now() - timedelta(days=3),
            status="optimal"
        ),
        Material(
            id=6,
            name="ADIC",
            description="Aditivo especial - Impermeabilizante",
            current_stock=180.0,  # kg
            min_stock=50.0,
            max_stock=300.0,
            unit="kg",
            cost_per_unit=45.00,
            supplier="Tecnología en Concreto",
            last_restock=datetime.now() - timedelta(days=25),
            status="critical"
        ),
        Material(
            id=7,
            name="GRAVA",
            description="Grava triturada 3/4''",
            current_stock=980.0,  # m³
            min_stock=300.0,
            max_stock=1200.0,
            unit="m³",
            cost_per_unit=65.00,
            supplier="Cantera Central",
            last_restock=datetime.now() - timedelta(days=7),
            status="optimal"
        )
    ]
    
    # Material usage data
    _usage_data = [
        MaterialUsage(
            material_id=1,
            date=datetime.now().date(),
            quantity_used=45.5,
            project="Torre Norte",
            mix_type="C-30"
        ),
        MaterialUsage(
            material_id=2,
            date=datetime.now().date(),
            quantity_used=22.8,
            project="Centro Comercial Plaza",
            mix_type="C-25"
        ),
        MaterialUsage(
            material_id=5,
            date=datetime.now().date(),
            quantity_used=1200.0,
            project="Hospital Regional",
            mix_type="C-35"
        )
    ]
    
    # Material requirements for different mix types (kg per m³ of concrete)
    _mix_requirements = {
        "C-20": {
            "ARENA": 800,  # kg/m³
            "AGUA": 180,   # kg/m³
            "ADT1": 2,     # kg/m³
            "CMTO": 300,   # kg/m³
            "GRAVA": 1100  # kg/m³
        },
        "C-25": {
            "ARENA": 750,
            "AGUA": 175,
            "ADT1": 3,
            "CMTO": 350,
            "GRAVA": 1050
        },
        "C-30": {
            "ARENA": 700,
            "AGUA": 170,
            "ADT1": 4,
            "ADT2": 2,
            "CMTO": 400,
            "GRAVA": 1000
        },
        "C-35": {
            "ARENA": 650,
            "AGUA": 165,
            "ADT1": 5,
            "ADT2": 3,
            "ADIC": 1,
            "CMTO": 450,
            "GRAVA": 950
        }
    }
    
    @staticmethod
    def get_all_materials() -> List[Material]:
        """
        Get all materials
        """
        return InventoryService._materials_db
    
    @staticmethod
    def get_material_by_id(material_id: int) -> Optional[Material]:
        """
        Get material by ID
        """
        return next((material for material in InventoryService._materials_db 
                    if material.id == material_id), None)
    
    @staticmethod
    def get_materials_by_status(status: str) -> List[Material]:
        """
        Get materials by status
        """
        return [material for material in InventoryService._materials_db 
                if material.status == status]
    
    @staticmethod
    def update_material_stock(material_id: int, new_stock: float) -> bool:
        """
        Update material stock and recalculate status
        """
        material = InventoryService.get_material_by_id(material_id)
        if material:
            material.current_stock = new_stock
            # Update status based on stock levels
            stock_percentage = (new_stock / material.max_stock) * 100
            if stock_percentage <= 15:
                material.status = "critical"
            elif stock_percentage <= 30:
                material.status = "low"
            elif stock_percentage <= 80:
                material.status = "optimal"
            else:
                material.status = "high"
            return True
        return False
    
    @staticmethod
    def get_material_usage(material_id: int) -> Optional[Dict[str, Any]]:
        """
        Get material usage statistics
        """
        material = InventoryService.get_material_by_id(material_id)
        if not material:
            return None
        
        # Calculate usage for last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        recent_usage = [usage for usage in InventoryService._usage_data 
                       if usage.material_id == material_id and 
                       usage.date >= week_ago.date()]
        
        total_used = sum(usage.quantity_used for usage in recent_usage)
        avg_daily_usage = total_used / 7 if recent_usage else 0
        
        # Calculate days of stock remaining
        days_remaining = material.current_stock / avg_daily_usage if avg_daily_usage > 0 else float('inf')
        
        return {
            "material": material,
            "total_used_week": total_used,
            "avg_daily_usage": avg_daily_usage,
            "days_remaining": days_remaining,
            "recent_usage": recent_usage
        }
    
    @staticmethod
    def get_inventory_summary() -> Dict[str, Any]:
        """
        Get inventory summary statistics
        """
        total_materials = len(InventoryService._materials_db)
        critical_materials = len(InventoryService.get_materials_by_status("critical"))
        low_materials = len(InventoryService.get_materials_by_status("low"))
        optimal_materials = len(InventoryService.get_materials_by_status("optimal"))
        
        total_inventory_value = sum(
            material.current_stock * material.cost_per_unit 
            for material in InventoryService._materials_db
        )
        
        return {
            "total_materials": total_materials,
            "critical_materials": critical_materials,
            "low_materials": low_materials,
            "optimal_materials": optimal_materials,
            "total_inventory_value": round(total_inventory_value, 2),
            "needs_restock": critical_materials + low_materials
        }
    
    @staticmethod
    def calculate_material_requirements(mix_type: str, volume: float) -> Dict[str, float]:
        """
        Calculate material requirements for a specific mix type and volume
        """
        if mix_type not in InventoryService._mix_requirements:
            return {}
        
        requirements = InventoryService._mix_requirements[mix_type]
        return {material: quantity * volume for material, quantity in requirements.items()}
    
    @staticmethod
    def check_availability(requirements: Dict[str, float]) -> Dict[str, Any]:
        """
        Check if required materials are available in stock
        """
        result = {
            "available": True,
            "missing_materials": [],
            "available_materials": []
        }
        
        for material_name, required_quantity in requirements.items():
            material = next((m for m in InventoryService._materials_db 
                           if m.name == material_name), None)
            
            if material:
                if material.current_stock >= required_quantity:
                    result["available_materials"].append({
                        "name": material_name,
                        "required": required_quantity,
                        "available": material.current_stock,
                        "status": "available"
                    })
                else:
                    result["available"] = False
                    result["missing_materials"].append({
                        "name": material_name,
                        "required": required_quantity,
                        "available": material.current_stock,
                        "deficit": required_quantity - material.current_stock,
                        "status": "insufficient"
                    })
            else:
                result["available"] = False
                result["missing_materials"].append({
                    "name": material_name,
                    "required": required_quantity,
                    "available": 0,
                    "deficit": required_quantity,
                    "status": "not_found"
                })
        
        return result