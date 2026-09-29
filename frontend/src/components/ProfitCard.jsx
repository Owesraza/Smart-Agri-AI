import { formatCurrency } from '../utils/formatters'
import { useLanguage } from '../context/LanguageContext'

// Profit summary card
const ProfitCard = ({ data }) => {
  const { t } = useLanguage()
  const isPositive = data.netProfit >= 0

  return (
    <div className="bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100 shadow-sm">
      <h3 className="text-base font-bold text-[#333333] mb-5 flex items-center gap-2">
        <span>💰</span> {t('dashboard.profitSummary', 'Profit Summary')}
      </h3>

      <div className="space-y-4">
        {/* Income */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-sm text-gray-600">{t('ledger.totalIncome', 'Total Income')}</span>
          </div>
          <span className="text-sm font-bold text-green-700">{formatCurrency(data.totalIncome)}</span>
        </div>

        {/* Expenses */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-400" />
            <span className="text-sm text-gray-600">{t('ledger.totalExpense', 'Total Expenses')}</span>
          </div>
          <span className="text-sm font-bold text-red-600">{formatCurrency(data.totalExpenses)}</span>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between">
            <span className="text-base font-bold text-[#333333]">{t('ledger.netProfit', 'Net Profit')}</span>
            <span className={`text-xl font-extrabold ${isPositive ? 'text-[#2E7D32]' : 'text-red-600'}`}>
              {formatCurrency(data.netProfit)}
            </span>
          </div>
        </div>

        {/* Profit margin */}
        <div className="mt-2">
          <div className="flex justify-between text-xs text-gray-500 mb-1.5">
            <span>{t('ledger.profitMargin', 'Profit Margin')}</span>
            <span className="font-semibold text-[#2E7D32]">{data.profitMargin}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-[#2E7D32] to-[#81C784] h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(data.profitMargin, 100)}%` }}
            />
          </div>
        </div>

        {/* Monthly change */}
        {data.monthlyChange !== undefined && (
          <div className="mt-1 text-sm text-center text-gray-500">
            <span className="font-semibold text-green-600">▲ {data.monthlyChange}%</span> {t('units.vsLastMonth', 'vs last month')}
          </div>
        )}
      </div>
    </div>
  )
}

export default ProfitCard
