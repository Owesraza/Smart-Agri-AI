import axiosClient from '../api/axiosClient'

const iconToEmoji = (iconCode) => {
  const map = {
    '01d': '☀️', '01n': '🌙',
    '02d': '⛅', '02n': '🌥️',
    '03d': '🌥️', '03n': '🌥️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌦️', '10n': '🌧️',
    '11d': '⛈️', '11n': '⛈️',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️',
  }
  return map[iconCode] || '⛅'
}

const parseCityName = (city) => (city ? city.split(',')[0].trim() : 'Nashik')

// Fetch current weather via FastAPI Backend Weather API
export const fetchCurrentWeather = async (city) => {
  const cityName = parseCityName(city)
  const res = await axiosClient.get(`/api/v1/weather/current?location=${encodeURIComponent(cityName)}`)
  
  if (res.data && res.data.success && res.data.data) {
    const data = res.data.data
    return {
      city: data.location || `${cityName}, Maharashtra`,
      temperature: Math.round(data.temperature || 27),
      feelsLike: Math.round(data.feels_like || 28),
      condition: data.condition || 'Partly Cloudy',
      humidity: data.humidity || 65,
      wind: Math.round(data.wind_speed || 12),
      iconUrl: typeof data.icon === 'string' && data.icon.startsWith('http') ? data.icon : null,
      icon: iconToEmoji(data.iconCode || (typeof data.icon === 'string' && !data.icon.startsWith('http') ? data.icon : '02d')),
      iconCode: data.iconCode || '02d',
      pressure: data.pressure || 1013,
      rain_probability: data.rain_probability || 0,
      farming_advisory: data.farming_advisory || 'Favorable conditions for routine farming operations.',
      harvest_risk: data.harvest_risk || 'Low',
      rain_risk: data.rain_risk || 'Low'
    }
  }
  throw new Error('FAILED_TO_FETCH_WEATHER')
}

// Fetch 5-day forecast via FastAPI Backend Weather API
export const fetchForecast = async (city) => {
  const cityName = parseCityName(city)
  const res = await axiosClient.get(`/api/v1/weather/forecast?location=${encodeURIComponent(cityName)}`)
  
  if (res.data && res.data.success && res.data.data && Array.isArray(res.data.data.forecast)) {
    return res.data.data.forecast.map((item) => ({
      day: item.day || item.date || 'Day',
      temp: Math.round(item.temp || item.temperature || 27),
      icon: item.icon || iconToEmoji(item.iconCode),
      condition: item.condition || 'Clear',
      rain_prob: item.rain_probability || 0
    }))
  }
  return []
}
