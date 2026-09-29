// Currency formatter – Indian Rupee
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount)
}

// Number formatter with Indian locale
export const formatNumber = (num) => {
  return new Intl.NumberFormat('en-IN').format(num)
}

// Date formatter
export const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

// Short date
export const formatShortDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })
}

// Percentage change formatter
export const formatChange = (val) => {
  const sign = val > 0 ? '+' : ''
  return `${sign}${val}`
}

// Capitalize first letter
export const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// Status color helper
export const getStatusColor = (status) => {
  const map = {
    Growing: 'text-green-700 bg-green-100',
    Harvesting: 'text-orange-700 bg-orange-100',
    Harvested: 'text-blue-700 bg-blue-100',
    Fallow: 'text-gray-700 bg-gray-100',
    Pending: 'text-yellow-700 bg-yellow-100',
    'In Progress': 'text-blue-700 bg-blue-100',
    Completed: 'text-green-700 bg-green-100',
    Upcoming: 'text-purple-700 bg-purple-100',
    High: 'text-red-700 bg-red-100',
    Medium: 'text-yellow-700 bg-yellow-100',
    Low: 'text-green-700 bg-green-100',
    Income: 'text-green-700 bg-green-100',
    Expense: 'text-red-700 bg-red-100',
  }
  return map[status] || 'text-gray-700 bg-gray-100'
}

// Truncate long text
export const truncate = (str, maxLen = 40) => {
  if (!str) return ''
  return str.length > maxLen ? str.slice(0, maxLen) + '...' : str
}
