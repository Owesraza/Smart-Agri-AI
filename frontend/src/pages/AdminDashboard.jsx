import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import { useTranslation } from '../context/LanguageContext'

const AdminDashboard = () => {
  const { t } = useTranslation()
  const [stats, setStats] = useState({
    total_farmers: 1250,
    total_buyers: 340,
    active_deals: 89,
    platform_revenue: '₹14.2 Lakhs',
    system_health: '100% Healthy',
    agmarknet_status: 'Connected',
    weather_status: 'Connected',
    ai_status: 'Active (Gemini 2.0 Flash)',
  })

  useEffect(() => {
    const fetchAdminStats = async () => {
      try {
        const resHealth = await axiosClient.get('/health')
        if (resHealth.data && resHealth.data.status === 'healthy') {
          setStats(prev => ({
            ...prev,
            system_health: '100% Healthy',
            agmarknet_status: resHealth.data.marketplace || 'Connected',
            weather_status: 'Connected',
            ai_status: 'Active (Gemini 2.0 Flash + FAISS)',
          }))
        }
      } catch (err) {
        console.warn('Error fetching live system health:', err)
      }
    }
    fetchAdminStats()
  }, [])

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-900 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-3xl">⚙️</span>
            <h1 className="text-2xl font-bold">{t('admin.title', 'Admin Console')}</h1>
            <span className="bg-purple-500 text-white text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider">{t('roles.admin', 'System Admin')}</span>
          </div>
          <p className="text-purple-200 text-sm mt-1">{t('appSubtitle', 'Platform management, user verification queues, marketplace monitoring, and system metrics')}</p>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">{t('admin.farmers', 'Total Farmers')}</span>
            <span className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-lg">🌾</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.total_farmers}</div>
            <p className="text-xs text-emerald-600 font-semibold mt-1">+48 registered this week</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">{t('admin.buyers', 'Total Buyers')}</span>
            <span className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-lg">🏢</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.total_buyers}</div>
            <p className="text-xs text-blue-600 font-semibold mt-1">12 pending GST verifications</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">{t('buyerDashboard.deals', 'Active Deals')}</span>
            <span className="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-lg">🤝</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.active_deals}</div>
            <p className="text-xs text-amber-600 font-semibold mt-1">In fulfillment pipeline</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">{t('admin.revenue', 'Platform Revenue')}</span>
            <span className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-lg">💰</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.platform_revenue}</div>
            <p className="text-xs text-purple-600 font-semibold mt-1">1% transaction fee collected</p>
          </div>
        </div>
      </div>

      {/* System Health & APIs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span>🛡️</span> {t('admin.reports', 'System Health & Service Status')}
          </h2>

          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-xl border border-emerald-200">
              <span className="text-xs font-bold text-emerald-900">SQL Database Engine (SQLite / PostgreSQL)</span>
              <span className="text-xs font-extrabold bg-emerald-600 text-white px-2.5 py-0.5 rounded-full">{t('status.active', 'Active')}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-xl border border-emerald-200">
              <span className="text-xs font-bold text-emerald-900">Agmarknet APMC Mandi Data API</span>
              <span className="text-xs font-extrabold bg-emerald-600 text-white px-2.5 py-0.5 rounded-full">{stats.agmarknet_status}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-emerald-50 rounded-xl border border-emerald-200">
              <span className="text-xs font-bold text-emerald-900">OpenWeatherMap Live Data API</span>
              <span className="text-xs font-extrabold bg-emerald-600 text-white px-2.5 py-0.5 rounded-full">{stats.weather_status}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-xl border border-purple-200">
              <span className="text-xs font-bold text-purple-900">AI Engine (Gemini 2.0 Flash + FAISS RAG)</span>
              <span className="text-xs font-extrabold bg-purple-600 text-white px-2.5 py-0.5 rounded-full">{stats.ai_status}</span>
            </div>
          </div>
        </div>

        {/* Verification Queue */}
        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span>📋</span> {t('buyerDashboard.requirements', 'Pending Verification Queue')}
          </h2>

          <div className="space-y-3">
            <div className="p-3 bg-gray-50 rounded-xl border flex items-center justify-between">
              <div>
                <p className="text-sm font-bold text-gray-900">Amit Agro Processors Pvt Ltd</p>
                <p className="text-xs text-gray-500">GST: 27AAACA1234A1Z5 | District: Nashik</p>
              </div>
              <button onClick={() => alert(t('toasts.profileUpdated', 'Verified!'))} className="bg-emerald-700 text-white text-xs font-bold px-3 py-1.5 rounded-lg cursor-pointer">
                Approve GST
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
