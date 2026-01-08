// ============================================
// Bike Rental Prediction - Frontend Script
// ============================================

const API_URL = window.location.origin;

// DOM Elements
const form = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const btnText = predictBtn.querySelector('.btn-text');
const btnLoading = predictBtn.querySelector('.btn-loading');
const resultCard = document.getElementById('resultCard');
const errorCard = document.getElementById('errorCard');
const predictionValue = document.getElementById('predictionValue');
const resultMessage = document.getElementById('resultMessage');
const errorMessage = document.getElementById('errorMessage');
const gaugeBar = document.getElementById('gaugeBar');

// Slider elements
const sliders = {
    temp: { element: document.getElementById('temp'), display: document.getElementById('tempValue'), 
            format: (v) => `${Math.round(v * 41)}°C` },
    atemp: { element: document.getElementById('atemp'), display: document.getElementById('atempValue'), 
             format: (v) => `${Math.round(v * 50)}°C` },
    hum: { element: document.getElementById('hum'), display: document.getElementById('humValue'), 
           format: (v) => `${Math.round(v * 100)}%` },
    windspeed: { element: document.getElementById('windspeed'), display: document.getElementById('windspeedValue'), 
                 format: (v) => `${Math.round(v * 67)} km/h` }
};

// ============================================
// Initialize Sliders
// ============================================

Object.keys(sliders).forEach(key => {
    const slider = sliders[key];
    
    // Set initial value
    slider.display.textContent = slider.format(parseFloat(slider.element.value));
    
    // Update on change
    slider.element.addEventListener('input', (e) => {
        slider.display.textContent = slider.format(parseFloat(e.target.value));
    });
});

// ============================================
// Form Submission
// ============================================

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    setLoading(true);
    hideCards();
    
    // Collect form data
    const formData = {
        season: parseInt(document.getElementById('season').value),
        yr: parseInt(document.getElementById('yr').value),
        mnth: parseInt(document.getElementById('mnth').value),
        hr: parseInt(document.getElementById('hr').value),
        holiday: parseInt(document.getElementById('holiday').value),
        weekday: parseInt(document.getElementById('weekday').value),
        workingday: parseInt(document.getElementById('workingday').value),
        weathersit: parseInt(document.getElementById('weathersit').value),
        temp: parseFloat(document.getElementById('temp').value),
        atemp: parseFloat(document.getElementById('atemp').value),
        hum: parseFloat(document.getElementById('hum').value),
        windspeed: parseFloat(document.getElementById('windspeed').value)
    };
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(data.prediction, data.message);
        } else {
            showError(data.detail || 'Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the server. Please ensure the API is running.');
    } finally {
        setLoading(false);
    }
});

// ============================================
// UI Helper Functions
// ============================================

function setLoading(loading) {
    predictBtn.disabled = loading;
    btnText.style.display = loading ? 'none' : 'inline';
    btnLoading.style.display = loading ? 'inline-flex' : 'none';
}

function hideCards() {
    resultCard.style.display = 'none';
    errorCard.style.display = 'none';
}

function showResult(prediction, message) {
    // Animate the number
    animateNumber(predictionValue, 0, prediction, 600);
    
    // Set message
    resultMessage.textContent = message || `Predicted ${prediction} bike rentals for the given conditions.`;
    
    // Update gauge (max around 1000 for visualization)
    const gaugePercent = Math.min((prediction / 800) * 100, 100);
    gaugeBar.style.width = '0%';
    
    // Show card with animation
    resultCard.style.display = 'block';
    resultCard.style.animation = 'none';
    resultCard.offsetHeight; // Trigger reflow
    resultCard.style.animation = 'fadeInUp 0.6s ease-out';
    
    // Animate gauge after a delay
    setTimeout(() => {
        gaugeBar.style.width = `${gaugePercent}%`;
    }, 200);
}

function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    errorCard.style.animation = 'none';
    errorCard.offsetHeight;
    errorCard.style.animation = 'fadeInUp 0.6s ease-out';
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (end - start) * easeOut);
        
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// ============================================
// Health Check on Load
// ============================================

async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (!data.model_loaded) {
            showError('Model not loaded. Please run the notebook first to train and save the model.');
        }
    } catch (error) {
        console.warn('Health check failed:', error);
    }
}

// Run health check on page load
document.addEventListener('DOMContentLoaded', checkHealth);
