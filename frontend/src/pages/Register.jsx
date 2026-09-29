import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Button from '../components/Button'
import Input from '../components/Input'

const Register = () => {
  const navigate = useNavigate()
  const { register } = useAuth()

  const [form, setForm] = useState({
    name: '', phone: '', email: '', password: '', confirmPassword: '',
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const validate = () => {
    const e = {}
    if (!form.name.trim()) e.name = 'Full name is required'
    if (!form.phone.trim()) e.phone = 'Phone number is required'
    else if (!/^[6-9]\d{9}$/.test(form.phone)) e.phone = 'Enter a valid 10-digit mobile number'
    if (!form.email) e.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(form.email)) e.email = 'Enter a valid email'
    if (!form.password) e.password = 'Password is required'
    else if (form.password.length < 6) e.password = 'Password must be at least 6 characters'
    if (!form.confirmPassword) e.confirmPassword = 'Please confirm your password'
    else if (form.password !== form.confirmPassword) e.confirmPassword = 'Passwords do not match'
    return e
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }
    setLoading(true)
    await new Promise((r) => setTimeout(r, 1200))
    register(form)
    navigate('/dashboard')
  }

  const handleChange = (field) => (e) => {
    setForm({ ...form, [field]: e.target.value })
    if (errors[field]) setErrors({ ...errors, [field]: '' })
  }

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-50 py-12 px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-4xl mx-auto mb-4 shadow-lg">
            🌱
          </div>
          <h2 className="text-3xl font-extrabold text-[#333333]">Create Account</h2>
          <p className="text-gray-500 mt-2">Join SmartAgri AI – It's free!</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8">
          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <Input
              id="name"
              label="Full Name"
              placeholder="Ramesh Patil"
              value={form.name}
              onChange={handleChange('name')}
              error={errors.name}
              icon="👤"
              required
            />
            <Input
              id="phone"
              label="Mobile Number"
              type="tel"
              placeholder="9876543210"
              value={form.phone}
              onChange={handleChange('phone')}
              error={errors.phone}
              icon="📱"
              required
            />
            <Input
              id="email"
              label="Email Address"
              type="email"
              placeholder="ramesh@example.com"
              value={form.email}
              onChange={handleChange('email')}
              error={errors.email}
              icon="📧"
              required
            />
            <div className="relative">
              <Input
                id="password"
                label="Password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Minimum 6 characters"
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
            <Input
              id="confirmPassword"
              label="Confirm Password"
              type="password"
              placeholder="Re-enter your password"
              value={form.confirmPassword}
              onChange={handleChange('confirmPassword')}
              error={errors.confirmPassword}
              icon="✅"
              required
            />

            <div className="pt-2">
              <Button type="submit" fullWidth loading={loading} size="lg">
                🚀 Create My Account
              </Button>
            </div>
          </form>

          <p className="text-center text-xs text-gray-400 mt-5">
            By registering, you agree to our Terms of Service and Privacy Policy
          </p>

          <p className="text-center text-sm text-gray-500 mt-4">
            Already have an account?{' '}
            <Link to="/login" className="font-bold text-[#2E7D32] hover:underline">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Register
