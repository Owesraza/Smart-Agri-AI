import { Link } from 'react-router-dom'
import { useLanguage } from '../context/LanguageContext'

const RegisterChoice = () => {
  const { t } = useLanguage()

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 py-12 px-4">
      <div className="w-full max-w-4xl space-y-8 text-center">
        {/* Logo & Header */}
        <div className="space-y-3">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-5xl mx-auto shadow-xl">
            🌾
          </div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            {t('appName', 'SmartAgri AI')}
          </h1>
          <p className="text-gray-600 max-w-lg mx-auto text-base">
            {t('auth.chooseAccountType', 'Choose Account Type')}
          </p>
        </div>

        {/* Account Type Selection Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
          {/* Farmer Card */}
          <div className="bg-white rounded-3xl border-2 border-emerald-200 hover:border-emerald-500 shadow-lg hover:shadow-2xl transition-all duration-300 p-8 flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center text-3xl font-bold group-hover:scale-110 transition-transform">
                🌾
              </div>
              <h2 className="text-2xl font-bold text-gray-900">{t('auth.farmerAccount', 'Farmer Account')}</h2>
              <p className="text-sm text-gray-600">
                {t('auth.farmerAccountDesc', 'For individual farmers, farm owners, and agricultural producers looking to sell crops directly to verified buyers.')}
              </p>

              <ul className="space-y-2.5 pt-2 text-xs font-semibold text-gray-700">
                <li className="flex items-center gap-2">
                  <span className="text-emerald-600 font-bold">✓</span> {t('features.cropListing', 'Direct crop listings & buyer offers')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-emerald-600 font-bold">✓</span> {t('features.aiPriceRec', 'AI price & sell recommendations')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-emerald-600 font-bold">✓</span> {t('features.ledger', 'Digital ledger & farm plot manager')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-emerald-600 font-bold">✓</span> {t('features.directConnect', 'Guaranteed payment workflows')}
                </li>
              </ul>
            </div>

            <div className="pt-8">
              <Link
                to="/register/farmer"
                className="w-full block text-center bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-3.5 rounded-2xl shadow-md transition-all cursor-pointer text-sm"
              >
                {t('auth.registerAsFarmer', 'Register as Farmer →')}
              </Link>
            </div>
          </div>

          {/* Buyer Card */}
          <div className="bg-white rounded-3xl border-2 border-blue-200 hover:border-blue-500 shadow-lg hover:shadow-2xl transition-all duration-300 p-8 flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-blue-100 text-blue-800 flex items-center justify-center text-3xl font-bold group-hover:scale-110 transition-transform">
                🏢
              </div>
              <h2 className="text-2xl font-bold text-gray-900">{t('auth.buyerAccount', 'Buyer Account')}</h2>
              <p className="text-sm text-gray-600">
                {t('auth.buyerAccountDesc', 'For agribusinesses, traders, food processors, and wholesalers procuring bulk agricultural commodities.')}
              </p>

              <ul className="space-y-2.5 pt-2 text-xs font-semibold text-gray-700">
                <li className="flex items-center gap-2">
                  <span className="text-blue-600 font-bold">✓</span> {t('features.buyingReqs', 'Post bulk buying requirements')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-blue-600 font-bold">✓</span> {t('features.aiMatcher', 'AI Matcher for top farmer recommendations')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-blue-600 font-bold">✓</span> {t('features.realTimeDeals', 'Real-time negotiation & deal timelines')}
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-blue-600 font-bold">✓</span> {t('features.taxInvoice', 'Tax invoice & transaction management')}
                </li>
              </ul>
            </div>

            <div className="pt-8">
              <Link
                to="/register/buyer"
                className="w-full block text-center bg-blue-700 hover:bg-blue-800 text-white font-bold py-3.5 rounded-2xl shadow-md transition-all cursor-pointer text-sm"
              >
                {t('auth.registerAsBuyer', 'Register as Buyer →')}
              </Link>
            </div>
          </div>
        </div>

        {/* Footer Login Link */}
        <div className="pt-4">
          <p className="text-sm text-gray-600">
            {t('auth.alreadyHaveAccount', 'Already have an account?')}{' '}
            <Link to="/login" className="font-bold text-emerald-700 hover:underline">
              {t('auth.loginHere', 'Sign In Here')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default RegisterChoice
