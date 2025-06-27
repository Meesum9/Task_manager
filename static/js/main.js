function getWeather() {
    const cityInput = document.getElementById('cityInput');
    const weatherInfo = document.getElementById('weatherInfo');
    
    if (!cityInput.value) {
        alert('Please enter a city name');
        return;
    }
    
    // Show loading state
    weatherInfo.innerHTML = '<div class="weather-card"><p>Loading weather information...</p></div>';
    
    fetch('/get_weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city: cityInput.value })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            weatherInfo.innerHTML = `<div class="weather-card"><p>${data.error}</p></div>`;
            return;
        }
        
        // Update weather information
        weatherInfo.innerHTML = `
            <div class="weather-card">
                <h2>${data.city}, ${data.country}</h2>
                <p>Temperature: ${data.temperature}°C</p>
                <p>Weather: ${data.description}</p>
                <p>Humidity: ${data.humidity}%</p>
                <p>Wind Speed: ${data.wind_speed} m/s</p>
            </div>
        `;
    })
    .catch(error => {
        weatherInfo.innerHTML = `<div class="weather-card"><p>Error: ${error.message}</p></div>`;
    });
}
