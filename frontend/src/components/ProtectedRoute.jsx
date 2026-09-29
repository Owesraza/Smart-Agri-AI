import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Loader from './Loader'

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, role, isAuthenticated, loading } = useAuth()

  if (loading) return <Loader fullPage text="Verifying permissions..." />

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Role validation
  if (allowedRoles && !allowedRoles.includes(role)) {
    // Redirect unauthorized user to their role portal
    if (role === 'Buyer') return <Navigate to="/buyer" replace />
    if (role === 'Admin') return <Navigate to="/admin" replace />
    return <Navigate to="/dashboard" replace />
  }

  return children
}

export default ProtectedRoute
