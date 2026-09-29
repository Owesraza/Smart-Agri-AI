import React, { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import { useTranslation } from '../context/LanguageContext'

export default function AIPriceRecommendationCard({
  crop,
  district = 'Nashik',
  quantity = 100,
  qualityGrade = 'Grade A',
  role = 'farmer',
  userPrice = '',
  onUseAiPrice
}) {
  const { t, language } = useTranslation()
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const isFarmer = role.toLowerCase() === 'farmer'

  const fetchRecommendation = async () => {
    if (!crop || crop.trim() === '') return
    setLoading(true)
    setError(null)

    try {
      const res = await axiosClient.post('/api/v1/ai/recommend-price', {
        crop: crop,
        district: district || 'Nashik',
        quantity: parseFloat(quantity) || 100,
        quality_grade: qualityGrade || 'Grade A',
        role: role,
        user_price: userPrice ? parseFloat(userPrice) : null,
        language: (language === 'Hindi' || language === 'hi') ? 'Hindi' : (language === 'Marathi' || language === 'mr') ? 'Marathi' : 'English'
      })

      if (res.data && res.data.success) {
        setRecommendation(res.data.data)
      }
    } catch (err) {
      console.warn('Price recommendation fetch error:', err)
      setError('Could not fetch AI price recommendation')
    } finally {
      setLoading(false)
    }
  }

  // Trigger auto fetch when crop, district, role or language changes
  useEffect(() => {
    fetchRecommendation()
  }, [crop, district, role, language])

  // Re-check warning when userPrice changes
  useEffect(() => {
    if (userPrice && recommendation) {
      const uPrice = parseFloat(userPrice)
      const rPrice = recommendation.recommended_price
      let warning = null

      if (isFarmer) {
        if (uPrice > rPrice * 1.15) {
          const pct = Math.round(((uPrice - recommendation.market_price) / recommendation.market_price) * 100)
          warning = `⚠ Your price is ${pct}% above current market. It may take longer to find buyers.`
        } else if (uPrice < rPrice * 0.90) {
          const loss = Math.round(rPrice - uPrice)
          warning = `⚠ You may lose approximately ₹${loss} per quintal. AI recommends ₹${rPrice}.`
        }
      } else {
        if (uPrice < rPrice * 0.90) {
          warning = `⚠ Offer is below market value. Farmers may reject your request.`
        } else if (uPrice > rPrice * 1.10) {
          warning = `⚠ Offer is higher than current mandi rates.`
        }
      }
      setRecommendation(prev => prev ? { ...prev, price_warning: warning } : prev)
    }
  }, [userPrice])

  if (!crop) return null

  return (
    <div className={`rounded-2xl border shadow-md overflow-hidden my-4 transition-all ${
      isFarmer ? 'border-emerald-200 bg-gradient-to-br from-emerald-50/90 to-teal-50/50' : 'border-blue-200 bg-gradient-to-br from-blue-50/90 to-indigo-50/50'
    }`}>
      {/* Header */}
      <div className={`px-5 py-3 flex items-center justify-between text-white ${
        isFarmer ? 'bg-gradient-to-r from-emerald-700 to-teal-700' : 'bg-gradient-to-r from-blue-700 to-indigo-700'
      }`}>
        <div className="flex items-center gap-2">
          <span className="text-xl">🤖</span>
          <h3 className="font-bold text-sm">
            {isFarmer ? 'AI Smart Selling Price Recommendation' : 'AI Smart Buying Price Recommendation'}
          </h3>
        </div>
        {recommendation && (
          <span className="text-xs font-extrabold bg-white/20 px-2.5 py-0.5 rounded-full backdrop-blur-sm">
            ⚡ {recommendation.confidence}% {t('ai.confidence', 'Confidence')}
          </span>
        )}
      </div>

      <div className="p-5 space-y-4">
        {loading ? (
          <div className="py-6 text-center text-sm text-gray-500 flex items-center justify-center gap-2 animate-pulse">
            <span className="animate-spin text-lg">⚡</span> Analyzing AGMARKNET Mandis, EMA-30 & Weather Risk...
          </div>
        ) : error ? (
          <div className="text-xs text-red-600 bg-red-50 p-3 rounded-xl border border-red-100 flex items-center justify-between">
            <span>{error}</span>
            <button onClick={fetchRecommendation} className="font-bold underline text-red-700 cursor-pointer">Retry</button>
          </div>
        ) : recommendation ? (
          <>
            {/* Price Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* Recommended Price Main Box */}
              <div className={`p-4 rounded-xl border text-center flex flex-col justify-center ${
                isFarmer ? 'bg-emerald-100/80 border-emerald-300' : 'bg-blue-100/80 border-blue-300'
              }`}>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">
                  {isFarmer ? 'Recommended Selling Price' : 'Recommended Buying Price'}
                </span>
                <span className={`text-2xl font-black mt-1 ${isFarmer ? 'text-emerald-900' : 'text-blue-900'}`}>
                  ₹{recommendation.recommended_price} <span className="text-xs font-normal">/ Qtl</span>
                </span>
              </div>

              {/* Today's Market Price */}
              <div className="p-3 rounded-xl bg-white border border-gray-200 text-center flex flex-col justify-center shadow-xs">
                <span className="text-xs text-gray-500 font-semibold">Today's Mandi Modal Price</span>
                <span className="text-lg font-bold text-gray-800 mt-0.5">₹{recommendation.market_price} <span className="text-xs font-normal text-gray-500">/ Qtl</span></span>
                <span className="text-[10px] text-emerald-700 font-bold bg-emerald-50 rounded px-1.5 py-0.5 mt-1 self-center border border-emerald-100">
                  {recommendation.data_sources?.market_data?.includes('AGMARKNET') ? 'Source: AGMARKNET' : 'Source: Mandi Rate'}
                </span>
              </div>

              {/* Market Range */}
              <div className="p-3 rounded-xl bg-white border border-gray-200 text-center flex flex-col justify-center shadow-xs">
                <span className="text-xs text-gray-500 font-semibold">
                  {isFarmer ? 'Expected Market Range' : 'Negotiation Price Range'}
                </span>
                <span className="text-sm font-extrabold text-gray-800 mt-1">
                  ₹{recommendation.minimum_price} - ₹{recommendation.maximum_price}
                </span>
              </div>
            </div>

            {/* Badges Bar (Trend, Weather Risk, EMAs, AGMARKNET Source) */}
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className={`px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 ${
                recommendation.trend === 'UPTREND' ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' :
                recommendation.trend === 'DOWNTREND' ? 'bg-rose-100 text-rose-800 border border-rose-200' : 'bg-gray-100 text-gray-800 border border-gray-200'
              }`}>
                📈 Trend: <b>{recommendation.trend}</b>
              </span>

              <span className={`px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 ${
                recommendation.weather_risk === 'HIGH' ? 'bg-amber-100 text-amber-900 border border-amber-200' : 'bg-blue-50 text-blue-800 border border-blue-200'
              }`}>
                ⛈ Weather Risk: <b>{recommendation.weather_risk}</b>
              </span>

              <span className="bg-gray-100 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 font-medium">
                📊 EMA-7: ₹{recommendation.ema7} | EMA-30: ₹{recommendation.ema30}
              </span>

              {recommendation.data_sources?.market_data && (
                <span className="bg-emerald-50 text-emerald-800 px-2.5 py-1 rounded-lg border border-emerald-200 font-bold text-[11px] flex items-center gap-1">
                  🏛️ {recommendation.data_sources.market_data}
                </span>
              )}
            </div>

            {/* Gemini Reason Text Box */}
            <div className="bg-white p-3.5 rounded-xl border border-gray-200 text-xs text-gray-700 leading-relaxed shadow-xs">
              <span className="font-bold text-gray-900 block mb-1">💡 AI Market Insight:</span>
              <p className="italic text-gray-600">{recommendation.reason}</p>
            </div>

            {/* Warning Alert Banner (Bonus Requirement) */}
            {recommendation.price_warning && (
              <div className="bg-amber-50 border border-amber-300 text-amber-900 text-xs font-semibold p-3 rounded-xl flex items-center gap-2 shadow-xs animate-fadeIn">
                <span className="text-base">⚠️</span>
                <span>{recommendation.price_warning}</span>
              </div>
            )}

            {/* Action Buttons */}
            <div className="pt-2 flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={() => onUseAiPrice && onUseAiPrice(recommendation.recommended_price)}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold text-white shadow-sm transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
                  isFarmer ? 'bg-emerald-600 hover:bg-emerald-700 active:scale-98' : 'bg-blue-600 hover:bg-blue-700 active:scale-98'
                }`}
              >
                <span>🎯</span> Use AI Recommended Price (₹{recommendation.recommended_price})
              </button>

              <button
                type="button"
                onClick={fetchRecommendation}
                className="py-2.5 px-3 rounded-xl text-xs font-semibold bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 transition-all cursor-pointer flex items-center gap-1"
                title="Refresh recommendation"
              >
                <span>🔄</span> Refresh
              </button>
            </div>
          </>
        ) : null}
      </div>
    </div>
  )
}
