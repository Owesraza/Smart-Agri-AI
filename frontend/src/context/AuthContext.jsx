import { createContext, useContext, useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'

const AuthContext = createContext(null)

const SESSION_KEY = 'smartagri_user'
const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  const role = user?.role || 'Farmer'

  // Helper to obtain real backend JWT token
  const obtainBackendToken = async (email, password) => {
    try {
      const res = await axiosClient.post('/api/v1/auth/login', {
        email: email,
        password: password,
      })

      if (res.data?.success && res.data?.data) {
        const { access_token, refresh_token, user: apiUser } = res.data.data
        localStorage.setItem(ACCESS_TOKEN_KEY, access_token)
        if (refresh_token) localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token)
        return { access_token, apiUser }
      }
    } catch (err) {
      console.warn('Backend login attempt failed:', err)
      throw err
    }
    return null
  }

  useEffect(() => {
    const initializeAuth = async () => {
      const savedUser = localStorage.getItem(SESSION_KEY)
      const token = localStorage.getItem(ACCESS_TOKEN_KEY)

      if (savedUser && token) {
        try {
          const parsed = JSON.parse(savedUser)
          if (!parsed.role) parsed.role = 'Farmer'
          if (parsed.district) parsed.location = parsed.district
          setUser(parsed)
          setIsAuthenticated(true)
        } catch (e) {
          setIsAuthenticated(false)
        }
      } else {
        setIsAuthenticated(false)
      }
      setLoading(false)
    }

    initializeAuth()
  }, [])

  const login = async (email, password) => {
    const tokenRes = await obtainBackendToken(email, password)
    if (tokenRes) {
      const { apiUser } = tokenRes
      const userRole = (apiUser.role || 'Farmer').toLowerCase() === 'buyer' ? 'Buyer' : (apiUser.role || 'Farmer').toLowerCase() === 'admin' ? 'Admin' : 'Farmer'
      const userData = {
        id: apiUser.id,
        email: apiUser.email,
        name: apiUser.full_name || email.split('@')[0],
        phone: apiUser.mobile_number || '',
        location: apiUser.district || 'Pune',
        district: apiUser.district || 'Pune',
        role: userRole,
      }
      setUser(userData)
      setIsAuthenticated(true)
      localStorage.setItem(SESSION_KEY, JSON.stringify(userData))
      return userData
    }

    throw new Error('Invalid email or password')
  }

  const registerFarmer = async (data) => {
    const userDistrict = data.district || 'Pune'
    const response = await axiosClient.post('/api/v1/auth/register', {
      full_name: data.fullName,
      email: data.email,
      mobile_number: data.mobileNumber,
      password: data.password,
      state: data.state || 'Maharashtra',
      district: userDistrict,
      village: data.village || userDistrict,
      role: 'Farmer',
    })

    const resData = response.data
    if (resData.success) {
      const loggedIn = await login(data.email, data.password)
      const updatedUser = { ...loggedIn, location: userDistrict, district: userDistrict }
      setUser(updatedUser)
      localStorage.setItem(SESSION_KEY, JSON.stringify(updatedUser))
      return updatedUser
    }
  }

  const registerBuyer = async (data) => {
    const userDistrict = data.district || 'Pune'
    const response = await axiosClient.post('/api/v1/buyer/register', {
      full_name: data.companyName,
      email: data.email,
      mobile_number: data.mobileNumber,
      password: data.password,
      company_name: data.companyName,
      owner_name: data.ownerName,
      gst_number: data.gstNumber,
      business_license: data.businessLicense,
      district: userDistrict,
      state: data.state || 'Maharashtra',
      buying_crops: data.preferredCrops,
      daily_capacity: parseFloat(data.dailyCapacity) || 100.0,
    })

    const resData = response.data
    if (resData.success) {
      const loggedIn = await login(data.email, data.password)
      const updatedUser = { ...loggedIn, location: userDistrict, district: userDistrict }
      setUser(updatedUser)
      localStorage.setItem(SESSION_KEY, JSON.stringify(updatedUser))
      return updatedUser
    }
  }

  const logout = () => {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem(SESSION_KEY)
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  }

  const updateUser = (updatedFields) => {
    setUser((prev) => {
      const next = { ...prev, ...updatedFields }
      if (updatedFields.location) next.district = updatedFields.location
      if (updatedFields.district) next.location = updatedFields.district
      localStorage.setItem(SESSION_KEY, JSON.stringify(next))
      return next
    })
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        role,
        isAuthenticated,
        loading,
        login,
        registerFarmer,
        registerBuyer,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
