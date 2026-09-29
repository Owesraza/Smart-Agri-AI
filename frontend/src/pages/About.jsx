const techStack = [
  { category: 'Frontend', items: ['React.js 18', 'Tailwind CSS', 'React Router v6', 'Recharts', 'Axios'], icon: '💻', color: 'from-blue-500 to-indigo-600' },
  { category: 'Backend', items: ['FastAPI (Python)', 'MongoDB (Atlas)', 'JWT Authentication', 'RESTful APIs', 'CORS Middleware'], icon: '⚙️', color: 'from-green-500 to-emerald-600' },
  { category: 'AI / ML', items: ['Google Gemini 1.5', 'LangChain Framework', 'FAISS Vector DB', 'Prompt Engineering', 'RAG Pipeline'], icon: '🤖', color: 'from-purple-500 to-violet-600' },
  { category: 'Deployment', items: ['Vercel (Frontend)', 'Railway (Backend)', 'MongoDB Atlas', 'Docker', 'GitHub Actions'], icon: '🚀', color: 'from-orange-500 to-red-600' },
]

const timeline = [
  { phase: 'Phase 1', title: 'Frontend Development', desc: 'Complete React.js UI with all pages and components', status: 'Completed' },
  { phase: 'Phase 2', title: 'Backend API', desc: 'FastAPI with MongoDB integration and JWT auth', status: 'In Progress' },
  { phase: 'Phase 3', title: 'AI Integration', desc: 'Gemini AI + LangChain for market recommendations', status: 'Upcoming' },
  { phase: 'Phase 4', title: 'Testing & Deployment', desc: 'End-to-end testing and cloud deployment', status: 'Upcoming' },
]

const About = () => {
  return (
    <div className="py-16">
      {/* Hero */}
      <section className="bg-gradient-to-br from-[#1B3A1C] to-[#2E7D32] text-white py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-4 py-2 mb-6 text-sm font-medium">
            Final Year B.Tech · Computer Engineering · 2025–26
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold mb-6">About SmartAgri AI</h1>
          <p className="text-lg text-white/80 max-w-3xl mx-auto leading-relaxed">
            An AI-powered closed-loop agricultural management platform that empowers Indian farmers
            with intelligent market insights, automated workflow guidance, and data-driven profit optimization.
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Vision & Mission */}
        <section className="py-16 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-[#F8F9FA] rounded-2xl p-8 border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-[#2E7D32]/10 flex items-center justify-center text-2xl mb-5">🎯</div>
            <h2 className="text-2xl font-extrabold text-[#333333] mb-4">Our Vision</h2>
            <p className="text-gray-600 leading-relaxed">
              To create an intelligent digital ecosystem where every Indian farmer, regardless of technical literacy,
              can access market intelligence, AI-driven insights, and financial management tools to maximize
              their agricultural income and reduce post-harvest losses.
            </p>
          </div>
          <div className="bg-[#F8F9FA] rounded-2xl p-8 border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-[#FF9800]/10 flex items-center justify-center text-2xl mb-5">🚀</div>
            <h2 className="text-2xl font-extrabold text-[#333333] mb-4">Our Mission</h2>
            <p className="text-gray-600 leading-relaxed">
              To bridge the information gap between farmers and markets through AI-powered recommendations,
              real-time APMC price aggregation, and a simplified decision-support system that guides
              farmers from sowing to selling – maximizing profits at every step.
            </p>
          </div>
        </section>

        {/* Research Objectives */}
        <section className="pb-16">
          <h2 className="text-3xl font-extrabold text-[#333333] mb-8 text-center">Research Objectives</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              'Develop an AI model for agricultural market price prediction',
              'Build a RAG-based chatbot for farmer query resolution',
              'Create a closed-loop workflow from planting to selling',
              'Design an accessible UI for low digital literacy users',
              'Integrate real-time APMC mandi data aggregation',
              'Implement profit optimization using historical data analysis',
            ].map((obj, i) => (
              <div key={i} className="flex items-start gap-4 p-5 bg-[#F8F9FA] rounded-xl border border-gray-100">
                <span className="w-8 h-8 rounded-lg bg-[#2E7D32] text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                  {i + 1}
                </span>
                <p className="text-sm text-gray-700 font-medium leading-relaxed">{obj}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Tech Stack */}
        <section className="pb-16">
          <h2 className="text-3xl font-extrabold text-[#333333] mb-8 text-center">Technology Stack</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {techStack.map((tech) => (
              <div key={tech.category} className="bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100 hover:shadow-md transition-shadow">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${tech.color} flex items-center justify-center text-2xl mb-4 shadow-sm`}>
                  {tech.icon}
                </div>
                <h3 className="text-base font-bold text-[#333333] mb-3">{tech.category}</h3>
                <ul className="space-y-2">
                  {tech.items.map((item) => (
                    <li key={item} className="text-xs text-gray-600 flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#2E7D32] flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Development Timeline */}
        <section className="pb-16">
          <h2 className="text-3xl font-extrabold text-[#333333] mb-8 text-center">Development Timeline</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {timeline.map((t, i) => (
              <div key={t.phase} className="relative bg-[#F8F9FA] rounded-2xl p-6 border border-gray-100">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-xs font-bold text-[#2E7D32] bg-green-100 px-2.5 py-1 rounded-full">{t.phase}</span>
                  <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                    t.status === 'Completed' ? 'bg-green-100 text-green-700' :
                    t.status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                    'bg-gray-100 text-gray-500'
                  }`}>{t.status}</span>
                </div>
                <h3 className="text-sm font-bold text-[#333333] mb-2">{t.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{t.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}

export default About
