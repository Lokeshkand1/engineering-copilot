"""
Material Database and Selection Module

Comprehensive material properties and intelligent selection algorithms.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class MaterialCategory(Enum):
    """Material categories"""
    METAL = "metal"
    POLYMER = "polymer"
    CERAMIC = "ceramic"
    COMPOSITE = "composite"


@dataclass
class MaterialProperties:
    """Comprehensive material properties"""
    # Identification
    name: str
    category: MaterialCategory
    grade: str
    
    # Mechanical Properties
    youngs_modulus: float  # GPa
    yield_strength: float  # MPa
    ultimate_strength: float  # MPa
    poissons_ratio: float
    density: float  # kg/m³
    hardness: Optional[float] = None  # HB (Brinell)
    
    # Thermal Properties
    thermal_conductivity: float = 0.0  # W/(m⋅K)
    thermal_expansion: float = 0.0  # 1/K (×10⁻⁶)
    max_service_temp: float = 0.0  # °C
    melting_point: Optional[float] = None  # °C
    
    # Cost & Availability
    cost_per_kg: float = 0.0  # USD/kg
    availability: str = "common"  # common, moderate, rare
    
    # Corrosion & Environment
    corrosion_resistance: str = "moderate"  # poor, moderate, good, excellent
    
    # Manufacturability
    machinability: str = "moderate"  # poor, moderate, good, excellent
    weldability: str = "moderate"  # poor, moderate, good, excellent
    
    def __str__(self) -> str:
        return f"{self.name} ({self.grade})"


class MaterialDatabase:
    """Database of engineering materials"""
    
    def __init__(self):
        self.materials: List[MaterialProperties] = []
        self._load_materials()
    
    def _load_materials(self):
        """Load material database"""
        
        # Structural Steels
        self.materials.extend([
            MaterialProperties(
                name="Steel A36",
                category=MaterialCategory.METAL,
                grade="ASTM A36",
                youngs_modulus=200,
                yield_strength=250,
                ultimate_strength=400,
                poissons_ratio=0.26,
                density=7850,
                hardness=119,
                thermal_conductivity=51.9,
                thermal_expansion=11.7,
                max_service_temp=425,
                melting_point=1510,
                cost_per_kg=1.50,
                availability="common",
                corrosion_resistance="poor",
                machinability="good",
                weldability="excellent"
            ),
            MaterialProperties(
                name="Steel 4140",
                category=MaterialCategory.METAL,
                grade="AISI 4140",
                youngs_modulus=205,
                yield_strength=415,
                ultimate_strength=655,
                poissons_ratio=0.29,
                density=7850,
                hardness=197,
                thermal_conductivity=42.6,
                thermal_expansion=12.3,
                max_service_temp=425,
                melting_point=1416,
                cost_per_kg=2.20,
                availability="common",
                corrosion_resistance="moderate",
                machinability="moderate",
                weldability="good"
            ),
            MaterialProperties(
                name="Stainless Steel 304",
                category=MaterialCategory.METAL,
                grade="AISI 304",
                youngs_modulus=193,
                yield_strength=215,
                ultimate_strength=505,
                poissons_ratio=0.29,
                density=8000,
                hardness=123,
                thermal_conductivity=16.2,
                thermal_expansion=17.3,
                max_service_temp=870,
                melting_point=1450,
                cost_per_kg=4.50,
                availability="common",
                corrosion_resistance="excellent",
                machinability="moderate",
                weldability="excellent"
            ),
        ])
        
        # Aluminum Alloys
        self.materials.extend([
            MaterialProperties(
                name="Aluminum 6061-T6",
                category=MaterialCategory.METAL,
                grade="AA 6061-T6",
                youngs_modulus=69,
                yield_strength=276,
                ultimate_strength=310,
                poissons_ratio=0.33,
                density=2700,
                hardness=95,
                thermal_conductivity=167,
                thermal_expansion=23.6,
                max_service_temp=200,
                melting_point=582,
                cost_per_kg=3.50,
                availability="common",
                corrosion_resistance="good",
                machinability="excellent",
                weldability="good"
            ),
            MaterialProperties(
                name="Aluminum 7075-T6",
                category=MaterialCategory.METAL,
                grade="AA 7075-T6",
                youngs_modulus=71.7,
                yield_strength=503,
                ultimate_strength=572,
                poissons_ratio=0.33,
                density=2810,
                hardness=150,
                thermal_conductivity=130,
                thermal_expansion=23.4,
                max_service_temp=175,
                melting_point=477,
                cost_per_kg=5.00,
                availability="common",
                corrosion_resistance="moderate",
                machinability="good",
                weldability="poor"
            ),
        ])
        
        # Titanium Alloys
        self.materials.append(
            MaterialProperties(
                name="Titanium Ti-6Al-4V",
                category=MaterialCategory.METAL,
                grade="Grade 5",
                youngs_modulus=113.8,
                yield_strength=880,
                ultimate_strength=950,
                poissons_ratio=0.342,
                density=4430,
                hardness=334,
                thermal_conductivity=6.7,
                thermal_expansion=8.6,
                max_service_temp=400,
                melting_point=1660,
                cost_per_kg=35.00,
                availability="moderate",
                corrosion_resistance="excellent",
                machinability="poor",
                weldability="moderate"
            )
        )
        
        # Polymers
        self.materials.extend([
            MaterialProperties(
                name="ABS Plastic",
                category=MaterialCategory.POLYMER,
                grade="Standard",
                youngs_modulus=2.3,
                yield_strength=40,
                ultimate_strength=45,
                poissons_ratio=0.35,
                density=1050,
                thermal_conductivity=0.25,
                thermal_expansion=90,
                max_service_temp=80,
                cost_per_kg=2.50,
                availability="common",
                corrosion_resistance="excellent",
                machinability="excellent",
                weldability="poor"
            ),
            MaterialProperties(
                name="Nylon 6/6",
                category=MaterialCategory.POLYMER,
                grade="PA66",
                youngs_modulus=2.9,
                yield_strength=75,
                ultimate_strength=85,
                poissons_ratio=0.39,
                density=1140,
                thermal_conductivity=0.25,
                thermal_expansion=80,
                max_service_temp=120,
                cost_per_kg=3.00,
                availability="common",
                corrosion_resistance="excellent",
                machinability="good",
                weldability="poor"
            ),
        ])
    
    def search(
        self,
        min_strength: Optional[float] = None,
        max_cost: Optional[float] = None,
        min_temp: Optional[float] = None,
        category: Optional[MaterialCategory] = None,
        corrosion_resistance: Optional[str] = None
    ) -> List[MaterialProperties]:
        """
        Search materials based on criteria
        
        Args:
            min_strength: Minimum yield strength (MPa)
            max_cost: Maximum cost per kg (USD)
            min_temp: Minimum service temperature (°C)
            category: Material category
            corrosion_resistance: Required corrosion resistance level
        """
        results = self.materials.copy()
        
        if min_strength is not None:
            results = [m for m in results if m.yield_strength >= min_strength]
        
        if max_cost is not None:
            results = [m for m in results if m.cost_per_kg <= max_cost]
        
        if min_temp is not None:
            results = [m for m in results if m.max_service_temp >= min_temp]
        
        if category is not None:
            results = [m for m in results if m.category == category]
        
        if corrosion_resistance is not None:
            resistance_levels = ["poor", "moderate", "good", "excellent"]
            min_level = resistance_levels.index(corrosion_resistance)
            results = [
                m for m in results 
                if resistance_levels.index(m.corrosion_resistance) >= min_level
            ]
        
        return results
    
    def get_by_name(self, name: str) -> Optional[MaterialProperties]:
        """Get material by name"""
        for material in self.materials:
            if material.name.lower() == name.lower():
                return material
        return None


class MaterialSelector:
    """Intelligent material selection"""
    
    def __init__(self):
        self.db = MaterialDatabase()
    
    def recommend(
        self,
        min_strength: Optional[float] = None,
        max_cost: Optional[float] = None,
        min_temp: Optional[float] = None,
        corrosion_resistance: Optional[str] = None,
        optimize_for: str = "cost"  # cost, weight, strength
    ) -> Optional[MaterialProperties]:
        """
        Recommend best material based on requirements
        
        Args:
            min_strength: Minimum yield strength (MPa)
            max_cost: Maximum cost per kg (USD)
            min_temp: Minimum service temperature (°C)
            corrosion_resistance: Required corrosion resistance
            optimize_for: Optimization criterion (cost, weight, strength)
        """
        # Search for matching materials
        candidates = self.db.search(
            min_strength=min_strength,
            max_cost=max_cost,
            min_temp=min_temp,
            corrosion_resistance=corrosion_resistance
        )
        
        if not candidates:
            return None
        
        # Optimize based on criterion
        if optimize_for == "cost":
            return min(candidates, key=lambda m: m.cost_per_kg)
        elif optimize_for == "weight":
            return min(candidates, key=lambda m: m.density)
        elif optimize_for == "strength":
            return max(candidates, key=lambda m: m.yield_strength)
        else:
            return candidates[0]
    
    def compare(self, material_names: List[str]) -> Dict[str, MaterialProperties]:
        """Compare multiple materials"""
        comparison = {}
        for name in material_names:
            material = self.db.get_by_name(name)
            if material:
                comparison[name] = material
        return comparison
