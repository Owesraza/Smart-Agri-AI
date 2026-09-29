import { useState } from 'react'
import axiosClient from '../api/axiosClient'
import { useLanguage } from '../context/LanguageContext'

const STAGES = [
  { id: 'confirmed', label: 'Order Confirmed', shortLabel: 'Confirmed', icon: '📝' },
  { id: 'dispatched', label: 'Dispatched', shortLabel: 'Dispatched', icon: '🚚' },
  { id: 'out_for_delivery', label: 'Out for Delivery', shortLabel: 'Out for Delivery', icon: '📦' },
  { id: 'delivered', label: 'Delivered', shortLabel: 'Delivered', icon: '✅' },
]

const getStageIndex = (statusStr) => {
  if (!statusStr) return 0
  const s = statusStr.toLowerCase()
  if (s.includes('deliver')) return 3
  if (s.includes('out')) return 2
  if (s.includes('dispatch')) return 1
  return 0
}

const OrderTrackingCard = ({
  deal,
  role = 'Farmer',
  onStatusUpdated,
  onOpenRateModal,
  onDownloadInvoice,
}) => {
  const { t, translateStatus, translateCrop, translateMandi } = useLanguage()
  const [updating, setUpdating] = useState(false)
  const [localStatus, setLocalStatus] = useState(deal.order_status || 'Order Confirmed')

  const currentStageIndex = getStageIndex(localStatus)
  const orderNumber = deal.order_number || `ORD-${(deal.deal_id || deal.id || '').substring(0, 8).toUpperCase()}`
  const crop = deal.crop || 'Crop'
  const quantity = deal.quantity || 0
  const agreedPrice = deal.agreed_price || deal.offered_price || deal.final_price || 0
  const totalAmount = deal.total_amount || (quantity * agreedPrice) || 0
  const distanceKm = deal.distance_km != null ? deal.distance_km : 120
  const expectedDate = deal.formatted_expected_date || (deal.expected_delivery_date ? new Date(deal.expected_delivery_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Pending')
  const sourceLocation = deal.source_location || deal.listing_location || 'Pune'
  const destLocation = deal.destination_location || deal.buyer_district || deal.farmer_district || 'Nashik'
  const farmerName = deal.farmer_name || 'Farmer'
  const buyerName = deal.buyer_name || 'Buyer'
  const dealId = deal.deal_id || deal.id

  const handleAdvanceStatus = async (nextStatus) => {
    if (!dealId) return
    setUpdating(true)
    try {
      const res = await axiosClient.patch(`/api/v1/deals/${dealId}/order-status`, {
        order_status: nextStatus,
      })
      if (res.data?.success) {
        setLocalStatus(nextStatus)
        if (onStatusUpdated) onStatusUpdated(res.data.data)
      }
    } catch (err) {
      console.error('Error updating order status:', err)
      // Fallback try PUT if PATCH fails
      try {
        const res2 = await axiosClient.put(`/api/v1/deals/${dealId}/order-status`, {
          order_status: nextStatus,
        })
        if (res2.data?.success) {
          setLocalStatus(nextStatus)
          if (onStatusUpdated) onStatusUpdated(res2.data.data)
        }
      } catch (err2) {
        console.error('Retry failed:', err2)
      }
    } finally {
      setUpdating(false)
    }
  }

  // Dynamic Stage checkpoints localized
  const STAGES_LIST = [
    { id: 'confirmed', label: t('orders.orderConfirmed', 'Order Confirmed'), shortLabel: t('orders.orderConfirmed', 'Confirmed'), icon: '📝' },
    { id: 'dispatched', label: t('orders.dispatched', 'Dispatched'), shortLabel: t('orders.dispatched', 'Dispatched'), icon: '🚚' },
    { id: 'out_for_delivery', label: t('orders.outForDelivery', 'Out for Delivery'), shortLabel: t('orders.outForDelivery', 'Out for Delivery'), icon: '📦' },
    { id: 'delivered', label: t('orders.delivered', 'Delivered'), shortLabel: t('orders.delivered', 'Delivered'), icon: '✅' },
  ]

  // Calculate filled progress percentage (0%, 33.3%, 66.6%, 100%)
  const progressPercent = (currentStageIndex / 3) * 100

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all p-5 sm:p-6 space-y-6">
      {/* Top Banner Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-gray-100 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center text-xl font-bold border border-emerald-200">
            📦
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-gray-900 text-base">{orderNumber}</span>
              <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                currentStageIndex === 3
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : currentStageIndex === 2
                  ? 'bg-blue-100 text-blue-800 border border-blue-300 animate-pulse'
                  : currentStageIndex === 1
                  ? 'bg-amber-100 text-amber-800 border border-amber-300'
                  : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              }`}>
                {translateStatus ? translateStatus(localStatus) : localStatus}
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-0.5">
              🌾 <b className="text-gray-800">{translateCrop ? translateCrop(crop) : crop}</b> • {quantity} {t('units.quintal', 'Quintals')}
            </p>
          </div>
        </div>

        {/* Expected Delivery & Distance Pill */}
        <div className="flex items-center gap-3 bg-gradient-to-r from-emerald-50/80 to-teal-50/80 border border-emerald-200/80 px-4 py-2 rounded-xl text-xs">
          <div>
            <span className="text-[10px] uppercase font-bold text-gray-500 block">{t('orders.expectedDelivery', 'Expected Delivery')}</span>
            <span className="font-extrabold text-emerald-900 text-sm flex items-center gap-1">
              🗓️ {expectedDate}
            </span>
          </div>
          <div className="h-7 w-px bg-emerald-200" />
          <div>
            <span className="text-[10px] uppercase font-bold text-gray-500 block">{t('orders.estimatedDistance', 'Estimated Distance')}</span>
            <span className="font-extrabold text-emerald-900 text-sm flex items-center gap-1">
              📍 {distanceKm} km
            </span>
          </div>
        </div>
      </div>

      {/* Horizontal Progress Timeline Tracker */}
      <div className="px-2 sm:px-6 py-4 bg-gray-50/70 rounded-2xl border border-gray-100">
        <div className="relative flex items-center justify-between">
          {/* Background Track Line */}
          <div className="absolute left-4 right-4 sm:left-6 sm:right-6 top-5 h-1.5 bg-gray-200 rounded-full -z-0" />

          {/* Active Filled Progress Line */}
          <div
            className="absolute left-4 sm:left-6 top-5 h-1.5 bg-emerald-600 rounded-full transition-all duration-500 ease-in-out -z-0"
            style={{ width: `calc((100% - 2rem) * ${progressPercent / 100})` }}
          />

          {/* Step Checkpoints */}
          {STAGES_LIST.map((stage, idx) => {
            const isCompleted = idx < currentStageIndex
            const isCurrent = idx === currentStageIndex

            return (
              <div key={stage.id} className="relative z-10 flex flex-col items-center text-center">
                {/* Checkpoint Circle */}
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 shadow-sm ${
                    isCompleted
                      ? 'bg-emerald-600 text-white ring-4 ring-emerald-100'
                      : isCurrent
                      ? currentStageIndex === 3
                        ? 'bg-emerald-600 text-white ring-4 ring-emerald-200 scale-110'
                        : 'bg-emerald-700 text-white ring-4 ring-emerald-200 scale-110 shadow-md'
                      : 'bg-white text-gray-400 border-2 border-gray-300'
                  }`}
                >
                  {isCompleted ? (
                    <span className="text-base font-black">✓</span>
                  ) : isCurrent ? (
                    currentStageIndex === 3 ? (
                      <span className="text-base font-black">✓</span>
                    ) : (
                      <span className="text-sm font-black">{idx + 1}</span>
                    )
                  ) : (
                    <span className="text-xs font-semibold">{idx + 1}</span>
                  )}
                </div>

                {/* Stage Label */}
                <span
                  className={`mt-2 text-xs font-bold transition-colors ${
                    isCompleted
                      ? 'text-emerald-800'
                      : isCurrent
                      ? 'text-emerald-950 font-black'
                      : 'text-gray-400'
                  }`}
                >
                  <span className="hidden sm:inline">{stage.label}</span>
                  <span className="sm:hidden">{stage.shortLabel}</span>
                </span>

                {/* Status Indicator Pill below current */}
                {isCurrent && (
                  <span className="mt-1 text-[9px] font-extrabold uppercase px-2 py-0.5 bg-emerald-100 text-emerald-900 rounded-full tracking-wider border border-emerald-300 shadow-xs">
                    {currentStageIndex === 3 ? t('orders.completed', 'Completed') : t('orders.inTransit', 'In Transit')}
                  </span>
                )}
              </div>
            )
          })}
        </div>
      </div>

      {/* Order Info & Logistics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-white p-3.5 rounded-xl border border-gray-200">
        <div>
          <span className="text-gray-400 block text-[10px] uppercase font-semibold">{t('orders.route', 'Route')}</span>
          <span className="font-bold text-gray-800 flex items-center gap-1 truncate mt-0.5">
            📍 {translateMandi ? translateMandi(sourceLocation) : sourceLocation} → 🏢 {translateMandi ? translateMandi(destLocation) : destLocation}
          </span>
        </div>
        <div>
          <span className="text-gray-400 block text-[10px] uppercase font-semibold">{t('orders.agreedRate', 'Agreed Rate')}</span>
          <span className="font-bold text-emerald-700 text-sm mt-0.5 block">
            ₹{agreedPrice} / {t('units.quintal', 'Qtl')}
          </span>
        </div>
        <div>
          <span className="text-gray-400 block text-[10px] uppercase font-semibold">{t('orders.totalAmount', 'Total Amount')}</span>
          <span className="font-bold text-emerald-900 text-sm mt-0.5 block">
            ₹{Number(totalAmount).toLocaleString()}
          </span>
        </div>
        <div>
          <span className="text-gray-400 block text-[10px] uppercase font-semibold">
            {role === 'Farmer' ? t('orders.buyerName', 'Buyer Name') : t('orders.farmerName', 'Farmer Name')}
          </span>
          <span className="font-bold text-gray-900 truncate mt-0.5 block">
            👤 {role === 'Farmer' ? buyerName : farmerName}
          </span>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        {/* WhatsApp Link */}
        {deal.whatsapp_url ? (
          <a
            href={deal.whatsapp_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-800 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-3.5 py-2 rounded-xl transition-all cursor-pointer shadow-xs"
          >
            <span>💬</span> {t('orders.chatOnWhatsApp', 'Chat on WhatsApp with')} {role === 'Farmer' ? buyerName : farmerName}
          </a>
        ) : (
          <div className="text-xs text-gray-400">{t('orders.directWhatsAppVerified', 'Direct WhatsApp Verified')}</div>
        )}

        {/* State Transition Actions for Farmer */}
        <div className="flex items-center gap-2">
          {role === 'Farmer' && currentStageIndex === 0 && (
            <button
              onClick={() => handleAdvanceStatus('Dispatched')}
              disabled={updating}
              className="bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <span>🚚</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markDispatched', 'Mark as Dispatched')}
            </button>
          )}

          {role === 'Farmer' && currentStageIndex === 1 && (
            <button
              onClick={() => handleAdvanceStatus('Out for Delivery')}
              disabled={updating}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <span>📦</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markOutForDelivery', 'Out for Delivery')}
            </button>
          )}

          {role === 'Farmer' && currentStageIndex === 2 && (
            <button
              onClick={() => handleAdvanceStatus('Delivered')}
              disabled={updating}
              className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <span>✅</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markDelivered', 'Mark as Delivered')}
            </button>
          )}

          {/* Delivered State Actions */}
          {currentStageIndex === 3 && (
            <>
              {onDownloadInvoice && (
                <button
                  onClick={() => onDownloadInvoice(dealId)}
                  className="bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-bold px-3.5 py-2 rounded-xl transition-all cursor-pointer flex items-center gap-1 shadow-xs"
                >
                  📄 {t('orders.invoice', 'Invoice')}
                </button>
              )}

              {onOpenRateModal && (
                <button
                  onClick={() => onOpenRateModal(deal)}
                  disabled={deal.has_rated}
                  className={`text-xs font-bold px-3.5 py-2 rounded-xl transition-all cursor-pointer flex items-center gap-1 shadow-xs ${
                    deal.has_rated
                      ? 'bg-gray-100 text-gray-500 border border-gray-200 cursor-not-allowed'
                      : 'bg-amber-500 hover:bg-amber-600 text-white'
                  }`}
                >
                  ⭐ {deal.has_rated ? `${t('orders.rated', 'Rated')} (${deal.user_rating || 5}★)` : role === 'Farmer' ? t('orders.rateBuyer', 'Rate Buyer') : t('orders.rateFarmer', 'Rate Farmer')}
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default OrderTrackingCard
