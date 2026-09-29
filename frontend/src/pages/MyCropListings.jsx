import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import axiosClient from '../api/axiosClient'
import AIPriceRecommendationCard from '../components/AIPriceRecommendationCard'
import CropListingOrderTimeline from '../components/CropListingOrderTimeline'

const MyCropListings = () => {
  const { user } = useAuth()
  const { t, translateStatus, translateCrop, translateMandi } = useLanguage()
  
  const [listings, setListings] = useState([])
  const [requests, setRequests] = useState([])
  const [confirmedOrders, setConfirmedOrders] = useState([])
  const [activeTab, setActiveTab] = useState('listings') // 'listings' | 'requests'
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState(null)
  
  // Modals
  const [showListingModal, setShowListingModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [selectedListing, setSelectedListing] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  // Rating Modal State
  const [showRateModal, setShowRateModal] = useState(false)
  const [ratingTarget, setRatingTarget] = useState(null)
  const [stars, setStars] = useState(5)
  const [selectedTags, setSelectedTags] = useState(['Prompt Full Payment', 'Fair Mandi Weighing'])
  const [reviewText, setReviewText] = useState('')
  const [ratingSubmitting, setRatingSubmitting] = useState(false)

  // Form State
  const [newListing, setNewListing] = useState({
    crop: '',
    quantity: '',
    expected_price: '',
    quality_grade: 'Grade A',
    location: user?.location || 'Nashik APMC Yard',
    photo_url: '',
  })

  useEffect(() => {
    fetchMyListings()
    fetchFarmerRequests()
    fetchUserDeals()
    const interval = setInterval(() => {
      fetchFarmerRequests()
      fetchUserDeals()
    }, 4000)
    const handleFocus = () => {
      fetchFarmerRequests()
      fetchUserDeals()
      fetchMyListings()
    }
    window.addEventListener('focus', handleFocus)
    return () => {
      clearInterval(interval)
      window.removeEventListener('focus', handleFocus)
    }
  }, [])

  const showToast = (msg, type = 'success') => {
    setNotification({ msg, type })
    setTimeout(() => setNotification(null), 4000)
  }

  const handleOpenRateBuyer = (buyerObj) => {
    setRatingTarget(buyerObj)
    setStars(5)
    setSelectedTags(['Prompt Full Payment', 'Fair Mandi Weighing'])
    setReviewText('')
    setShowRateModal(true)
  }

  const handleToggleTag = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag))
    } else {
      setSelectedTags([...selectedTags, tag])
    }
  }

  const handleSubmitRating = async (e) => {
    e.preventDefault()
    if (!ratingTarget) return
    setRatingSubmitting(true)
    try {
      const fullReview = `${selectedTags.join(', ')}. ${reviewText}`.trim()
      const payload = {
        to_user_id: ratingTarget.buyer_id || ratingTarget.id,
        deal_id: ratingTarget.deal_id || ratingTarget.id,
        rating: parseFloat(stars),
        review: fullReview || 'Verified farmer rating',
      }
      const res = await axiosClient.post('/api/v1/ratings', payload)
      if (res.data?.success) {
        showToast(`⭐ ${stars}-Star Rating & Feedback submitted for ${ratingTarget.buyer_name || 'buyer'}!`)
        setShowRateModal(false)
      }
    } catch (err) {
      showToast('Error submitting buyer rating', 'error')
    } finally {
      setRatingSubmitting(false)
    }
  }

  const fetchMyListings = async () => {
    setLoading(true)
    try {
      const response = await axiosClient.get('/api/v1/listings/my')
      if (response.data && response.data.success) {
        setListings(response.data.data)
      }
    } catch (err) {
      console.error('Error fetching farmer listings:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchFarmerRequests = async () => {
    try {
      const response = await axiosClient.get('/api/v1/requests/farmer')
      if (response.data && response.data.success) {
        setRequests(response.data.data)
      }
    } catch (err) {
      console.warn('Error fetching farmer purchase requests:', err)
    }
  }

  const fetchUserDeals = async () => {
    try {
      const response = await axiosClient.get('/api/v1/deals/my')
      if (response.data && response.data.success) {
        // Only keep confirmed orders (e.g., status is "Farmer Accepted", "Order Confirmed", "Dispatched", "Out for Delivery", "Delivered")
        const confirmed = response.data.data.filter(d => 
          d.order_status || ['farmer accepted', 'deal confirmed', 'delivered', 'payment completed'].includes((d.status || '').toLowerCase())
        )
        setConfirmedOrders(confirmed)
      }
    } catch (err) {
      console.warn('Error fetching user deals:', err)
    }
  }

  const handleCreateListing = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      const payload = {
        crop: newListing.crop,
        quantity: parseFloat(newListing.quantity),
        expected_price: parseFloat(newListing.expected_price),
        quality_grade: newListing.quality_grade,
        location: newListing.location || 'Nashik',
        photo_url: newListing.photo_url || null,
        advance_days: parseInt(newListing.advance_days || 0),
        status: 'ACTIVE',
      }
      const response = await axiosClient.post('/api/v1/listings', payload)
      if (response.data?.success) {
        showToast('🎉 Crop listing published successfully!')
        setShowListingModal(false)
        setNewListing({
          crop: '',
          quantity: '',
          expected_price: '',
          quality_grade: 'Grade A',
          location: user?.location || 'Nashik APMC Yard',
          photo_url: '',
          advance_days: 0,
        })
        await fetchMyListings()
      }
    } catch (err) {
      console.error('Error publishing crop listing:', err)
      const errorMsg = err.response?.data?.message || err.response?.data?.detail || err.message || 'Error publishing crop listing'
      showToast(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg), 'error')
    } finally {
      setSubmitting(false)
    }
  }

  const handleUpdateListing = async (e) => {
    e.preventDefault()
    if (!selectedListing) return
    setSubmitting(true)
    try {
      const payload = {
        crop: selectedListing.crop,
        quantity: parseFloat(selectedListing.quantity),
        expected_price: parseFloat(selectedListing.expected_price),
        quality_grade: selectedListing.quality_grade,
        location: selectedListing.location,
        advance_days: parseInt(selectedListing.advance_days || 0),
        status: selectedListing.status,
      }
      const response = await axiosClient.put(`/api/v1/listings/${selectedListing.id}`, payload)
      if (response.data?.success) {
        showToast('✅ Crop listing updated!')
        setShowEditModal(false)
        await fetchMyListings()
      }
    } catch (err) {
      showToast('Error updating listing', 'error')
    } finally {
      setSubmitting(false)
    }
  }

  const handleMarkAsSold = async (listing) => {
    try {
      const updated = { ...listing, status: 'SOLD' }
      const response = await axiosClient.put(`/api/v1/listings/${listing.id}`, updated)
      if (response.data?.success) {
        showToast('🏷️ Listing marked as SOLD!')
        await fetchMyListings()
      }
    } catch (err) {
      showToast('Error marking listing as sold', 'error')
    }
  }

  const handleDeleteListing = async (id) => {
    if (!window.confirm('Are you sure you want to delete this crop listing?')) return
    try {
      const res = await axiosClient.delete(`/api/v1/listings/${id}`)
      if (res.data?.success) {
        showToast('🗑️ Crop listing deleted!')
        await fetchMyListings()
      }
    } catch (err) {
      showToast('Error deleting listing', 'error')
    }
  }

  // Handle Accept Purchase Request
  const handleAcceptRequest = async (reqId) => {
    try {
      const res = await axiosClient.put(`/api/v1/requests/${reqId}/accept`)
      if (res.data?.success) {
        showToast('🎉 Purchase Request Accepted! Order confirmed and delivery tracking started.')
        await fetchFarmerRequests()
        await fetchUserDeals()
      }
    } catch (err) {
      showToast('Error accepting purchase request', 'error')
    }
  }

  // Handle Reject Purchase Request
  const handleRejectRequest = async (reqId) => {
    try {
      const res = await axiosClient.put(`/api/v1/requests/${reqId}/reject`)
      if (res.data?.success) {
        showToast('❌ Purchase Request Declined')
        await fetchFarmerRequests()
      }
    } catch (err) {
      showToast('Error rejecting purchase request', 'error')
    }
  }

  // Download PDF Invoice
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
      showToast('📄 Official PDF Invoice downloaded!')
    } catch (err) {
      showToast('Failed to download invoice PDF', 'error')
    }
  }

  const pendingRequestsCount = requests.filter(r => r.status?.toLowerCase() === 'pending').length

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
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-gradient-to-r from-emerald-800 via-green-800 to-teal-800 text-white p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <span>📦</span> {t('myListings.title', 'My Crop Listings & Buyer Requests')}
          </h1>
          <p className="text-emerald-100 text-sm mt-1">
            {t('myListings.subtitle', 'Manage your published crop inventory, track views, and accept buyer purchase requests with direct WhatsApp connection.')}
          </p>
        </div>

        <button
          onClick={() => setShowListingModal(true)}
          className="bg-white text-emerald-900 hover:bg-emerald-50 font-bold px-5 py-3 rounded-xl shadow-lg transition-all flex items-center gap-2 text-sm cursor-pointer"
        >
          <span>➕</span> {t('myListings.publishNew', 'Publish New Crop Listing')}
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('listings')}
          className={`pb-3 px-4 font-bold text-sm transition-all border-b-2 cursor-pointer ${
            activeTab === 'listings' ? 'border-emerald-600 text-emerald-800' : 'border-transparent text-gray-500 hover:text-gray-800'
          }`}
        >
          🌾 {t('myListings.publishedListings', 'Published Crop Listings')} ({listings.length})
        </button>
        <button
          onClick={() => setActiveTab('requests')}
          className={`pb-3 px-4 font-bold text-sm transition-all border-b-2 flex items-center gap-2 cursor-pointer ${
            activeTab === 'requests' ? 'border-emerald-600 text-emerald-800' : 'border-transparent text-gray-500 hover:text-gray-800'
          }`}
        >
          <span>💬 {t('myListings.buyerRequests', 'Buyer Purchase Requests')} ({requests.length})</span>
          {pendingRequestsCount > 0 && (
            <span className="bg-amber-500 text-white text-xs font-extrabold px-2 py-0.5 rounded-full animate-bounce">
              {pendingRequestsCount} {t('myListings.newBadge', 'New')}
            </span>
          )}
        </button>
      </div>

      {/* TAB 1: FARMER'S PUBLISHED CROP LISTINGS */}
      {activeTab === 'listings' && (
        <div>
          {loading ? (
            <div className="py-12 text-center text-gray-500 animate-pulse">{t('myListings.loading', 'Loading your crop listings...')}</div>
          ) : listings.length === 0 ? (
            <div className="bg-white p-12 rounded-2xl border text-center space-y-4">
              <div className="text-4xl">🌾</div>
              <h3 className="text-lg font-bold text-gray-800">{t('myListings.noListings', 'No Crop Listings Published Yet')}</h3>
              <p className="text-gray-500 text-sm max-w-md mx-auto">
                {t('myListings.noListingsDesc', 'Publish your harvested crops to make them visible to real registered buyers in the Buyer Marketplace.')}
              </p>
              <button
                onClick={() => setShowListingModal(true)}
                className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-6 py-2.5 rounded-xl text-sm transition-all cursor-pointer inline-flex items-center gap-2"
              >
                <span>➕</span> {t('myListings.publishFirst', 'Publish First Listing')}
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {listings.map((item) => {
                // Find all confirmed orders for this specific crop listing
                const itemConfirmedDeals = []
                const seenDealIds = new Set()

                confirmedOrders.forEach((deal) => {
                  const isMatch = (deal.listing_id && deal.listing_id === item.id) ||
                    (deal.request_id && requests.some(r => r.id === deal.request_id && r.crop_listing_id === item.id))
                  if (isMatch) {
                    const key = deal.deal_id || deal.id || deal.order_number
                    if (key && !seenDealIds.has(key)) {
                      seenDealIds.add(key)
                      itemConfirmedDeals.push(deal)
                    }
                  }
                })

                requests.filter(r => r.status?.toLowerCase() === 'accepted' && r.crop_listing_id === item.id).forEach((req) => {
                  const key = req.deal_id || req.id || req.order_number
                  if (key && !seenDealIds.has(key)) {
                    seenDealIds.add(key)
                    itemConfirmedDeals.push(req)
                  }
                })

                return (
                <div key={item.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">{item.quality_grade || 'Grade A'}</span>
                      <span className={`text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase ${
                        item.status === 'SOLD' ? 'bg-gray-200 text-gray-700' : 'bg-emerald-600 text-white'
                      }`}>
                        {translateStatus(item.status || 'ACTIVE')}
                      </span>
                    </div>

                    <div className="mt-3">
                      <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                        <span>🌾</span> {translateCrop ? translateCrop(item.crop) : (t('crops.' + (item.crop || '').toLowerCase(), item.crop))}
                      </h3>
                      <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                        📍 {t('common.location', 'Location')}: <b>{translateMandi ? translateMandi(item.location || 'Nashik APMC Yard') : (item.location || 'Nashik APMC Yard')}</b>
                      </p>
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-2 bg-gray-50 p-3 rounded-xl border border-gray-100">
                      <div>
                        <span className="text-xs text-gray-500 block">{t('common.quantity', 'Quantity')}</span>
                        <span className="text-sm font-bold text-gray-800">{item.quantity} {t('units.quintal', 'Quintals')}</span>
                      </div>
                      <div>
                        <span className="text-xs text-gray-500 block">{t('myListings.expectedPrice', 'Expected Price')}</span>
                        <span className="text-sm font-bold text-emerald-700">₹{item.expected_price} / {t('units.quintal', 'Qtl')}</span>
                      </div>
                    </div>

                    {/* ⏱️ Dynamic Pre-Harvest Advance Order & Time-Decay Box */}
                    {(item.advance_days > 0 || (item.remaining_advance_days != null && item.remaining_advance_days > 0) || item.discount_pct > 0) ? (
                      <div className="mt-3 bg-gradient-to-br from-emerald-50 to-teal-50/60 border border-emerald-300 rounded-xl p-3 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black text-emerald-950 flex items-center gap-1">
                            <span>⏱️</span> {t('myListings.preHarvest', 'Pre-Harvest Advance Order')}
                          </span>
                          <span className="bg-emerald-700 text-white text-[10px] font-black px-2.5 py-0.5 rounded-full shadow-xs">
                            {item.discount_pct > 0 ? `${item.discount_pct}% OFF` : t('myListings.spotRate', 'Spot Rate')}
                          </span>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs bg-white/90 p-2.5 rounded-lg border border-emerald-100">
                          <div>
                            <span className="text-[10px] text-gray-500 font-semibold block uppercase">{t('myListings.remainingLeadTime', 'Remaining Lead Time')}</span>
                            <span className="text-xs font-black text-emerald-900 flex items-center gap-1 mt-0.5">
                              ⏳ {item.remaining_advance_days ?? item.advance_days} {t('myListings.daysLeft', 'Days Left')}
                            </span>
                            <span className="text-[9px] text-gray-400">
                              ({item.elapsed_days || 0}d {t('myListings.passedOf', 'passed of')} {item.initial_advance_days || item.advance_days}d)
                            </span>
                          </div>
                          <div>
                            <span className="text-[10px] text-gray-500 font-semibold block uppercase">{t('myListings.advanceRate', 'Advance Buyer Rate')}</span>
                            <span className="text-sm font-black text-emerald-700 block">
                              ₹{item.discounted_price || Math.round(item.expected_price * (1 - (item.discount_pct || 0) / 100))} <span className="text-[10px] font-normal text-gray-500">/ {t('units.quintal', 'Qtl')}</span>
                            </span>
                            {item.discount_pct > 0 && (
                              <span className="text-[9px] text-emerald-600 font-bold">
                                {t('myListings.save', 'Save')} ₹{Math.round(item.expected_price - (item.discounted_price || item.expected_price * (1 - (item.discount_pct || 0) / 100)))} / {t('units.quintal', 'Qtl')}
                              </span>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center justify-between text-[10px] text-emerald-800 font-semibold pt-1 border-t border-emerald-200/60">
                          <span>🏷️ {item.tier_label || ((item.remaining_advance_days ?? item.advance_days) >= 10 ? '🌟 Super Early Bird' : (item.remaining_advance_days ?? item.advance_days) >= 5 ? '⚡ Standard Early Bird' : (item.remaining_advance_days ?? item.advance_days) >= 3 ? '⏱️ Advance Saver' : t('myListings.spotRate', 'Spot Rate'))}</span>
                          <span className="text-gray-400 font-normal">Auto-decays over time</span>
                        </div>
                      </div>
                    ) : (
                      <div className="mt-3 bg-gray-50 border border-gray-200 rounded-xl p-2.5 flex items-center justify-between text-xs text-gray-500">
                        <span>🛒 {t('myListings.spotRate', 'Spot Market Delivery')}</span>
                        <span className="font-semibold text-gray-700">0% Discount</span>
                      </div>
                    )}

                    {/* 🚚 Confirmed Order Delivery Timeline (Only visible when order is confirmed, individual for every order) */}
                    {itemConfirmedDeals.length > 0 && (
                      <div className="space-y-3">
                        {itemConfirmedDeals.map((deal) => (
                          <CropListingOrderTimeline
                            key={deal.deal_id || deal.id || deal.order_number}
                            deal={deal}
                            onStatusUpdated={() => {
                              fetchFarmerRequests()
                              fetchUserDeals()
                              fetchMyListings()
                              showToast(t('toasts.orderStatusUpdated', '✅ Order delivery status updated!'))
                            }}
                            onOpenRateBuyer={handleOpenRateBuyer}
                            onDownloadInvoice={handleDownloadInvoice}
                          />
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="mt-5 pt-3 border-t border-gray-100 flex items-center gap-2">
                    <button
                      onClick={() => { setSelectedListing(item); setShowEditModal(true) }}
                      className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold py-2 rounded-xl text-xs transition-all cursor-pointer"
                    >
                      ✏️ {t('myListings.editListing', 'Edit')}
                    </button>
                    {item.status !== 'SOLD' && (
                      <button
                        onClick={() => handleMarkAsSold(item)}
                        className="flex-1 bg-amber-50 hover:bg-amber-100 text-amber-800 font-bold py-2 rounded-xl text-xs transition-all cursor-pointer"
                      >
                        🏷️ {t('myListings.markSold', 'Mark Sold')}
                      </button>
                    )}
                    <button
                      onClick={() => handleDeleteListing(item.id)}
                      className="px-3 bg-red-50 hover:bg-red-100 text-red-700 font-bold py-2 rounded-xl text-xs transition-all cursor-pointer"
                      title={t('myListings.deleteListing', 'Delete')}
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              )})}
            </div>
          )}
        </div>
      )}

      {/* TAB 2: BUYER PURCHASE REQUESTS */}
      {activeTab === 'requests' && (
        <div className="space-y-6">
          {requests.length === 0 ? (
            <div className="bg-white p-8 rounded-xl text-center text-gray-500 border space-y-2">
              <p className="font-bold text-gray-700">{t('myListings.noRequests', 'No purchase requests received yet')}</p>
              <p className="text-xs text-gray-400">{t('myListings.noRequestsDesc', 'When verified buyers submit purchase requests for your crops, they will appear here with direct WhatsApp contact buttons.')}</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                  <span>📩</span> {t('myListings.buyerRequests', 'Buyer Purchase Requests')} ({requests.length})
                </h2>
                <span className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full font-bold">
                  {t('myListings.directWhatsApp', 'Direct WhatsApp Connections')}
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {requests.map((req) => (
                  <div key={req.id} className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm space-y-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-bold text-gray-900 text-base flex items-center gap-2">
                          <span>🏢</span> {req.buyer_name}
                        </h4>
                        <p className="text-xs text-gray-500">📍 {t('common.location', 'District')}: <b>{translateMandi ? translateMandi(req.buyer_district || 'Nashik') : (req.buyer_district || 'Nashik')}</b> • {t('common.crop', 'Crop')}: <b>{translateCrop ? translateCrop(req.crop) : (t('crops.' + (req.crop || '').toLowerCase(), req.crop))}</b></p>
                      </div>
                      <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                        req.status?.toLowerCase() === 'accepted'
                          ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                          : req.status?.toLowerCase() === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {translateStatus(req.status)}
                      </span>
                    </div>

                    <div className="grid grid-cols-3 gap-2 bg-emerald-50/50 p-3 rounded-xl border border-emerald-100 text-xs">
                      <div>
                        <span className="text-gray-500 block">{t('myListings.offeredPrice', 'Offered Price')}</span>
                        <span className="font-bold text-emerald-700">₹{req.offered_price} / {t('units.quintal', 'Qtl')}</span>
                      </div>
                      <div>
                        <span className="text-gray-500 block">{t('common.quantity', 'Quantity')}</span>
                        <span className="font-bold text-gray-800">{req.quantity} {t('units.quintal', 'Quintals')}</span>
                      </div>
                      <div>
                        <span className="text-gray-500 block">{t('common.total', 'Total Value')}</span>
                        <span className="font-bold text-emerald-800">₹{(req.quantity * req.offered_price).toLocaleString()}</span>
                      </div>
                    </div>

                    {req.message && (
                      <div className="bg-gray-50 p-2.5 rounded-lg border text-xs text-gray-700">
                        <b>{t('common.details', 'Message')}:</b> "{req.message}"
                      </div>
                    )}

                    <div className="pt-2 border-t border-gray-100 flex items-center justify-between gap-2">
                      {req.status?.toLowerCase() === 'pending' ? (
                        <>
                          <button
                            onClick={() => handleAcceptRequest(req.id)}
                            className="flex-1 bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                          >
                            ✅ {t('myListings.acceptOffer', 'Accept Offer')}
                          </button>
                          <button
                            onClick={() => handleRejectRequest(req.id)}
                            className="px-4 bg-red-50 hover:bg-red-100 text-red-700 font-bold py-2 rounded-xl text-xs transition-all cursor-pointer"
                          >
                            ❌ {t('myListings.declineOffer', 'Decline Offer')}
                          </button>
                        </>
                      ) : req.status?.toLowerCase() === 'accepted' ? (
                        <div className="flex items-center justify-between w-full">
                          <span className="text-xs text-emerald-700 font-bold flex items-center gap-1">
                            ✅ {t('status.accepted', 'Accepted')} • {t('myListings.confirmedLogistics', 'Delivery tracked in Crop Listings')}
                          </span>
                          {req.whatsapp_url && (
                            <a
                              href={req.whatsapp_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-xs font-bold text-emerald-800 bg-emerald-100 hover:bg-emerald-200 px-3 py-1.5 rounded-xl transition-all"
                            >
                              <span>💬</span> {t('orders.whatsAppBuyer', 'WhatsApp Buyer')}
                            </a>
                          )}
                        </div>
                      ) : (
                        <span className="text-xs text-gray-400 italic">{t('status.rejected', 'Request Declined')}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Create Listing Modal */}
      {showListingModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleCreateListing} className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">🌾 {t('myListings.modalPublishTitle', 'Publish New Crop Listing')}</h3>
              <button type="button" onClick={() => setShowListingModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.cropName', 'Crop Name')} *</label>
                <input
                  type="text"
                  value={newListing.crop}
                  onChange={e => setNewListing({ ...newListing, crop: e.target.value })}
                  placeholder="e.g. Wheat, Onion, Tomato"
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.quantityQuintals', 'Quantity (Quintals)')} *</label>
                  <input
                    type="number"
                    step="0.1"
                    value={newListing.quantity}
                    onChange={e => setNewListing({ ...newListing, quantity: e.target.value })}
                    placeholder="100"
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.expectedPriceQtl', 'Expected Price (₹/Qtl)')} *</label>
                  <input
                    type="number"
                    step="0.1"
                    value={newListing.expected_price}
                    onChange={e => setNewListing({ ...newListing, expected_price: e.target.value })}
                    placeholder="2350"
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.qualityGrade', 'Quality Grade')}</label>
                  <select
                    value={newListing.quality_grade}
                    onChange={e => setNewListing({ ...newListing, quality_grade: e.target.value })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="Grade A">Grade A</option>
                    <option value="Grade B">Grade B</option>
                    <option value="Grade C">Grade C</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.mandiFarmLocation', 'Location / Mandi')}</label>
                  <input
                    type="text"
                    value={newListing.location}
                    onChange={e => setNewListing({ ...newListing, location: e.target.value })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              {/* ⏱️ Farmer Advance Booking & Time-Based Demand Option */}
              <div className="bg-emerald-50/80 p-3.5 rounded-xl border border-emerald-200">
                <label className="text-xs font-bold text-emerald-900 block mb-1 flex items-center justify-between">
                  <span>⏱️ {t('myListings.preHarvest', 'Pre-Harvest Advance Order Discount')}</span>
                  <span className="text-[10px] text-emerald-700 font-normal">Farmer Lead-Time Incentive</span>
                </label>
                <div className="grid grid-cols-2 gap-3 mt-1.5">
                  <div>
                    <label className="text-[11px] font-semibold text-gray-700 block mb-0.5">{t('myListings.harvestLeadTime', 'Pre-Order Lead Time (Days)')}</label>
                    <input
                      type="number"
                      value={newListing.advance_days || ''}
                      onChange={e => setNewListing({ ...newListing, advance_days: e.target.value })}
                      placeholder="e.g. 10 Days"
                      className="w-full px-3 py-2 border rounded-lg text-xs outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-semibold text-gray-700 block mb-0.5">{t('myListings.spotRate', 'Auto Discount Tier')}</label>
                    <input
                      type="text"
                      value={(parseInt(newListing.advance_days) || 0) >= 10 ? '10% OFF (Super Early)' : (parseInt(newListing.advance_days) || 0) >= 5 ? '5% OFF (Standard)' : (parseInt(newListing.advance_days) || 0) >= 3 ? '2% OFF (Saver)' : '0% OFF (Spot)'}
                      disabled
                      className="w-full px-3 py-2 border rounded-lg text-xs outline-none bg-gray-100 font-bold text-emerald-700"
                    />
                  </div>
                </div>
                {(parseInt(newListing.advance_days) || 0) > 0 && (parseFloat(newListing.expected_price) || 0) > 0 && (
                  <p className="text-[11px] text-emerald-800 font-semibold mt-2">
                    ✨ Buyers placing orders {newListing.advance_days} days before harvest get discounted rate of ₹{Math.round(parseFloat(newListing.expected_price) * (1 - ((parseInt(newListing.advance_days) || 0) >= 10 ? 0.10 : (parseInt(newListing.advance_days) || 0) >= 5 ? 0.05 : 0.02)))}/Qtl!
                  </p>
                )}
              </div>
            </div>

            {/* AI SMART PRICE RECOMMENDATION CARD */}
            {newListing.crop && newListing.crop.trim() !== '' && (
              <AIPriceRecommendationCard
                crop={newListing.crop}
                district={newListing.location || user?.district || 'Nashik'}
                quantity={newListing.quantity || 100}
                qualityGrade={newListing.quality_grade || 'Grade A'}
                role="farmer"
                userPrice={newListing.expected_price}
                onUseAiPrice={(recPrice) => setNewListing(prev => ({ ...prev, expected_price: recPrice }))}
              />
            )}

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowListingModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('common.cancel', 'Cancel')}</button>
              <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {submitting ? t('common.submitting', 'Publishing...') : `${t('myListings.publishBtn', 'Publish Listing')} →`}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Edit Listing Modal */}
      {showEditModal && selectedListing && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleUpdateListing} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">✏️ {t('myListings.modalEditTitle', 'Edit Crop Listing')}</h3>
              <button type="button" onClick={() => setShowEditModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.cropName', 'Crop Name')} *</label>
                <input
                  type="text"
                  value={selectedListing.crop}
                  onChange={e => setSelectedListing({ ...selectedListing, crop: e.target.value })}
                  className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.quantityQuintals', 'Quantity (Quintals)')}</label>
                  <input
                    type="number"
                    step="0.1"
                    value={selectedListing.quantity}
                    onChange={e => setSelectedListing({ ...selectedListing, quantity: e.target.value })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">{t('myListings.expectedPriceQtl', 'Expected Price (₹/Qtl)')}</label>
                  <input
                    type="number"
                    step="0.1"
                    value={selectedListing.expected_price}
                    onChange={e => setSelectedListing({ ...selectedListing, expected_price: e.target.value })}
                    className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
              </div>

              {/* Edit Advance Order Days */}
              <div className="bg-emerald-50/80 p-3 rounded-xl border border-emerald-200">
                <label className="text-xs font-bold text-emerald-900 block mb-1">
                  ⏱️ {t('myListings.harvestLeadTime', 'Pre-Harvest Advance Order Lead Time (Days)')}
                </label>
                <div className="grid grid-cols-2 gap-3 mt-1">
                  <div>
                    <input
                      type="number"
                      value={selectedListing.advance_days || ''}
                      onChange={e => setSelectedListing({ ...selectedListing, advance_days: e.target.value })}
                      placeholder="e.g. 10 Days"
                      className="w-full px-3 py-2 border rounded-lg text-xs outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
                    />
                  </div>
                  <div>
                    <input
                      type="text"
                      value={(parseInt(selectedListing.advance_days) || 0) >= 10 ? '10% OFF (Super Early)' : (parseInt(selectedListing.advance_days) || 0) >= 5 ? '5% OFF (Standard)' : (parseInt(selectedListing.advance_days) || 0) >= 3 ? '2% OFF (Saver)' : '0% OFF (Spot Rate)'}
                      disabled
                      className="w-full px-3 py-2 border rounded-lg text-xs outline-none bg-gray-100 font-bold text-emerald-700"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowEditModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('common.cancel', 'Cancel')}</button>
              <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {submitting ? t('common.submitting', 'Updating...') : `${t('myListings.updateBtn', 'Save Changes')} →`}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ⭐ Rate Buyer Modal */}
      {showRateModal && ratingTarget && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSubmitRating} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>⭐</span> {t('myListings.rateBuyerTitle', 'Rate & Review Buyer')}
              </h3>
              <button type="button" onClick={() => setShowRateModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            {/* Buyer Details */}
            <div className="bg-amber-50/80 p-3.5 rounded-xl border border-amber-200">
              <h4 className="font-bold text-amber-950 text-sm flex items-center gap-1.5">
                <span>🏢</span> {ratingTarget.buyer_name || ratingTarget.name || t('myListings.buyer', 'Buyer')}
              </h4>
              <p className="text-xs text-amber-800 mt-0.5">
                {t('profile.district', 'District')}: <b>{translateMandi ? translateMandi(ratingTarget.buyer_district || ratingTarget.district || 'Maharashtra') : (ratingTarget.buyer_district || ratingTarget.district || 'Maharashtra')}</b>
              </p>
            </div>

            {/* Interactive Star Rating Selector */}
            <div>
              <label className="text-xs font-bold text-gray-700 block mb-2">
                {t('myListings.rateExperience', 'Overall Deal Experience (1 to 5 Stars)')} *
              </label>
              <div className="flex items-center gap-2 justify-center py-2 bg-gray-50 rounded-xl border border-gray-200">
                {[1, 2, 3, 4, 5].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setStars(num)}
                    className="text-3xl transition-transform hover:scale-125 focus:outline-none cursor-pointer"
                  >
                    {num <= stars ? '⭐' : '☆'}
                  </button>
                ))}
              </div>
            </div>

            {/* Quick Experience Tags */}
            <div>
              <label className="text-xs font-bold text-gray-700 block mb-1.5">
                {t('myListings.quickTags', 'Quick Deal Highlights')}
              </label>
              <div className="flex flex-wrap gap-1.5">
                {[
                  t('myListings.promptFullPayment', 'Prompt Full Payment'),
                  t('myListings.fairMandiWeighing', 'Fair Mandi Weighing'),
                  t('myListings.timelyPickup', 'Timely Logistics Pickup'),
                  t('myListings.politeCommunication', 'Polite Communication')
                ].map((tag) => (
                  <button
                    key={tag}
                    type="button"
                    onClick={() => handleToggleTag(tag)}
                    className={`text-xs px-2.5 py-1 rounded-full border transition-all cursor-pointer font-medium ${
                      selectedTags.includes(tag)
                        ? 'bg-emerald-700 text-white border-emerald-700 shadow-xs'
                        : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100'
                    }`}
                  >
                    {selectedTags.includes(tag) ? '✓ ' : '+ '}{tag}
                  </button>
                ))}
              </div>
            </div>

            {/* Detailed Comment */}
            <div>
              <label className="text-xs font-bold text-gray-700 block mb-1">
                {t('myListings.additionalComments', 'Additional Comments / Farmer Review (Optional)')}
              </label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="e.g., Buyer made full payment via RTGS on the day of dispatch. Very fair APMC weighing."
                className="w-full px-3.5 py-2.5 border rounded-xl text-xs outline-none focus:ring-2 focus:ring-emerald-500 h-20 resize-none"
              />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowRateModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('common.cancel', 'Cancel')}</button>
              <button type="submit" disabled={ratingSubmitting} className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer shadow-sm">
                {ratingSubmitting ? t('common.submitting', 'Submitting...') : `${t('myListings.submitRating', 'Submit Rating')} ⭐`}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

export default MyCropListings
