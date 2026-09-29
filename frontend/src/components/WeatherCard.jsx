import { useLanguage } from '../context/LanguageContext'

const WeatherCard = ({ data, loading = false, error = null, onRefresh }) => {
  const { t, translateWeather, translateDay, translateMandi } = useLanguage()

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-sky-500 to-blue-700 rounded-2xl p-6 text-white shadow-md h-52 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-white/30 border-t-white rounded-full animate-spin" />
          <p className="text-white/80 text-sm font-medium">{t('weather.loadingWeather', 'Loading weather...')}</p>
        </div>
      </div>
    )
  }

  if (!data) return null

  const hasApiKey = import.meta.env.VITE_WEATHER_API_KEY &&
    import.meta.env.VITE_WEATHER_API_KEY !== 'your_openweathermap_api_key_here'

  return (
    <div className="bg-gradient-to-br from-sky-500 to-blue-700 rounded-2xl p-6 text-white shadow-md overflow-hidden relative">
      {/* Decorative circles */}
      <div className="absolute -top-8 -right-8 w-32 h-32 bg-white/10 rounded-full" />
      <div className="absolute top-1/2 -right-4 w-20 h-20 bg-white/5 rounded-full" />

      <div className="relative z-10">
        {/* Header row */}
        <div className="flex items-start justify-between mb-1">
          <p className="text-white/70 text-sm font-medium truncate max-w-[200px]">
            📍 {translateMandi ? translateMandi(data.city) : data.city}
          </p>
          <div className="flex items-center gap-2">
            {hasApiKey && !error && (
              <span className="flex items-center gap-1 text-[10px] font-bold bg-white/20 px-2 py-0.5 rounded-full">
                <span className="w-1.5 h-1.5 bg-green-300 rounded-full animate-pulse" />
                {t('dashboard.live', 'LIVE')}
              </span>
            )}
            {onRefresh && (
              <button
                onClick={onRefresh}
                className="w-7 h-7 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors cursor-pointer"
                title="Refresh weather"
              >
                <span className="text-sm">🔄</span>
              </button>
            )}
          </div>
        </div>

        {/* Temperature + icon */}
        <div className="flex items-end gap-2 mt-2">
          <div>
            <div className="flex items-end gap-1">
              <span className="text-5xl font-extrabold">{data.temperature}°</span>
              <span className="text-xl mb-2">C</span>
            </div>
            <p className="text-white/80 font-medium capitalize">{translateWeather ? translateWeather(data.condition) : data.condition}</p>
            {data.feelsLike != null && (
              <p className="text-white/60 text-xs mt-0.5">{t('weather.feelsLike', 'Feels like')} {data.feelsLike}°C</p>
            )}
          </div>
          {data.iconUrl || (typeof data.icon === 'string' && data.icon.startsWith('http')) ? (
            <img src={data.iconUrl || data.icon} alt={translateWeather ? translateWeather(data.condition) : data.condition} className="w-16 h-16 object-contain ml-auto drop-shadow-md" />
          ) : (
            <div className="text-6xl ml-auto">{data.icon || '⛅'}</div>
          )}
        </div>

        {/* Stats row */}
        <div className="flex flex-wrap gap-3 mt-4 text-sm">
          <div className="flex items-center gap-1.5">
            <span>💧</span>
            <span className="text-white/70">{t('weather.humidity', 'Humidity')}</span>
            <span className="font-semibold">{data.humidity}%</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span>💨</span>
            <span className="text-white/70">{t('weather.wind', 'Wind')}</span>
            <span className="font-semibold">{data.wind} km/h</span>
          </div>
          {data.pressure && (
            <div className="flex items-center gap-1.5">
              <span>🌡️</span>
              <span className="font-semibold">{data.pressure} hPa</span>
            </div>
          )}
        </div>

        {/* 5-day forecast */}
        {data.forecast && data.forecast.length > 0 && (
          <div className="mt-5 pt-4 border-t border-white/20 flex justify-between">
            {data.forecast.map((day, i) => (
              <div key={i} className="flex flex-col items-center gap-1 text-center">
                <span className="text-white/60 text-xs font-medium">{translateDay ? translateDay(day.day) : day.day}</span>
                {typeof day.icon === 'string' && day.icon.startsWith('http') ? (
                  <img src={day.icon} alt={translateWeather ? translateWeather(day.condition) : day.condition} className="w-8 h-8 object-contain" />
                ) : (
                  <span className="text-lg">{day.icon || '⛅'}</span>
                )}
                <span className="text-sm font-semibold">{day.temp}°</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default WeatherCard
