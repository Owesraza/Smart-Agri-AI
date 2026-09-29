import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import axiosClient from '../api/axiosClient'

const Profile = () => {
  const { user, role, updateUser } = useAuth()
  const { t, transliterate, translateMandi } = useLanguage()

  const [form, setForm] = useState({
    name: user?.full_name || user?.name || '',
    phone: user?.mobile_number || user?.phone || '',
    location: user?.district || user?.location || 'Pune',
    farmName: user?.farmName || '',
    companyName: user?.companyName || '',
    gstNumber: user?.gstNumber || '',
  })

  const [saved, setSaved] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    updateUser({
      name: form.name,
      phone: form.phone,
      mobile_number: form.phone,
      whatsapp_number: form.phone,
      location: form.location,
      district: form.location,
      farmName: form.farmName,
      companyName: form.companyName,
      gstNumber: form.gstNumber,
    })
    try {
      await axiosClient.put('/api/v1/users/me', {
        full_name: form.name,
        mobile_number: form.phone,
        whatsapp_number: form.phone,
        district: form.location,
        village: form.location,
      })
    } catch (err) {
      console.warn('Backend profile sync:', err)
    }
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const roleBadgeColor = role === 'Buyer'
    ? 'bg-blue-100 text-blue-800 border-blue-200'
    : role === 'Admin'
    ? 'bg-purple-100 text-purple-800 border-purple-200'
    : 'bg-emerald-100 text-emerald-800 border-emerald-200'

  const displayName = user?.name ? transliterate(user.name) : 'User'

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      {/* Profile Header */}
      <div className="bg-gradient-to-r from-emerald-800 to-green-700 text-white p-6 rounded-2xl shadow-xl flex flex-col sm:flex-row items-center gap-6">
        <div className="w-20 h-20 rounded-full bg-amber-400 text-emerald-950 font-black text-3xl flex items-center justify-center shadow-md ring-4 ring-white/20">
          {displayName.charAt(0)?.toUpperCase() || 'U'}
        </div>
        <div className="text-center sm:text-left space-y-1">
          <div className="flex items-center justify-center sm:justify-start gap-3">
            <h1 className="text-2xl font-bold">{displayName}</h1>
            <span className={`text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider border ${roleBadgeColor}`}>
              🔒 {role === 'Buyer' ? t('roles.buyer') : role === 'Admin' ? t('roles.admin') : t('roles.farmer')} ({t('roles.readOnly')})
            </span>
          </div>
          <p className="text-emerald-100 text-sm">{user?.email}</p>
          <p className="text-xs text-emerald-200">📍 {translateMandi(form.location || 'Nashik, Maharashtra')}</p>
        </div>
      </div>

      {saved && (
        <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl text-emerald-800 font-bold text-xs text-center">
          ✅ {t('toasts.profileUpdated', 'Profile Updated')}
        </div>
      )}

      {/* Profile Edit Form */}
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-5">
        <h2 className="text-lg font-bold text-gray-900 border-b pb-3 flex items-center justify-between">
          <span>{t('profile.title', 'Account & Location Details')}</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">{t('profile.fullName', 'Full Name')}</label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.emailLabel', 'Email Address')}</label>
            <input
              type="email"
              value={user?.email || ''}
              disabled
              className="w-full px-3.5 py-2.5 border rounded-xl text-sm bg-gray-100 text-gray-500 cursor-not-allowed"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">{t('profile.mobileNumber', 'Mobile Number')}</label>
            <input
              type="tel"
              value={form.phone}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
              className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">{t('profile.city', 'City / District / Village')}</label>
            <input
              type="text"
              placeholder="e.g. Nashik, Pune, Baramati"
              value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })}
              className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>
        </div>

        {role === 'Farmer' ? (
          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">{t('profile.farmName', 'Farm Name')}</label>
            <input
              type="text"
              placeholder="Ramesh Organic Farms"
              value={form.farmName}
              onChange={(e) => setForm({ ...form, farmName: e.target.value })}
              className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.companyName', 'Company Name')}</label>
              <input
                type="text"
                value={form.companyName}
                onChange={(e) => setForm({ ...form, companyName: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.gstNumber', 'GST Number')}</label>
              <input
                type="text"
                value={form.gstNumber}
                onChange={(e) => setForm({ ...form, gstNumber: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>
        )}

        <div className="pt-3 border-t flex justify-end">
          <button type="submit" className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-6 py-2.5 rounded-xl text-xs transition-all cursor-pointer">
            {t('profile.saveProfile', 'Save Profile')}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Profile
