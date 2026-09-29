import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import { useTranslation } from '../context/LanguageContext'
import { useAuth } from '../context/AuthContext'

const BuyerDashboard = () => {
  const { t, translateCrop, translateMandi, translateCropsList } = useTranslation()
  const { user } = useAuth()

  const [listings, setListings] = useState([])
  const [stats, setStats] = useState({
    todays_buying_requests: 0,
    active_deals: 0,
    completed_purchases: 0,
    pending_offers: 0,
    average_purchase_price: 0.0,
    total_quantity_purchased: 0,
    total_spent_amount: 0,
  })
  const [loading, setLoading] = useState(true)
  const [searchCrop, setSearchCrop] = useState('')
  const [searchLocation, setSearchLocation] = useState('')
  const [notification, setNotification] = useState(null)

  // Modals
  const [showFarmerProfileModal, setShowFarmerProfileModal] = useState(false)
  const [profileData, setProfileData] = useState(null)
  const [profileLoading, setProfileLoading] = useState(false)

  const [showPurchaseReqModal, setShowPurchaseReqModal] = useState(false)
  const [selectedItem, setSelectedItem] = useState(null)
  const [offerPrice, setOfferPrice] = useState('')
  const [offerQty, setOfferQty] = useState('')
  const [reqMessage, setReqMessage] = useState('')
  const [sendingRequest, setSendingRequest] = useState(false)

  // AI Negotiator Modal
  const [showNegotiateModal, setShowNegotiateModal] = useState(false)
  const [negotiatingItem, setNegotiatingItem] = useState(null)
  const [negotiating, setNegotiating] = useState(false)
  const [negotiationResult, setNegotiationResult] = useState(null)
  const [customBuyerOffer, setCustomBuyerOffer] = useState('')

  const showToast = (msg, type = 'success') => {
    setNotification({ msg, type })
    setTimeout(() => setNotification(null), 4000)
  }

  const fetchBuyerData = async (isBackground = false) => {
    if (!isBackground) setLoading(true)
    try {
      // 1. Fetch Real Active Farmer Crop Listings
      const resListings = await axiosClient.get('/api/v1/listings/')
      if (resListings.data && resListings.data.success) {
        setListings(resListings.data.data)
      }

      // 2. Fetch Buyer Stats
      const resStats = await axiosClient.get('/api/v1/buyer/dashboard')
      if (resStats.data && resStats.data.success) {
        setStats(resStats.data.data)
      }
    } catch (err) {
      console.warn('Error fetching buyer dashboard data:', err)
    } finally {
      if (!isBackground) setLoading(false)
    }
  }

  useEffect(() => {
    fetchBuyerData(false)
    const interval = setInterval(() => {
      fetchBuyerData(true)
    }, 5000)
    const handleFocus = () => fetchBuyerData(true)
    window.addEventListener('focus', handleFocus)
    return () => {
      clearInterval(interval)
      window.removeEventListener('focus', handleFocus)
    }
  }, [])

  // Open Real Farmer Profile
  const handleOpenFarmerProfile = async (farmerId) => {
    if (!farmerId) return
    setProfileData(null)
    setProfileLoading(true)
    setShowFarmerProfileModal(true)
    try {
      const res = await axiosClient.get(`/api/v1/marketplace/farmers/${farmerId}`)
      if (res.data && res.data.success) {
        setProfileData(res.data.data)
      }
    } catch (err) {
      showToast('Could not load farmer profile details', 'error')
    } finally {
      setProfileLoading(false)
    }
  }

  // Open WhatsApp Contact
  const handleWhatsAppContact = async (farmerId, crop, quantity, price) => {
    try {
      const res = await axiosClient.get('/api/v1/contact/whatsapp-url', {
        params: {
          target_user_id: farmerId,
          crop: crop || 'Wheat',
          quantity: quantity || 100,
          price: price || 2500,
          contact_type: 'buyer_to_farmer'
        }
      })
      if (res.data && res.data.success && res.data.data.whatsapp_url) {
        window.open(res.data.data.whatsapp_url, '_blank', 'noopener,noreferrer')
      } else {
        showToast('Unable to generate WhatsApp link', 'error')
      }
    } catch (err) {
      showToast('Could not connect to WhatsApp', 'error')
    }
  }

  // Send Purchase Request
  const handleSendPurchaseRequest = async (e) => {
    e.preventDefault()
    if (!selectedItem) return
    setSendingRequest(true)
    try {
      const payload = {
        crop_listing_id: selectedItem.id,
        quantity: parseFloat(offerQty) || selectedItem.quantity,
        offered_price: parseFloat(offerPrice) || selectedItem.expected_price,
        message: reqMessage || `Interested in purchasing ${selectedItem.crop}. Please confirm delivery timeline.`,
      }
      const res = await axiosClient.post('/api/v1/requests/', payload)
      if (res.data && res.data.success) {
        showToast(`🎉 Purchase request sent to ${selectedItem.farmer_name || 'farmer'}!`)
        setShowPurchaseReqModal(false)
        setReqMessage('')
      }
    } catch (err) {
      showToast('Failed to send purchase request', 'error')
    } finally {
      setSendingRequest(false)
    }
  }

  // AI Negotiation
  const handleRunNegotiation = async (item) => {
    setNegotiatingItem(item)
    setCustomBuyerOffer(Math.round(item.expected_price * 0.94))
    setNegotiationResult(null)
    setShowNegotiateModal(true)
    await executeNegotiation(item, Math.round(item.expected_price * 0.94))
  }

  const executeNegotiation = async (item, buyerPrice) => {
    setNegotiating(true)
    try {
      const res = await axiosClient.post('/api/v1/marketplace/negotiate', {
        crop: item.crop,
        buyer_offered_price: parseFloat(buyerPrice),
        farmer_expected_price: parseFloat(item.expected_price),
        district: item.location ? item.location.split(',')[0].trim() : 'Nashik'
      })
      if (res.data && res.data.success) {
        setNegotiationResult(res.data.data)
      }
    } catch (err) {
      showToast('AI Negotiation service unavailable', 'error')
    } finally {
      setNegotiating(false)
    }
  }

  // Filter listings
  const filteredListings = listings.filter((item) => {
    const matchCrop = (item.crop || '').toLowerCase().includes(searchCrop.toLowerCase())
    const matchLoc = (item.location || item.farmer_district || '').toLowerCase().includes(searchLocation.toLowerCase())
    return matchCrop && matchLoc
  })

  return (
    <div className="space-y-6 pb-12">
      {/* Toast Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-xl shadow-xl text-white text-sm font-semibold flex items-center gap-2 ${
          notification.type === 'error' ? 'bg-red-600' : 'bg-emerald-600'
        }`}>
          <span>{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-900 text-white p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-3xl">🏢</span>
            <h1 className="text-2xl font-bold">{t('buyerDashboard.title', 'Buyer Dashboard')}</h1>
            <span className="bg-blue-500 text-white text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              {user?.full_name || 'Verified Buyer'}
            </span>
          </div>
          <p className="text-blue-200 text-sm mt-1">
            Browse real crop harvests published by registered farmers across Maharashtra APMCs with instant WhatsApp direct contact & AI negotiation.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchBuyerData}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2.5 rounded-xl shadow-md transition-all flex items-center gap-2 text-sm cursor-pointer"
          >
            🔄 Refresh Listings
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Published Farmer Crops</span>
            <span className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-lg">🌾</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{listings.length} Lots</div>
            <p className="text-xs text-emerald-600 font-semibold mt-1">Direct from registered farmers</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Available Volume</span>
            <span className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-lg">📦</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">
              {listings.reduce((acc, curr) => acc + (parseFloat(curr.quantity) || 0), 0)} Qtl
            </div>
            <p className="text-xs text-blue-600 font-semibold mt-1">Ready for dispatch / booking</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Active Buying Demands</span>
            <span className="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-lg">📋</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.todays_buying_requests ?? 0}</div>
            <p className="text-xs text-amber-600 font-semibold mt-1">Open purchase requirements</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Procurement Status</span>
            <span className="w-9 h-9 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-lg">🤝</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-gray-900">{stats.active_deals || 0} Deals</div>
            <p className="text-xs text-indigo-600 font-semibold mt-1">In fulfillment workflow</p>
          </div>
        </div>
      </div>

      {/* Main Section: Published Farmer Crop Listings */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-gray-200 shadow-xs">
          <div>
            <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <span>🌾</span> Published Farmer Crop Listings ({filteredListings.length})
            </h2>
            <p className="text-xs text-gray-500">Only showing verified crops published by registered farmers</p>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search crop (e.g. Wheat, Tomato)..."
              value={searchCrop}
              onChange={(e) => setSearchCrop(e.target.value)}
              className="px-3.5 py-2 border border-gray-300 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 outline-none w-44"
            />
            <input
              type="text"
              placeholder="Search mandi/district..."
              value={searchLocation}
              onChange={(e) => setSearchLocation(e.target.value)}
              className="px-3.5 py-2 border border-gray-300 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 outline-none w-44"
            />
          </div>
        </div>

        {loading ? (
          <div className="py-16 text-center text-emerald-700 animate-pulse font-semibold text-sm">
            Loading published crops from registered farmers...
          </div>
        ) : filteredListings.length === 0 ? (
          <div className="bg-white p-12 rounded-2xl border text-center space-y-2">
            <span className="text-4xl">🌾</span>
            <h3 className="text-base font-bold text-gray-800">No matching published crops found</h3>
            <p className="text-xs text-gray-500 max-w-md mx-auto">
              No registered farmer has published crop listings matching your search filters.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredListings.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">
                      {item.quality_grade || 'Grade A'}
                    </span>
                    <span className="text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase bg-emerald-600 text-white">
                      {item.status || 'ACTIVE'}
                    </span>
                  </div>

                  <div className="mt-3">
                    <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                      <span>🌾</span> {translateCrop ? translateCrop(item.crop) : item.crop}
                    </h3>
                    <p className="text-xs text-gray-700 font-semibold mt-1">
                      🧑‍🌾 Farmer: <b className="text-emerald-800">{item.farmer_name || 'Verified Farmer'}</b>
                    </p>
                    <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                      📍 <b>{translateMandi ? translateMandi(item.location || item.farmer_district || 'Maharashtra APMC') : (item.location || item.farmer_district || 'Maharashtra APMC')}</b>
                    </p>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-2 bg-gray-50 p-3 rounded-xl border border-gray-100 text-xs">
                    <div>
                      <span className="text-gray-500 block">Available Quantity</span>
                      <span className="text-sm font-bold text-gray-800">{item.quantity} Quintals</span>
                    </div>
                    <div>
                      <span className="text-gray-500 block">Expected Spot Price</span>
                      <span className="text-sm font-bold text-emerald-700">₹{item.expected_price} / Qtl</span>
                    </div>
                  </div>

                  {/* Pre-Harvest Advance Order Box */}
                  {(item.advance_days > 0 || (item.remaining_advance_days != null && item.remaining_advance_days > 0) || item.discount_pct > 0) && (
                    <div className="mt-3 bg-gradient-to-br from-emerald-50 to-teal-50/60 border border-emerald-300 rounded-xl p-3 space-y-1.5 text-xs">
                      <div className="flex items-center justify-between font-bold text-emerald-950">
                        <span>⏱️ Advance Lead Time ({item.remaining_advance_days ?? item.advance_days} Days Left)</span>
                        <span className="bg-emerald-700 text-white text-[10px] px-2 py-0.5 rounded-full font-black">
                          {item.discount_pct || 10}% OFF
                        </span>
                      </div>
                      <p className="text-[11px] text-emerald-800 font-bold">
                        Discounted Rate: <span className="text-emerald-700 font-black text-sm">
                          ₹{item.discounted_price || Math.round(item.expected_price * (1 - (item.discount_pct || 10) / 100))} / Qtl
                        </span>
                      </p>
                      <span className="text-[10px] text-gray-400 block border-t border-emerald-200/60 pt-1">
                        🏷️ {item.tier_label || '🌟 Super Early Bird Booking'} (Save ₹{Math.round(item.expected_price - (item.discounted_price || item.expected_price * 0.9))}/Qtl)
                      </span>
                    </div>
                  )}
                </div>

                <div className="mt-5 pt-3 border-t border-gray-100 space-y-2">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleOpenFarmerProfile(item.farmer_id)}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-xl text-xs transition-all cursor-pointer"
                    >
                      👤 Farmer Profile
                    </button>
                    <button
                      onClick={() => handleRunNegotiation(item)}
                      className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 rounded-xl text-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                    >
                      🤝 AI Negotiate
                    </button>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleWhatsAppContact(item.farmer_id, item.crop, item.quantity, item.expected_price)}
                      className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                    >
                      💬 WhatsApp
                    </button>
                    <button
                      onClick={() => {
                        setSelectedItem(item)
                        setOfferPrice(item.discounted_price || item.expected_price)
                        setOfferQty(item.quantity)
                        setShowPurchaseReqModal(true)
                      }}
                      className="flex-1 bg-emerald-800 hover:bg-emerald-900 text-white font-bold py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-1"
                    >
                      📩 Send Request
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* REAL FARMER PROFILE MODAL */}
      {showFarmerProfileModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>🌾</span> Real Farmer Profile (Database Verified)
              </h3>
              <button onClick={() => setShowFarmerProfileModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            {profileLoading ? (
              <div className="py-8 text-center text-emerald-700 animate-pulse font-semibold">Loading real farmer profile from SQL database...</div>
            ) : profileData ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-full bg-emerald-700 text-white font-bold text-xl flex items-center justify-center shadow-md">
                    🧑‍🌾
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-base">{profileData.name}</h4>
                    <span className="text-xs text-emerald-800 font-bold bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      Verified {profileData.role || 'Farmer'}
                    </span>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-xl border space-y-2 text-xs">
                  <p className="text-gray-700">🆔 <b>Farmer ID:</b> {profileData.id}</p>
                  <p className="text-gray-700">📍 <b>Location:</b> {translateMandi ? translateMandi(profileData.location) : profileData.location}</p>
                  <p className="text-gray-700">📞 <b>Mobile Number:</b> {profileData.mobile_number || profileData.mobile}</p>
                  <p className="text-gray-700">🚜 <b>Farm Size:</b> {profileData.farm_size}</p>
                  <p className="text-gray-700">🌾 <b>Available Crops:</b> {translateCropsList ? translateCropsList(profileData.available_crops) : profileData.available_crops}</p>
                  <p className="text-gray-700">📦 <b>Total Crop Quantity:</b> {profileData.crop_quantity} Quintals</p>
                  <p className="text-gray-700">💰 <b>Expected Price:</b> ₹{profileData.expected_price} / Qtl</p>
                  <p className="text-gray-700">📅 <b>Harvest Date:</b> {profileData.harvest_date}</p>
                  <p className="text-gray-700">⭐ <b>Farmer Trust Rating:</b> {profileData.farmer_rating} / 5.0</p>
                </div>

                <div className="pt-2 flex justify-end gap-2">
                  <button onClick={() => setShowFarmerProfileModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">Close</button>
                  <button
                    onClick={() => {
                      setShowFarmerProfileModal(false)
                      handleWhatsAppContact(profileData.id, profileData.available_crops, profileData.crop_quantity, profileData.expected_price)
                    }}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold cursor-pointer flex items-center gap-1"
                  >
                    💬 Contact Farmer on WhatsApp
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}

      {/* SEND PURCHASE REQUEST MODAL */}
      {showPurchaseReqModal && selectedItem && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSendPurchaseRequest} className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>📩</span> Send Purchase Request
              </h3>
              <button type="button" onClick={() => setShowPurchaseReqModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="bg-emerald-50 p-3 rounded-xl border border-emerald-200 space-y-1">
              <h4 className="font-bold text-emerald-900 text-sm">🌾 {translateCrop ? translateCrop(selectedItem.crop) : selectedItem.crop} ({selectedItem.quality_grade})</h4>
              <p className="text-xs text-emerald-800">
                Farmer: <b>{selectedItem.farmer_name || 'Verified Farmer'}</b> · Location: <b>{translateMandi ? translateMandi(selectedItem.location) : selectedItem.location}</b>
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Offer Price (₹/Qtl) *</label>
                <input
                  type="number"
                  step="1"
                  value={offerPrice}
                  onChange={(e) => setOfferPrice(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Quantity (Quintals) *</label>
                <input
                  type="number"
                  step="0.1"
                  value={offerQty}
                  onChange={(e) => setOfferQty(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-700 block mb-1">Message to Farmer (Optional)</label>
              <textarea
                value={reqMessage}
                onChange={(e) => setReqMessage(e.target.value)}
                placeholder="e.g. Can take delivery at Lasalgaon APMC yard next Monday. Payment via RTGS on weighing."
                className="w-full px-3 py-2 border rounded-xl text-xs outline-none focus:ring-2 focus:ring-emerald-500 h-20 resize-none"
              />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button type="button" onClick={() => setShowPurchaseReqModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">Cancel</button>
              <button type="submit" disabled={sendingRequest} className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer">
                {sendingRequest ? 'Sending...' : 'Send Purchase Offer →'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* AI NEGOTIATION MODAL */}
      {showNegotiateModal && negotiatingItem && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <span>🤝</span> AI Price Negotiation Engine
              </h3>
              <button onClick={() => setShowNegotiateModal(false)} className="text-gray-400 hover:text-gray-600 text-xl font-bold cursor-pointer">✕</button>
            </div>

            <div className="bg-emerald-50 p-3.5 rounded-xl border border-emerald-200 space-y-1">
              <div className="flex justify-between items-center">
                <span className="font-bold text-emerald-950 text-sm">🌾 {translateCrop ? translateCrop(negotiatingItem.crop) : negotiatingItem.crop}</span>
                <span className="text-xs bg-emerald-700 text-white px-2 py-0.5 rounded-full font-extrabold">{negotiatingItem.quantity} Qtl</span>
              </div>
              <p className="text-xs text-emerald-800">
                Farmer Expectation: <b>₹{negotiatingItem.expected_price} / Qtl</b> · Location: <b>{translateMandi ? translateMandi(negotiatingItem.location) : negotiatingItem.location}</b>
              </p>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="number"
                value={customBuyerOffer}
                onChange={(e) => setCustomBuyerOffer(e.target.value)}
                placeholder="Enter Buyer Offer Price (₹)"
                className="flex-1 px-3 py-2 border rounded-xl text-xs outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button
                onClick={() => executeNegotiation(negotiatingItem, customBuyerOffer)}
                disabled={negotiating}
                className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold cursor-pointer disabled:opacity-50"
              >
                {negotiating ? 'Analyzing...' : 'Re-Calculate AI ⚡'}
              </button>
            </div>

            {negotiating ? (
              <div className="py-8 text-center text-xs text-emerald-700 animate-pulse font-semibold">
                Consulting APMC Mandi Modal Rates & Gemini AI Engine...
              </div>
            ) : negotiationResult ? (
              <div className="space-y-3 bg-gray-50 p-4 rounded-xl border border-gray-200 text-xs">
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="font-bold text-gray-700">🎯 Recommended Win-Win Compromise:</span>
                  <span className="text-sm font-black text-emerald-700">₹{negotiationResult.fair_compromise_price} / Qtl</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">APMC Mandi Modal Benchmark:</span>
                  <span className="font-bold text-gray-800">₹{negotiationResult.mandi_modal_price} / Qtl</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Deal Feasibility:</span>
                  <span className="font-extrabold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full">
                    {negotiationResult.feasibility || 'High Probability'}
                  </span>
                </div>
                <p className="text-gray-700 bg-white p-2.5 rounded-lg border italic">
                  💡 <b>AI Strategy:</b> {negotiationResult.strategy}
                </p>
              </div>
            ) : null}

            <div className="pt-2 flex justify-end gap-2">
              <button onClick={() => setShowNegotiateModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-xl text-xs font-semibold cursor-pointer">Close</button>
              <button
                onClick={() => {
                  setShowNegotiateModal(false)
                  setSelectedItem(negotiatingItem)
                  setOfferPrice(negotiationResult?.fair_compromise_price || customBuyerOffer)
                  setOfferQty(negotiatingItem.quantity)
                  setShowPurchaseReqModal(true)
                }}
                className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold cursor-pointer"
              >
                Apply AI Rate & Send Offer →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default BuyerDashboard
