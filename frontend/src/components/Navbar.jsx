import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useLanguage } from '../context/LanguageContext'

// Public Navbar for landing pages
const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()
  const { language, setLanguage, t } = useLanguage()

  const links = [
    { label: t('nav.home', 'Home'), href: '/' },
    { label: t('nav.about', 'About'), href: '/about' },
    { label: t('nav.features', 'Features'), href: '/#features' },
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-40 bg-white/90 backdrop-blur-md border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-white text-lg font-bold shadow-sm group-hover:scale-105 transition-transform">
              🌾
            </div>
            <div>
              <span className="text-lg font-extrabold text-[#2E7D32]">SmartAgri</span>
              <span className="text-lg font-extrabold text-[#FF9800]"> AI</span>
            </div>
          </Link>

          {/* Desktop Nav links */}
          <nav className="hidden md:flex items-center gap-1">
            {links.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className={`
                  px-4 py-2 rounded-lg text-sm font-medium transition-all
                  ${location.pathname === link.href
                    ? 'text-[#2E7D32] bg-green-50'
                    : 'text-gray-600 hover:text-[#2E7D32] hover:bg-green-50'
                  }
                `}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* CTA Buttons + Language Selector */}
          <div className="hidden md:flex items-center gap-3">
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

            <Link
              to="/login"
              className="px-4 py-2 text-sm font-semibold text-[#2E7D32] border-2 border-[#2E7D32] rounded-xl hover:bg-[#2E7D32] hover:text-white transition-all duration-200"
            >
              {t('auth.loginBtn', 'Login')}
            </Link>
            <Link
              to="/register"
              className="px-4 py-2 text-sm font-semibold text-white bg-[#2E7D32] rounded-xl hover:bg-[#1B5E20] shadow-sm transition-all duration-200"
            >
              {t('auth.getStarted', 'Get Started')}
            </Link>
          </div>

          {/* Mobile menu toggle */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden w-10 h-10 rounded-lg flex items-center justify-center text-gray-600 hover:bg-gray-100 transition-colors cursor-pointer"
            aria-label="Toggle menu"
            aria-expanded={menuOpen}
          >
            {menuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-4 pb-4">
          <nav className="flex flex-col gap-1 pt-2">
            <div className="py-2">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full text-xs font-bold bg-emerald-50 border border-emerald-300 rounded-xl px-3 py-2 text-emerald-900 outline-none cursor-pointer"
                aria-label="Select Language"
              >
                <option value="English">English</option>
                <option value="Hindi">हिंदी</option>
                <option value="Marathi">मराठी</option>
              </select>
            </div>
            {links.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                onClick={() => setMenuOpen(false)}
                className="px-4 py-3 rounded-lg text-sm font-medium text-gray-700 hover:text-[#2E7D32] hover:bg-green-50 transition-all"
              >
                {link.label}
              </Link>
            ))}
            <div className="flex gap-3 pt-2">
              <Link
                to="/login"
                onClick={() => setMenuOpen(false)}
                className="flex-1 text-center py-2.5 text-sm font-semibold text-[#2E7D32] border-2 border-[#2E7D32] rounded-xl"
              >
                {t('auth.loginBtn', 'Login')}
              </Link>
              <Link
                to="/register"
                onClick={() => setMenuOpen(false)}
                className="flex-1 text-center py-2.5 text-sm font-semibold text-white bg-[#2E7D32] rounded-xl"
              >
                {t('auth.getStarted', 'Get Started')}
              </Link>
            </div>
          </nav>
        </div>
      )}
    </header>
  )
}

export default Navbar
