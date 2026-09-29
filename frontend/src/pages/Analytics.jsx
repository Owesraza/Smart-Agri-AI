import { useState, useEffect, useMemo } from 'react'
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import axiosClient from '../api/axiosClient'
import Card, { CardHeader } from '../components/Card'
import StatCard from '../components/StatCard'
import { formatCurrency } from '../utils/formatters'
import { useTranslation } from '../context/LanguageContext'

const PIE_COLORS = ['#2E7D32', '#FF9800', '#1565C0', '#00695C', '#C62828']

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-lg p-3 text-sm">
      <p className="font-bold text-[#333333] mb-1">{label}</p>
      {payload.map((p) => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name}: {formatCurrency(p.value)}
        </p>
      ))}
    </div>
  )
}

const Analytics = () => {
  const { t, language } = useTranslation()

  const [loading, setLoading] = useState(true)
  const [profitSummary, setProfitSummary] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    netProfit: 0,
    profitMargin: 0,
    monthlyChange: 0
  })
  const [monthlyProfitData, setMonthlyProfitData] = useState([])
  const [cropShareData, setCropShareData] = useState([])
  const [cropPerformanceData, setCropPerformanceData] = useState([])

  useEffect(() => {
    const fetchRealAnalytics = async () => {
      setLoading(true)
      try {
        const [resSummary, resMonthly, resCrop] = await Promise.all([
          axiosClient.get('/api/v1/ledger/summary'),
          axiosClient.get('/api/v1/analytics/monthly-profit'),
          axiosClient.get('/api/v1/analytics/crop-summary')
        ])

        if (resSummary.data && resSummary.data.success && resSummary.data.data) {
          const d = resSummary.data.data
          const income = d.total_income || 0
          const exp = d.total_expenses || 0
          const net = d.net_profit !== undefined ? d.net_profit : (income - exp)
          const margin = income > 0 ? Math.round((net / income) * 1000) / 10 : 0.0

          setProfitSummary({
            totalIncome: income,
            totalExpenses: exp,
            netProfit: net,
            profitMargin: margin,
            monthlyChange: d.monthly_change_pct || 0.0
          })
        }

        if (resMonthly.data && resMonthly.data.success && Array.isArray(resMonthly.data.data)) {
          setMonthlyProfitData(resMonthly.data.data)
        }

        if (resCrop.data && resCrop.data.success && Array.isArray(resCrop.data.data)) {
          const rawCrops = resCrop.data.data
          setCropShareData(rawCrops.map(c => ({
            name: c.crop || c.name || 'Wheat',
            value: c.share_pct || c.value || 50
          })))
          setCropPerformanceData(rawCrops.map(c => ({
            crop: c.crop || 'Wheat',
            income: c.income || 0,
            expense: c.expense || 0,
            profit: c.profit || (c.income || 0) - (c.expense || 0)
          })))
        }
      } catch (err) {
        console.warn('Error fetching analytics:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchRealAnalytics()
  }, [])

  const translatedCropShare = useMemo(() => {
    return cropShareData.map((item) => ({
      ...item,
      translatedName: t(`crops.${item.name.toLowerCase()}`, item.name)
    }))
  }, [cropShareData, language, t])

  const translatedCropPerformance = useMemo(() => {
    return cropPerformanceData.map((item) => ({
      ...item,
      translatedCrop: t(`crops.${item.crop.toLowerCase()}`, item.crop)
    }))
  }, [cropPerformanceData, language, t])

  const topCropName = useMemo(() => {
    if (cropPerformanceData.length === 0) return 'None'
    const sorted = [...cropPerformanceData].sort((a, b) => b.income - a.income)
    return sorted[0]?.crop || 'None'
  }, [cropPerformanceData])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-[#333333]">{t('nav.analytics', 'Analytics')}</h1>
        <p className="text-gray-500 text-sm mt-1">{t('appSubtitle', 'Crop performance, market trends, and profit analysis')}</p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard title={`${t('ledger.netProfit', 'Net Profit')} (YTD)`} value={formatCurrency(profitSummary.netProfit)} icon="💰" color="green" change={profitSummary.monthlyChange} changeLabel="vs last month" />
        <StatCard title={t('ledger.totalIncome', 'Total Income')} value={formatCurrency(profitSummary.totalIncome)} icon="📈" color="teal" />
        <StatCard title={t('ledger.profitMargin', 'Profit Margin')} value={`${profitSummary.profitMargin}%`} icon="📊" color="blue" />
        <StatCard title={t('charts.topCrop', 'Top Crop')} value={t(`crops.${topCropName.toLowerCase()}`, topCropName)} icon="🌾" color="purple" />
      </div>

      {/* Row 1: Bar + Pie */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Bar Chart */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader title={`${t('ledger.income', 'Income')} vs ${t('ledger.expense', 'Expenses')}`} icon="📊" subtitle="Real Ledger Summary" />
            <div className="h-72">
              {loading ? (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">Loading monthly profit analytics...</div>
              ) : monthlyProfitData.length === 0 ? (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">No monthly profit entries recorded in digital ledger yet.</div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={monthlyProfitData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                    <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#6B7280' }} />
                    <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} tickFormatter={(v) => `₹${v / 1000}k`} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '12px' }} />
                    <Bar dataKey="income" name={t('ledger.income', 'Income')} fill="#2E7D32" radius={[6, 6, 0, 0]} />
                    <Bar dataKey="expenses" name={t('ledger.expense', 'Expenses')} fill="#EF4444" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </Card>
        </div>

        {/* Crop Share Pie Chart */}
        <Card>
          <CardHeader title={t('charts.cropPerformance', 'Crop Revenue Distribution')} icon="🥧" />
          <div className="h-52">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-gray-400">Loading crop share...</div>
            ) : translatedCropShare.length === 0 ? (
              <div className="h-full flex items-center justify-center text-xs text-gray-400">No crop ledger records available.</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={translatedCropShare}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={85}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {translatedCropShare.map((_, i) => (
                      <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(v) => [`${v}%`, '']} contentStyle={{ borderRadius: '12px', fontSize: '12px' }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div className="mt-2 space-y-1.5">
            {translatedCropShare.map((item, i) => (
              <div key={item.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ background: PIE_COLORS[i % PIE_COLORS.length] }} />
                  <span className="text-gray-600 font-medium">{item.translatedName || item.name}</span>
                </div>
                <span className="font-bold text-gray-800">{item.value}%</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Row 2: Crop Performance Chart */}
      <Card>
        <CardHeader title={t('charts.revenueByCrop', 'Revenue Breakdown by Crop')} icon="🌾" />
        <div className="h-64">
          {loading ? (
            <div className="h-full flex items-center justify-center text-xs text-gray-400">Loading crop performance...</div>
          ) : translatedCropPerformance.length === 0 ? (
            <div className="h-full flex items-center justify-center text-xs text-gray-400">No crop sales records logged.</div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={translatedCropPerformance} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis dataKey="translatedCrop" tick={{ fontSize: 12, fill: '#6B7280' }} />
                <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} tickFormatter={(v) => `₹${v / 1000}k`} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="income" name={t('ledger.income', 'Income')} fill="#2E7D32" radius={[6, 6, 0, 0]} />
                <Bar dataKey="profit" name={t('ledger.netProfit', 'Net Profit')} fill="#FF9800" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </Card>
    </div>
  )
}

export default Analytics
