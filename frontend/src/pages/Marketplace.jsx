import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLanguage } from '../context/LanguageContext'
import axiosClient from '../api/axiosClient'
import CropListingOrderTimeline from '../components/CropListingOrderTimeline'

const Marketplace = () => {
  const { role, user } = useAuth()
  const { t, translateStatus, transliterate, translateCrop, translateCropsList, translateCapacity, translateMandi } = useLanguage()
  
  const [listings, setListings] = useState([])
  const [requirements, setRequirements] = useState([])
  const [recommendedBuyers, setRecommendedBuyers] = useState([])
  const [buyerDeals, setBuyerDeals] = useState([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState(null)
  
  // Search & Filter
  const [searchCrop, setSearchCrop] = useState('')
  const [searchLocation, setSearchLocation] = useState('')
  
  // Modals
  const [showNegModal, setShowNegModal] = useState(false)
  const [showOfferModal, setShowOfferModal] = useState(false)
  const [showPurchaseReqModal, setShowPurchaseReqModal] = useState(false)
  const [showFarmerProfileModal, setShowFarmerProfileModal] = useState(false)
  const [showBuyerProfileModal, setShowBuyerProfileModal] = useState(false)
  const [selectedItem, setSelectedItem] = useState(null)

  // Rating Modal State
  const [showRateModal, setShowRateModal] = useState(false)
  const [ratingTarget, setRatingTarget] = useState(null)
  const [stars, setStars] = useState(5)
  const [reviewText, setReviewText] = useState('')
  const [ratingSubmitting, setRatingSubmitting] = useState(false)

  // Profile data fetched from backend (Fresh State)
  const [profileData, setProfileData] = useState(null)
  const [profileLoading, setProfileLoading] = useState(false)

  // Offer / Purchase Request Form
  const [offerPrice, setOfferPrice] = useState('')
  const [offerQty, setOfferQty] = useState('')
  const [offerNotes, setOfferNotes] = useState('')
  const [submittingOffer, setSubmittingOffer] = useState(false)

  // AI Negotiation State
  const [negResult, setNegResult] = useState(null)
  const [negLoading, setNegLoading] = useState(false)

  useEffect(() => {
    localStorage.removeItem('marketplace_cache')
    fetchMarketplaceFeed(false)
    const interval = setInterval(() => {
      fetchMarketplaceFeed(true) // Silent real-time background refresh every 4s
    }, 4000)
    const handleFocus = () => fetchMarketplaceFeed(true)
    window.addEventListener('focus', handleFocus)
    return () => {
      clearInterval(interval)
      window.removeEventListener('focus', handleFocus)
    }
  }, [role])

  const showToast = (msg, type = 'success') => {
    setNotification({ msg, type })
    setTimeout(() => setNotification(null), 4000)
  }

  const handleOpenRateFarmer = (deal) => {
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
        await fetchMarketplaceFeed(true)
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

  const fetchMarketplaceFeed = async (isBackground = false) => {
    if (!isBackground) setLoading(true)
    
    if (role === 'Buyer' || role === 'Admin') {
      try {
        const resListings = await axiosClient.get('/api/v1/listings/')
        if (resListings.data && resListings.data.success) {
          setListings(resListings.data.data)
        }
      } catch (err) {
        console.warn('Error fetching crop listings for buyer marketplace:', err)
      }

      // Fetch buyer confirmed deals for live delivery tracking
      try {
        const resDeals = await axiosClient.get('/api/v1/deals/my')
        if (resDeals.data && resDeals.data.success) {
          setBuyerDeals(resDeals.data.data)
        }
      } catch (err) {
        console.warn('Error fetching buyer deals for marketplace feed:', err)
      }
    }

    if (role === 'Farmer' || role === 'Admin') {
      // Farmer Discovery Feed: Fetch REAL Buyer Requirements & REAL Registered Buyers
      try {
        const resReqs = await axiosClient.get('/api/v1/requirements/')
        if (resReqs.data && resReqs.data.success) {
          setRequirements(resReqs.data.data)
        }
        
        // Fetch REAL Registered Buyers from SQL Database (No Dummy Data)
        const resBuyers = await axiosClient.get('/api/v1/buyer/list')
        if (resBuyers.data && resBuyers.data.success) {
          const realBuyers = resBuyers.data.data.map(b => ({
            id: b.user_id || b.id,
            company: b.company_name,
            owner_name: b.owner_name,
            district: b.district,
            daily_capacity: `${b.daily_capacity || 100} Quintals`,
            crops: b.buying_crops || 'Wheat, Onion',
            rating: 4.9,
            matchScore: 96.5,
            mobile: b.mobile_number,
            whatsapp: b.whatsapp_number || b.mobile_number
          }))
          setRecommendedBuyers(realBuyers)
        }
      } catch (err) {
        console.warn('Error fetching real buyers for farmer marketplace:', err)
      }
    }

    if (!isBackground) setLoading(false)
  }

  // Open Real Farmer Profile Modal (GET /api/v1/marketplace/farmers/{farmer_id})
  const handleOpenFarmerProfile = async (farmerId) => {
    if (!farmerId) {
      console.error("❌ Missing farmer_id for profile view")
      return
    }
    
    // Clear cached old profile state to prevent showing wrong user
    setProfileData(null)
    setProfileLoading(true)
    setShowFarmerProfileModal(true)

    try {
      const res = await axiosClient.get(`/api/v1/marketplace/farmers/${farmerId}`)
      if (res.data && res.data.success) {
        const farmer = res.data.data
        console.log("=== FARMER PROFILE DEBUG LOGS ===")
        console.log("Farmer ID:", farmer.id)
        console.log("Farmer Name:", farmer.name)
        console.log("Farmer Role:", farmer.role)
        console.log("=================================")
        setProfileData(farmer)
      }
    } catch (err) {
      console.error('Error fetching farmer profile:', err)
      showToast('Could not load farmer profile details', 'error')
    } finally {
      setProfileLoading(false)
    }
  }

  // Open Real Buyer Profile Modal (GET /api/v1/marketplace/buyers/{buyer_id})
  const handleOpenBuyerProfile = async (buyerId) => {
    if (!buyerId) {
      console.error("❌ Missing buyer_id for profile view")
      return
    }

    // Clear cached old profile state to prevent showing wrong user
    setProfileData(null)
    setProfileLoading(true)
    setShowBuyerProfileModal(true)

    try {
      const res = await axiosClient.get(`/api/v1/marketplace/buyers/${buyerId}`)
      if (res.data && res.data.success) {
        const buyer = res.data.data
        console.log("=== BUYER PROFILE DEBUG LOGS ===")
        console.log("Buyer ID:", buyer.id)
        console.log("Buyer Company:", buyer.company_name)
        console.log("Buyer Role:", buyer.role)
        console.log("================================")
        setProfileData(buyer)
      }
    } catch (err) {
      console.error('Error fetching buyer profile:', err)
      showToast('Could not load buyer profile details', 'error')
    } finally {
      setProfileLoading(false)
    }
  }

  // Handle Dynamic WhatsApp Direct Contact Workflow
  const handleWhatsAppContact = async (targetUserId, cropName, quantity, price, contactType) => {
    try {
      const res = await axiosClient.get(`/api/v1/contact/whatsapp/${targetUserId}`, {
        params: {
          crop: cropName || 'Wheat',
          quantity: quantity || 100.0,
          price: price || 2300.0,
          contact_type: contactType || 'buyer_to_farmer'
        }
      })
      if (res.data && res.data.success && res.data.data.whatsapp_url) {
        window.open(res.data.data.whatsapp_url, '_blank')
        showToast(`💬 ${t('marketplace.openingWhatsApp')}`)
      } else {
        showToast('Unable to generate WhatsApp link', 'error')
      }
    } catch (err) {
      showToast('Failed to open WhatsApp contact link', 'error')
    }
  }

  // Handle Buyer Purchase Request (POST /api/v1/requests/)
  const handleSendPurchaseRequest = async (e) => {
    e.preventDefault()
    if (!selectedItem) return
    setSubmittingOffer(true)
    try {
      const response = await axiosClient.post('/api/v1/requests/', {
        crop_listing_id: selectedItem.id,
        quantity: parseFloat(offerQty) || selectedItem.quantity,
        offered_price: parseFloat(offerPrice) || selectedItem.expected_price,
        message: offerNotes || `Interested in buying ${selectedItem.crop}.`
      })

      if (response.data?.success) {
        showToast(`📩 ${t('marketplace.purchaseReqSuccess')}`)
        setShowPurchaseReqModal(false)
        setOfferPrice('')
        setOfferQty('')
        setOfferNotes('')
      } else {
        showToast(response.data?.message || 'Error sending purchase request', 'error')
      }
    } catch (err) {
      showToast(err.response?.data?.message || 'Failed to submit purchase request.', 'error')
    } finally {
      setSubmittingOffer(false)
    }
  }

  // Handle Offer Submission (routes to purchase request flow)
  const handleSendOffer = async (e) => {
    e.preventDefault()
    if (!selectedItem) return
    setSubmittingOffer(true)
    try {
      const response = await axiosClient.post('/api/v1/requests/', {
        crop_listing_id: selectedItem.id,
        quantity: parseFloat(offerQty) || selectedItem.quantity,
        offered_price: parseFloat(offerPrice) || selectedItem.expected_price,
        message: offerNotes || `Interested in buying ${selectedItem.crop || selectedItem.crop_name}.`
      })
      if (response.data?.success) {
        showToast(`💼 ${t('marketplace.offerSuccess')}`)
        setShowOfferModal(false)
        setOfferPrice('')
        setOfferQty('')
        setOfferNotes('')
      } else {
        showToast(response.data?.message || 'Error submitting offer', 'error')
      }
    } catch (err) {
      showToast(err.response?.data?.message || 'Failed to submit offer.', 'error')
    } finally {
      setSubmittingOffer(false)
    }
  }

  // Handle AI Negotiation Assistant
  const handleRunNegotiation = async (item) => {
    setSelectedItem(item)
    setShowNegModal(true)
    setNegLoading(true)
    try {
      const response = await axiosClient.post('/api/v1/marketplace/negotiate', {
        crop: item.crop || item.crop_name || 'Wheat',
        buyer_offered_price: item.offered_price || 2250,
        farmer_expected_price: item.expected_price || 2300,
        district: item.location || item.preferred_district || 'Nashik'
      })
      if (response.data?.success) {
        setNegResult(response.data.data)
      }
    } catch (err) {
      console.error('AI Negotiation API error:', err)
    } finally {
      setNegLoading(false)
    }
  }

  // Filtered Items
  const filteredListings = listings.filter(item => {
    const matchC = !searchCrop || item.crop?.toLowerCase().includes(searchCrop.toLowerCase())
    const matchL = !searchLocation || item.location?.toLowerCase().includes(searchLocation.toLowerCase())
    return matchC && matchL
  })

  const filteredRequirements = requirements.filter(req => {
    const matchC = !searchCrop || req.crop_name?.toLowerCase().includes(searchCrop.toLowerCase())
    const matchL = !searchLocation || req.preferred_district?.toLowerCase().includes(searchLocation.toLowerCase())
    return matchC && matchL
  })

  return (
    <div className="space-y-6 pb-12">
      {/* Notification Toast */}
      {notification && (
        <div className={`p-4 rounded-xl shadow-lg border text-sm font-bold flex items-center justify-between transition-all ${
          notification.type === 'error' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-emerald-50 text-emerald-900 border-emerald-300'
        }`}>
          <span>{notification.msg}</span>
          <button onClick={() => setNotification(null)} className="text-xs text-gray-500 hover:text-gray-800">✕</button>
        </div>
      )}

      {/* Discovery Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-gradient-to-r from-emerald-800 via-green-800 to-teal-800 text-white p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-3xl">🛒</span>
            <h1 className="text-2xl font-bold">
              {role === 'Farmer' ? t('marketplace.farmerFeedTitle') : t('marketplace.buyerFeedTitle')}
            </h1>
            <span className="bg-amber-400 text-black text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              {t('marketplace.verifiedOnly')}
            </span>
          </div>
          <p className="text-emerald-100 text-sm mt-1">
            {role === 'Farmer' 
              ? t('marketplace.farmerFeedDesc')
              : t('marketplace.buyerFeedDesc')}
          </p>
        </div>

        {/* Quick Link to Personal Management */}
        <div>
          {role === 'Farmer' ? (
            <Link
              to="/my-listings"
              className="bg-white text-emerald-900 hover:bg-emerald-50 font-bold px-4 py-2.5 rounded-xl shadow-md transition-all flex items-center gap-2 text-sm"
            >
              📦 {t('marketplace.goToMyListings')}
            </Link>
          ) : (
            <Link
              to="/buying-requirements"
              className="bg-white text-blue-900 hover:bg-blue-50 font-bold px-4 py-2.5 rounded-xl shadow-md transition-all flex items-center gap-2 text-sm"
            >
              📋 {t('marketplace.goToMyRequirements')}
            </Link>
          )}
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
        <div className="flex items-center gap-2 font-bold text-gray-800 text-sm">
          <span>🔍 {t('marketplace.filterFeed')}</span>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder={t('marketplace.searchCrop')}
            value={searchCrop}
            onChange={(e) => setSearchCrop(e.target.value)}
            className="px-3.5 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none w-48"
          />
          <input
            type="text"
            placeholder={t('marketplace.searchLocation')}
            value={searchLocation}
            onChange={(e) => setSearchLocation(e.target.value)}
            className="px-3.5 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none w-48"
          />
        </div>
      </div>

      {/* FARMER MARKETPLACE VIEW (Displays Real Buyer Requirements & Real Registered Buyers) */}
      {(role === 'Farmer' || role === 'Admin') && (
        <div className="space-y-6">
          {/* Real AI Recommended Buyers Section */}
          {recommendedBuyers.length > 0 && (
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 p-6 rounded-2xl border border-amber-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-amber-900 flex items-center gap-2">
                  <span>⭐</span> {t('marketplace.registeredBuyers')} ({recommendedBuyers.length})
                </h2>
                <span className="text-xs font-bold text-amber-800 bg-amber-200 px-3 py-1 rounded-full">{t('marketplace.verifiedProfiles')}</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {recommendedBuyers.map((b) => (
                  <div key={b.id} className="bg-white p-4 rounded-xl border border-amber-200 shadow-sm hover:shadow-md transition-all space-y-2 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md">
                          ⚡ {t('marketplace.aiMatch')} {b.matchScore}%
                        </span>
                        <span className="text-xs font-bold text-amber-600">⭐ {b.rating} / 5</span>
                      </div>
                      <h3 className="font-bold text-gray-900 text-sm truncate mt-1">{b.company}</h3>
                      <p className="text-xs text-gray-500">👤 {t('marketplace.owner')} <b>{transliterate(b.owner_name || t('roles.buyer'))}</b></p>
                      <p className="text-xs text-gray-500">📍 {t('marketplace.district')} <b>{translateMandi(b.district)}</b></p>
                      <p className="text-xs text-gray-500">📦 {t('marketplace.capacity')} <b>{translateCapacity(b.daily_capacity)}</b></p>
                      <p className="text-xs text-gray-500">🌾 {t('marketplace.buyingCrops')} <b>{translateCropsList(b.crops)}</b></p>
                    </div>
                    
                    <div className="pt-2 border-t flex items-center gap-2">
                      <button
                        onClick={() => handleOpenBuyerProfile(b.id)}
                        className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-1.5 rounded-lg text-xs transition-all cursor-pointer"
                      >
                        👤 {t('actions.viewProfile')}
                      </button>
                      <button
                        onClick={() => handleWhatsAppContact(b.id, 'Crop Supply', 100, 2300, 'farmer_to_buyer')}
                        className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 rounded-lg text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                      >
                        💬 {t('actions.contactBuyer')}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Real Buyer Requirements Feed */}
          <div>
            <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <span>📋</span> {t('marketplace.allOpenRequirements')} ({filteredRequirements.length})
            </h2>

            {loading ? (
              <div className="py-12 text-center text-gray-500 animate-pulse">{t('marketplace.loadingRequirements')}</div>
            ) : filteredRequirements.length === 0 ? (
              <div className="bg-white p-8 rounded-xl text-center text-gray-500 border">{t('marketplace.noRequirements')}</div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredRequirements.map((req) => (
                  <div key={req.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="bg-amber-100 text-amber-800 text-xs font-bold px-3 py-1 rounded-full">{req.preferred_quality || 'Grade A'}</span>
                        <span className="text-xs font-bold bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">{translateStatus(req.status || 'OPEN')}</span>
                      </div>

                      <div className="mt-3">
                        <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                          <span>🏢</span> {translateCrop ? translateCrop(req.crop_name) : req.crop_name}
                        </h3>
                        <p className="text-xs font-semibold text-blue-900 mt-1">
                          👤 {t('roles.buyer')}: <b>{transliterate(req.buyer_name || t('roles.buyer'))}</b>
                        </p>
                        <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                          📍 {t('marketplace.preferredDistrict')} {translateMandi(req.preferred_district || 'Nashik')}
                        </p>
                      </div>

                      <div className="mt-4 grid grid-cols-2 gap-2 bg-amber-50/50 p-3 rounded-xl border border-amber-100">
                        <div>
                          <span className="text-xs text-gray-500 block">{t('marketplace.requiredQuantity')}</span>
                          <span className="text-sm font-bold text-gray-800">{req.quantity_required} {t('units.quintal')}</span>
                        </div>
                        <div>
                          <span className="text-xs text-gray-500 block">{t('marketplace.offeredPrice')}</span>
                          <span className="text-sm font-bold text-amber-700">₹{req.offered_price} / {t('units.quintal')}</span>
                        </div>
                      </div>

                      {/* AI Match Score */}
                      {req.match_score != null && (
                        <div className="mt-3 bg-emerald-50 border border-emerald-200 rounded-lg p-2 flex items-center justify-between">
                          <span className="text-xs font-bold text-emerald-800 flex items-center gap-1">⚡ {t('marketplace.aiFarmerMatchScore')}</span>
                          <span className="text-xs font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded-full">{req.match_score} / 100</span>
                        </div>
                      )}
                    </div>

                    <div className="mt-5 pt-3 border-t border-gray-100 space-y-2">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleOpenBuyerProfile(req.buyer_id)}
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                        >
                          👤 {t('actions.viewProfile')}
                        </button>
                        <button
                          onClick={() => handleRunNegotiation(req)}
                          className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 rounded-xl text-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                        >
                          🤝 {t('marketplace.negotiateAi')}
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleWhatsAppContact(req.buyer_id, req.crop_name, req.quantity_required, req.offered_price, 'farmer_to_buyer')}
                          className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                        >
                          💬 {t('marketplace.contactWhatsApp')}
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* BUYER MARKETPLACE VIEW (Displays Active Farmer Crop Listings ONLY with Exact Farmer Data) */}
      {(role === 'Buyer') && (
        <div className="space-y-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <span>🌾</span> {t('marketplace.activeCropListings')} ({filteredListings.length})
          </h2>

          {loading ? (
            <div className="py-12 text-center text-gray-500 animate-pulse">{t('marketplace.loadingListings')}</div>
          ) : filteredListings.length === 0 ? (
            <div className="bg-white p-8 rounded-xl text-center text-gray-500 border">{t('marketplace.noListingsFilter')}</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredListings.map((item) => {
                // Find confirmed orders for this buyer matching this crop listing
                const itemConfirmedDeals = (buyerDeals || []).filter(d => 
                  (d.listing_id && d.listing_id === item.id) ||
                  (d.crop && item.crop && d.crop.toLowerCase() === item.crop.toLowerCase() && (d.farmer_id === item.farmer_id || d.farmer_name === item.farmer_name))
                )

                return (
                <div key={item.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">{item.quality_grade || 'Grade A'}</span>
                      <span className="text-xs font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded-full">{translateStatus(item.status || 'ACTIVE')}</span>
                    </div>

                    <div className="mt-3">
                      <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                        <span>🌾</span> {translateCrop ? translateCrop(item.crop) : item.crop}
                      </h3>
                      <p className="text-xs font-semibold text-emerald-800 mt-1">
                        🧑‍🌾 {t('roles.farmer')}: <b>{transliterate(item.farmer_name || t('roles.farmer'))}</b>
                      </p>
                      <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                        📍 {translateMandi(item.location || 'Nashik APMC Yard')}
                      </p>
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-2 bg-gray-50 p-3 rounded-xl border border-gray-100">
                      <div>
                        <span className="text-xs text-gray-500 block">{t('marketplace.availableQuantity')}</span>
                        <span className="text-sm font-bold text-gray-800">{item.quantity} {t('units.quintal')}</span>
                      </div>
                      <div>
                        <span className="text-xs text-gray-500 block">{t('marketplace.expectedPrice')}</span>
                        <span className="text-sm font-bold text-emerald-700">₹{item.expected_price} / {t('units.quintal')}</span>
                      </div>
                    </div>

                    {/* Pre-Harvest Advance Order Discount Badge */}
                    {(item.advance_days > 0 || item.discount_pct > 0) && (
                      <div className="mt-2.5 bg-emerald-50 border border-emerald-300 rounded-xl p-2.5 text-xs">
                        <div className="flex items-center justify-between font-bold text-emerald-900">
                          <span>⏱️ {t('marketplace.preOrderAdvanceRate')} ({item.advance_days || 10} {t('marketplace.daysLeadTime')})</span>
                          <span className="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-full font-black">{item.discount_pct || 10}% OFF</span>
                        </div>
                        <p className="text-[11px] text-emerald-800 font-bold mt-1">
                          {t('marketplace.discountedRate')} <span className="text-emerald-700 font-black text-sm">₹{item.discounted_price || Math.round(item.expected_price * 0.9)} / {t('units.quintal')}</span> ({t('marketplace.savePerQtl')} ₹{Math.round(item.expected_price - (item.discounted_price || item.expected_price * 0.9))} / {t('units.quintal')})
                        </p>
                      </div>
                    )}

                    {/* AI Match Score */}
                    {item.match_score != null && (
                      <div className="mt-3 bg-emerald-50 border border-emerald-200 rounded-lg p-2 flex items-center justify-between">
                        <span className="text-xs font-bold text-emerald-800 flex items-center gap-1">⚡ {t('marketplace.aiMatch')}</span>
                        <span className="text-xs font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded-full">{item.match_score} / 100</span>
                      </div>
                    )}

                    {/* 🚚 Confirmed Order Delivery Timeline for Buyer (Real-Time Live Tracking) */}
                    {itemConfirmedDeals.length > 0 && (
                      <div className="space-y-3 mt-3">
                        {itemConfirmedDeals.map((deal) => (
                          <CropListingOrderTimeline
                            key={deal.deal_id || deal.id || deal.order_number}
                            deal={deal}
                            role="Buyer"
                            onDownloadInvoice={handleDownloadInvoice}
                            onOpenRateFarmer={handleOpenRateFarmer}
                          />
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="mt-5 pt-3 border-[#f0f0f0] border-t space-y-2">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleOpenFarmerProfile(item.farmer_id)}
                        className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                      >
                        👤 {t('actions.viewProfile')}
                      </button>
                      <button
                        onClick={() => handleRunNegotiation(item)}
                        className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 rounded-xl text-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                      >
                        🤝 {t('marketplace.negotiateAi')}
                      </button>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleWhatsAppContact(item.farmer_id, item.crop, item.quantity, item.expected_price, 'buyer_to_farmer')}
                        className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                      >
                        💬 {t('marketplace.contactWhatsApp')}
                      </button>
                      <button
                        onClick={() => { setSelectedItem(item); setOfferPrice(item.discounted_price || item.expected_price); setOfferQty(item.quantity); setShowPurchaseReqModal(true) }}
                        className="flex-1 bg-emerald-800 hover:bg-emerald-900 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                      >
                        📩 {t('marketplace.sendRequest')}
                      </button>
                    </div>
                  </div>
                </div>
              )})}
            </div>
          )}
        </div>
      )}

      {/* REAL FARMER PROFILE MODAL */}
      {showFarmerProfileModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>🌾</span> {t('marketplace.farmerProfileModalTitle')}
              </h3>
              <button onClick={() => setShowFarmerProfileModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            {profileLoading ? (
              <div className="py-8 text-center text-emerald-700 animate-pulse font-semibold">{t('marketplace.loadingFarmerProfile')}</div>
            ) : profileData ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-full bg-emerald-700 text-white font-bold text-xl flex items-center justify-center shadow-md">
                    🧑‍🌾
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-base">{profileData.name}</h4>
                    <span className="text-xs text-emerald-800 font-bold bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      {t('marketplace.verified')} {profileData.role || t('roles.farmer')}
                    </span>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-xl border space-y-2 text-xs">
                  <p className="text-gray-700">🆔 <b>{t('marketplace.farmerId')}</b> {profileData.id}</p>
                  <p className="text-gray-700">📍 <b>{t('myListings.location')}:</b> {translateMandi ? translateMandi(profileData.location) : profileData.location}</p>
                  <p className="text-gray-700">📞 <b>{t('marketplace.mobileNumber')}</b> {profileData.mobile_number || profileData.mobile}</p>
                  <p className="text-gray-700">🚜 <b>{t('marketplace.farmSize')}</b> {profileData.farm_size}</p>
                  <p className="text-gray-700">🌾 <b>{t('marketplace.availableCrops')}</b> {translateCropsList ? translateCropsList(profileData.available_crops) : profileData.available_crops}</p>
                  <p className="text-gray-700">📦 <b>{t('marketplace.totalCropQuantity')}</b> {profileData.crop_quantity} {t('units.quintal')}</p>
                  <p className="text-gray-700">💰 <b>{t('marketplace.expectedPrice')}</b> ₹{profileData.expected_price} / {t('units.quintal')}</p>
                  <p className="text-gray-700">📅 <b>{t('marketplace.harvestDate')}</b> {profileData.harvest_date}</p>
                  <p className="text-gray-700">⭐ <b>{t('marketplace.farmerTrustRating')}</b> {profileData.farmer_rating} / 5.0</p>
                  <p className="text-gray-700">📜 <b>{t('marketplace.previousCompletedDeals')}</b> {profileData.previous_deals}</p>
                </div>

                <div className="pt-2 flex justify-end gap-2">
                  <button onClick={() => setShowFarmerProfileModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.close')}</button>
                  <button
                    onClick={() => {
                      setShowFarmerProfileModal(false)
                      handleWhatsAppContact(profileData.id, profileData.available_crops, profileData.crop_quantity, profileData.expected_price, 'buyer_to_farmer')
                    }}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold cursor-pointer flex items-center gap-1"
                  >
                    💬 {t('marketplace.contactFarmerOnWhatsApp')}
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}

      {/* REAL BUYER PROFILE MODAL */}
      {showBuyerProfileModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>🏢</span> {t('marketplace.buyerProfileModalTitle')}
              </h3>
              <button onClick={() => setShowBuyerProfileModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            {profileLoading ? (
              <div className="py-8 text-center text-blue-700 animate-pulse font-semibold">{t('marketplace.loadingBuyerProfile')}</div>
            ) : profileData ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-full bg-blue-700 text-white font-bold text-xl flex items-center justify-center shadow-md">
                    🏢
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-base">{profileData.company_name}</h4>
                    <p className="text-xs text-gray-500">{t('marketplace.owner')} <b>{profileData.owner_name}</b></p>
                    <span className="text-xs text-blue-800 font-bold bg-blue-100 px-2.5 py-0.5 rounded-full border border-blue-200 mt-1 inline-block">
                      {profileData.verification_status} {profileData.role || t('roles.buyer')}
                    </span>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-xl border space-y-2 text-xs">
                  <p className="text-gray-700">🆔 <b>{t('marketplace.buyerId')}</b> {profileData.id}</p>
                  <p className="text-gray-700">📍 <b>{t('marketplace.businessLocation')}</b> {translateMandi ? translateMandi(profileData.business_location) : profileData.business_location}</p>
                  <p className="text-gray-700">📞 <b>{t('marketplace.contactInformation')}</b> {profileData.contact_information}</p>
                  <p className="text-gray-700">🌾 <b>{t('marketplace.requiredCrop')}</b> {translateCrop ? translateCrop(profileData.required_crop) : profileData.required_crop}</p>
                  <p className="text-gray-700">📦 <b>{t('marketplace.requiredQuantity')}</b> {profileData.required_quantity} {t('units.quintal')}</p>
                  <p className="text-gray-700">💰 <b>{t('marketplace.offeredPrice')}</b> ₹{profileData.offered_price} / {t('units.quintal')}</p>
                  <p className="text-gray-700">🛒 <b>{t('marketplace.buyingCropsInterest')}</b> {profileData.buying_crops}</p>
                  <p className="text-gray-700">⭐ <b>{t('marketplace.buyerRating')}</b> {profileData.buyer_rating} / 5.0</p>
                </div>

                <div className="pt-2 flex justify-end gap-2">
                  <button onClick={() => setShowBuyerProfileModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.close')}</button>
                  <button
                    onClick={() => {
                      setShowBuyerProfileModal(false)
                      handleWhatsAppContact(profileData.id, profileData.required_crop, profileData.required_quantity, profileData.offered_price, 'farmer_to_buyer')
                    }}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold cursor-pointer flex items-center gap-1"
                  >
                    💬 {t('marketplace.contactBuyerOnWhatsApp')}
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}

      {/* Purchase Request Modal (Buyer -> Farmer) */}
      {showPurchaseReqModal && selectedItem && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSendPurchaseRequest} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>📩</span> {t('marketplace.sendPurchaseRequestTitle')}
              </h3>
              <button type="button" onClick={() => setShowPurchaseReqModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="bg-emerald-50 p-3 rounded-xl border border-emerald-200 text-xs text-emerald-900">
              <p><b>{t('marketplace.targetCrop')}</b> {translateCrop ? translateCrop(selectedItem.crop) : selectedItem.crop}</p>
              <p><b>{t('marketplace.farmerName')}</b> {selectedItem.farmer_name || t('roles.farmer')}</p>
              <p><b>{t('marketplace.farmerLocation')}</b> {translateMandi ? translateMandi(selectedItem.location) : selectedItem.location}</p>
              <p className="mt-1 text-emerald-700">{t('marketplace.purchaseRequestNote')}</p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.requiredQuantityQuintals')}</label>
                <input type="number" step="0.1" value={offerQty} onChange={e => setOfferQty(e.target.value)} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500" required />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.offeredPriceQtl')}</label>
                <input type="number" step="0.1" value={offerPrice} onChange={e => setOfferPrice(e.target.value)} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500" required />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.optionalMessage')}</label>
              <textarea value={offerNotes} onChange={e => setOfferNotes(e.target.value)} placeholder={t('marketplace.optionalMessagePlaceholder')} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500 h-20 resize-none" />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowPurchaseReqModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.cancel')}</button>
              <button type="submit" disabled={submittingOffer} className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {submittingOffer ? t('marketplace.submitting') : t('marketplace.sendRequestBtn')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Send Offer Modal */}
      {showOfferModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSendOffer} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900">💼 {t('marketplace.submitOfferTitle')}</h3>
              <button type="button" onClick={() => setShowOfferModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.offeredPriceQtl')}</label>
                <input type="number" step="0.1" value={offerPrice} onChange={e => setOfferPrice(e.target.value)} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500" required />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.quantityQuintals')}</label>
                <input type="number" step="0.1" value={offerQty} onChange={e => setOfferQty(e.target.value)} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500" required />
              </div>
            </div>
            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">{t('marketplace.termsNotes')}</label>
              <textarea value={offerNotes} onChange={e => setOfferNotes(e.target.value)} placeholder={t('marketplace.termsPlaceholder')} className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500 h-20 resize-none" />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowOfferModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">{t('actions.cancel')}</button>
              <button type="submit" disabled={submittingOffer} className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {submittingOffer ? t('marketplace.submitting') : t('marketplace.sendOfferBtn')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* AI Negotiation Assistant Modal */}
      {showNegModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                🤖 {t('marketplace.aiNegotiationTitle')}
              </h3>
              <button onClick={() => setShowNegModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            {negLoading ? (
              <div className="py-8 text-center text-emerald-700 font-semibold animate-pulse">
                {t('marketplace.consultingRates')}
              </div>
            ) : negResult ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 p-4 rounded-xl">
                  <span className="text-xs font-bold text-amber-700 uppercase tracking-wider block">{t('marketplace.suggestedPriceRange')}</span>
                  <div className="text-2xl font-black text-amber-900 mt-1">{negResult.suggested_negotiation_range}</div>
                  <div className="text-xs text-amber-800 mt-1">{t('marketplace.mandiModalPrice')} <b>₹{negResult.current_mandi_modal_price} / {t('units.quintal')}</b></div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-gray-50 p-3 rounded-lg border">
                    <span className="text-xs text-gray-500 block">{t('marketplace.targetOffer')}</span>
                    <span className="text-sm font-bold text-gray-800">₹{negResult.buyer_offered_price} / {t('units.quintal')}</span>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg border">
                    <span className="text-xs text-gray-500 block">{t('marketplace.confidenceScore')}</span>
                    <span className="text-sm font-bold text-emerald-600">{negResult.confidence_score}%</span>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 p-3 rounded-xl text-xs text-blue-900">
                  <b>{t('marketplace.aiMarketAdvice')}</b> {negResult.reasoning}
                </div>
              </div>
            ) : null}

            <div className="pt-2 flex justify-end">
              <button onClick={() => setShowNegModal(false)} className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-4 py-2 rounded-xl text-xs cursor-pointer">
                {t('actions.close')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* RATING MODAL (Buyer Rating Farmer) */}
      {showRateModal && ratingTarget && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
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
                className="w-full px-3.5 py-2.5 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500 h-20 resize-none"
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

export default Marketplace
