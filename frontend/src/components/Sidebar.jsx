import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, role, logout } = useAuth()
  const { t, transliterate } = useLanguage()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const farmerNav = [
    { label: t('nav.dashboard', 'Farmer Dashboard'), href: '/dashboard', icon: '🏠' },
    { label: t('nav.marketplace', 'Agricultural Marketplace'), href: '/marketplace', icon: '🛒' },
    { label: t('nav.myListings', 'My Crop Listings'), href: '/my-listings', icon: '📦' },
    { label: t('nav.aiAssistant', 'AI Advisory Assistant'), href: '/ai-assistant', icon: '🤖' },
    { label: t('nav.market', 'Market Intelligence'), href: '/market', icon: '📊' },
    { label: t('nav.ledger', 'Digital Ledger'), href: '/ledger', icon: '💰' },
    { label: t('nav.profile', 'User Profile'), href: '/profile', icon: '👤' },
  ]

  const buyerNav = [
    { label: t('nav.buyerDashboard', 'Buyer Dashboard'), href: '/buyer', icon: '🏠' },
    { label: t('nav.marketplace', 'Agricultural Marketplace'), href: '/marketplace', icon: '🛒' },
    { label: t('nav.buyingRequirements', 'Buying Requirements'), href: '/buying-requirements', icon: '📋' },
    { label: t('nav.market', 'Market Intelligence'), href: '/market', icon: '📊' },
    { label: t('nav.purchaseAnalytics', 'Purchase Analytics'), href: '/purchase-analytics', icon: '📈' },
    { label: t('nav.profile', 'User Profile'), href: '/profile', icon: '👤' },
  ]

  const adminNav = [
    { label: t('nav.adminDashboard', 'Admin Console'), href: '/admin', icon: '⚙️' },
    { label: t('nav.marketplace', 'Agricultural Marketplace'), href: '/marketplace', icon: '🛒' },
    { label: t('nav.market', 'Market Intelligence'), href: '/admin/market-data', icon: '📊' },
    { label: t('nav.analytics', 'Analytics'), href: '/admin/analytics', icon: '📈' },
    { label: t('nav.profile', 'User Profile'), href: '/profile', icon: '👤' },
  ]

  const navItems = role === 'Buyer' ? buyerNav : role === 'Admin' ? adminNav : farmerNav
  const portalTitle = role === 'Buyer' ? t('roles.buyer') : role === 'Admin' ? t('roles.admin') : t('roles.farmer')

  const roleBadgeColor = role === 'Buyer' 
    ? 'bg-blue-600 border-blue-400 text-white' 
    : role === 'Admin' 
    ? 'bg-purple-600 border-purple-400 text-white' 
    : 'bg-emerald-600 border-emerald-400 text-white'

  const displayName = user?.full_name ? transliterate(user.full_name) : user?.name ? transliterate(user.name) : 'User'

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={`
          fixed top-0 left-0 h-full z-40 w-64 bg-[#1B3A1C] text-white
          flex flex-col shadow-2xl transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:static lg:shadow-none
        `}
      >
        {/* Logo & Portal Banner */}
        <div className="p-5 border-b border-white/10">
          <div className="flex items-center justify-between">
            <Link to={role === 'Buyer' ? '/buyer' : role === 'Admin' ? '/admin' : '/dashboard'} className="flex items-center gap-2.5" onClick={onClose}>
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-xl font-bold">
                🌾
              </div>
              <div>
                <span className="text-base font-extrabold text-white">SmartAgri</span>
                <span className="text-base font-extrabold text-[#FF9800]"> AI</span>
              </div>
            </Link>
            <button
              onClick={onClose}
              className="lg:hidden w-7 h-7 rounded-lg flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
            >
              ✕
            </button>
          </div>

          <div className="mt-3 flex items-center justify-between">
            <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider border ${roleBadgeColor}`}>
              {portalTitle}
            </span>
          </div>
        </div>

        {/* User Info */}
        <Link
          to="/profile"
          onClick={onClose}
          className="mx-3 my-2 px-3 py-3 rounded-xl flex items-center gap-3 hover:bg-white/10 transition-colors group"
          title="View Profile"
        >
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#FF9800] to-[#F57C00] flex items-center justify-center text-white font-bold text-sm flex-shrink-0 ring-2 ring-transparent group-hover:ring-white/30 transition-all">
            {displayName.charAt(0)?.toUpperCase() || 'U'}
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-bold text-white truncate group-hover:text-[#FF9800] transition-colors">{displayName}</p>
            <p className="text-xs text-white/50 truncate">
              {role === 'Buyer' ? t('roles.buyer') : role === 'Admin' ? t('roles.admin') : t('roles.farmer')}
            </p>
          </div>
          <span className="text-white/30 text-xs group-hover:text-white/60 transition-colors">›</span>
        </Link>
        <div className="mx-3 border-b border-white/10 mb-1" />

        {/* Dynamic Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <li key={item.href}>
                  <Link
                    to={item.href}
                    onClick={onClose}
                    className={`
                      flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all duration-150
                      ${isActive
                        ? 'bg-[#2E7D32] text-white shadow-sm font-bold'
                        : 'text-white/70 hover:text-white hover:bg-white/10'
                      }
                    `}
                  >
                    <span className="text-lg">{item.icon}</span>
                    {item.label}
                    {isActive && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-amber-400" />}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-white/10">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium text-white/70 hover:text-white hover:bg-red-600/30 transition-all cursor-pointer"
          >
            <span className="text-lg">🚪</span>
            {t('nav.logout', 'Sign Out')}
          </button>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
