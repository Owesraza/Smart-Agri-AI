import { useState, useRef, useEffect } from 'react'
import { useLocation, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import axiosClient from '../api/axiosClient'

const TopNav = ({ onMenuToggle }) => {
  const { user, role } = useAuth()
  const { language, setLanguage, t, transliterate } = useLanguage()
  const location = useLocation()

  const [activityOpen, setActivityOpen] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const dropdownRef = useRef(null)

  // Real-Time Notification Polling Loop (Every 5 seconds)
  const fetchNotifications = async () => {
    try {
      const res = await axiosClient.get('/api/v1/notifications/')
      if (res.data && res.data.success && Array.isArray(res.data.data)) {
        setNotifications(res.data.data)
        const unread = res.data.data.filter(n => !n.is_read).length
        setUnreadCount(unread)
      }
    } catch (err) {
      // Silent error handling for polling loop
    }
  }

  useEffect(() => {
    fetchNotifications()
    const interval = setInterval(fetchNotifications, 5000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) setActivityOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const markAllAsRead = async () => {
    try {
      await axiosClient.patch('/api/v1/notifications/read')
      setUnreadCount(0)
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
    } catch (err) {
      console.warn('Error marking notifications as read:', err)
    }
  }

  const roleBadgeStyle = role === 'Buyer'
    ? 'bg-blue-100 text-blue-800 border-blue-200'
    : role === 'Admin'
    ? 'bg-purple-100 text-purple-800 border-purple-200'
    : 'bg-emerald-100 text-emerald-800 border-emerald-200'

  const displayName = user?.full_name ? transliterate(user.full_name) : user?.name ? transliterate(user.name) : 'User'

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 sticky top-0 z-20 shadow-sm">
      {/* Left: hamburger + title */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuToggle}
          className="lg:hidden w-9 h-9 rounded-lg flex items-center justify-center text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors cursor-pointer"
        >
          ☰
        </button>
        <div>
          <h1 className="text-lg font-bold text-gray-900">{t('appName')}</h1>
          <p className="text-xs text-gray-400 hidden sm:block">{t('appSubtitle')}</p>
        </div>
      </div>

      {/* Right Toolbar */}
      <div className="flex items-center gap-3">
        {/* Multi-Language Selector Dropdown (English / Hindi / Marathi) */}
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="text-xs font-bold bg-emerald-50 border border-emerald-300 rounded-xl px-3 py-1.5 text-emerald-900 outline-none cursor-pointer hover:bg-emerald-100 transition-all shadow-2xs"
          aria-label="Select Language"
        >
          <option value="English">English</option>
          <option value="Hindi">हिंदी</option>
          <option value="Marathi">मराठी</option>
        </select>

        {/* Permanent Read-Only Role Badge */}
        <div className={`flex items-center gap-1.5 text-xs font-extrabold px-3 py-1.5 rounded-full border ${roleBadgeStyle}`}>
          <span>{role === 'Buyer' ? t('roles.buyer', 'Buyer') : role === 'Admin' ? t('roles.admin', 'Admin') : t('roles.farmer', 'Farmer')}</span>
        </div>

        {/* Notification Bell with Real-Time Unread Badge */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => {
              setActivityOpen(!activityOpen)
              if (!activityOpen && unreadCount > 0) markAllAsRead()
            }}
            className="relative w-10 h-10 rounded-xl flex items-center justify-center text-gray-600 hover:text-emerald-700 hover:bg-emerald-50 transition-all cursor-pointer"
            title={t('notifications.title', 'Notifications')}
          >
            <span className="text-xl">🔔</span>
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-600 text-white text-[10px] font-black px-1.5 py-0.5 rounded-full animate-bounce shadow-xs">
                {unreadCount}
              </span>
            )}
          </button>

          {/* Notification Dropdown Panel */}
          {activityOpen && (
            <div className="absolute right-0 top-12 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 overflow-hidden">
              <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-gray-50">
                <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                  <span>🔔</span> {t('notifications.title', 'Notifications')} ({notifications.length})
                </h3>
                <button onClick={() => setActivityOpen(false)} className="text-gray-400 hover:text-gray-600 text-xs cursor-pointer">✕</button>
              </div>

              <div className="max-h-80 overflow-y-auto divide-y divide-gray-100 text-xs">
                {notifications.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    {t('notifications.noNotifications', 'No new notifications.')}
                  </div>
                ) : (
                  notifications.map((n) => (
                    <div key={n.id} className={`p-3.5 space-y-1 transition-all ${n.is_read ? 'bg-white' : 'bg-emerald-50/60 font-semibold'}`}>
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-gray-900">{t(`notifications.${n.id}`, n.title || n.type)}</span>
                        <span className="text-[10px] text-gray-400">{n.created_at ? n.created_at.split('T')[0] : 'Just now'}</span>
                      </div>
                      <p className="text-gray-600 leading-snug">{n.message}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Avatar */}
        <Link to="/profile" className="flex items-center gap-2 group cursor-pointer" title={displayName}>
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-600 to-green-500 text-white font-bold text-sm flex items-center justify-center shadow-sm">
            {displayName.charAt(0)?.toUpperCase() || 'U'}
          </div>
        </Link>
      </div>
    </header>
  )
}

export default TopNav
