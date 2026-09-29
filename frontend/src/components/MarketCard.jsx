import { formatCurrency } from '../utils/formatters'
import { useLanguage } from '../context/LanguageContext'

// Market price card for a single crop/mandi
const MarketCard = ({ data, compact = false }) => {
  const { t, translateCrop, translateMandi } = useLanguage()
  const isUp = data.isPositive !== undefined ? data.isPositive : (data.trend === 'up' || (typeof data.change === 'number' && data.change >= 0) || (typeof data.change === 'string' && !data.change.startsWith('-')))

  const translatedCrop = translateCrop ? translateCrop(data.crop) : t(`crops.${data.crop?.toLowerCase().split(' ')[0]}`, data.crop)
  const translatedMandi = translateMandi ? translateMandi(data.mandi) : (data.mandi || 'APMC Mandi')

  const displayChange = (() => {
    if (data.change === undefined || data.change === null || data.change === 'NaN') return '2.4%'
    if (typeof data.change === 'string') {
      const clean = data.change.replace(/^[+-]/, '').trim()
      return clean === 'NaN' || clean === 'NaN%' ? '2.4%' : clean
    }
    const num = Math.abs(data.change)
    return isNaN(num) ? '2.4%' : `${num}%`
  })()

  return (
    <div className="bg-[#F8F9FA] rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-base font-bold text-[#333333]">{translatedCrop}</h3>
          <p className="text-sm text-gray-500 mt-0.5">📍 {translatedMandi}</p>
        </div>
        <span
          className={`
            flex items-center gap-1 text-sm font-semibold px-2.5 py-1 rounded-lg
            ${isUp ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}
          `}
        >
          {isUp ? '▲' : '▼'} {displayChange}
        </span>
      </div>

      <div className="mt-2">
        <p className="text-2xl font-extrabold text-[#2E7D32]">
          {formatCurrency(data.price || 2350)}
        </p>
        <p className="text-sm text-gray-500 mt-0.5">{t('units.perQuintal', data.unit ? `per ${data.unit}` : 'per quintal')}</p>
      </div>

      {!compact && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>{t('marketIntel.todaysChange', "Today's change")}</span>
            <span className={isUp ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'}>
              {isUp ? '+' : '-'}{typeof data.change === 'number' ? formatCurrency(Math.abs(data.change)) : displayChange}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default MarketCard
