import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import Card, { CardHeader } from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import SearchBar from '../components/SearchBar'
import Modal from '../components/Modal'
import { getStatusColor } from '../utils/formatters'
import useDebounce from '../hooks/useDebounce'
import { useLanguage } from '../context/LanguageContext'

const emptyForm = {
  plot_name: '',
  area: '',
  crop_name: 'Wheat',
  status: 'Growing',
  sowing_date: new Date().toISOString().split('T')[0],
  expected_harvest: '',
  soil_type: 'Black Cotton',
}

const LIFECYCLE_STAGES = [
  { name: 'Sowing', label: '🌱 Sowing', pct: 25 },
  { name: 'Growing', label: '🌿 Growing', pct: 65 },
  { name: 'Harvesting', label: '🌾 Harvesting', pct: 90 },
  { name: 'Completed', label: '📦 Completed', pct: 100 },
]

const PlotManagement = () => {
  const { t, translateCrop, translateStatus } = useLanguage()
  const [plots, setPlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [editId, setEditId] = useState(null)
  const [deleteId, setDeleteId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [toastMessage, setToastMessage] = useState(null)

  const statusOptions = ['All', 'Sowing', 'Growing', 'Harvesting', 'Completed']
  const debouncedSearch = useDebounce(search)

  const showToast = (text, type = 'success') => {
    setToastMessage({ text, type })
    setTimeout(() => setToastMessage(null), 3000)
  }

  // Fetch Real Database Plots
  const fetchPlots = async () => {
    setLoading(true)
    try {
      const res = await axiosClient.get('/api/v1/plots/')
      if (res.data && res.data.success && Array.isArray(res.data.data)) {
        setPlots(res.data.data)
      }
    } catch (err) {
      console.warn('Failed to fetch plots from database:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPlots()
  }, [])

  const filtered = plots.filter((p) => {
    const pName = p.plot_name || p.name || ''
    const pCrop = p.crop_name || p.crop || ''
    const pStatus = p.status || 'Growing'

    const matchSearch =
      pName.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
      pCrop.toLowerCase().includes(debouncedSearch.toLowerCase())
    const matchStatus = statusFilter === 'All' || pStatus === statusFilter
    return matchSearch && matchStatus
  })

  const openAdd = () => {
    setForm(emptyForm)
    setEditId(null)
    setIsModalOpen(true)
  }

  const openEdit = (plot) => {
    setForm({
      plot_name: plot.plot_name || plot.name || '',
      area: plot.area || '',
      crop_name: plot.crop_name || plot.crop || 'Wheat',
      status: plot.status || 'Growing',
      sowing_date: plot.sowing_date || plot.sowingDate || '',
      expected_harvest: plot.expected_harvest || plot.harvestDate || '',
      soil_type: plot.soil_type || plot.soilType || 'Black Cotton',
    })
    setEditId(plot.id)
    setIsModalOpen(true)
  }

  // Handle Save (Create / Update in SQL Database)
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.plot_name || !form.crop_name || !form.area) return

    setSubmitting(true)
    try {
      const payload = {
        plot_name: form.plot_name,
        crop_name: form.crop_name,
        area: parseFloat(form.area) || 1.0,
        soil_type: form.soil_type || 'Black Cotton',
        sowing_date: form.sowing_date || null,
        expected_harvest: form.expected_harvest || null,
        status: form.status || 'Growing',
      }

      if (editId) {
        await axiosClient.put(`/api/v1/plots/${editId}`, payload)
        showToast('✅ Plot updated successfully in database!')
      } else {
        await axiosClient.post('/api/v1/plots/', payload)
        showToast('🎉 New Plot added to SQL database!')
      }

      setIsModalOpen(false)
      fetchPlots()
    } catch (err) {
      console.error('Error saving plot:', err)
      showToast('Failed to save plot to database', 'error')
    } finally {
      setSubmitting(false)
    }
  }

  // Handle Delete Plot from SQL Database
  const handleDelete = async () => {
    if (!deleteId) return
    try {
      await axiosClient.delete(`/api/v1/plots/${deleteId}`)
      showToast('🗑️ Plot deleted from database!')
      setDeleteId(null)
      fetchPlots()
    } catch (err) {
      console.error('Error deleting plot:', err)
      showToast('Failed to delete plot', 'error')
    }
  }

  // Advance Crop Lifecycle Stage
  const handleAdvanceLifecycle = async (plot, newStatus) => {
    try {
      await axiosClient.put(`/api/v1/plots/${plot.id}`, {
        plot_name: plot.plot_name || plot.name,
        crop_name: plot.crop_name || plot.crop,
        area: plot.area,
        soil_type: plot.soil_type || 'Black Cotton',
        sowing_date: plot.sowing_date,
        expected_harvest: plot.expected_harvest,
        status: newStatus,
      })
      showToast(`🌱 Crop lifecycle advanced to '${newStatus}'!`)
      fetchPlots()
    } catch (err) {
      console.error('Error advancing plot lifecycle:', err)
      showToast('Failed to advance crop lifecycle', 'error')
    }
  }

  return (
    <div className="space-y-6">
      {/* Toast */}
      {toastMessage && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-xl shadow-xl text-xs font-bold transition-all ${
          toastMessage.type === 'error' ? 'bg-red-600 text-white' : 'bg-emerald-700 text-white'
        }`}>
          {toastMessage.text}
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-gray-900">{t('plot.title', 'Plot Management & Crop Lifecycle')}</h1>
          <p className="text-gray-500 text-xs mt-1">Track crop lifecycle stages from sowing to harvest and manage farm plots.</p>
        </div>
        <Button icon="+" onClick={openAdd}>{t('plot.addNewPlot', 'Add New Plot')}</Button>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Plots', value: plots.length, icon: '🗺️' },
          { label: 'Growing Stage', value: plots.filter((p) => (p.status || 'Growing') === 'Growing').length, icon: '🌿' },
          { label: 'Harvesting Stage', value: plots.filter((p) => p.status === 'Harvesting').length, icon: '🌾' },
          { label: 'Total Area', value: `${plots.reduce((s, p) => s + parseFloat(p.area || 0), 0).toFixed(1)} ac`, icon: '📐' },
        ].map((stat, idx) => (
          <div key={idx} className="bg-white p-4 rounded-2xl border border-gray-100 shadow-xs flex items-center gap-3">
            <span className="text-2xl">{stat.icon}</span>
            <div>
              <p className="text-xs text-gray-500 font-semibold">{stat.label}</p>
              <p className="text-xl font-extrabold text-gray-900 mt-0.5">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1">
          <SearchBar value={search} onChange={setSearch} placeholder="Search plots or crops..." />
        </div>
        <div className="flex items-center gap-1 overflow-x-auto pb-1">
          {statusOptions.map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-2 rounded-xl text-xs font-semibold whitespace-nowrap cursor-pointer transition-all ${
                statusFilter === st ? 'bg-emerald-700 text-white shadow-xs' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Plot Cards Grid */}
      {loading ? (
        <div className="py-12 text-center text-xs text-gray-400 animate-pulse">Loading plots from SQL database...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-white p-12 rounded-2xl border border-gray-200 text-center space-y-3">
          <span className="text-4xl">🗺️</span>
          <h3 className="text-base font-bold text-gray-800">No Farm Plots Found</h3>
          <p className="text-xs text-gray-500">Click <b>"Add New Plot"</b> to start tracking your land and crop lifecycle stages.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((plot) => {
            const currentStatus = plot.status || 'Growing'
            const currentStage = LIFECYCLE_STAGES.find(s => s.name.toLowerCase() === currentStatus.toLowerCase()) || LIFECYCLE_STAGES[1]

            return (
              <div key={plot.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      📍 {plot.plot_name || plot.name}
                    </span>
                    <span className={`text-xs font-extrabold px-2.5 py-0.5 rounded-full ${getStatusColor(currentStatus)}`}>
                      {translateStatus ? translateStatus(currentStatus) : currentStatus}
                    </span>
                  </div>

                  <div className="mt-3">
                    <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                      <span>🌾</span> {translateCrop ? translateCrop(plot.crop_name || plot.crop) : (plot.crop_name || plot.crop)}
                    </h3>
                    <p className="text-xs text-gray-500 mt-0.5">
                      📐 Area: <b>{plot.area} Acres</b> | Soil: <b>{plot.soil_type || 'Black Cotton'}</b>
                    </p>
                  </div>

                  {/* CROP LIFECYCLE STAGE TRACKER */}
                  <div className="mt-4 bg-gray-50 p-3.5 rounded-xl border border-gray-100 space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold text-gray-800">
                      <span>Crop Lifecycle Stage:</span>
                      <span className="text-emerald-700">{currentStage.label} ({currentStage.pct}%)</span>
                    </div>

                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-emerald-600 to-teal-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${currentStage.pct}%` }}
                      />
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-gray-500 pt-1">
                      <span>📅 Sown: {plot.sowing_date || '2026-06-01'}</span>
                      <span>🌾 Harvest: {plot.expected_harvest || '2026-10-15'}</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-gray-100 flex items-center gap-2">
                  <button
                    onClick={() => openEdit(plot)}
                    className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                  >
                    ✏️ Edit Plot
                  </button>
                  <button
                    onClick={() => handleAdvanceLifecycle(plot, currentStatus === 'Sowing' ? 'Growing' : currentStatus === 'Growing' ? 'Harvesting' : 'Completed')}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                  >
                    <span>🌱</span> Next Stage
                  </button>
                  <button
                    onClick={() => setDeleteId(plot.id)}
                    className="px-3 bg-red-50 hover:bg-red-100 text-red-600 font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Add / Edit Plot Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editId ? '✏️ Edit Farm Plot' : '➕ Add New Farm Plot'}>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <Input label="Plot Name *" value={form.plot_name} onChange={(e) => setForm({ ...form, plot_name: e.target.value })} placeholder="e.g. North Field Plot #1" required />
          <div>
            <label className="font-semibold text-gray-700 block mb-1">Crop Name *</label>
            <select
              value={form.crop_name}
              onChange={(e) => setForm({ ...form, crop_name: e.target.value })}
              className="w-full px-3.5 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-600 bg-white font-medium"
              required
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
          <Input label="Plot Area (Acres) *" type="number" step="0.1" value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} placeholder="5.0" required />

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-semibold text-gray-700 block mb-1">Lifecycle Stage</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} className="w-full px-3.5 py-2 border rounded-xl text-sm">
                <option value="Sowing">Sowing</option>
                <option value="Growing">Growing</option>
                <option value="Harvesting">Harvesting</option>
                <option value="Completed">Completed</option>
              </select>
            </div>
            <div>
              <label className="font-semibold text-gray-700 block mb-1">Soil Type</label>
              <input type="text" value={form.soil_type} onChange={(e) => setForm({ ...form, soil_type: e.target.value })} placeholder="Black Cotton / Red Soil" className="w-full px-3.5 py-2 border rounded-xl text-sm" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Input label="Sowing Date" type="date" value={form.sowing_date} onChange={(e) => setForm({ ...form, sowing_date: e.target.value })} />
            <Input label="Expected Harvest Date" type="date" value={form.expected_harvest} onChange={(e) => setForm({ ...form, expected_harvest: e.target.value })} />
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={submitting}>{submitting ? 'Saving...' : 'Save Plot →'}</Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal isOpen={!!deleteId} onClose={() => setDeleteId(null)} title="🗑️ Delete Plot Confirmation">
        <p className="text-xs text-gray-600 mb-4">Are you sure you want to delete this farm plot? This action cannot be undone.</p>
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={() => setDeleteId(null)}>Cancel</Button>
          <button onClick={handleDelete} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl cursor-pointer">Delete Plot</button>
        </div>
      </Modal>
    </div>
  )
}

export default PlotManagement
