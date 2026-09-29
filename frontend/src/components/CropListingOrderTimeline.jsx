import { useState, useEffect } from 'react'
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
  const s = statusStr.toLowerCase().trim()
  // Must check 'delivered' (exact) BEFORE 'out for delivery' — both contain 'deliver'
  if (s === 'delivered' || s === 'delivery completed' || s === 'payment completed' || s === 'closed') return 3
  if (s.includes('out for delivery') || s.includes('out_for_delivery')) return 2
  if (s.includes('dispatch')) return 1
  return 0
}

const CropListingOrderTimeline = ({
  deal,
  role = 'Farmer',
  onStatusUpdated,
  onOpenRateBuyer,
  onOpenRateFarmer,
  onDownloadInvoice,
}) => {
  const { t, translateStatus } = useLanguage()
  const [updating, setUpdating] = useState(false)
  const [localStatus, setLocalStatus] = useState(deal.order_status || 'Order Confirmed')

  // Real-time synchronization: when deal updates from polling or farmer action, sync localStatus immediately
  useEffect(() => {
    if (deal?.order_status) {
      setLocalStatus(deal.order_status)
    }
  }, [deal?.order_status])

  const dealId = deal.deal_id || deal.id
  const stageIndex = getStageIndex(localStatus)
  const orderNumber = deal.order_number || `ORD-${(dealId || '').substring(0, 8).toUpperCase()}`
  const distanceKm = deal.distance_km != null ? deal.distance_km : 120
  const expectedDate = deal.formatted_expected_date || (deal.expected_delivery_date ? new Date(deal.expected_delivery_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Pending')
  const sourceLoc = deal.source_location || deal.listing_location || 'Pune'
  const destLoc = deal.destination_location || deal.buyer_district || 'Nashik'
  const buyerName = deal.buyer_name || 'Buyer'
  const farmerName = deal.farmer_name || 'Farmer'
  const quantity = deal.quantity || 0
  const agreedPrice = deal.agreed_price || deal.offered_price || deal.final_price || 0
  const totalAmount = deal.total_amount || (quantity * agreedPrice) || 0

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
      try {
        const res2 = await axiosClient.put(`/api/v1/deals/${dealId}/order-status`, {
          order_status: nextStatus,
        })
        if (res2.data?.success) {
          setLocalStatus(nextStatus)
          if (onStatusUpdated) onStatusUpdated(res2.data.data)
        }
      } catch (err2) {
        console.error('Retry status update failed:', err2)
      }
    } finally {
      setUpdating(false)
    }
  }

  // Dynamic Stages localized
  const STAGES_LIST = [
    { id: 'confirmed', label: t('orders.orderConfirmed', 'Order Confirmed'), shortLabel: t('orders.orderConfirmed', 'Confirmed'), icon: '📝' },
    { id: 'dispatched', label: t('orders.dispatched', 'Dispatched'), shortLabel: t('orders.dispatched', 'Dispatched'), icon: '🚚' },
    { id: 'out_for_delivery', label: t('orders.outForDelivery', 'Out for Delivery'), shortLabel: t('orders.outForDelivery', 'Out for Delivery'), icon: '📦' },
    { id: 'delivered', label: t('orders.delivered', 'Delivered'), shortLabel: t('orders.delivered', 'Delivered'), icon: '✅' },
  ]

  // Progress percentage (0%, 33.3%, 66.6%, 100%)
  const progressPercent = (stageIndex / 3) * 100

  return (
    <div className="mt-3 bg-gradient-to-br from-emerald-50 via-teal-50/70 to-emerald-50/50 border-2 border-emerald-400/90 rounded-xl p-3.5 space-y-3 shadow-xs">
      {/* Top Header: matches Pre-Harvest Advance Order styling */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-sm">🚚</span>
          <span className="text-xs font-black text-emerald-950">
            {t('orders.deliveryTracking', 'Order Delivery Tracking')}
          </span>
          <span className="text-[10px] font-bold text-emerald-800 bg-white px-1.5 py-0.5 rounded border border-emerald-300">
            {orderNumber}
          </span>
        </div>
        <span
          className={`text-[10px] font-black px-2.5 py-0.5 rounded-full shadow-xs uppercase tracking-wider ${
            stageIndex === 3
              ? 'bg-emerald-700 text-white'
              : stageIndex === 2
              ? 'bg-blue-600 text-white animate-pulse'
              : stageIndex === 1
              ? 'bg-amber-600 text-white'
              : 'bg-emerald-800 text-white'
          }`}
        >
          {translateStatus ? translateStatus(localStatus) : localStatus}
        </span>
      </div>

      {/* Inner White Container */}
      <div className="bg-white/95 p-3 rounded-lg border border-emerald-200/80 shadow-xs space-y-3">
        {/* Horizontal 4-Stage Progress Tracker */}
        <div className="relative px-2 py-1">
          {/* Background Track */}
          <div className="absolute left-6 right-6 top-4 h-1 bg-gray-200 rounded-full -z-0" />
          {/* Active Filled Track */}
          <div
            className="absolute left-6 top-4 h-1 bg-emerald-600 rounded-full transition-all duration-500 -z-0"
            style={{ width: `calc((100% - 3rem) * ${progressPercent / 100})` }}
          />

          <div className="flex items-center justify-between relative z-10">
            {STAGES_LIST.map((st, idx) => {
              const isCompleted = idx < stageIndex
              const isCurrent = idx === stageIndex

              return (
                <div key={st.id} className="flex flex-col items-center text-center">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black transition-all ${
                      isCompleted
                        ? 'bg-emerald-600 text-white ring-2 ring-emerald-100'
                        : isCurrent
                        ? stageIndex === 3
                          ? 'bg-emerald-600 text-white ring-4 ring-emerald-200 scale-110'
                          : 'bg-emerald-700 text-white ring-4 ring-emerald-200 scale-110 shadow-sm'
                        : 'bg-white text-gray-400 border border-gray-300'
                    }`}
                  >
                    {isCompleted || (isCurrent && stageIndex === 3) ? (
                      <span>✓</span>
                    ) : (
                      <span>{idx + 1}</span>
                    )}
                  </div>
                  <span
                    className={`text-[10px] mt-1 font-bold leading-tight ${
                      isCompleted
                        ? 'text-emerald-800'
                        : isCurrent
                        ? 'text-emerald-950 font-black'
                        : 'text-gray-400'
                    }`}
                  >
                    {st.shortLabel}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Delivery Logistics Specs Grid */}
        <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-emerald-100">
          <div>
            <span className="text-[10px] text-gray-500 font-semibold block uppercase">{t('orders.route', 'Remaining / Route')}</span>
            <span className="text-xs font-black text-emerald-900 flex items-center gap-1 mt-0.5">
              📍 {distanceKm} km
            </span>
            <span className="text-[9px] text-gray-500 truncate block">
              {sourceLoc} → {destLoc}
            </span>
          </div>
          <div>
            <span className="text-[10px] text-gray-500 font-semibold block uppercase">{t('orders.expectedDelivery', 'Expected Delivery')}</span>
            <span className="text-xs font-black text-emerald-800 flex items-center gap-1 mt-0.5">
              🗓️ {expectedDate}
            </span>
            <span className="text-[9px] text-emerald-700 font-bold block truncate">
              {role === 'Buyer' ? `🧑‍🌾 ${t('orders.farmer', 'Farmer:')} ${farmerName}` : `👤 ${t('orders.buyer', 'Buyer:')} ${buyerName}`}
            </span>
          </div>
        </div>

        {/* Order Details (Quantity & Amount) */}
        <div className="flex items-center justify-between text-[11px] bg-emerald-50/50 p-2 rounded-lg border border-emerald-100">
          <span className="text-gray-600">
            📦 {t('orders.confirmed', 'Confirmed:')} <b className="text-gray-900">{quantity} {t('units.quintal', 'Qtl')}</b> @ ₹{agreedPrice}/{t('units.quintal', 'Qtl')}
          </span>
          <span className="font-extrabold text-emerald-900">
            {t('orders.total', 'Total:')} ₹{Number(totalAmount).toLocaleString()}
          </span>
        </div>

        {/* Action Buttons Row */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-emerald-100">
          {deal.whatsapp_url ? (
            <a
              href={deal.whatsapp_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 px-2.5 py-1.5 rounded-lg transition-all shadow-2xs"
            >
              <span>💬</span> {role === 'Buyer' ? t('orders.whatsAppFarmer', 'WhatsApp Farmer') : t('orders.whatsAppBuyer', 'WhatsApp Buyer')}
            </a>
          ) : (
            <span className="text-[10px] text-gray-400">{t('orders.directOrderConnected', 'Direct Order Connected')}</span>
          )}

          <div className="flex items-center gap-1.5 ml-auto">
            {/* FARMER ACTIONS */}
            {role === 'Farmer' && (
              <>
                {stageIndex === 0 && (
                  <button
                    onClick={() => handleAdvanceStatus('Dispatched')}
                    disabled={updating}
                    className="bg-emerald-700 hover:bg-emerald-800 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition-all shadow-xs flex items-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <span>🚚</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markDispatched', 'Mark Dispatched')}
                  </button>
                )}

                {stageIndex === 1 && (
                  <button
                    onClick={() => handleAdvanceStatus('Out for Delivery')}
                    disabled={updating}
                    className="bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition-all shadow-xs flex items-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <span>📦</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markOutForDelivery', 'Out for Delivery')}
                  </button>
                )}

                {stageIndex === 2 && (
                  <button
                    onClick={() => handleAdvanceStatus('Delivered')}
                    disabled={updating}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition-all shadow-xs flex items-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <span>✅</span> {updating ? t('orders.updating', 'Updating...') : t('orders.markDelivered', 'Mark Delivered')}
                  </button>
                )}

                {stageIndex === 3 && (
                  <div className="flex items-center gap-1.5">
                    {onDownloadInvoice && (
                      <button
                        onClick={() => onDownloadInvoice(dealId)}
                        className="bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-[11px] font-bold px-2.5 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1"
                      >
                        📄 {t('orders.invoice', 'Invoice')}
                      </button>
                    )}
                    {onOpenRateBuyer && (
                      <button
                        onClick={() => onOpenRateBuyer(deal)}
                        disabled={deal.has_rated}
                        className={`text-[11px] font-bold px-2.5 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1 ${
                          deal.has_rated
                            ? 'bg-gray-100 text-gray-500 border border-gray-200 cursor-not-allowed'
                            : 'bg-amber-500 hover:bg-amber-600 text-white'
                        }`}
                      >
                        ⭐ {deal.has_rated ? `${t('orders.rated', 'Rated')} (${deal.user_rating || 5}★)` : t('orders.rateBuyer', 'Rate Buyer')}
                      </button>
                    )}
                  </div>
                )}
              </>
            )}

            {/* BUYER ACTIONS & STATUS */}
            {role === 'Buyer' && (
              <>
                {stageIndex < 3 ? (
                  <span className="text-[11px] font-bold text-emerald-900 bg-emerald-100/90 border border-emerald-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5 shadow-2xs">
                    <span className="w-2 h-2 rounded-full bg-emerald-600 animate-ping inline-block" />
                    {stageIndex === 2
                      ? `📦 ${t('orders.outForDeliveryToday', 'Out for Delivery (Arriving Today)')}`
                      : stageIndex === 1
                      ? `🚚 ${t('orders.dispatchedInTransit', 'Dispatched (In Transit)')}`
                      : `📝 ${t('orders.confirmedByFarmer', 'Confirmed by Farmer')}`}
                  </span>
                ) : (
                  <div className="flex items-center gap-1.5">
                    {onDownloadInvoice && (
                      <button
                        onClick={() => onDownloadInvoice(dealId)}
                        className="bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-[11px] font-bold px-2.5 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1 shadow-2xs"
                      >
                        📄 {t('orders.invoice', 'Invoice')}
                      </button>
                    )}
                    {(onOpenRateFarmer || onOpenRateBuyer) && (
                      <button
                        onClick={() => (onOpenRateFarmer || onOpenRateBuyer)(deal)}
                        disabled={deal.has_rated}
                        className={`text-[11px] font-bold px-2.5 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1 shadow-2xs ${
                          deal.has_rated
                            ? 'bg-gray-100 text-gray-500 border border-gray-200 cursor-not-allowed'
                            : 'bg-amber-500 hover:bg-amber-600 text-white'
                        }`}
                      >
                        ⭐ {deal.has_rated ? `${t('orders.rated', 'Rated')} (${deal.user_rating || 5}★)` : t('orders.rateFarmer', 'Rate Farmer')}
                      </button>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Footer: matches Pre-Harvest Advance Order footer */}
      <div className="flex items-center justify-between text-[10px] text-emerald-800 font-semibold pt-0.5 border-t border-emerald-200/60">
        <span className="flex items-center gap-1">
          <span>⚡</span> {t('orders.liveLogisticsTracking', 'Live Logistics Tracking')}
        </span>
        <span className="text-gray-500 font-normal">
          {t('orders.gpsCalculatedEta', 'GPS-calculated ETA')}
        </span>
      </div>
    </div>
  )
}

export default CropListingOrderTimeline
