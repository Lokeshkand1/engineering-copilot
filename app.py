"""
Engineering Copilot Web Application

Flask-based web interface for engineering calculations and design assistance.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

from copilot.structural import BeamAnalyzer, ColumnAnalyzer, Material
from copilot.materials import MaterialSelector, MaterialDatabase

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/beam/analyze', methods=['POST'])
def analyze_beam():
    """Analyze beam structure"""
    try:
        data = request.json
        
        # Get material
        material_name = data.get('material', 'steel_a36')
        if material_name == 'steel_a36':
            material = Material.steel_a36()
        elif material_name == 'aluminum_6061':
            material = Material.aluminum_6061()
        else:
            material = Material.steel_a36()
        
        # Create analyzer
        analyzer = BeamAnalyzer(material)
        
        # Get beam type and parameters
        beam_type = data.get('beam_type', 'simply_supported')
        length = float(data.get('length', 2.0))
        load = float(data.get('load', 1000))
        width = float(data.get('width', 0.05))
        height = float(data.get('height', 0.1))
        
        # Analyze based on type
        if beam_type == 'cantilever':
            result = analyzer.cantilever_beam(length, load, width, height)
        elif beam_type == 'distributed':
            result = analyzer.distributed_load_beam(load, width, height)
        else:  # simply_supported
            load_position = float(data.get('load_position', length / 2))
            result = analyzer.simply_supported_point_load(
                length, load, load_position, width, height
            )
        
        # Return results
        return jsonify({
            'success': True,
            'results': {
                'max_deflection': round(result.max_deflection, 3),
                'max_stress': round(result.max_stress, 2),
                'max_moment': round(result.max_moment, 2),
                'max_shear': round(result.max_shear, 2),
                'safety_factor': round(result.safety_factor, 2),
                'weight': round(result.weight, 3),
                'cost': round(result.cost, 2),
                'is_safe': result.is_safe(),
                'summary': result.summary()
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/column/analyze', methods=['POST'])
def analyze_column():
    """Analyze column buckling"""
    try:
        data = request.json
        
        # Get material
        material_name = data.get('material', 'steel_a36')
        if material_name == 'steel_a36':
            material = Material.steel_a36()
        elif material_name == 'aluminum_6061':
            material = Material.aluminum_6061()
        else:
            material = Material.steel_a36()
        
        # Create analyzer
        analyzer = ColumnAnalyzer(material)
        
        # Get parameters
        length = float(data.get('length', 3.0))
        width = float(data.get('width', 0.1))
        height = float(data.get('height', 0.1))
        end_condition = data.get('end_condition', 'pinned-pinned')
        
        # Analyze
        result = analyzer.euler_buckling_load(length, width, height, end_condition)
        
        return jsonify({
            'success': True,
            'results': {
                'critical_load_kn': round(result['critical_load_kn'], 2),
                'slenderness_ratio': round(result['slenderness_ratio'], 2),
                'end_condition': result['end_condition'],
                'is_long_column': result['is_long_column']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/materials/search', methods=['POST'])
def search_materials():
    """Search for materials"""
    try:
        data = request.json
        
        db = MaterialDatabase()
        
        # Get search criteria
        min_strength = data.get('min_strength')
        max_cost = data.get('max_cost')
        min_temp = data.get('min_temp')
        corrosion = data.get('corrosion_resistance')
        
        # Search
        results = db.search(
            min_strength=min_strength,
            max_cost=max_cost,
            min_temp=min_temp,
            corrosion_resistance=corrosion
        )
        
        # Format results
        materials = []
        for mat in results:
            materials.append({
                'name': mat.name,
                'grade': mat.grade,
                'yield_strength': mat.yield_strength,
                'density': mat.density,
                'cost_per_kg': mat.cost_per_kg,
                'max_service_temp': mat.max_service_temp,
                'corrosion_resistance': mat.corrosion_resistance,
                'machinability': mat.machinability
            })
        
        return jsonify({
            'success': True,
            'count': len(materials),
            'materials': materials
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/materials/recommend', methods=['POST'])
def recommend_material():
    """Get material recommendation"""
    try:
        data = request.json
        
        selector = MaterialSelector()
        
        # Get criteria
        min_strength = data.get('min_strength')
        max_cost = data.get('max_cost')
        min_temp = data.get('min_temp')
        corrosion = data.get('corrosion_resistance')
        optimize_for = data.get('optimize_for', 'cost')
        
        # Get recommendation
        material = selector.recommend(
            min_strength=min_strength,
            max_cost=max_cost,
            min_temp=min_temp,
            corrosion_resistance=corrosion,
            optimize_for=optimize_for
        )
        
        if material:
            return jsonify({
                'success': True,
                'material': {
                    'name': material.name,
                    'grade': material.grade,
                    'yield_strength': material.yield_strength,
                    'ultimate_strength': material.ultimate_strength,
                    'density': material.density,
                    'cost_per_kg': material.cost_per_kg,
                    'max_service_temp': material.max_service_temp,
                    'thermal_conductivity': material.thermal_conductivity,
                    'corrosion_resistance': material.corrosion_resistance,
                    'machinability': material.machinability,
                    'weldability': material.weldability
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No materials found matching criteria'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print("🚀 Engineering Copilot starting...")
    print("📊 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
