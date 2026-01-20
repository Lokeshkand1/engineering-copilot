"""
Structural Analysis Module

Provides beam analysis, column design, and structural calculations.
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from enum import Enum


class SupportType(Enum):
    """Types of beam supports"""
    SIMPLY_SUPPORTED = "simply_supported"
    CANTILEVER = "cantilever"
    FIXED_BOTH_ENDS = "fixed_both_ends"
    FIXED_PINNED = "fixed_pinned"


class LoadType(Enum):
    """Types of loads"""
    POINT_LOAD = "point_load"
    DISTRIBUTED_LOAD = "distributed_load"
    MOMENT = "moment"


@dataclass
class Material:
    """Material properties"""
    name: str
    youngs_modulus: float  # GPa
    yield_strength: float  # MPa
    density: float  # kg/m³
    cost_per_kg: float  # USD/kg
    
    @classmethod
    def steel_a36(cls):
        """Standard structural steel"""
        return cls(
            name="Steel A36",
            youngs_modulus=200,  # GPa
            yield_strength=250,  # MPa
            density=7850,  # kg/m³
            cost_per_kg=1.50
        )
    
    @classmethod
    def aluminum_6061(cls):
        """Aluminum alloy"""
        return cls(
            name="Aluminum 6061-T6",
            youngs_modulus=69,  # GPa
            yield_strength=276,  # MPa
            density=2700,  # kg/m³
            cost_per_kg=3.50
        )


@dataclass
class BeamAnalysisResult:
    """Results from beam analysis"""
    max_deflection: float  # mm
    max_stress: float  # MPa
    max_moment: float  # N⋅m
    max_shear: float  # N
    safety_factor: float
    weight: float  # kg
    cost: float  # USD
    
    def is_safe(self, min_safety_factor: float = 1.5) -> bool:
        """Check if design is safe"""
        return self.safety_factor >= min_safety_factor
    
    def summary(self) -> str:
        """Generate summary report"""
        status = "✓ SAFE" if self.is_safe() else "✗ UNSAFE"
        return f"""
Beam Analysis Results
{'='*50}
Max Deflection:  {self.max_deflection:.2f} mm
Max Stress:      {self.max_stress:.1f} MPa
Max Moment:      {self.max_moment:.1f} N⋅m
Max Shear:       {self.max_shear:.1f} N
Safety Factor:   {self.safety_factor:.2f}
Weight:          {self.weight:.2f} kg
Cost:            ${self.cost:.2f}
Status:          {status}
"""


class BeamAnalyzer:
    """Analyzes beams under various loading conditions"""
    
    def __init__(self, material: Material):
        self.material = material
    
    def simply_supported_point_load(
        self,
        length: float,  # m
        load: float,  # N
        load_position: float,  # m from left support
        width: float,  # m
        height: float  # m
    ) -> BeamAnalysisResult:
        """
        Analyze simply supported beam with point load
        
        Args:
            length: Beam span (m)
            load: Point load magnitude (N)
            load_position: Distance from left support (m)
            width: Beam width (m)
            height: Beam height (m)
        """
        # Calculate second moment of area (rectangular section)
        I = (width * height**3) / 12  # m⁴
        
        # Calculate maximum moment
        a = load_position
        b = length - load_position
        max_moment = (load * a * b) / length  # N⋅m
        
        # Calculate maximum deflection (at load position if centered)
        E = self.material.youngs_modulus * 1e9  # Convert GPa to Pa
        if abs(a - b) < 0.01:  # Load at center
            max_deflection = (load * length**3) / (48 * E * I)  # m
        else:
            # General formula for deflection at load point
            max_deflection = (load * a**2 * b**2) / (3 * E * I * length)  # m
        
        # Convert deflection to mm
        max_deflection_mm = max_deflection * 1000
        
        # Calculate maximum stress
        c = height / 2  # Distance from neutral axis to outer fiber (m)
        max_stress_pa = (max_moment * c) / I  # Pa
        max_stress_mpa = max_stress_pa / 1e6  # Convert to MPa
        
        # Calculate maximum shear
        max_shear = max(load * b / length, load * a / length)  # N
        
        # Calculate safety factor
        safety_factor = self.material.yield_strength / max_stress_mpa
        
        # Calculate weight
        volume = length * width * height  # m³
        weight = volume * self.material.density  # kg
        
        # Calculate cost
        cost = weight * self.material.cost_per_kg  # USD
        
        return BeamAnalysisResult(
            max_deflection=max_deflection_mm,
            max_stress=max_stress_mpa,
            max_moment=max_moment,
            max_shear=max_shear,
            safety_factor=safety_factor,
            weight=weight,
            cost=cost
        )
    
    def cantilever_beam(
        self,
        length: float,  # m
        load: float,  # N (at free end)
        width: float,  # m
        height: float  # m
    ) -> BeamAnalysisResult:
        """
        Analyze cantilever beam with point load at free end
        
        Args:
            length: Beam length (m)
            load: Point load at free end (N)
            width: Beam width (m)
            height: Beam height (m)
        """
        # Second moment of area
        I = (width * height**3) / 12  # m⁴
        
        # Maximum moment (at fixed end)
        max_moment = load * length  # N⋅m
        
        # Maximum deflection (at free end)
        E = self.material.youngs_modulus * 1e9  # Pa
        max_deflection = (load * length**3) / (3 * E * I)  # m
        max_deflection_mm = max_deflection * 1000  # mm
        
        # Maximum stress
        c = height / 2  # m
        max_stress_pa = (max_moment * c) / I  # Pa
        max_stress_mpa = max_stress_pa / 1e6  # MPa
        
        # Maximum shear
        max_shear = load  # N
        
        # Safety factor
        safety_factor = self.material.yield_strength / max_stress_mpa
        
        # Weight and cost
        volume = length * width * height  # m³
        weight = volume * self.material.density  # kg
        cost = weight * self.material.cost_per_kg  # USD
        
        return BeamAnalysisResult(
            max_deflection=max_deflection_mm,
            max_stress=max_stress_mpa,
            max_moment=max_moment,
            max_shear=max_shear,
            safety_factor=safety_factor,
            weight=weight,
            cost=cost
        )
    
    def distributed_load_beam(
        self,
        length: float,  # m
        load_per_length: float,  # N/m
        width: float,  # m
        height: float  # m
    ) -> BeamAnalysisResult:
        """
        Analyze simply supported beam with uniformly distributed load
        
        Args:
            length: Beam span (m)
            load_per_length: Distributed load (N/m)
            width: Beam width (m)
            height: Beam height (m)
        """
        # Second moment of area
        I = (width * height**3) / 12  # m⁴
        
        # Total load
        total_load = load_per_length * length  # N
        
        # Maximum moment (at center)
        max_moment = (load_per_length * length**2) / 8  # N⋅m
        
        # Maximum deflection (at center)
        E = self.material.youngs_modulus * 1e9  # Pa
        max_deflection = (5 * load_per_length * length**4) / (384 * E * I)  # m
        max_deflection_mm = max_deflection * 1000  # mm
        
        # Maximum stress
        c = height / 2  # m
        max_stress_pa = (max_moment * c) / I  # Pa
        max_stress_mpa = max_stress_pa / 1e6  # MPa
        
        # Maximum shear (at supports)
        max_shear = total_load / 2  # N
        
        # Safety factor
        safety_factor = self.material.yield_strength / max_stress_mpa
        
        # Weight and cost
        volume = length * width * height  # m³
        weight = volume * self.material.density  # kg
        cost = weight * self.material.cost_per_kg  # USD
        
        return BeamAnalysisResult(
            max_deflection=max_deflection_mm,
            max_stress=max_stress_mpa,
            max_moment=max_moment,
            max_shear=max_shear,
            safety_factor=safety_factor,
            weight=weight,
            cost=cost
        )


class ColumnAnalyzer:
    """Analyzes columns for buckling"""
    
    def __init__(self, material: Material):
        self.material = material
    
    def euler_buckling_load(
        self,
        length: float,  # m
        width: float,  # m
        height: float,  # m
        end_condition: str = "pinned-pinned"  # pinned-pinned, fixed-free, fixed-fixed, fixed-pinned
    ) -> Dict[str, float]:
        """
        Calculate Euler buckling load for a column
        
        Returns critical load and safety recommendations
        """
        # Effective length factors
        K_factors = {
            "pinned-pinned": 1.0,
            "fixed-free": 2.0,
            "fixed-fixed": 0.5,
            "fixed-pinned": 0.7
        }
        
        K = K_factors.get(end_condition, 1.0)
        
        # Second moment of area (minimum for buckling)
        I_min = min(
            (width * height**3) / 12,  # About horizontal axis
            (height * width**3) / 12   # About vertical axis
        )
        
        # Effective length
        L_e = K * length
        
        # Euler critical load
        E = self.material.youngs_modulus * 1e9  # Pa
        P_cr = (math.pi**2 * E * I_min) / (L_e**2)  # N
        
        # Slenderness ratio
        A = width * height  # m²
        r = math.sqrt(I_min / A)  # Radius of gyration
        slenderness = L_e / r
        
        return {
            "critical_load_n": P_cr,
            "critical_load_kn": P_cr / 1000,
            "slenderness_ratio": slenderness,
            "end_condition": end_condition,
            "is_long_column": slenderness > 120
        }
