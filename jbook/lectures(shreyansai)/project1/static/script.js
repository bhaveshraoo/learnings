document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('predictionForm');
    const oldpeakSlider = document.getElementById('Oldpeak');
    const oldpeakVal = document.getElementById('oldpeakVal');
    const resetBtn = document.getElementById('resetFormBtn');
    
    // View States
    const placeholderState = document.getElementById('placeholderState');
    const loadingState = document.getElementById('loadingState');
    const outputState = document.getElementById('outputState');
    const resultsCard = document.getElementById('resultsCard');
    
    // Output Elements
    const statusBanner = document.getElementById('statusBanner');
    const statusIcon = document.getElementById('statusIcon');
    const riskTitle = document.getElementById('riskTitle');
    const riskScorePct = document.getElementById('riskScorePct');
    const ringVal = document.getElementById('ringVal');
    const lowProbText = document.getElementById('lowProbText');
    const highProbText = document.getElementById('highProbText');
    const obsList = document.getElementById('obsList');
    const neighborsPills = document.getElementById('neighborsPills');
    
    // Demo Preset Chips
    const presetChips = document.querySelectorAll('.preset-chip');

    const presets = {
        low_risk: {
            Age: 40, Sex: 'M', ChestPainType: 'ATA', RestingBP: 120,
            Cholesterol: 210, FastingBS: '0', RestingECG: 'Normal',
            MaxHR: 172, ExerciseAngina: 'N', Oldpeak: '0.0', ST_Slope: 'Up'
        },
        moderate_risk: {
            Age: 52, Sex: 'F', ChestPainType: 'NAP', RestingBP: 135,
            Cholesterol: 230, FastingBS: '0', RestingECG: 'Normal',
            MaxHR: 142, ExerciseAngina: 'N', Oldpeak: '1.0', ST_Slope: 'Flat'
        },
        high_risk: {
            Age: 63, Sex: 'M', ChestPainType: 'ASY', RestingBP: 160,
            Cholesterol: 288, FastingBS: '1', RestingECG: 'ST',
            MaxHR: 108, ExerciseAngina: 'Y', Oldpeak: '2.5', ST_Slope: 'Flat'
        }
    };

    // Slider display update
    oldpeakSlider.addEventListener('input', (e) => {
        oldpeakVal.textContent = `${parseFloat(e.target.value).toFixed(1)} mm`;
    });

    // Preset chip click handlers
    presetChips.forEach(chip => {
        chip.addEventListener('click', (e) => {
            e.preventDefault();
            presetChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            const key = chip.getAttribute('data-preset');
            if (presets[key]) {
                loadPreset(presets[key]);
                submitPrediction();
            }
        });
    });

    function loadPreset(data) {
        document.getElementById('Age').value = data.Age;
        setRadio('Sex', data.Sex);
        setRadio('ChestPainType', data.ChestPainType);
        document.getElementById('RestingBP').value = data.RestingBP;
        document.getElementById('Cholesterol').value = data.Cholesterol;
        document.getElementById('FastingBS').value = data.FastingBS;
        document.getElementById('RestingECG').value = data.RestingECG;
        document.getElementById('MaxHR').value = data.MaxHR;
        document.getElementById('ExerciseAngina').value = data.ExerciseAngina;
        
        oldpeakSlider.value = data.Oldpeak;
        oldpeakVal.textContent = `${parseFloat(data.Oldpeak).toFixed(1)} mm`;
        setRadio('ST_Slope', data.ST_Slope);
    }

    function setRadio(name, val) {
        const radio = document.querySelector(`input[name="${name}"][value="${val}"]`);
        if (radio) radio.checked = true;
    }

    function getRadio(name) {
        const radio = document.querySelector(`input[name="${name}"]:checked`);
        return radio ? radio.value : null;
    }

    // Reset Form
    resetBtn.addEventListener('click', () => {
        form.reset();
        oldpeakSlider.value = 0.0;
        oldpeakVal.textContent = '0.0 mm';
        presetChips.forEach(c => c.classList.remove('active'));
        setState('placeholder');
    });

    // Form Submit
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        submitPrediction();
    });

    async function submitPrediction() {
        const formData = {
            Age: parseFloat(document.getElementById('Age').value) || 45,
            Sex: getRadio('Sex') || 'M',
            ChestPainType: getRadio('ChestPainType') || 'ATA',
            RestingBP: parseFloat(document.getElementById('RestingBP').value) || 120,
            Cholesterol: parseFloat(document.getElementById('Cholesterol').value) || 200,
            FastingBS: parseInt(document.getElementById('FastingBS').value) || 0,
            RestingECG: document.getElementById('RestingECG').value || 'Normal',
            MaxHR: parseFloat(document.getElementById('MaxHR').value) || 150,
            ExerciseAngina: document.getElementById('ExerciseAngina').value || 'N',
            Oldpeak: parseFloat(oldpeakSlider.value) || 0.0,
            ST_Slope: getRadio('ST_Slope') || 'Up'
        };

        setState('loading');

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('API server error');

            const data = await response.json();
            renderResults(data);
            setState('output');

            if (window.innerWidth < 860) {
                resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (err) {
            console.error(err);
            alert('Unable to reach server. Please ensure python3 app.py is running on http://127.0.0.1:5005');
            setState('placeholder');
        }
    }

    function setState(state) {
        placeholderState.classList.add('hidden');
        loadingState.classList.add('hidden');
        outputState.classList.add('hidden');

        if (state === 'placeholder') placeholderState.classList.remove('hidden');
        else if (state === 'loading') loadingState.classList.remove('hidden');
        else if (state === 'output') outputState.classList.remove('hidden');
    }

    function renderResults(res) {
        const isHigh = res.prediction === 1;

        // Status Banner
        statusBanner.className = `status-banner ${isHigh ? 'high' : 'low'}`;
        statusIcon.innerHTML = isHigh 
            ? '<i class="fa-solid fa-triangle-exclamation"></i>' 
            : '<i class="fa-solid fa-shield-heart"></i>';
        
        riskTitle.textContent = res.risk_label;

        // Score Ring
        const pct = res.risk_percentage;
        riskScorePct.textContent = `${pct}%`;
        riskScorePct.style.color = isHigh ? '#ef4444' : '#10b981';

        // Circumference of r=42 is 2 * PI * 42 = 263.89
        const circumference = 263.89;
        const offset = circumference - (pct / 100) * circumference;
        if (ringVal) {
            ringVal.style.strokeDashoffset = offset;
            ringVal.style.stroke = isHigh ? '#ef4444' : '#10b981';
        }

        lowProbText.textContent = `${res.probabilities.low_risk}%`;
        highProbText.textContent = `${res.probabilities.high_risk}%`;

        // Observations
        obsList.innerHTML = '';
        if (res.risk_factors && res.risk_factors.length > 0) {
            res.risk_factors.forEach(f => {
                const div = document.createElement('div');
                div.className = `obs-item ${f.severity}`;
                div.innerHTML = `<strong>${f.name}</strong>${f.detail}`;
                obsList.appendChild(div);
            });
        } else {
            obsList.innerHTML = `
                <div class="obs-item" style="border-left-color: #10b981;">
                    <strong>All Vitals Normal</strong>No high risk parameters detected.
                </div>
            `;
        }

        // Neighbors Pills
        neighborsPills.innerHTML = '';
        if (res.nearest_neighbors) {
            res.nearest_neighbors.forEach(n => {
                const span = document.createElement('span');
                span.className = 'n-pill';
                span.textContent = `#${n.rank}: Sample ${n.sample_index} (${n.distance} dist)`;
                neighborsPills.appendChild(span);
            });
        }
    }
});
