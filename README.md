# Engineering AI 🛠️

An intelligent engineering assistant that helps engineers with real-time calculations, design validation, material selection, and technical documentation generation.

## 🎯 Overview

Engineering Copilot is an AI-powered tool that acts as a smart assistant for mechanical, electrical, and civil engineers. It provides instant calculations, validates designs against engineering standards, suggests optimal materials, and generates professional documentation.

## ✨ Features

### 1. **Smart Engineering Calculations**
- Structural analysis (beam deflection, stress, buckling)
- Thermal calculations (heat transfer, thermal expansion)
- Fluid dynamics (flow rates, pressure drops)
- Electrical circuits (voltage, current, power)
- Material properties database

### 2. **Design Validation**
- Safety factor verification
- Standards compliance checking (ASME, AISC, IEC)
- Constraint satisfaction
- Optimization suggestions

### 3. **Material Intelligence**
- Material selection based on requirements
- Cost-performance optimization
- Availability and sourcing information
- Environmental impact analysis

### 4. **Documentation Generator**
- Technical specifications
- Design reports
- Bill of materials (BOM)
- Engineering drawings annotations
- Calculation sheets

### 5. **Interactive Web Interface**
- Real-time calculation updates
- Visual design feedback
- 3D visualization of stress/strain
- Export to PDF/Excel

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web application
python app.py

# Open browser to http://localhost:5000
```

## 💡 Use Cases

### Mechanical Engineering
```python
from copilot import StructuralAnalyzer

# Analyze a cantilever beam
beam = StructuralAnalyzer.cantilever_beam(
    length=2.0,  # meters
    load=1000,   # Newtons
    material="steel_a36",
    cross_section="rectangular",
    width=0.05,
    height=0.1
)

results = beam.analyze()
print(f"Max Deflection: {results.max_deflection} mm")
print(f"Max Stress: {results.max_stress} MPa")
print(f"Safety Factor: {results.safety_factor}")
```

### Material Selection
```python
from copilot import MaterialSelector

# Find best material for high-temperature application
selector = MaterialSelector()
material = selector.recommend(
    max_temperature=500,  # Celsius
    min_strength=400,     # MPa
    max_cost=50,          # USD/kg
    corrosion_resistance="high"
)

print(f"Recommended: {material.name}")
print(f"Properties: {material.properties}")
```

## 🏗️ Architecture

```
engineering-copilot/
├── app.py                  # Flask web application
├── copilot/
│   ├── structural/         # Structural analysis modules
│   ├── thermal/            # Thermal calculations
│   ├── materials/          # Material database & selection
│   ├── standards/          # Engineering standards
│   └── documentation/      # Report generation
├── static/                 # Web UI assets
├── templates/              # HTML templates
└── tests/                  # Test suite
```

## 🎓 Technical Highlights

- **Physics-based calculations**: Real engineering formulas, not approximations
- **Standards compliance**: Built-in ASME, AISC, IEC standards
- **Material database**: 500+ materials with verified properties
- **Optimization algorithms**: Genetic algorithms for design optimization
- **Professional output**: LaTeX-quality documentation generation

## 🔬 Example: Beam Design

The copilot can design a beam to meet your requirements:

```python
from copilot import BeamDesigner

designer = BeamDesigner()
solution = designer.design(
    span=5.0,              # meters
    load=10000,            # N/m (distributed)
    max_deflection=10,     # mm
    material_type="steel",
    optimize_for="cost"
)

print(solution.summary())
# Output:
# Optimal Design:
#   Material: Steel A36
#   Section: W10x49
#   Weight: 245 kg
#   Cost: $367
#   Safety Factor: 2.1
#   Max Deflection: 8.3 mm
```

## 📊 Supported Calculations

### Structural
- Beam analysis (simply supported, cantilever, fixed)
- Column buckling (Euler, Johnson)
- Truss analysis
- Plate bending
- Connection design (bolted, welded)

### Thermal
- Heat conduction (1D, 2D, 3D)
- Convection heat transfer
- Radiation
- Thermal expansion
- Heat exchanger design

### Fluid
- Pipe flow (laminar, turbulent)
- Pressure drop
- Pump sizing
- Valve selection

### Electrical
- Circuit analysis (DC, AC)
- Power calculations
- Wire sizing
- Motor selection

## 🎨 Web Interface

Beautiful, modern web interface with:
- Real-time calculation updates
- Interactive parameter sliders
- Visual feedback (color-coded safety factors)
- 3D stress visualization
- Export to PDF/Excel
- Dark mode support

## 📈 Performance

- Calculations: < 100ms for most analyses
- Material search: < 50ms across 500+ materials
- Report generation: < 2s for complete documentation
- Web interface: 60 FPS animations

## 🤝 Contributing

This is a portfolio project demonstrating engineering software development capabilities.

## 📄 License

MIT License

## 👤 Author

Built to demonstrate full-stack engineering software development skills, combining domain expertise in mechanical engineering with modern software practices.

---

**Empowering engineers with intelligent tools for better, faster design decisions.**
