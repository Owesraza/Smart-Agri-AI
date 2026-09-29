"""
SQLAlchemy ORM Database Models — Complete Agricultural Marketplace & Plot Manager
Supports Users, Buyer Profiles, Crop Listings, Buyer Requirements, Offers, Purchase Requests, Matches,
Conversations, Messages, Notifications, Deals, Transactions, Ratings, Market Connections, Plots, Ledger,
Workflow Tasks, Market Prices, Weather Cache, Historical Prices, Api Logs, Recommendations, Analytics.
"""
import uuid
from datetime import datetime, timezone, date
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Date, ForeignKey, Text, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def generate_uuid():
    return uuid.uuid4().hex


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    full_name = Column(String(100), nullable=False)
    mobile_number = Column(String(20), unique=True, index=True, nullable=False)
    whatsapp_number = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    village = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    farm_size = Column(Float, nullable=True)
    preferred_language = Column(String(50), default="Hindi")
    role = Column(String(20), default="Farmer")  # Farmer, Buyer, Admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class BuyerProfileModel(Base):
    __tablename__ = "buyer_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    company_name = Column(String(150), nullable=False)
    owner_name = Column(String(100), nullable=False)
    gst_number = Column(String(50), nullable=True)
    business_license = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    buying_crops = Column(String(255), nullable=True)  # Comma separated
    daily_capacity = Column(Float, default=0.0)
    preferred_payment_time = Column(String(50), default="Immediate")
    bank_details = Column(String(255), nullable=True)
    verification_status = Column(String(30), default="Verified")  # Pending Verification, Verified, Rejected
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PlotModel(Base):
    __tablename__ = "plots"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    plot_name = Column(String(100), nullable=False)
    crop_name = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    soil_type = Column(String(100), nullable=True)
    sowing_date = Column(Date, nullable=True)
    expected_harvest = Column(Date, nullable=True)
    status = Column(String(50), default="Growing")
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class LedgerModel(Base):
    __tablename__ = "ledger"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    type = Column(String(20), nullable=False)  # Income or Expense
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    date = Column(Date, nullable=False)
    crop = Column(String(100), nullable=True)
    plot_id = Column(String(36), nullable=True)
    transport_cost = Column(Float, default=0.0)
    labour_cost = Column(Float, default=0.0)
    packaging_cost = Column(Float, default=0.0)
    net_profit = Column(Float, nullable=True)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TaskModel(Base):
    __tablename__ = "workflow_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    task_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(String(20), default="Medium")
    status = Column(String(20), default="Pending")
    plot_id = Column(String(36), nullable=True)
    crop = Column(String(100), nullable=True)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(500), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ResetTokenModel(Base):
    __tablename__ = "reset_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(500), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class MarketPriceModel(Base):
    __tablename__ = "market_prices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    state = Column(String(100), index=True)
    district = Column(String(100), index=True)
    market_name = Column(String(150), index=True)
    commodity = Column(String(100), index=True)
    variety = Column(String(100), nullable=True)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    arrival_quantity = Column(Float, default=0.0)
    arrival_unit = Column(String(20), default="Quintal")
    date = Column(Date, index=True, nullable=False)
    source = Column(String(50), default="SEED", index=True)
    fetched_at = Column(DateTime(timezone=True), nullable=True)
    market_date = Column(Date, nullable=True, index=True)
    source_record_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class WeatherCacheModel(Base):
    __tablename__ = "weather_cache"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    location = Column(String(150), unique=True, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(String(20), default="NW")
    pressure = Column(Float, default=1013.0)
    uv_index = Column(Float, default=5.0)
    condition = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    icon = Column(String(20), default="⛅")
    rain_probability = Column(Float, default=0.0)
    rain_prediction = Column(String(255), nullable=True)
    farming_advisory = Column(Text, nullable=True)
    forecast_json = Column(Text, nullable=True)
    last_updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class HistoricalPriceModel(Base):
    __tablename__ = "historical_prices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    state = Column(String(100), nullable=True, index=True)
    district = Column(String(100), nullable=True, index=True)
    market_name = Column(String(150), nullable=True)
    commodity = Column(String(100), index=True, nullable=False)
    modal_price = Column(Float, nullable=False)
    date = Column(Date, index=True, nullable=False)
    source = Column(String(50), default="Imported")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ApiLogModel(Base):
    __tablename__ = "api_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_name = Column(String(50), index=True, nullable=False)
    endpoint = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)  # SUCCESS, FAILED, RETRIED
    response_time_ms = Column(Float, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class MarketCacheModel(Base):
    __tablename__ = "market_cache"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    cache_key = Column(String(150), unique=True, index=True, nullable=False)
    data_json = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop = Column(String(100), index=True, nullable=False)
    recommendation = Column(String(20), nullable=False)  # SELL, WAIT, STORE
    confidence = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    risk_level = Column(String(50), default="Low")
    suggested_market = Column(String(150), nullable=True)
    expected_price_trend = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AnalyticsModel(Base):
    __tablename__ = "analytics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    commodity = Column(String(100), unique=True, index=True, nullable=False)
    today_avg_price = Column(Float, default=0.0)
    weekly_avg_price = Column(Float, default=0.0)
    monthly_avg_price = Column(Float, default=0.0)
    highest_price = Column(Float, default=0.0)
    lowest_price = Column(Float, default=0.0)
    price_change_pct = Column(Float, default=0.0)
    volatility_score = Column(Float, default=0.0)
    ema_7 = Column(Float, nullable=True)
    ema_14 = Column(Float, nullable=True)
    ema_30 = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ── Marketplace Models ─────────────────────────────────────

class BuyerRequirementModel(Base):
    __tablename__ = "buyer_requirements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    buyer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False, index=True)
    quantity_required = Column(Float, nullable=False)
    offered_price = Column(Float, nullable=False)
    required_before = Column(Date, nullable=True)
    preferred_quality = Column(String(50), default="Grade A")
    preferred_district = Column(String(100), nullable=True, index=True)
    delivery_location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    advance_days = Column(Integer, default=0)
    discount_pct = Column(Float, default=0.0)
    discounted_price = Column(Float, nullable=True)
    status = Column(String(20), default="Open")  # Open, Closed, Completed
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class CropListingModel(Base):
    __tablename__ = "crop_listings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    farmer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plot_id = Column(String(36), nullable=True)
    crop = Column(String(100), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    expected_price = Column(Float, nullable=False)
    harvest_date = Column(Date, nullable=True)
    quality_grade = Column(String(50), default="Grade A")
    location = Column(String(200), nullable=True, index=True)
    available_until = Column(Date, nullable=True)
    photo_url = Column(String(500), nullable=True)
    advance_days = Column(Integer, default=0)
    discount_pct = Column(Float, default=0.0)
    discounted_price = Column(Float, nullable=True)
    status = Column(String(20), default="Available")  # Available, Reserved, Sold
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PurchaseRequestModel(Base):
    __tablename__ = "purchase_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    buyer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farmer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_listing_id = Column(String(36), ForeignKey("crop_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    offered_price = Column(Float, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String(20), default="Pending")  # Pending, Accepted, Rejected
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class OfferModel(Base):
    __tablename__ = "offers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    listing_id = Column(String(36), ForeignKey("crop_listings.id", ondelete="CASCADE"), nullable=True, index=True)
    requirement_id = Column(String(36), ForeignKey("buyer_requirements.id", ondelete="CASCADE"), nullable=True, index=True)
    buyer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farmer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    offered_price = Column(Float, nullable=False)
    counter_price = Column(Float, nullable=True)
    message = Column(Text, nullable=True)
    expected_pickup_date = Column(Date, nullable=True)
    status = Column(String(20), default="Pending")  # Pending, Accepted, Rejected, Counter, Completed
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class MatchModel(Base):
    __tablename__ = "matches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    requirement_id = Column(String(36), ForeignKey("buyer_requirements.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id = Column(String(36), ForeignKey("crop_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    buyer_id = Column(String(36), nullable=False)
    farmer_id = Column(String(36), nullable=False)
    match_score = Column(Float, nullable=False)  # 0 to 100
    crop_match = Column(Boolean, default=True)
    quantity_match_pct = Column(Float, default=100.0)
    price_diff_pct = Column(Float, default=0.0)
    distance_km = Column(Float, default=10.0)
    buyer_rating = Column(Float, default=5.0)
    farmer_rating = Column(Float, default=5.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user1_id = Column(String(36), nullable=False, index=True)
    user2_id = Column(String(36), nullable=False, index=True)
    listing_id = Column(String(36), nullable=True)
    offer_id = Column(String(36), nullable=True)
    last_message = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(String(36), nullable=False, index=True)
    receiver_id = Column(String(36), nullable=False, index=True)
    text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="Info")  # Offer, Match, Deal, Payment, System
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DealModel(Base):
    __tablename__ = "deals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    offer_id = Column(String(36), ForeignKey("offers.id", ondelete="CASCADE"), nullable=True, index=True)
    request_id = Column(String(36), ForeignKey("purchase_requests.id", ondelete="CASCADE"), nullable=True, index=True)
    listing_id = Column(String(36), nullable=True)
    requirement_id = Column(String(36), nullable=True)
    buyer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farmer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), default="Request Sent")  # Request Sent, Farmer Accepted, WhatsApp Communication Started, Negotiation, Deal Confirmed, Harvest, Delivery, Payment Completed, Ledger Updated
    order_status = Column(String(40), default="Order Confirmed")  # Order Confirmed, Dispatched, Out for Delivery, Delivered
    order_number = Column(String(50), nullable=True, index=True)
    source_location = Column(String(100), nullable=True)
    destination_location = Column(String(100), nullable=True)
    distance_km = Column(Float, nullable=True)
    expected_delivery_date = Column(Date, nullable=True)
    dispatched_at = Column(DateTime(timezone=True), nullable=True)
    out_for_delivery_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    timeline_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    deal_id = Column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    buyer_id = Column(String(36), nullable=False, index=True)
    farmer_id = Column(String(36), nullable=False, index=True)
    crop = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    final_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    transport_cost = Column(Float, default=0.0)
    platform_fee = Column(Float, default=0.0)
    payment_status = Column(String(30), default="Completed")
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    completion_date = Column(Date, nullable=False)


class RatingModel(Base):
    __tablename__ = "ratings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    deal_id = Column(String(36), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    from_user_id = Column(String(36), nullable=False, index=True)
    to_user_id = Column(String(36), nullable=False, index=True)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    review = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class MarketConnectionModel(Base):
    __tablename__ = "market_connections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    farmer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    buyer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id = Column(String(36), nullable=True)
    requirement_id = Column(String(36), nullable=True)
    connection_type = Column(String(50), default="Direct WhatsApp")
    match_score = Column(Float, default=95.0)
    status = Column(String(30), default="Active")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
