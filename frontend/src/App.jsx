import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { LanguageProvider } from './context/LanguageContext'

// Layouts
import PublicLayout from './layouts/PublicLayout'
import DashboardLayout from './layouts/DashboardLayout'
import ProtectedRoute from './components/ProtectedRoute'

// Public & Authentication Pages
import Home from './pages/Home'
import About from './pages/About'
import Login from './pages/Login'
import RegisterChoice from './pages/RegisterChoice'
import FarmerRegister from './pages/FarmerRegister'
import BuyerRegister from './pages/BuyerRegister'
import ForgotPassword from './pages/ForgotPassword'

// Portal & Shared Pages
import Dashboard from './pages/Dashboard'
import BuyerDashboard from './pages/BuyerDashboard'
import AdminDashboard from './pages/AdminDashboard'
import Marketplace from './pages/Marketplace'
import MyCropListings from './pages/MyCropListings'
import MyBuyingRequirements from './pages/MyBuyingRequirements'
import PlotManagement from './pages/PlotManagement'
import MarketIntelligence from './pages/MarketIntelligence'
import AIAssistant from './pages/AIAssistant'
import Workflow from './pages/Workflow'
import Ledger from './pages/Ledger'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'

// Helper component for automatic root redirect based on permanent user role
const RootRedirect = () => {
  const { role, isAuthenticated } = useAuth()
  if (!isAuthenticated) return <PublicLayout><Home /></PublicLayout>
  if (role === 'Buyer') return <Navigate to="/buyer" replace />
  if (role === 'Admin') return <Navigate to="/admin" replace />
  return <Navigate to="/dashboard" replace />
}

const App = () => {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <Routes>
            {/* Public & Authentication Routes */}
            <Route path="/" element={<RootRedirect />} />
            <Route path="/public" element={<PublicLayout><Home /></PublicLayout>} />
            <Route path="/about" element={<PublicLayout><About /></PublicLayout>} />
            <Route path="/login" element={<PublicLayout><Login /></PublicLayout>} />
            <Route path="/register" element={<PublicLayout><RegisterChoice /></PublicLayout>} />
            <Route path="/register/farmer" element={<PublicLayout><FarmerRegister /></PublicLayout>} />
            <Route path="/register/buyer" element={<PublicLayout><BuyerRegister /></PublicLayout>} />
            <Route path="/forgot-password" element={<PublicLayout><ForgotPassword /></PublicLayout>} />

            {/* Shared Discovery Marketplace Route */}
            <Route
              path="/marketplace"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Marketplace /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Profile /></DashboardLayout>
                </ProtectedRoute>
              }
            />

            {/* Shared & Farmer Portal Routes */}
            <Route
              path="/farmer/dashboard"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Admin']}>
                  <DashboardLayout><Dashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Dashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/my-listings"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Admin']}>
                  <DashboardLayout><MyCropListings /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/plots"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Admin']}>
                  <DashboardLayout><PlotManagement /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/market"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><MarketIntelligence /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/ai-assistant"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Admin']}>
                  <DashboardLayout><AIAssistant /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/workflow"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Workflow /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/ledger"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Ledger /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/analytics"
              element={
                <ProtectedRoute allowedRoles={['Farmer', 'Buyer', 'Admin']}>
                  <DashboardLayout><Analytics /></DashboardLayout>
                </ProtectedRoute>
              }
            />

            {/* Buyer Portal Routes */}
            <Route
              path="/buyer/dashboard"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><BuyerDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/buyer"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><BuyerDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/buying-requirements"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><MyBuyingRequirements /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/recommended-farmers"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><Marketplace /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/my-deals"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><BuyerDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/purchase-analytics"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><Analytics /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/messages"
              element={
                <ProtectedRoute allowedRoles={['Buyer']}>
                  <DashboardLayout><Marketplace /></DashboardLayout>
                </ProtectedRoute>
              }
            />

            {/* Admin Console Routes */}
            <Route
              path="/admin/dashboard"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/farmers"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/buyers"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/transactions"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/market-data"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><MarketIntelligence /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/analytics"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><Analytics /></DashboardLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/settings"
              element={
                <ProtectedRoute allowedRoles={['Admin']}>
                  <DashboardLayout><AdminDashboard /></DashboardLayout>
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  )
}

export default App
