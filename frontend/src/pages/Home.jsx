import { Link } from 'react-router-dom'

const features = [
  {
    icon: '📊',
    title: 'Real-Time Market Prices',
    desc: 'Get live APMC mandi prices for all major crops across Maharashtra and India.',
    color: 'from-green-500 to-emerald-600',
  },
  {
    icon: '🤖',
    title: 'AI-Powered Recommendations',
    desc: 'Gemini AI analyzes market trends and recommends the best time and mandi to sell.',
    color: 'from-blue-500 to-indigo-600',
  },
  {
    icon: '🌱',
    title: 'Plot Management',
    desc: 'Track all your farm plots, crops, sowing dates, and harvest schedules in one place.',
    color: 'from-teal-500 to-cyan-600',
  },
  {
    icon: '💰',
    title: 'Profit Calculator',
    desc: 'Track income, expenses, and net profit per crop with automatic calculations.',
    color: 'from-orange-500 to-amber-600',
  },
  {
    icon: '📈',
    title: 'Advanced Analytics',
    desc: 'Visualize crop performance, price trends, and seasonal patterns with charts.',
    color: 'from-purple-500 to-violet-600',
  },
  {
    icon: '📋',
    title: 'Smart Workflow',
    desc: 'Follow guided farming steps from soil prep to market selling with reminders.',
    color: 'from-rose-500 to-pink-600',
  },
]

const stats = [
  { value: '50,000+', label: 'Farmers Helped' },
  { value: '200+', label: 'APMC Mandis Covered' },
  { value: '98%', label: 'Accuracy Rate' },
  { value: '₹2Cr+', label: 'Profit Generated' },
]

const testimonials = [
  {
    name: 'Suresh Yadav',
    role: 'Wheat Farmer, Nashik',
    text: 'SmartAgri AI told me to wait 2 more weeks before selling. I earned ₹28,000 extra!',
    avatar: 'SY',
  },
  {
    name: 'Kavita Deshmukh',
    role: 'Onion Farmer, Lasalgaon',
    text: 'The mandi price comparison helped me find the best market. My profit margin went up 34%.',
    avatar: 'KD',
  },
  {
    name: 'Raju Patil',
    role: 'Multi-Crop Farmer, Pune',
    text: 'The dashboard is very easy to use. Even my father who is 65 can use it comfortably.',
    avatar: 'RP',
  },
]

const Home = () => {
  return (
    <div className="overflow-x-hidden">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-[#1B3A1C] via-[#2E7D32] to-[#388E3C] text-white py-28 md:py-36 overflow-hidden">
        {/* Background decorations */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="absolute top-1/2 right-1/4 w-32 h-32 bg-[#FF9800]/20 rounded-full blur-xl" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 backdrop-blur-sm rounded-full px-4 py-2 mb-8 text-sm font-medium">
            <span className="w-2 h-2 bg-[#FF9800] rounded-full animate-pulse" />
            Final Year B.Tech Project · AI-Powered Agriculture Platform
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold leading-tight tracking-tight mb-6">
            Smart Farming,{' '}
            <span className="text-[#FF9800] relative">
              Maximum Profit
              <svg className="absolute -bottom-2 left-0 w-full" height="8" viewBox="0 0 300 8" fill="none">
                <path d="M0 6 Q75 0 150 6 Q225 12 300 6" stroke="#FF9800" strokeWidth="3" strokeLinecap="round" fill="none" opacity="0.5"/>
              </svg>
            </span>
          </h1>

          <p className="text-lg sm:text-xl md:text-2xl text-white/80 max-w-3xl mx-auto mb-10 leading-relaxed">
            SmartAgri AI guides farmers from market price discovery to final profit calculation,
            powered by Gemini AI. Know the right time, the right mandi, and the right price.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="inline-flex items-center justify-center gap-2 bg-[#FF9800] hover:bg-[#F57C00] text-white font-bold text-lg px-8 py-4 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 hover:-translate-y-0.5"
            >
              🚀 Start for Free
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center justify-center gap-2 bg-white/10 border border-white/30 hover:bg-white/20 text-white font-bold text-lg px-8 py-4 rounded-2xl backdrop-blur-sm transition-all duration-200"
            >
              🔑 Farmer Login
            </Link>
          </div>

          {/* Hero stats */}
          <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto">
            {stats.map((s) => (
              <div key={s.label} className="bg-white/10 border border-white/20 backdrop-blur-sm rounded-2xl p-4">
                <p className="text-2xl font-extrabold text-[#FF9800]">{s.value}</p>
                <p className="text-sm text-white/70 mt-1">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-[#2E7D32] uppercase tracking-wider">Features</span>
            <h2 className="text-4xl font-extrabold text-[#333333] mt-2 mb-4">
              Everything a farmer needs
            </h2>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto">
              From real-time market intelligence to AI-powered sell decisions – all in one platform.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div
                key={f.title}
                className="group bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center text-3xl mb-5 shadow-md group-hover:scale-110 transition-transform`}>
                  {f.icon}
                </div>
                <h3 className="text-lg font-bold text-[#333333] mb-2">{f.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 bg-gradient-to-br from-[#F8F9FA] to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-[#2E7D32] uppercase tracking-wider">How It Works</span>
            <h2 className="text-4xl font-extrabold text-[#333333] mt-2 mb-4">3 Simple Steps</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '01', icon: '📝', title: 'Register Your Farm', desc: 'Create your free account and add your farm plots and crops.' },
              { step: '02', icon: '📊', title: 'Check Market Prices', desc: 'Get real-time APMC prices and AI-powered selling recommendations.' },
              { step: '03', icon: '💰', title: 'Maximize Profit', desc: 'Sell at the right time, track your earnings, and grow your income.' },
            ].map((s) => (
              <div key={s.step} className="relative text-center group">
                <div className="w-16 h-16 rounded-2xl bg-[#2E7D32]/10 flex items-center justify-center text-3xl mx-auto mb-5 group-hover:bg-[#2E7D32] group-hover:scale-105 transition-all duration-300">
                  <span className="group-hover:hidden">{s.icon}</span>
                  <span className="hidden group-hover:block text-white font-extrabold">{s.step}</span>
                </div>
                <h3 className="text-xl font-bold text-[#333333] mb-3">{s.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed max-w-xs mx-auto">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-[#2E7D32] uppercase tracking-wider">Testimonials</span>
            <h2 className="text-4xl font-extrabold text-[#333333] mt-2 mb-4">Farmers Love SmartAgri AI</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((t) => (
              <div
                key={t.name}
                className="bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="flex gap-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className="text-[#FF9800]">★</span>
                  ))}
                </div>
                <p className="text-gray-600 text-sm leading-relaxed mb-5 italic">"{t.text}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-white font-bold text-sm">
                    {t.avatar}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-[#333333]">{t.name}</p>
                    <p className="text-xs text-gray-400">{t.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-[#1B3A1C] to-[#2E7D32] text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-8 left-8 text-8xl">🌾</div>
          <div className="absolute top-8 right-8 text-8xl">🚜</div>
          <div className="absolute bottom-8 left-1/4 text-8xl">🌱</div>
        </div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl sm:text-5xl font-extrabold mb-6">
            Ready to grow your profit?
          </h2>
          <p className="text-xl text-white/80 mb-10">
            Join thousands of farmers who are already making smarter decisions with SmartAgri AI.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center justify-center gap-2 bg-[#FF9800] hover:bg-[#F57C00] text-white font-bold text-xl px-10 py-5 rounded-2xl shadow-2xl hover:shadow-[#FF9800]/30 hover:-translate-y-1 transition-all duration-200"
          >
            🌾 Start Your Free Journey
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
