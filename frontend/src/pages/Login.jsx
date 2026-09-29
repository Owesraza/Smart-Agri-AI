import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import Button from '../components/Button'
import Input from '../components/Input'

const Login = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  const { t } = useLanguage()

  const [form, setForm] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [loginError, setLoginError] = useState(null)

  const validate = () => {
    const e = {}
    if (!form.email) e.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(form.email)) e.email = 'Enter a valid email address'
    if (!form.password) e.password = 'Password is required'
    else if (form.password.length < 6) e.password = 'Password must be at least 6 characters'
    return e
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoginError(null)
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }

    setLoading(true)
    try {
      // Properly await async login function
      const userObj = await login(form.email, form.password)
      const role = userObj?.role || 'Farmer'

      // Automatic Role-based Redirect from Permanent User Profile
      if (role === 'Buyer') navigate('/buyer')
      else if (role === 'Admin') navigate('/admin')
      else navigate('/dashboard')
    } catch (err) {
      console.error('Sign in error:', err)
      const backendMsg = err.response?.data?.message || err.message || 'Invalid email or password. Please check your credentials.'
      setLoginError(backendMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field) => (e) => {
    setForm({ ...form, [field]: e.target.value })
    if (errors[field]) setErrors({ ...errors, [field]: '' })
    if (loginError) setLoginError(null)
  }

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 py-12 px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-4xl mx-auto mb-4 shadow-lg">
            🌾
          </div>
          <h2 className="text-3xl font-extrabold text-gray-900">{t('auth.welcomeBack', 'Welcome Back')}</h2>
          <p className="text-gray-500 mt-2 text-sm">{t('auth.loginSubtitle', 'Sign in to your SmartAgri AI marketplace account')}</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 space-y-6">
          {loginError && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs font-bold rounded-xl text-center">
              ⚠️ {loginError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <Input
              id="email"
              label={t('auth.email', 'Email Address')}
              type="email"
              placeholder="user@smartagri.com"
              value={form.email}
              onChange={handleChange('email')}
              error={errors.email}
              icon="📧"
              required
            />

            <div className="relative">
              <Input
                id="password"
                label={t('auth.password', 'Password')}
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange('password')}
                error={errors.password}
                icon="🔒"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-[42px] text-gray-400 hover:text-gray-600 text-sm cursor-pointer"
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between text-xs">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4 h-4 rounded border-gray-300 text-emerald-700 accent-emerald-700"
                />
                <span className="text-gray-600 font-medium">{t('auth.rememberMe', 'Remember me')}</span>
              </label>
              <Link to="/forgot-password" className="font-bold text-emerald-700 hover:underline">
                {t('auth.forgotPassword', 'Forgot password?')}
              </Link>
            </div>

            <Button type="submit" fullWidth loading={loading} size="lg" className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-3.5 rounded-2xl text-sm cursor-pointer">
              {loading ? t('auth.signingIn', 'Signing in...') : `${t('auth.signInBtn', 'Sign In')} →`}
            </Button>
          </form>

          {/* Account Registration Link */}
          <div className="pt-2 text-center border-t border-gray-100">
            <p className="text-xs text-gray-500">
              {t('auth.dontHaveAccount', "Don't have an account yet?")}{' '}
              <Link to="/register" className="font-bold text-emerald-700 hover:underline">
                {t('auth.registerHere', 'Create Account Here')}
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
