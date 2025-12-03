let gaugeChart;
let currentTemperature = 0;

// Initialize the gauge chart
function initGauge() {
    const ctx = document.getElementById('gaugeChart').getContext('2d');

    gaugeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    '#7ed321',
                    '#e8f5d8'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            cutout: '75%'
        }
    });
}

// Update gauge value
function updateGauge(value) {
    if (value < 0) value = 0;
    if (value > 100) value = 100;

    currentTemperature = value;

    // Update chart data
    gaugeChart.data.datasets[0].data = [value, 100 - value];

    // Update colors based on value
    let color;
    if (value < 30) {
        color = '#7ed321'; // Green
    } else if (value < 60) {
        color = '#f5a623'; // Orange
    } else {
        color = '#d0021b'; // Red
    }

    gaugeChart.data.datasets[0].backgroundColor = [color, '#e8f5d8'];
    gaugeChart.update();

    // Update text value
    document.getElementById('gaugeValue').textContent = value.toFixed(2) + '%';
}

// Control LED
async function controlLED(command) {
    try {
        const response = await fetch('/device/led/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command })
        });

        const data = await response.json();

        if (data.result === 'ok') {
            document.getElementById('ledStatus').textContent = data.led;
            console.log('LED control successful:', data.message);
        } else {
            console.error('LED control failed:', data.message);
            alert('Failed to control LED: ' + (data.message || 'unknown'));
        }
    } catch (error) {
        console.error('Error controlling LED:', error);
        alert('Error controlling LED: ' + error.message);
    }
}

// Get LED status
async function getLEDStatus() {
    try {
        const response = await fetch('/device/led/state');
        const data = await response.json();

        if (data.result === 'ok') {
            document.getElementById('ledStatus').textContent = data.led;
        }
    } catch (error) {
        console.error('Error getting LED status:', error);
    }
}

// Get temperature
async function getTemperature() {
    try {
        const response = await fetch('/device/metrics/tempvar');
        const data = await response.json();

        if (data.result === 'ok') {
            const temp = parseFloat(data.temperature_c);
            if (!Number.isNaN(temp)) {
                document.getElementById('temperature').textContent = temp.toFixed(2);
                // Update gauge with temperature mapping (0..50°C mapped to 0..100)
                const pct = Math.max(0, Math.min(100, (temp / 50) * 100));
                updateGauge(pct);
            }
        }
    } catch (error) {
        console.error('Error getting temperature:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initGauge();

    // Initial data fetch
    getLEDStatus();
    getTemperature();

    // Update temperature every 3 seconds
    setInterval(getTemperature, 3000);

    // Update LED status every 6 seconds
    setInterval(getLEDStatus, 6000);
});
