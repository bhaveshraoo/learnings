document.addEventListener('DOMContentLoaded', () => {
    
    // Bind all slider inputs to update live badges
    const sliders = ['Age', 'Avg_Daily_Usage_Hours', 'Daily_Unlocks', 'Sleep_Hours_Per_Night', 'Physical_Activity_Hours', 'Study_Hours'];
    
    sliders.forEach(id => {
        const slider = document.getElementById(id);
        const badge = document.getElementById(`val-${id}`);
        if (slider && badge) {
            slider.addEventListener('input', (e) => {
                badge.textContent = e.target.value;
            });
        }
    });

    // Radio Pill Groups toggle behavior
    const pillGroups = document.querySelectorAll('.pill-options');
    pillGroups.forEach(group => {
        const pillBtns = group.querySelectorAll('.pill-btn');
        pillBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                pillBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const radio = btn.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
            });
        });
    });

    // Form submission handling
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const resultContainer = document.getElementById('result-container');
    const reassessBtn = document.getElementById('reassess-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state on button
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Analyzing Habits...';
        form.classList.add('loading-pulse');

        // Extract form values
        const formData = new FormData(form);
        const payload = {};
        formData.forEach((value, key) => {
            payload[key] = value;
        });

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                renderResult(data);
            } else {
                alert('Prediction Error: ' + (data.error || 'Unable to compute score'));
            }
        } catch (err) {
            console.error('Fetch error:', err);
            alert('Could not connect to predictor server. Please verify backend is running.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Predict Mental Health Score';
            form.classList.remove('loading-pulse');
        }
    });

    // Render results in card with smooth score dial animation
    function renderResult(data) {
        resultContainer.classList.remove('hidden');

        // Smooth scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Update score text counter
        const scoreValueElem = document.getElementById('score-value');
        animateValue(scoreValueElem, 0, data.score, 1200);

        // Update progress ring offset
        const circle = document.getElementById('score-ring');
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius; // ~427.25
        
        const offset = circumference - (data.score_percent / 100) * circumference;
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = offset;

        // Status badge
        const statusBadge = document.getElementById('status-badge');
        statusBadge.textContent = data.status;
        statusBadge.className = `status-badge ${data.color_class}`;

        // Summary text
        document.getElementById('status-summary').textContent = data.summary;

        // Tips list
        const tipsList = document.getElementById('tips-list');
        tipsList.innerHTML = '';
        
        data.tips.forEach(tip => {
            const tipItem = document.createElement('div');
            tipItem.className = 'tip-item';
            tipItem.innerHTML = `
                <div>
                    <h5>${tip.title}</h5>
                    <p>${tip.desc}</p>
                </div>
            `;
            tipsList.appendChild(tipItem);
        });
    }

    // Number animation helper
    function animateValue(elem, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentVal = (progress * (end - start) + start).toFixed(2);
            elem.textContent = currentVal;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Reassess button click
    reassessBtn.addEventListener('click', () => {
        resultContainer.classList.add('hidden');
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});
