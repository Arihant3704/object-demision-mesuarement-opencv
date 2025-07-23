async function fetchMeasurement() {
    try {
        const response = await fetch('/latest_measurement');
        const data = await response.json();

        if (data) {
            document.getElementById('timestamp').textContent = data.Timestamp;
            document.getElementById('width').textContent = data['Width (cm)'];
            document.getElementById('height').textContent = data['Height (cm)'];
            document.getElementById('measurement-image').src = `/images/${data['Image Filename']}`;
        }
    } catch (error) {
        console.error('Error fetching measurement:', error);
    }
}

// Fetch data every 2 seconds
setInterval(fetchMeasurement, 2000);

// Initial fetch
fetchMeasurement();
