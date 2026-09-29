import { Link } from 'react-router-dom'

// Public Footer
const Footer = () => {
  return (
    <footer className="bg-[#1B3A1C] text-white pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-white text-xl font-bold">
                🌾
              </div>
              <div>
                <span className="text-xl font-extrabold text-white">SmartAgri</span>
                <span className="text-xl font-extrabold text-[#FF9800]"> AI</span>
              </div>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed max-w-sm">
              Empowering Indian farmers with AI-driven market intelligence, profit tracking,
              and smart agricultural planning. A Final Year B.Tech Computer Engineering Project.
            </p>
            <div className="flex gap-3 mt-5">
              {['📧', '📱', '🌐'].map((icon, i) => (
                <button
                  key={i}
                  className="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center text-base hover:bg-white/20 transition-colors cursor-pointer"
                >
                  {icon}
                </button>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Quick Links</h4>
            <ul className="space-y-2.5">
              {[
                { label: 'Home', href: '/' },
                { label: 'About', href: '/about' },
                { label: 'Login', href: '/login' },
                { label: 'Register', href: '/register' },
              ].map((link) => (
                <li key={link.href}>
                  <Link
                    to={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Features */}
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Features</h4>
            <ul className="space-y-2.5 text-sm text-gray-400">
              {['Market Intelligence', 'AI Assistant', 'Plot Management', 'Ledger & Profit', 'Analytics'].map((f) => (
                <li key={f}>{f}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/10 pt-8 flex flex-col sm:flex-row justify-between items-center gap-3">
          <p className="text-gray-500 text-sm">
            © 2026 SmartAgri AI. Final Year B.Tech Project – Computer Engineering.
          </p>
          <p className="text-gray-500 text-sm">
            Made with ❤️ for Indian Farmers 🇮🇳
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
