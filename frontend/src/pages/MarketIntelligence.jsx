import { useState, useEffect, useMemo } from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import axiosClient from '../api/axiosClient'
import SearchBar from '../components/SearchBar'
import MarketCard from '../components/MarketCard'
import Card, { CardHeader } from '../components/Card'
import useDebounce from '../hooks/useDebounce'
import { useLanguage } from '../context/LanguageContext'
import { useAuth } from '../context/AuthContext'

const MarketIntelligence = () => {
  const { t, language, translateCrop, translateMandi } = useLanguage()
  const { user } = useAuth()
  const [search, setSearch] = useState('')
  const [marketPrices, setMarketPrices] = useState([])
  const [trendData, setTrendData] = useState([])
  const [loading, setLoading] = useState(true)
  const debouncedSearch = useDebounce(search)

  const [selectedCity, setSelectedCity] = useState('All Cities')
  const [agmarknetMeta, setAgmarknetMeta] = useState({
    source: 'AGMARKNET',
    status: 'Latest AGMARKNET Market Data',
    market_date: '',
    last_synced_at: '',
    badge_color: 'emerald'
  })

  const MAHARASHTRA_CITIES = [
    'All Cities', 'Nashik', 'Pune', 'Lasalgaon', 'Latur',
    'Kolhapur', 'Nagpur', 'Solapur', 'Sangli', 'Aurangabad', 'Ahmednagar'
  ]

  // Fetch Real Live Mandi Prices & Historical Trend Graph Data from SQL Database with 10s Real-Time Auto-Refresh
  useEffect(() => {
    const fetchPricesAndTrend = async (isBackground = false) => {
      if (!isBackground) setLoading(true)
      try {
        const priceUrl = selectedCity !== 'All Cities'
          ? `/api/v1/market/live?district=${encodeURIComponent(selectedCity)}`
          : '/api/v1/market/live?district=All%20Cities'

        let [resPrices, resTrend, resStatus] = await Promise.allSettled([
          axiosClient.get(priceUrl),
          axiosClient.get(`/api/v1/market/prices/trend?district=${encodeURIComponent(selectedCity)}`),
          axiosClient.get('/api/v1/market/status')
        ])

        if (resPrices.status === 'fulfilled' && resPrices.value?.data?.success && Array.isArray(resPrices.value.data.data) && resPrices.value.data.data.length > 0) {
          setMarketPrices(resPrices.value.data.data)
        } else {
          try {
            const fallbackRes = await axiosClient.get('/api/v1/market/live?district=All%20Cities')
            if (fallbackRes.data?.success && Array.isArray(fallbackRes.data.data)) {
              setMarketPrices(fallbackRes.data.data)
            }
          } catch (e) {}
        }

        if (resTrend.status === 'fulfilled' && resTrend.value?.data?.success && Array.isArray(resTrend.value.data.data)) {
          setTrendData(resTrend.value.data.data)
        }

        if (resStatus.status === 'fulfilled' && resStatus.value?.data?.success && resStatus.value.data.data) {
          setAgmarknetMeta(resStatus.value.data.data)
        }
      } catch (err) {
        console.warn('Error fetching market prices or trend:', err)
      } finally {
        if (!isBackground) setLoading(false)
      }
    }
    fetchPricesAndTrend(false)
    const interval = setInterval(() => fetchPricesAndTrend(true), 10000)
    return () => clearInterval(interval)
  }, [user, selectedCity])

  // Deduplicate entries by unique (crop + mandi) key to eliminate duplicates
  const uniquePrices = useMemo(() => {
    const map = new Map()
    for (const m of marketPrices) {
      const key = `${(m.crop || '').toLowerCase().trim()}_${(m.mandi || '').toLowerCase().trim()}`
      if (!map.has(key)) {
        map.set(key, m)
      }
    }
    return Array.from(map.values())
  }, [marketPrices])

  // Filter prices by search term and selected city
  const filtered = uniquePrices.filter((p) => {
    const cropName = (p.crop || '').toLowerCase()
    const mandiName = (p.mandi || '').toLowerCase()
    const distName = (p.district || '').toLowerCase()

    const matchSearch =
      cropName.includes(debouncedSearch.toLowerCase()) ||
      mandiName.includes(debouncedSearch.toLowerCase()) ||
      distName.includes(debouncedSearch.toLowerCase())

    const matchCity =
      selectedCity === 'All Cities' ||
      mandiName.includes(selectedCity.toLowerCase()) ||
      distName.includes(selectedCity.toLowerCase())

    return matchSearch && matchCity
  })

  // Dynamically compute the top performing market pick (highest modal price rate) from live prices
  const topPick = useMemo(() => {
    if (uniquePrices.length === 0) return null
    return [...uniquePrices].sort((a, b) => (b.modal_price || b.price || 0) - (a.modal_price || a.price || 0))[0]
  }, [uniquePrices])

  const checkTopPick = () => {
    if (topPick) {
      setSearch(topPick.crop || '')
      setSelectedCity('All Cities')
      window.scrollTo({ top: 150, behavior: 'smooth' })
    }
  }

  const CROP_COLORS = {
    onion: '#D97706',
    wheat: '#059669',
    tomato: '#DC2626',
    grapes: '#7C3AED',
    cotton: '#2563EB',
    soybean: '#0284C7',
    maize: '#EAB308',
    potato: '#84CC16',
    garlic: '#64748B',
    pomegranate: '#E11D48',
    rice: '#059669',
    bajra: '#B45309',
    sugarcane: '#10B981',
    turmeric: '#F59E0B',
    chilli: '#EF4444',
    mango: '#F97316'
  }

  // Dynamically compute active trend crops based on search term or city selection
  const activeTrendCrops = useMemo(() => {
    if (!trendData || trendData.length === 0) return ['wheat', 'onion', 'tomato', 'soybean', 'cotton']
    const availableKeys = Object.keys(trendData[0]).filter(k => k !== 'week')
    if (!debouncedSearch) return availableKeys

    const query = debouncedSearch.toLowerCase().trim()
    const matched = availableKeys.filter(k => k.includes(query) || query.includes(k))
    return matched.length > 0 ? matched : availableKeys
  }, [debouncedSearch, trendData])

  const getAgmarknetStatusText = (status) => {
    if (!status) return t('marketIntel.latestAgmarknet', 'Latest AGMARKNET Market Data')
    if (status.includes('Latest')) return t('marketIntel.latestAgmarknet', 'Latest AGMARKNET Market Data')
    if (status.includes('Cached')) return t('marketIntel.cachedAgmarknet', 'Cached AGMARKNET Market Data')
    if (status.includes('Unavailable')) return t('marketIntel.agmarknetUnavailable', 'AGMARKNET Unavailable (Seed Baseline)')
    return status
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">{t('marketIntel.title', 'Live APMC Market Intelligence')}</h1>
        <p className="text-gray-500 text-xs mt-1">
          {t('marketIntel.subtitle', 'Official AGMARKNET mandi rates, minimum/maximum price bounds, and historical trends.')
            .replace('{district}', selectedCity !== 'All Cities' 
              ? translateMandi(selectedCity) 
              : (user?.district ? translateMandi(user.district) : (language === 'Hindi' || language === 'hi' ? 'महाराष्ट्र' : language === 'Marathi' || language === 'mr' ? 'महाराष्ट्र' : 'Maharashtra')))}
        </p>
      </div>

      {/* AGMARKNET Metadata Status Card */}
      <div className="bg-white p-3.5 rounded-2xl border border-gray-200 shadow-xs flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5">
          <span className={`w-2.5 h-2.5 rounded-full ${
            agmarknetMeta.status?.includes('Latest') ? 'bg-emerald-500 animate-pulse' : (agmarknetMeta.status?.includes('Cached') ? 'bg-amber-500' : 'bg-rose-500')
          }`}></span>
          <span className="font-extrabold text-gray-900">{getAgmarknetStatusText(agmarknetMeta.status)}</span>
          <span className="text-gray-300">|</span>
          <span className="text-gray-600 font-medium">
            Source: <strong className="text-emerald-900 font-extrabold">AGMARKNET</strong> (Directorate of Marketing & Inspection, Govt. of India)
          </span>
        </div>
        <div className="flex items-center gap-4 text-gray-500 font-semibold text-[11px]">
          {agmarknetMeta.latest_market_date && (
            <span>Market Date: <strong className="text-gray-800 font-bold">{agmarknetMeta.latest_market_date}</strong></span>
          )}
          {agmarknetMeta.last_synced_at && (
            <span>Last Updated: <strong className="text-gray-800 font-bold">{new Date(agmarknetMeta.last_synced_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong></span>
          )}
        </div>
      </div>

      {/* Action Bar: Search + City Selector + Top Pick Button */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-xs space-y-3">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <SearchBar
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('marketIntel.searchCrop', 'Search crop, mandi, or city name...')}
            className="flex-1"
          />

          <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            {/* City Selector Dropdown */}
            <div className="flex items-center gap-1.5 bg-gray-50 border border-gray-200 px-3 py-2 rounded-xl text-xs font-bold">
              <span>🏙️ {t('marketIntel.city', 'City:')}</span>
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="bg-transparent text-emerald-800 font-extrabold outline-none cursor-pointer"
              >
                {MAHARASHTRA_CITIES.map((city) => (
                  <option key={city} value={city}>
                    {city === 'All Cities' ? t('marketIntel.allCities', 'All Cities') : translateMandi(city)}
                  </option>
                ))}
              </select>
            </div>

            {/* Check Top Pick Button */}
            <button
              onClick={checkTopPick}
              className="bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 text-slate-950 px-4 py-2 rounded-xl text-xs font-black transition-all cursor-pointer shadow-sm flex items-center gap-1.5 whitespace-nowrap"
            >
              <span>🏆</span> {t('marketIntel.checkTopPick', 'Check Top Mandi Pick')}
            </button>
          </div>
        </div>

        {/* Quick City Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 pt-1 scrollbar-thin">
          <span className="text-[10px] text-gray-400 font-bold uppercase whitespace-nowrap">{t('marketIntel.quickCities', 'Quick Cities:')}</span>
          {MAHARASHTRA_CITIES.map((city) => (
            <button
              key={city}
              onClick={() => setSelectedCity(city)}
              className={`px-3 py-1 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                selectedCity === city
                  ? 'bg-emerald-700 text-white shadow-xs font-extrabold'
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-200'
              }`}
            >
              {city === 'All Cities' ? `🌐 ${t('marketIntel.allCities', 'All')}` : translateMandi(city)}
            </button>
          ))}
        </div>
      </div>

      {/* Best Price Highlight */}
      {!debouncedSearch && topPick && (
        <div className="bg-gradient-to-br from-emerald-800 via-teal-900 to-slate-900 rounded-2xl p-6 text-white shadow-lg border border-emerald-500/20">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-amber-400 text-lg">⭐</span>
            <p className="text-xs font-bold text-emerald-200 uppercase tracking-wider">{t('marketIntel.bestMarketPick', 'Top Mandi Rate Today')}</p>
          </div>
          <div className="flex items-end gap-3 mb-2 flex-wrap">
            <span className="text-4xl font-black">{translateCrop ? translateCrop(topPick.crop || 'Wheat') : (topPick.crop || 'Wheat')}</span>
            <span className="text-sm text-emerald-200 mb-1">
              {language === 'Hindi' || language === 'hi' ? 'स्थान' : language === 'Marathi' || language === 'mr' ? 'ठिकाण' : 'at'}: {translateMandi ? translateMandi(topPick.mandi || 'Nashik APMC') : (topPick.mandi || 'Nashik APMC')} ({translateMandi ? translateMandi(topPick.district || 'Nashik') : (topPick.district || 'Nashik')})
            </span>
          </div>
          <p className="text-3xl font-black text-amber-400">₹{topPick.modal_price || topPick.price} / {t('marketIntel.perQuintal', 'quintal')}</p>
          <p className="text-xs text-emerald-300 mt-1 font-semibold">
            ▲ +{topPick.weekly_change || 2.4}% Weekly Gain · Range: ₹{topPick.min_price} – ₹{topPick.max_price} / Qtl
          </p>
        </div>
      )}

      {/* Price Cards Grid */}
      <div>
        <h2 className="text-base font-bold text-gray-900 mb-4 flex items-center justify-between">
          <span>
            {debouncedSearch ? `${t('marketIntel.searchResults', 'Results for')} "${debouncedSearch}"` : t('marketIntel.todayRates', "Today's Mandi Market Rates")}
            <span className="ml-2 text-xs font-semibold text-gray-500">({filtered.length} {t('marketIntel.mandis', 'Mandis')})</span>
          </span>
          <span className={`text-xs font-bold px-3 py-1 rounded-full border ${
            agmarknetMeta.status?.includes('Latest')
              ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
              : (agmarknetMeta.status?.includes('Cached') ? 'text-amber-700 bg-amber-50 border-amber-200' : 'text-rose-700 bg-rose-50 border-rose-200')
          }`}>
            {getAgmarknetStatusText(agmarknetMeta.status)}
          </span>
        </h2>

        {loading ? (
          <div className="py-12 text-center text-xs text-gray-400 animate-pulse">{t('marketIntel.loadingRates', 'Loading AGMARKNET mandi rates...')}</div>
        ) : filtered.length === 0 ? (
          <div className="bg-white p-8 text-center text-xs text-gray-500 rounded-2xl border border-dashed my-4">
            {t('marketIntel.noRates', 'No live crop prices found matching your search.')}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {filtered.map((m, idx) => (
              <MarketCard
                key={m.id || idx}
                data={{
                  id: m.id || idx,
                  crop: m.crop || 'Wheat',
                  mandi: m.mandi || 'Nashik APMC',
                  price: m.modal_price || m.price || 2350,
                  change: `${m.weekly_change >= 0 ? '+' : ''}${m.weekly_change || 2.4}%`,
                  isPositive: (m.weekly_change || 0) >= 0,
                  isNeutral: (m.weekly_change || 0) === 0
                }}
              />
            ))}
          </div>
        )}
      </div>

      {/* Price Trend Chart */}
      <Card>
        <CardHeader
          title={t('marketIntel.priceTrend', 'Historical Mandi Price Trends')}
          icon="📈"
          subtitle={
            debouncedSearch
              ? `Historical Price Trend for "${debouncedSearch}" in ${selectedCity}`
              : selectedCity === 'All Cities'
              ? 'Maharashtra State-wide APMC Benchmark (4-Week Real Trajectory)'
              : `${selectedCity} APMC Real Price Trend (${activeTrendCrops.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(' · ')})`
          }
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="week" tick={{ fontSize: 12, fill: '#6B7280' }} />
              <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} tickFormatter={(v) => `₹${v}`} />
              <Tooltip formatter={(v) => [`₹${v}`, '']} contentStyle={{ borderRadius: '12px', border: '1px solid #E5E7EB', fontSize: '12px' }} />
              <Legend />
              {activeTrendCrops.map((cropKey, idx) => {
                const color = CROP_COLORS[cropKey] || ['#059669', '#D97706', '#DC2626', '#7C3AED', '#2563EB', '#0284C7'][idx % 6]
                const formattedName = cropKey.charAt(0).toUpperCase() + cropKey.slice(1)
                return (
                  <Line
                    key={cropKey}
                    type="monotone"
                    dataKey={cropKey}
                    name={translateCrop ? translateCrop(cropKey) : formattedName}
                    stroke={color}
                    strokeWidth={2.5}
                    dot={{ r: 4, fill: color }}
                  />
                )
              })}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  )
}

export default MarketIntelligence
