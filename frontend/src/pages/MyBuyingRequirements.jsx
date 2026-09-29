import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import axiosClient from '../api/axiosClient'
import AIPriceRecommendationCard from '../components/AIPriceRecommendationCard'
import OrderTrackingCard from '../components/OrderTrackingCard'

const MyBuyingRequirements = () => {
  const { user } = useAuth()
  const { t, translateStatus, translateCrop, translateMandi } = useLanguage()
  const [requirements, setRequirements] = useState([])
  const [purchaseRequests, setPurchaseRequests] = useState([])
  const [confirmedOrders, setConfirmedOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [notification, setNotification] = useState(null)
  const [activeTab, setActiveTab] = useState('requirements') // 'requirements' | 'sent_requests'
  
  // Modals
  const [showReqModal, setShowReqModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)

  // Rating Modal State
  const [showRateModal, setShowRateModal] = useState(false)
  const [ratingTarget, setRatingTarget] = useState(null)
  const [stars, setStars] = useState(5)
  const [reviewText, setReviewText] = useState('')
  const [ratingSubmitting, setRatingSubmitting] = useState(false)

  const [newReq, setNewReq] = useState({
    crop_name: 'Wheat',
    quantity_required: 100,
    offered_price: 2250,
    preferred_quality: 'Grade A',
    preferred_district: user?.district || 'Nashik',
    delivery_location: 'Nashik APMC Yard'
  })

  useEffect(() => {
    fetchMyRequirements()
    fetchMyPurchaseRequests()
    fetchUserDeals()
    const interval = setInterval(() => {
      fetchMyPurchaseRequests()
      fetchUserDeals()
    }, 4000)
    const handleFocus = () => {
      fetchMyPurchaseRequests()
      fetchUserDeals()
    }
    window.addEventListener('focus', handleFocus)
    return () => {
      clearInterval(interval)
      window.removeEventListener('focus', handleFocus)
    }
  }, [])

  const fetchUserDeals = async () => {
    try {
      const response = await axiosClient.get('/api/v1/deals/my')
      if (response.data && response.data.success) {
        const confirmed = response.data.data.filter(d => 
          d.order_status || ['farmer accepted', 'deal confirmed', 'delivered', 'payment completed'].includes((d.status || '').toLowerCase())
        )
        setConfirmedOrders(confirmed)
      }
    } catch (err) {
      console.warn('Error fetching user deals for buyer:', err)
    }
  }

  const showToast = (msg, type = 'success') => {
    setNotification({ msg, type })
    setTimeout(() => setNotification(null), 4000)
  }

  const handleOpenRateModal = (deal) => {
    setRatingTarget(deal)
    setStars(5)
    setReviewText('')
    setShowRateModal(true)
  }

  const handleSubmitRating = async (e) => {
    e.preventDefault()
    if (!ratingTarget) return
    setRatingSubmitting(true)
    try {
      const payload = {
        to_user_id: ratingTarget.farmer_id || ratingTarget.owner_id,
        deal_id: ratingTarget.deal_id || ratingTarget.id,
        rating: parseFloat(stars),
        review: reviewText || 'Verified buyer trade rating',
      }
      const res = await axiosClient.post('/api/v1/ratings', payload)
      if (res.data?.success) {
        showToast(`⭐ ${stars}-Star ${t('marketplace.ratingSubmitted')}`)
        setShowRateModal(false)
        fetchMyPurchaseRequests()
      }
    } catch (err) {
      showToast(t('marketplace.ratingError'), 'error')
    } finally {
      setRatingSubmitting(false)
    }
  }

  const handleDownloadInvoice = async (dealId) => {
    try {
      const response = await axiosClient.get(`/api/v1/reports/deal/${dealId}/invoice/pdf`, {
        responseType: 'blob',
      })
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `SmartAgri_Invoice_${dealId.slice(0, 6)}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      showToast(`📄 ${t('marketplace.invoiceDownloaded')}`)
    } catch (err) {
      showToast(t('marketplace.invoiceError'), 'error')
    }
  }

  const fetchMyRequirements = async () => {
    setLoading(true)
    try {
      const res = await axiosClient.get('/api/v1/requirements/my')
      if (res.data && res.data.success) {
        setRequirements(res.data.data)
      }
    } catch (err) {
      console.error('Error fetching buyer requirements:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchMyPurchaseRequests = async () => {
    try {
      const res = await axiosClient.get('/api/v1/requests/buyer')
      if (res.data && res.data.success) {
        setPurchaseRequests(res.data.data)
      }
    } catch (err) {
      console.warn('Error fetching buyer purchase requests:', err)
    }
  }

  const handleCreateRequirement = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      const response = await axiosClient.post('/api/v1/requirements/', newReq)
      if (response.data?.success) {
        showToast(`🎉 ${t('myRequirements.reqPostedToast')}`)
        setShowReqModal(false)
        setNewReq({
          crop_name: 'Wheat',
          quantity_required: 100,
          offered_price: 2250,
          preferred_quality: 'Grade A',
          preferred_district: user?.district || 'Nashik',
          delivery_location: 'Nashik APMC Yard'
        })
        await fetchMyRequirements()
      }
    } catch (err) {
      showToast(err.response?.data?.message || 'Error posting requirement', 'error')
    } finally {
      setSubmitting(false)
    }
  }

  const handleUpdateRequirement = async (e) => {
    e.preventDefault()
    if (!editingItem) return
    setSubmitting(true)
    try {
      const response = await axiosClient.put(`/api/v1/requirements/${editingItem.id}`, editingItem)
      if (response.data?.success) {
        showToast(`✅ ${t('myRequirements.reqUpdatedToast')}`)
        setShowEditModal(false)
        await fetchMyRequirements()
      }
    } catch (err) {
      showToast('Error updating requirement', 'error')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCloseRequirement = async (reqItem) => {
    try {
      const updated = { ...reqItem, status: 'Closed' }
      const response = await axiosClient.put(`/api/v1/requirements/${reqItem.id}`, updated)
      if (response.data?.success) {
        showToast(`🔒 ${t('myRequirements.reqClosedToast')}`)
        await fetchMyRequirements()
      }
    } catch (err) {
      showToast('Error closing requirement', 'error')
    }
  }

  const handleDeleteRequirement = async (id) => {
    if (!window.confirm(t('myRequirements.confirmDelete'))) return
    try {
      const res = await axiosClient.delete(`/api/v1/requirements/${id}`)
      if (res.data?.success) {
        showToast(`🗑️ ${t('myRequirements.reqDeletedToast')}`)
        await fetchMyRequirements()
      }
    } catch (err) {
      showToast('Error deleting requirement', 'error')
    }
  }

  return (
    <div className="space-y-6 pb-12">
      {/* Toast Notification */}
      {notification && (
        <div className={`p-4 rounded-xl shadow-lg border text-sm font-bold flex items-center justify-between transition-all ${
          notification.type === 'error' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-emerald-50 text-emerald-900 border-emerald-300'
        }`}>
          <span>{notification.msg}</span>
          <button onClick={() => setNotification(null)} className="text-xs text-gray-500 hover:text-gray-800">✕</button>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-3xl">📋</span>
            <h1 className="text-2xl font-bold">{t('myRequirements.title')}</h1>
            <span className="bg-blue-400 text-black text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              {t('myRequirements.badge')}
            </span>
          </div>
          <p className="text-blue-100 text-sm mt-1">
            {t('myRequirements.subtitle')}
          </p>
        </div>

        <button
          onClick={() => setShowReqModal(true)}
          className="bg-white text-blue-950 hover:bg-blue-50 font-bold px-5 py-3 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 text-sm cursor-pointer"
        >
          ➕ {t('myRequirements.postNew')}
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-3 border-b border-gray-200 pb-2">
        <button
          onClick={() => setActiveTab('requirements')}
          className={`px-5 py-2.5 rounded-xl font-bold text-sm transition-all cursor-pointer ${
            activeTab === 'requirements'
              ? 'bg-blue-900 text-white shadow-md'
              : 'bg-white text-gray-600 hover:bg-gray-100 border'
          }`}
        >
          📋 {t('myRequirements.tabMyReqs')} ({requirements.length})
        </button>
        <button
          onClick={() => setActiveTab('sent_requests')}
          className={`px-5 py-2.5 rounded-xl font-bold text-sm transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'sent_requests'
              ? 'bg-blue-900 text-white shadow-md'
              : 'bg-white text-gray-600 hover:bg-gray-100 border'
          }`}
        >
          <span>📩 {t('myRequirements.tabSentRequests')} ({purchaseRequests.length})</span>
          {purchaseRequests.filter(r => r.status?.toLowerCase() === 'accepted').length > 0 && (
            <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full border border-emerald-300 shadow-sm">
              {purchaseRequests.filter(r => r.status?.toLowerCase() === 'accepted').length} {t('myRequirements.acceptedBadge')}
            </span>
          )}
        </button>
      </div>

      {/* MY REQUIREMENTS TAB */}
      {activeTab === 'requirements' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">{t('myRequirements.postedDemandOrders')} ({requirements.length})</h2>
            <span className="text-xs text-gray-500">{t('myRequirements.autoSynced')}</span>
          </div>

          {loading ? (
            <div className="py-12 text-center text-gray-500 animate-pulse">{t('myRequirements.loadingReqs')}</div>
          ) : requirements.length === 0 ? (
            <div className="bg-white p-8 rounded-2xl text-center border border-gray-200 space-y-3">
              <span className="text-4xl">🏢</span>
              <h3 className="text-base font-bold text-gray-800">{t('myRequirements.noReqsTitle')}</h3>
              <p className="text-xs text-gray-500">{t('myRequirements.noReqsDesc')}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {requirements.map((item) => (
                <div key={item.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="bg-amber-100 text-amber-800 text-xs font-bold px-3 py-1 rounded-full">{item.preferred_quality || 'Grade A'}</span>
                      <span className={`text-xs font-extrabold px-2.5 py-0.5 rounded-full ${
                        item.status === 'Closed' ? 'bg-gray-200 text-gray-700' : 'bg-blue-600 text-white'
                      }`}>
                        {translateStatus(item.status || 'OPEN')}
                      </span>
                    </div>

                    <div className="mt-3">
                      <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                        <span>🏢</span> {translateCrop ? translateCrop(item.crop_name) : item.crop_name}
                      </h3>
                      <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                        📍 {t('myRequirements.preferredDistrict')}: {translateMandi ? translateMandi(item.preferred_district || 'Nashik') : (item.preferred_district || 'Nashik')}
                      </p>
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-2 bg-blue-50/50 p-3 rounded-xl border border-blue-100">
                      <div>
                        <span className="text-xs text-gray-500 block">{t('marketplace.requiredQuantity')}</span>
                        <span className="text-sm font-bold text-gray-800">{item.quantity_required} {t('units.quintal')}</span>
                      </div>
                      <div>
                        <span className="text-xs text-gray-500 block">{t('marketplace.offeredPrice')}</span>
                        <span className="text-sm font-bold text-blue-800">₹{item.offered_price} / {t('units.quintal')}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-5 pt-3 border-t border-gray-100 flex items-center justify-between gap-2">
                    <button
                      onClick={() => { setEditingItem(item); setShowEditModal(true) }}
                      className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                    >
                      ✏️ {t('actions.edit')}
                    </button>
                    {item.status !== 'Closed' && (
                      <button
                        onClick={() => handleCloseRequirement(item)}
                        className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                      >
                        🔒 {t('myRequirements.closeReq')}
                      </button>
                    )}
                    <button
                      onClick={() => handleDeleteRequirement(item.id)}
                      className="bg-red-50 hover:bg-red-100 text-red-600 font-semibold px-3 py-2 rounded-xl text-xs transition-all cursor-pointer"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* SENT PURCHASE REQUESTS & WHATSAPP TAB */}
      {activeTab === 'sent_requests' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">{t('myRequirements.submittedRequests')} ({purchaseRequests.length})</h2>
            <span className="text-xs text-gray-500">{t('myRequirements.directConnections')}</span>
          </div>

          {purchaseRequests.length === 0 ? (
            <div className="bg-white p-8 rounded-2xl text-center border border-gray-200 space-y-3">
              <span className="text-4xl">📩</span>
              <h3 className="text-base font-bold text-gray-800">{t('myRequirements.noSentRequests')}</h3>
              <p className="text-xs text-gray-500">{t('myRequirements.noSentDesc')}</p>
            </div>
          ) : (
            <>
              {/* Accepted Active Orders with Order Tracking Timeline */}
              {purchaseRequests.filter(r => r.status?.toLowerCase() === 'accepted').length > 0 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                      <span>🚚</span> {t('myRequirements.activeOrdersDelivery')} ({purchaseRequests.filter(r => r.status?.toLowerCase() === 'accepted').length})
                    </h2>
                    <span className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full font-bold">
                      {t('myRequirements.liveDeliveryProgress')}
                    </span>
                  </div>
                  <div className="space-y-4">
                    {purchaseRequests.filter(r => r.status?.toLowerCase() === 'accepted').map((req) => (
                      <OrderTrackingCard
                        key={req.deal_id || req.id}
                        deal={req}
                        role="Buyer"
                        onStatusUpdated={fetchMyPurchaseRequests}
                        onOpenRateModal={handleOpenRateModal}
                        onDownloadInvoice={handleDownloadInvoice}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Pending / Declined Purchase Requests */}
              {purchaseRequests.filter(r => r.status?.toLowerCase() !== 'accepted').length > 0 && (
                <div className="space-y-4 pt-2">
                  <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    <span>📩</span> {t('myRequirements.sentRequestsInquiries')} ({purchaseRequests.filter(r => r.status?.toLowerCase() !== 'accepted').length})
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {purchaseRequests.filter(r => r.status?.toLowerCase() !== 'accepted').map((req) => (
                      <div key={req.id} className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm space-y-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="font-bold text-gray-900 text-base">{t('roles.farmer')}: {req.farmer_name}</h4>
                            <p className="text-xs text-gray-500">📍 {t('myListings.location')}: <b>{req.listing_location || req.farmer_district || 'Nashik'}</b></p>
                          </div>
                          <span className={`text-xs font-extrabold px-3 py-1 rounded-full ${
                            req.status?.toLowerCase() === 'rejected' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'
                          }`}>
                            {translateStatus(req.status)}
                          </span>
                        </div>

                        <div className="bg-blue-50/60 p-3 rounded-xl border border-blue-100 grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-gray-500 block">{t('myRequirements.targetCrop')}</span>
                            <span className="font-bold text-gray-800">{translateCrop ? translateCrop(req.crop) : req.crop}</span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">{t('marketplace.offeredPrice')}</span>
                            <span className="font-bold text-blue-700">₹{req.offered_price} / {t('units.quintal')}</span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">{t('myRequirements.requestedQty')}</span>
                            <span className="font-bold text-gray-800">{req.quantity} {t('units.quintal')}</span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">{t('myRequirements.totalValue')}</span>
                            <span className="font-bold text-blue-900">₹{(req.quantity * req.offered_price).toLocaleString()}</span>
                          </div>
                        </div>

                        {req.message && (
                          <div className="bg-gray-50 p-2.5 rounded-lg border text-xs text-gray-700">
                            <b>{t('myRequirements.yourNote')}</b> "{req.message}"
                          </div>
                        )}

                        <div className="pt-2 border-t border-gray-100">
                          {req.status?.toLowerCase() === 'pending' ? (
                            <div className="text-center text-xs text-amber-700 font-semibold bg-amber-50 p-2 rounded-lg border border-amber-200">
                              ⏳ {t('myRequirements.awaitingAcceptance')}
                            </div>
                          ) : (
                            <div className="text-center text-xs text-red-600 font-semibold bg-red-50 p-2 rounded-lg border border-red-200">
                              ❌ {t('myRequirements.farmerDeclined')}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Post Requirement Modal */}
      {showReqModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleCreateRequirement} className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">📋 {t('myRequirements.postBuyingReqTitle')}</h3>
              <button type="button" onClick={() => setShowReqModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myRequirements.cropName')}</label>
                <input
                  type="text"
                  value={newReq.crop_name}
                  onChange={e => setNewReq({ ...newReq, crop_name: e.target.value })}
                  placeholder={t('myRequirements.cropPlaceholder')}
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.requiredQuantityQuintals')}</label>
                  <input
                    type="number"
                    step="0.1"
                    value={newReq.quantity_required}
                    onChange={e => setNewReq({ ...newReq, quantity_required: e.target.value === '' ? '' : Number(e.target.value) })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.offeredPriceQtl')}</label>
                  <input
                    type="number"
                    step="0.1"
                    value={newReq.offered_price}
                    onChange={e => setNewReq({ ...newReq, offered_price: e.target.value === '' ? '' : Number(e.target.value) })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myRequirements.preferredDistrict')}</label>
                <input
                  type="text"
                  value={newReq.preferred_district}
                  onChange={e => setNewReq({ ...newReq, preferred_district: e.target.value })}
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* AI SMART PRICE RECOMMENDATION CARD */}
            {newReq.crop_name && newReq.crop_name.trim() !== '' && (
              <AIPriceRecommendationCard
                crop={newReq.crop_name}
                district={newReq.preferred_district || user?.district || 'Nashik'}
                quantity={newReq.quantity_required || 100}
                qualityGrade={newReq.preferred_quality || 'Grade A'}
                role="buyer"
                userPrice={newReq.offered_price}
                onUseAiPrice={(recPrice) => setNewReq(prev => ({ ...prev, offered_price: recPrice }))}
              />
            )}

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowReqModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.cancel')}</button>
              <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-blue-900 hover:bg-blue-950 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {submitting ? t('myRequirements.posting') : t('myRequirements.postReqBtn')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Edit Requirement Modal */}
      {showEditModal && editingItem && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleUpdateRequirement} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">✏️ {t('myRequirements.editReqTitle')}</h3>
              <button type="button" onClick={() => setShowEditModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myRequirements.cropName')}</label>
                <input type="text" value={editingItem.crop_name} onChange={e => setEditingItem({ ...editingItem, crop_name: e.target.value })} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500" required />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myRequirements.requestedQty')}</label>
                  <input type="number" step="0.1" value={editingItem.quantity_required} onChange={e => setEditingItem({ ...editingItem, quantity_required: e.target.value === '' ? '' : Number(e.target.value) })} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500" required />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.offeredPriceQtl')}</label>
                  <input type="number" step="0.1" value={editingItem.offered_price} onChange={e => setEditingItem({ ...editingItem, offered_price: e.target.value === '' ? '' : Number(e.target.value) })} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500" required />
                </div>
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowEditModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.cancel')}</button>
              <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-blue-900 hover:bg-blue-950 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {t('myRequirements.saveChanges')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ⭐ Rate Farmer Modal */}
      {showRateModal && ratingTarget && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSubmitRating} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>⭐</span> {t('marketplace.rateFarmerTitle')} ({ratingTarget.farmer_name || t('roles.farmer')})
              </h3>
              <button type="button" onClick={() => setShowRateModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="text-center py-2 space-y-2">
              <p className="text-xs text-gray-500">Order #{ratingTarget.order_number} • {translateCrop ? translateCrop(ratingTarget.crop) : ratingTarget.crop} ({ratingTarget.quantity} {t('units.quintal')})</p>
              <div className="flex items-center justify-center gap-2">
                {[1, 2, 3, 4, 5].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setStars(num)}
                    className={`text-3xl transition-transform hover:scale-125 cursor-pointer ${
                      num <= stars ? 'text-amber-400' : 'text-gray-200'
                    }`}
                  >
                    ★
                  </button>
                ))}
              </div>
              <span className="text-xs font-bold text-amber-600 block">{stars} {t('marketplace.outOfStars')}</span>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.feedbackReview')}</label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder={t('marketplace.feedbackPlaceholder')}
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500 h-20 resize-none"
              />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowRateModal(false)} className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-semibold cursor-pointer">
                {t('actions.cancel')}
              </button>
              <button type="submit" disabled={ratingSubmitting} className="px-5 py-2 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl text-xs transition-all disabled:opacity-50 cursor-pointer shadow-xs">
                {ratingSubmitting ? t('marketplace.submitting') : t('marketplace.submitRatingBtn')}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

export default MyBuyingRequirements
