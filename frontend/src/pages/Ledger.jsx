import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import Card, { CardHeader } from '../components/Card'
import SearchBar from '../components/SearchBar'
import Modal from '../components/Modal'
import Button from '../components/Button'
import Input from '../components/Input'
import { formatCurrency } from '../utils/formatters'
import useDebounce from '../hooks/useDebounce'
import { useLanguage } from '../context/LanguageContext'

const emptyForm = {
  type: 'Expense',
  category: 'Fertilizer',
  amount: '',
  description: '',
  date: new Date().toISOString().split('T')[0],
  crop: 'Wheat',
  transport_cost: 0,
  packaging_cost: 0
}

const CATEGORY_OPTIONS = [
  'Crop Sale (Marketplace)',
  'Fertilizer',
  'Labour',
  'Seeds',
  'Irrigation',
  'Pesticide',
  'Machinery / Tractor',
  'Transport',
  'Packaging',
  'Government Subsidy',
  'Other Expense',
  'Other Income'
]

const Ledger = () => {
  const { t } = useLanguage()
  const [entries, setEntries] = useState([])
  const [summary, setSummary] = useState({ total_income: 0, total_expenses: 0, net_profit: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('All')
  const [categoryFilter, setCategoryFilter] = useState('All')
  
  // Modals
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)
  const [deleteId, setDeleteId] = useState(null)
  const [toastMessage, setToastMessage] = useState(null)

  const debouncedSearch = useDebounce(search)
  const typeFilters = ['All', 'Income', 'Expense']

  const translateCategory = (cat) => {
    const map = {
      'Crop Sale (Marketplace)': t('ledger.categories.cropSale', 'Crop Sale (Marketplace)'),
      'Fertilizer': t('ledger.categories.fertilizer', 'Fertilizer'),
      'Labour': t('ledger.categories.labour', 'Labour'),
      'Seeds': t('ledger.categories.seeds', 'Seeds'),
      'Irrigation': t('ledger.categories.irrigation', 'Irrigation'),
      'Pesticide': t('ledger.categories.pesticide', 'Pesticide'),
      'Machinery / Tractor': t('ledger.categories.machinery', 'Machinery / Tractor'),
      'Transport': t('ledger.categories.transport', 'Transport'),
      'Packaging': t('ledger.categories.packaging', 'Packaging'),
      'Government Subsidy': t('ledger.categories.subsidy', 'Government Subsidy'),
      'Other Expense': t('ledger.categories.otherExpense', 'Other Expense'),
      'Other Income': t('ledger.categories.otherIncome', 'Other Income'),
      'All': t('ledger.categories.all', 'All Categories')
    }
    return map[cat] || cat
  }

  const typeFilterLabels = {
    'All': t('ledger.allTransactions', 'All Transactions'),
    'Income': t('ledger.income', 'Income'),
    'Expense': t('ledger.expense', 'Expense')
  }

  const showToast = (text, type = 'success') => {
    setToastMessage({ text, type })
    setTimeout(() => setToastMessage(null), 3000)
  }

  // Load Real SQL Database Ledger Entries & Summary Stats
  const fetchLedgerData = async (isBackground = false) => {
    if (!isBackground) setLoading(true)
    try {
      // 1. Fetch Real Summary (Total Income, Total Expenses, Net Profit)
      const resSum = await axiosClient.get('/api/v1/ledger/summary')
      if (resSum.data && resSum.data.success && resSum.data.data) {
        setSummary({
          total_income: resSum.data.data.total_income || 0,
          total_expenses: resSum.data.data.total_expenses || resSum.data.data.total_expense || 0,
          net_profit: resSum.data.data.net_profit || 0
        })
      }

      // 2. Fetch Real Ledger Entries
      const resEntries = await axiosClient.get('/api/v1/ledger')
      if (resEntries.data && resEntries.data.success && Array.isArray(resEntries.data.data)) {
        setEntries(resEntries.data.data)
      }
    } catch (err) {
      console.warn('Error fetching ledger data from SQL database:', err)
    } finally {
      if (!isBackground) setLoading(false)
    }
  }

  useEffect(() => {
    fetchLedgerData(false)
    // 10s Background Auto-Refresh (Syncs marketplace sales automatically)
    const interval = setInterval(() => fetchLedgerData(true), 10000)
    return () => clearInterval(interval)
  }, [])

  // Filtered List
  const filtered = entries.filter((tr) => {
    const desc = tr.description || ''
    const cat = tr.category || ''
    const matchSearch =
      desc.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
      cat.toLowerCase().includes(debouncedSearch.toLowerCase())
    const matchType = typeFilter === 'All' || tr.type === typeFilter
    const matchCat = categoryFilter === 'All' || cat.includes(categoryFilter)
    return matchSearch && matchType && matchCat
  })

  // Create New Real Ledger Entry in SQL DB
  const handleCreateEntry = async (e) => {
    e.preventDefault()
    const parsedAmt = parseFloat(form.amount)
    if (!parsedAmt || parsedAmt <= 0 || !form.description) {
      showToast('Please enter a valid positive amount and description.', 'error')
      return
    }

    setSubmitting(true)
    try {
      const payload = {
        type: form.type || 'Expense',
        category: form.category || 'Fertilizer',
        amount: parsedAmt,
        description: form.description.trim(),
        date: form.date || new Date().toISOString().split('T')[0],
        crop: form.crop || 'Wheat',
        transport_cost: parseFloat(form.transport_cost) || 0,
        packaging_cost: parseFloat(form.packaging_cost) || 0,
      }

      const res = await axiosClient.post('/api/v1/ledger', payload)
      if (res.data && (res.data.success || res.status === 201 || res.status === 200)) {
        showToast('✅ Transaction added to Farm Ledger database!')
        setIsModalOpen(false)
        setForm(emptyForm)
        fetchLedgerData()
      } else {
        showToast(res.data?.message || 'Failed to add transaction to database', 'error')
      }
    } catch (err) {
      console.error('Error adding ledger entry:', err)
      const errMsg = err.response?.data?.message || err.response?.data?.detail || 'Failed to add transaction to database'
      showToast(`❌ ${typeof errMsg === 'string' ? errMsg : 'Validation error adding transaction'}`, 'error')
    } finally {
      setSubmitting(false)
    }
  }



  // Delete Real Entry from SQL DB
  const handleDeleteEntry = async () => {
    if (!deleteId) return
    try {
      await axiosClient.delete(`/api/v1/ledger/${deleteId}`)
      showToast('🗑️ Transaction entry deleted!')
      setDeleteId(null)
      fetchLedgerData()
    } catch (err) {
      console.error('Error deleting entry:', err)
      showToast('Failed to delete entry', 'error')
    }
  }

  return (
    <div className="space-y-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-xl shadow-xl text-xs font-bold transition-all ${
          toastMessage.type === 'error' ? 'bg-red-600 text-white' : 'bg-emerald-700 text-white'
        }`}>
          {toastMessage.text}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap bg-white p-6 rounded-2xl border border-gray-100 shadow-xs">
        <div>
          <h1 className="text-2xl font-extrabold text-gray-900">{t('ledger.title', 'Farm Ledger & Financial Accounting')}</h1>
          <p className="text-gray-500 text-xs mt-1">{t('ledger.subtitle', 'Real SQL database financial ledger. Tracks income, crop sales, input expenses, and net profit auto-synced with Marketplace transactions.')}</p>
        </div>

        <button
          onClick={() => { setForm(emptyForm); setIsModalOpen(true) }}
          className="bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all cursor-pointer shadow-sm flex items-center gap-1.5"
        >
          <span>➕</span> {t('ledger.addTransaction', 'Add Transaction')}
        </button>
      </div>

      {/* Real Summary Cards (Total Income, Total Expense, Net Profit) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-emerald-600 to-green-700 rounded-2xl p-5 text-white shadow-sm">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">💚</span>
            <p className="text-white/80 text-xs font-bold">{t('ledger.totalIncome', 'Total Income')}</p>
          </div>
          <p className="text-3xl font-extrabold">{formatCurrency(summary.total_income)}</p>
        </div>

        <div className="bg-gradient-to-br from-rose-600 to-red-700 rounded-2xl p-5 text-white shadow-sm">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">❤️</span>
            <p className="text-white/80 text-xs font-bold">{t('ledger.totalExpense', 'Total Expense')}</p>
          </div>
          <p className="text-3xl font-extrabold">{formatCurrency(summary.total_expenses)}</p>
        </div>

        <div className={`rounded-2xl p-5 text-white shadow-sm ${
          summary.net_profit >= 0 ? 'bg-gradient-to-br from-teal-700 to-emerald-800' : 'bg-gradient-to-br from-amber-600 to-orange-700'
        }`}>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">💰</span>
            <p className="text-white/80 text-xs font-bold">{t('ledger.netProfit', 'Net Profit')}</p>
          </div>
          <p className="text-3xl font-extrabold">{formatCurrency(summary.net_profit)}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <SearchBar
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={t('ledger.searchTransaction', 'Search transactions or categories...')}
          className="flex-1"
        />
        <div className="flex gap-2">
          {typeFilters.map((f) => (
            <button
              key={f}
              onClick={() => setTypeFilter(f)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold cursor-pointer transition-all ${
                typeFilter === f ? 'bg-emerald-700 text-white shadow-xs' : 'bg-white text-gray-600 border border-gray-200 hover:border-emerald-700'
              }`}
            >
              {typeFilterLabels[f] || f}
            </button>
          ))}
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex gap-2 overflow-x-auto pb-1">
        {['All', ...CATEGORY_OPTIONS].map((c) => (
          <button
            key={c}
            onClick={() => setCategoryFilter(c === 'All' ? 'All' : c)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap cursor-pointer transition-all ${
              categoryFilter === c ? 'bg-emerald-800 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:border-emerald-700'
            }`}
          >
            {translateCategory(c)}
          </button>
        ))}
      </div>

      {/* Transactions Table */}
      <Card>
        <CardHeader
          title={t('ledger.recentTransactions', 'Recent Transactions')}
          icon="📋"
          subtitle={`${filtered.length} ${t('ledger.entriesStored', 'Entries stored in SQL Database')}`}
        />

        <div className="overflow-x-auto pt-2">
          {loading ? (
            <div className="py-12 text-center text-xs text-gray-400 animate-pulse">{t('ledger.loadingLedger', 'Loading financial ledger from SQL database...')}</div>
          ) : filtered.length === 0 ? (
            <div className="py-10 px-6 text-center text-xs text-gray-500 bg-gray-50/80 rounded-2xl border border-dashed border-gray-300 my-4">
              <p className="font-semibold text-gray-700">{t('ledger.noRecords', 'No financial records found for your account yet.')}</p>
            </div>
          ) : (
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50/70 text-gray-500 font-bold uppercase tracking-wider">
                  <th className="py-3 px-4">{t('ledger.dateCol', 'Date')}</th>
                  <th className="py-3 px-4">{t('ledger.typeCol', 'Type')}</th>
                  <th className="py-3 px-4">{t('ledger.categoryCol', 'Category')}</th>
                  <th className="py-3 px-4">{t('ledger.descriptionCol', 'Description')}</th>
                  <th className="py-3 px-4">{t('ledger.cropCol', 'Crop Tag')}</th>
                  <th className="py-3 px-4 text-right">{t('ledger.amountCol', 'Amount (₹)')}</th>
                  <th className="py-3 px-4 text-center">{t('ledger.actionCol', 'Action')}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filtered.map((tr) => (
                  <tr key={tr.id} className="hover:bg-gray-50/80 transition-all">
                    <td className="py-3 px-4 font-medium text-gray-700 whitespace-nowrap">
                      📅 {tr.date ? tr.date.split('T')[0] : '2026-08-01'}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-extrabold ${
                        tr.type === 'Income' ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-rose-100 text-rose-800 border border-rose-200'
                      }`}>
                        {tr.type === 'Income' ? `🟢 ${t('ledger.income', 'INCOME')}` : `🔴 ${t('ledger.expense', 'EXPENSE')}`}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-bold text-gray-900">{translateCategory(tr.category)}</td>
                    <td className="py-3 px-4 text-gray-600 max-w-xs truncate">{tr.description}</td>
                    <td className="py-3 px-4 text-gray-500">🌾 {tr.crop || 'Wheat'}</td>
                    <td className={`py-3 px-4 text-right font-extrabold text-sm ${
                      tr.type === 'Income' ? 'text-emerald-700' : 'text-rose-600'
                    }`}>
                      {tr.type === 'Income' ? '+' : '-'}{formatCurrency(tr.amount)}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => setDeleteId(tr.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors p-1 cursor-pointer"
                        title={t('actions.delete', 'Delete Record')}
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </Card>

      {/* ADD TRANSACTION MODAL */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={`➕ ${t('ledger.logTransaction', 'Log Financial Transaction')}`}>
        <form onSubmit={handleCreateEntry} className="space-y-3 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-semibold text-gray-700 block mb-1">{t('ledger.type', 'Type')} *</label>
              <select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500 font-bold"
              >
                <option value="Expense">🔴 {t('ledger.expenseCost', 'Expense (Cost)')}</option>
                <option value="Income">🟢 {t('ledger.incomeRevenue', 'Income (Revenue)')}</option>
              </select>
            </div>
            <div>
              <label className="font-semibold text-gray-700 block mb-1">{t('ledger.categoryCol', 'Category')} *</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {CATEGORY_OPTIONS.map((cat) => (
                  <option key={cat} value={cat}>{translateCategory(cat)}</option>
                ))}
              </select>
            </div>
          </div>

          <Input
            label={`${t('ledger.amountCol', 'Amount (₹)')} *`}
            type="number"
            step="0.01"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
            placeholder="e.g. 4500"
            required
          />

          <Input
            label={`${t('ledger.descriptionCol', 'Description')} *`}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="e.g. Purchased 2 Bags NPK Fertilizer from Agri Shop"
            required
          />

          <div className="grid grid-cols-2 gap-3">
            <Input
              label={`${t('ledger.dateCol', 'Date')} *`}
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
            <div>
              <label className="font-semibold text-gray-700 block mb-1">{t('ledger.cropFocus', 'Crop Focus')} *</label>
              <select
                value={form.crop}
                onChange={(e) => setForm({ ...form, crop: e.target.value })}
                className="w-full px-3.5 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500 bg-white font-medium"
              >
                <option value="Onion">🧅 Onion</option>
                <option value="Wheat">🌾 Wheat</option>
                <option value="Tomato">🍅 Tomato</option>
                <option value="Grapes">🍇 Grapes</option>
                <option value="Cotton">☁️ Cotton</option>
                <option value="Maize">🌽 Maize</option>
                <option value="Soybean">🫘 Soybean</option>
                <option value="Potato">🥔 Potato</option>
                <option value="Garlic">🧄 Garlic</option>
                <option value="Pomegranate">🍎 Pomegranate</option>
                <option value="Rice">🌾 Rice</option>
                <option value="Bajra">🌾 Bajra</option>
                <option value="Sugarcane">🎋 Sugarcane</option>
                <option value="Turmeric">🟡 Turmeric</option>
                <option value="Chilli">🌶️ Chilli</option>
                <option value="Mango">🥭 Mango</option>
              </select>
            </div>
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>{t('ledger.cancel', 'Cancel')}</Button>
            <Button type="submit" disabled={submitting}>{submitting ? t('ledger.saving', 'Saving...') : t('ledger.saveTransaction', 'Save Transaction →')}</Button>
          </div>
        </form>
      </Modal>

      {/* DELETE CONFIRMATION MODAL */}
      <Modal isOpen={!!deleteId} onClose={() => setDeleteId(null)} title={`🗑️ ${t('ledger.deleteConfirmTitle', 'Delete Financial Entry')}`}>
        <p className="text-xs text-gray-600 mb-4">{t('ledger.deleteConfirmMsg', 'Are you sure you want to delete this financial record from your SQL database? This will update your net profit total.')}</p>
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={() => setDeleteId(null)}>{t('ledger.cancel', 'Cancel')}</Button>
          <button onClick={handleDeleteEntry} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl cursor-pointer">{t('ledger.deleteEntry', 'Delete Entry')}</button>
        </div>
      </Modal>
    </div>
  )
}

export default Ledger
