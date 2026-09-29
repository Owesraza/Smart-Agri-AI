// Mock data for the SmartAgri AI application
// Used throughout the frontend for demo purposes

export const mockWeather = {
  city: 'Nashik, Maharashtra',
  temperature: 28,
  condition: 'Partly Cloudy',
  humidity: 65,
  wind: 12,
  icon: '⛅',
  forecast: [
    { day: 'Mon', temp: 28, icon: '⛅' },
    { day: 'Tue', temp: 31, icon: '☀️' },
    { day: 'Wed', temp: 26, icon: '🌧️' },
    { day: 'Thu', temp: 29, icon: '⛅' },
    { day: 'Fri', temp: 30, icon: '☀️' },
  ],
}

export const mockMarketPrices = [
  { id: 1, crop: 'Wheat', mandi: 'Nashik APMC', price: 2150, unit: 'quintal', change: +80, trend: 'up' },
  { id: 2, crop: 'Tomato', mandi: 'Pune APMC', price: 1800, unit: 'quintal', change: -120, trend: 'down' },
  { id: 3, crop: 'Onion', mandi: 'Lasalgaon APMC', price: 2400, unit: 'quintal', change: +200, trend: 'up' },
  { id: 4, crop: 'Cotton', mandi: 'Aurangabad APMC', price: 6800, unit: 'quintal', change: +150, trend: 'up' },
  { id: 5, crop: 'Soybean', mandi: 'Latur APMC', price: 4200, unit: 'quintal', change: -50, trend: 'down' },
  { id: 6, crop: 'Sugarcane', mandi: 'Kolhapur APMC', price: 3100, unit: 'quintal', change: +100, trend: 'up' },
  { id: 7, crop: 'Rice (Basmati)', mandi: 'Nagpur APMC', price: 5200, unit: 'quintal', change: +300, trend: 'up' },
  { id: 8, crop: 'Maize', mandi: 'Solapur APMC', price: 1950, unit: 'quintal', change: -30, trend: 'down' },
]

export const mockPlots = [
  { id: 1, name: 'North Field', area: 2.5, unit: 'acres', crop: 'Wheat', status: 'Growing', sowingDate: '2025-11-15', harvestDate: '2026-03-20', health: 'Good', soilType: 'Loamy', irrigationType: 'Drip' },
  { id: 2, name: 'South Field', area: 1.8, unit: 'acres', crop: 'Onion', status: 'Harvesting', sowingDate: '2025-09-10', harvestDate: '2026-01-10', health: 'Excellent', soilType: 'Sandy Loam', irrigationType: 'Sprinkler' },
  { id: 3, name: 'East Patch', area: 0.75, unit: 'acres', crop: 'Tomato', status: 'Fallow', sowingDate: '', harvestDate: '', health: 'N/A', soilType: 'Clay Loam', irrigationType: 'Flood' },
  { id: 4, name: 'West Block', area: 3.2, unit: 'acres', crop: 'Cotton', status: 'Growing', sowingDate: '2025-06-01', harvestDate: '2026-02-15', health: 'Good', soilType: 'Black Cotton', irrigationType: 'Drip' },
  { id: 5, name: 'Central Plot', area: 1.0, unit: 'acres', crop: 'Soybean', status: 'Harvested', sowingDate: '2025-07-05', harvestDate: '2025-10-20', health: 'Good', soilType: 'Loamy', irrigationType: 'Rainfed' },
]

export const mockTasks = [
  { id: 1, title: 'Irrigate North Field', dueDate: 'Today', priority: 'High', status: 'Pending', crop: 'Wheat', plot: 'North Field' },
  { id: 2, title: 'Apply fertilizer – South Field', dueDate: 'Tomorrow', priority: 'Medium', status: 'Pending', crop: 'Onion', plot: 'South Field' },
  { id: 3, title: 'Soil testing – East Patch', dueDate: '2026-01-15', priority: 'Low', status: 'Completed', crop: '-', plot: 'East Patch' },
  { id: 4, title: 'Harvest Onion – South Field', dueDate: '2026-01-10', priority: 'High', status: 'In Progress', crop: 'Onion', plot: 'South Field' },
  { id: 5, title: 'Pesticide spray – West Block', dueDate: '2026-01-18', priority: 'Medium', status: 'Pending', crop: 'Cotton', plot: 'West Block' },
  { id: 6, title: 'Market visit – Lasalgaon APMC', dueDate: '2026-01-12', priority: 'High', status: 'Pending', crop: 'Onion', plot: '-' },
]

export const mockLedger = [
  { id: 1, date: '2026-01-05', type: 'Income', category: 'Crop Sale', description: 'Wheat sale – Nashik APMC', amount: 53750, crop: 'Wheat', plot: 'North Field' },
  { id: 2, date: '2026-01-03', type: 'Expense', category: 'Fertilizer', description: 'DAP Fertilizer purchase', amount: 4200, crop: 'Onion', plot: 'South Field' },
  { id: 3, date: '2025-12-28', type: 'Expense', category: 'Labour', description: 'Harvesting labour charges', amount: 3500, crop: 'Soybean', plot: 'Central Plot' },
  { id: 4, date: '2025-12-20', type: 'Income', category: 'Crop Sale', description: 'Soybean sale – Latur APMC', amount: 42000, crop: 'Soybean', plot: 'Central Plot' },
  { id: 5, date: '2025-12-15', type: 'Expense', category: 'Seeds', description: 'Wheat seed purchase', amount: 5600, crop: 'Wheat', plot: 'North Field' },
  { id: 6, date: '2025-12-10', type: 'Expense', category: 'Irrigation', description: 'Drip irrigation maintenance', amount: 2800, crop: '-', plot: 'North Field' },
  { id: 7, date: '2025-12-05', type: 'Income', category: 'Subsidy', description: 'PM-KISAN installment', amount: 6000, crop: '-', plot: '-' },
  { id: 8, date: '2025-11-28', type: 'Expense', category: 'Pesticide', description: 'Fungicide spray', amount: 1900, crop: 'Cotton', plot: 'West Block' },
]

export const mockProfitSummary = {
  totalIncome: 101750,
  totalExpenses: 18000,
  netProfit: 83750,
  profitMargin: 82.3,
  monthlyChange: +12.5,
}

export const mockAnalytics = {
  monthlyProfit: [
    { month: 'Aug', income: 45000, expenses: 12000, profit: 33000 },
    { month: 'Sep', income: 62000, expenses: 18000, profit: 44000 },
    { month: 'Oct', income: 38000, expenses: 9500, profit: 28500 },
    { month: 'Nov', income: 55000, expenses: 14000, profit: 41000 },
    { month: 'Dec', income: 78000, expenses: 19000, profit: 59000 },
    { month: 'Jan', income: 101750, expenses: 18000, profit: 83750 },
  ],
  cropPerformance: [
    { crop: 'Wheat', profit: 48150, area: 2.5 },
    { crop: 'Onion', profit: 22000, area: 1.8 },
    { crop: 'Soybean', profit: 38500, area: 1.0 },
    { crop: 'Cotton', profit: 15000, area: 3.2 },
    { crop: 'Tomato', profit: -3200, area: 0.75 },
  ],
  cropShare: [
    { name: 'Wheat', value: 35 },
    { name: 'Onion', value: 25 },
    { name: 'Soybean', value: 20 },
    { name: 'Cotton', value: 15 },
    { name: 'Tomato', value: 5 },
  ],
  priceTrend: [
    { week: 'W1', wheat: 2050, onion: 2200, tomato: 1900 },
    { week: 'W2', wheat: 2100, onion: 2350, tomato: 1750 },
    { week: 'W3', wheat: 2080, onion: 2100, tomato: 1820 },
    { week: 'W4', wheat: 2150, onion: 2400, tomato: 1800 },
  ],
}

export const mockMandis = [
  { id: 1, name: 'Nashik APMC', distance: '12 km', crops: ['Wheat', 'Onion', 'Tomato'], rating: 4.5, timings: '6 AM – 2 PM' },
  { id: 2, name: 'Lasalgaon APMC', distance: '28 km', crops: ['Onion', 'Garlic'], rating: 4.8, timings: '5 AM – 1 PM' },
  { id: 3, name: 'Pune APMC', distance: '210 km', crops: ['Tomato', 'Potato', 'Onion'], rating: 4.2, timings: '7 AM – 3 PM' },
  { id: 4, name: 'Aurangabad APMC', distance: '180 km', crops: ['Cotton', 'Soybean'], rating: 4.0, timings: '6 AM – 2 PM' },
]

export const mockAIMessages = [
  {
    id: 1,
    role: 'assistant',
    text: '🌾 Namaste! I am your SmartAgri AI Assistant. I can help you with crop prices, best selling times, market recommendations, and profit calculations. How can I assist you today?',
    time: '10:00 AM',
  },
]

export const mockSuggestedQuestions = [
  'What is the best price for Onion today?',
  'When should I sell my Wheat crop?',
  'Which mandi gives the best price for Tomato?',
  'Calculate my profit for North Field this season',
  'What crops should I plant next season?',
  'How is the weather affecting crop prices?',
]

export const mockWorkflowSteps = [
  {
    id: 1, title: 'Soil Preparation', status: 'Completed', date: '2025-11-01',
    description: 'Deep ploughing and soil testing done. pH: 6.8, Nitrogen: Adequate.',
    tasks: ['Deep ploughing', 'Soil testing', 'Add organic compost'],
  },
  {
    id: 2, title: 'Seed Sowing', status: 'Completed', date: '2025-11-15',
    description: 'HD-2967 Wheat variety sown at 100 kg/hectare seed rate.',
    tasks: ['Seed selection', 'Seed treatment', 'Sowing'],
  },
  {
    id: 3, title: 'Irrigation & Fertilization', status: 'In Progress', date: '2025-12-20',
    description: 'Crown root initiation irrigation done. Urea top dressing pending.',
    tasks: ['First irrigation', 'DAP application', 'Urea top dressing (Pending)'],
  },
  {
    id: 4, title: 'Pest Management', status: 'Upcoming', date: '2026-01-20',
    description: 'Monitor for aphids and rust disease. Spray schedule prepared.',
    tasks: ['Pest scouting', 'Fungicide spray', 'Insecticide spray if needed'],
  },
  {
    id: 5, title: 'Harvesting', status: 'Upcoming', date: '2026-03-20',
    description: 'Harvest when grain moisture drops to 12-14%.',
    tasks: ['Arrange harvester', 'Market price check', 'Transport arrangement'],
  },
  {
    id: 6, title: 'Market Selling', status: 'Upcoming', date: '2026-03-25',
    description: 'Sell at best available APMC or private buyer.',
    tasks: ['Grading & sorting', 'Transport to mandi', 'Negotiate price', 'Record transaction'],
  },
]

export const mockUser = {
  name: 'Ramesh Patil',
  email: 'ramesh.patil@smartagri.in',
  phone: '+91 98765 43210',
  location: 'Nashik, Maharashtra',
  farmName: 'Patil Agro Farm',
  totalArea: '9.25 acres',
  soilType: 'Loamy & Black Cotton',
  memberSince: 'January 2024',
  avatar: null,
}

export const mockRecentActivity = [
  { id: 1, action: 'Market price checked', item: 'Onion – Lasalgaon APMC', time: '2 hours ago', icon: '📊' },
  { id: 2, action: 'Task completed', item: 'Soil testing – East Patch', time: '1 day ago', icon: '✅' },
  { id: 3, action: 'Plot updated', item: 'West Block – Cotton growing', time: '2 days ago', icon: '🌱' },
  { id: 4, action: 'Transaction added', item: 'Income – Soybean sale ₹42,000', time: '3 days ago', icon: '💰' },
  { id: 5, action: 'AI consulted', item: 'Best time to sell wheat', time: '4 days ago', icon: '🤖' },
]
