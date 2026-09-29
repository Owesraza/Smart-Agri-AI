import { useState, useEffect, useCallback } from 'react'
import { fetchCurrentWeather, fetchForecast } from '../services/weatherService'

const DEFAULT_WEATHER = {
  city: 'Nashik, Maharashtra',
  temperature: 26,
  feelsLike: 27,
  condition: 'Partly Cloudy',
  humidity: 68,
  wind: 12,
  icon: '⛅',
  pressure: 1013,
  rain_probability: 20,
  farming_advisory: 'Favorable weather for routine crop monitoring and market harvesting.',
  harvest_risk: 'Low',
  forecast: [
    { day: 'Mon', temp: 27, icon: '⛅', condition: 'Partly Cloudy' },
    { day: 'Tue', temp: 28, icon: '☀️', condition: 'Clear' },
    { day: 'Wed', temp: 26, icon: '🌦️', condition: 'Light Rain' },
    { day: 'Thu', temp: 27, icon: '⛅', condition: 'Partly Cloudy' },
    { day: 'Fri', temp: 29, icon: '☀️', condition: 'Clear' }
  ]
}

export const useWeather = (city) => {
  const [weather, setWeather] = useState(DEFAULT_WEATHER)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const load = useCallback(async (cityName) => {
    const targetCity = cityName || 'Nashik'
    setLoading(true)
    setError(null)

    try {
      const current = await fetchCurrentWeather(targetCity)
      let forecast = []
      try {
        forecast = await fetchForecast(targetCity)
      } catch (fErr) {
        forecast = current.forecast || DEFAULT_WEATHER.forecast
      }

      setWeather({
        ...current,
        forecast: forecast.length > 0 ? forecast : (current.forecast || DEFAULT_WEATHER.forecast)
      })
    } catch (err) {
      console.warn('Weather fetch warning, using location fallback:', err)
      setWeather({
        ...DEFAULT_WEATHER,
        city: targetCity ? `${targetCity}, Maharashtra` : 'Nashik, Maharashtra'
      })
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load(city || 'Nashik')
  }, [city, load])

  const refresh = () => load(city || 'Nashik')

  return { weather, loading, error, refresh }
}

export default useWeather
