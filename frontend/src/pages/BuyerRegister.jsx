import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import Button from '../components/Button'

const BuyerRegister = () => {
  const navigate = useNavigate()
  const { registerBuyer } = useAuth()
  const { t } = useLanguage()

  const [form, setForm] = useState({
    companyName: '',
    ownerName: '',
    email: '',
    mobileNumber: '',
    password: '',
    confirmPassword: '',
    gstNumber: '27AAACA1234A1Z5',
    businessLicense: 'APMC-NSK-992',
    state: 'Maharashtra',
    district: 'Nashik',
    businessAddress: 'Market Yard, Nashik',
    preferredCrops: 'Wheat, Onion, Tomato',
    dailyCapacity: '200.0',
    paymentTerms: 'Immediate',
    preferredLanguage: 'English',
    termsAccepted: false,
  })

  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [registerError, setRegisterError] = useState(null)

  const validate = () => {
    const e = {}
    if (!form.companyName) e.companyName = t('auth.companyName', 'Company name is required')
    if (!form.ownerName) e.ownerName = t('auth.ownerName', 'Owner name is required')
    if (!form.email) e.email = t('auth.errors.emailReq', 'Email is required')
    if (!form.mobileNumber) e.mobileNumber = t('auth.errors.phoneReq', 'Mobile number is required')
    if (!form.password) e.password = t('auth.errors.passReq', 'Password is required')
    else if (form.password.length < 6) e.password = t('auth.errors.passMin', 'Password must be at least 6 characters')
    if (form.password !== form.confirmPassword) e.confirmPassword = t('auth.errors.passMatch', 'Passwords do not match')
    if (!form.termsAccepted) e.termsAccepted = t('auth.errors.termsReq', 'You must accept the terms and conditions')
    return e
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setRegisterError(null)
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }

    setLoading(true)
    try {
      await registerBuyer(form)
      navigate('/buyer')
    } catch (err) {
      console.error('Buyer registration error:', err)
      const msg = err.response?.data?.message || err.response?.data?.detail || err.message || 'Registration failed. Please try again.'
      setRegisterError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-[#1E293B]/5 via-blue-50 to-indigo-50 py-12 px-4">
      <div className="w-full max-w-2xl bg-white rounded-3xl shadow-xl border border-gray-100 p-8 space-y-6">
        {registerError && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs font-bold rounded-xl text-center">
            ⚠️ {registerError}
          </div>
        )}
        {/* Header with Buyer Illustration */}
        <div className="flex items-center gap-4 border-b pb-6">
          <div className="w-14 h-14 rounded-2xl bg-blue-100 text-blue-800 flex items-center justify-center text-3xl font-bold flex-shrink-0">
            🏢
          </div>
          <div>
            <span className="text-xs font-extrabold text-blue-800 bg-blue-100 px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              {t('auth.buyerAccount', 'Buyer Account Registration')}
            </span>
            <h2 className="text-2xl font-extrabold text-gray-900 mt-1">{t('auth.createBuyerAccount', 'Create Your Buyer Account')}</h2>
            <p className="text-xs text-gray-500">{t('auth.buyerRegSubtitle', 'Procure bulk agricultural commodities directly from verified farmers')}</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.companyName', 'Company / Firm Name *')}</label>
              <input
                type="text"
                placeholder="Amit Agro Processors Ltd"
                value={form.companyName}
                onChange={(e) => setForm({ ...form, companyName: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.companyName && <p className="text-xs text-red-500 mt-1">{errors.companyName}</p>}
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.ownerName', 'Owner / Representative Name *')}</label>
              <input
                type="text"
                placeholder="Amit Sharma"
                value={form.ownerName}
                onChange={(e) => setForm({ ...form, ownerName: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.ownerName && <p className="text-xs text-red-500 mt-1">{errors.ownerName}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.email', 'Email Address *')}</label>
              <input
                type="email"
                placeholder="buyer@smartagri.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email}</p>}
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.mobileNumber', 'Mobile Number *')}</label>
              <input
                type="tel"
                placeholder="9876599999"
                value={form.mobileNumber}
                onChange={(e) => setForm({ ...form, mobileNumber: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.mobileNumber && <p className="text-xs text-red-500 mt-1">{errors.mobileNumber}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.gstNumber', 'GST Number (Optional)')}</label>
              <input
                type="text"
                placeholder="27AAACA1234A1Z5"
                value={form.gstNumber}
                onChange={(e) => setForm({ ...form, gstNumber: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.apmcLicense', 'APMC License Number (Optional)')}</label>
              <input
                type="text"
                placeholder="APMC-NSK-992"
                value={form.businessLicense}
                onChange={(e) => setForm({ ...form, businessLicense: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.district', 'District *')}</label>
              <input
                type="text"
                value={form.district}
                onChange={(e) => setForm({ ...form, district: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.dailyCapacity', 'Daily Capacity (Quintals)')}</label>
              <input
                type="number"
                placeholder="200"
                value={form.dailyCapacity}
                onChange={(e) => setForm({ ...form, dailyCapacity: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.password', 'Password *')}</label>
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.password && <p className="text-xs text-red-500 mt-1">{errors.password}</p>}
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('auth.confirmPassword', 'Confirm Password *')}</label>
              <input
                type="password"
                value={form.confirmPassword}
                onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              />
              {errors.confirmPassword && <p className="text-xs text-red-500 mt-1">{errors.confirmPassword}</p>}
            </div>
          </div>

          {/* Terms checkbox */}
          <div className="pt-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={form.termsAccepted}
                onChange={(e) => setForm({ ...form, termsAccepted: e.target.checked })}
                className="w-4 h-4 rounded border-gray-300 text-blue-700 accent-blue-700"
              />
              <span className="text-xs text-gray-600">{t('auth.acceptTerms', 'I agree to the Terms & Conditions and Privacy Policy')}</span>
            </label>
            {errors.termsAccepted && <p className="text-xs text-red-500 mt-1">{errors.termsAccepted}</p>}
          </div>

          <div className="pt-4 flex items-center justify-between">
            <Link to="/register" className="text-xs font-semibold text-gray-500 hover:underline">
              ← {t('auth.chooseAccountType', 'Change Account Type')}
            </Link>
            <Button type="submit" loading={loading} className="bg-blue-700 hover:bg-blue-800 text-white font-bold px-8 py-3 rounded-2xl text-sm">
              {loading ? t('auth.creatingAccount', 'Creating Account...') : `${t('auth.registerAsBuyer', 'Create Buyer Account')} →`}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default BuyerRegister
