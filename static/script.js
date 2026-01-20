// Engineering Copilot JavaScript

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        // Add active class to clicked tab
        tab.classList.add('active');

        // Show corresponding content
        const tabName = tab.getAttribute('data-tab');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Beam Analysis
async function analyzeBeam() {
    const data = {
        beam_type: document.getElementById('beam-type').value,
        material: document.getElementById('beam-material').value,
        length: parseFloat(document.getElementById('beam-length').value),
        load: parseFloat(document.getElementById('beam-load').value),
        width: parseFloat(document.getElementById('beam-width').value),
        height: parseFloat(document.getElementById('beam-height').value)
    };

    try {
        const response = await fetch('/api/beam/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            displayBeamResults(result.results);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error analyzing beam: ' + error.message);
    }
}

function displayBeamResults(results) {
    document.getElementById('beam-deflection').textContent = results.max_deflection;
    document.getElementById('beam-stress').textContent = results.max_stress;
    document.getElementById('beam-safety').textContent = results.safety_factor;
    document.getElementById('beam-weight').textContent = results.weight;
    document.getElementById('beam-cost').textContent = results.cost;

    const statusCard = document.getElementById('beam-status');
    const statusValue = statusCard.querySelector('.result-value');

    if (results.is_safe) {
        statusValue.textContent = '✓ SAFE';
        statusCard.classList.add('safe');
        statusCard.classList.remove('unsafe');
    } else {
        statusValue.textContent = '✗ UNSAFE';
        statusCard.classList.add('unsafe');
        statusCard.classList.remove('safe');
    }

    document.getElementById('beam-results').classList.remove('hidden');
}

// Column Analysis
async function analyzeColumn() {
    const data = {
        material: document.getElementById('column-material').value,
        end_condition: document.getElementById('column-end').value,
        length: parseFloat(document.getElementById('column-length').value),
        width: parseFloat(document.getElementById('column-width').value),
        height: parseFloat(document.getElementById('column-height').value)
    };

    try {
        const response = await fetch('/api/column/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            displayColumnResults(result.results);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error analyzing column: ' + error.message);
    }
}

function displayColumnResults(results) {
    document.getElementById('column-load').textContent = results.critical_load_kn;
    document.getElementById('column-slenderness').textContent = results.slenderness_ratio;
    document.getElementById('column-type').textContent = results.is_long_column ? 'Long Column' : 'Short Column';

    document.getElementById('column-results').classList.remove('hidden');
}

// Material Recommendation
async function recommendMaterial() {
    const data = {
        min_strength: document.getElementById('mat-strength').value || null,
        max_cost: document.getElementById('mat-cost').value || null,
        min_temp: document.getElementById('mat-temp').value || null,
        corrosion_resistance: document.getElementById('mat-corrosion').value || null,
        optimize_for: document.getElementById('mat-optimize').value
    };

    // Convert to numbers
    if (data.min_strength) data.min_strength = parseFloat(data.min_strength);
    if (data.max_cost) data.max_cost = parseFloat(data.max_cost);
    if (data.min_temp) data.min_temp = parseFloat(data.min_temp);

    try {
        const response = await fetch('/api/materials/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            displayMaterialResults(result.material);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error finding material: ' + error.message);
    }
}

function displayMaterialResults(material) {
    const card = document.getElementById('material-card');

    card.innerHTML = `
        <div class="material-header">
            <div class="material-name">${material.name}</div>
            <div class="material-grade">${material.grade}</div>
        </div>
        <div class="material-props">
            <div class="prop-item">
                <span class="prop-label">Yield Strength:</span>
                <span class="prop-value">${material.yield_strength} MPa</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Ultimate Strength:</span>
                <span class="prop-value">${material.ultimate_strength} MPa</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Density:</span>
                <span class="prop-value">${material.density} kg/m³</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Cost:</span>
                <span class="prop-value">$${material.cost_per_kg}/kg</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Max Service Temp:</span>
                <span class="prop-value">${material.max_service_temp}°C</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Thermal Conductivity:</span>
                <span class="prop-value">${material.thermal_conductivity} W/(m⋅K)</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Corrosion Resistance:</span>
                <span class="prop-value">${material.corrosion_resistance}</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Machinability:</span>
                <span class="prop-value">${material.machinability}</span>
            </div>
            <div class="prop-item">
                <span class="prop-label">Weldability:</span>
                <span class="prop-value">${material.weldability}</span>
            </div>
        </div>
    `;

    document.getElementById('material-results').classList.remove('hidden');
}
