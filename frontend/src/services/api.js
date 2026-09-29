import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor – attach JWT token
api.interceptors.request.use(
  (config) => {
    const user = localStorage.getItem('smartagri_user')
    if (user) {
      const token = JSON.parse(user).token
      if (token) config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// Response interceptor – handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('smartagri_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

// Service functions (to be connected to FastAPI backend)
export const marketService = {
  getPrices: (crop) => api.get(`/market/prices?crop=${crop}`),
  getMandis: () => api.get('/market/mandis'),
}

export const plotService = {
  getAll: () => api.get('/plots'),
  create: (data) => api.post('/plots', data),
  update: (id, data) => api.put(`/plots/${id}`, data),
  delete: (id) => api.delete(`/plots/${id}`),
}

export const ledgerService = {
  getAll: () => api.get('/ledger'),
  create: (data) => api.post('/ledger', data),
}

export const aiService = {
  chat: (message) => api.post('/ai/chat', { message }),
}

export default api
