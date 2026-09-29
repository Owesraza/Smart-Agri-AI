import { useState } from 'react'
import { Link } from 'react-router-dom'
import axiosClient from '../api/axiosClient'
import { useLanguage } from '../context/LanguageContext'
import Button from '../components/Button'
import Input from '../components/Input'

const ForgotPassword = () => {
  const { t } = useLanguage()
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) return
    setLoading(true)
    setErrorMsg(null)
    try {
      await axiosClient.post('/api/v1/auth/forgot-password', { email })
      setSubmitted(true)
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.detail || 'Unable to process reset request. Please check the email address.'
      setErrorMsg(typeof msg === 'string' ? msg : JSON.stringify(msg))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 py-12 px-4">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl border border-gray-100 p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center text-3xl mx-auto shadow-md">
            🔒
          </div>
          <h2 className="text-2xl font-extrabold text-gray-900">{t('auth.resetPassword', 'Reset Password')}</h2>
          <p className="text-xs text-gray-500">{t('auth.resetSubtitle', 'Enter your registered email address to receive password reset instructions')}</p>
        </div>

        {submitted ? (
          <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-6 text-center space-y-3">
            <div className="text-4xl">📧</div>
            <h3 className="text-base font-bold text-emerald-900">{t('auth.resetSuccessTitle', 'Reset Verification Link Sent!')}</h3>
            <p className="text-xs text-emerald-700">
              {t('auth.resetSuccessDesc', 'We have sent password reset instructions to your email. Please check your inbox.')} ({email})
            </p>
            <div className="pt-2">
              <Link to="/login" className="text-xs font-extrabold text-emerald-800 hover:underline">
                {t('auth.returnToLogin', 'Return to Login')}
              </Link>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {errorMsg && (
              <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs font-bold rounded-xl text-center">
                ⚠️ {errorMsg}
              </div>
            )}
            <Input
              id="email"
              label={t('auth.email', 'Registered Email Address')}
              type="email"
              placeholder="user@smartagri.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              icon="📧"
              required
            />

            <Button type="submit" fullWidth loading={loading} className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-3 rounded-xl text-sm">
              {loading ? t('auth.signingIn', 'Sending...') : `${t('auth.sendResetLink', 'Send Reset Instructions')} →`}
            </Button>

            <div className="text-center pt-2">
              <Link to="/login" className="text-xs font-semibold text-gray-500 hover:underline">
                ← {t('auth.returnToLogin', 'Return to Login')}
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default ForgotPassword
