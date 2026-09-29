"""Application-wide constants."""

# ── Roles ──────────────────────────────────────────────────
class UserRole:
    FARMER = "farmer"
    BUYER = "buyer"
    ADMIN = "admin"
    ALL = [FARMER, BUYER, ADMIN]


# ── Plot Status ────────────────────────────────────────────
class PlotStatus:
    GROWING = "Growing"
    HARVESTING = "Harvesting"
    HARVESTED = "Harvested"
    FALLOW = "Fallow"
    ALL = [GROWING, HARVESTING, HARVESTED, FALLOW]


# ── Ledger Types ───────────────────────────────────────────
class LedgerType:
    INCOME = "Income"
    EXPENSE = "Expense"
    ALL = [INCOME, EXPENSE]


class LedgerCategory:
    CROP_SALE = "Crop Sale"
    CROP_SALE_MKT = "Crop Sale (Marketplace)"
    FERTILIZER = "Fertilizer"
    LABOUR = "Labour"
    SEEDS = "Seeds"
    IRRIGATION = "Irrigation"
    PESTICIDE = "Pesticide"
    MACHINERY = "Machinery / Tractor"
    TRANSPORT = "Transport"
    PACKAGING = "Packaging"
    GOVT_SUBSIDY = "Government Subsidy"
    SUBSIDY = "Subsidy"
    OTHER_EXPENSE = "Other Expense"
    OTHER_INCOME = "Other Income"
    OTHER = "Other"
    ALL = [
        CROP_SALE, CROP_SALE_MKT, FERTILIZER, LABOUR, SEEDS,
        IRRIGATION, PESTICIDE, MACHINERY, TRANSPORT, PACKAGING,
        GOVT_SUBSIDY, SUBSIDY, OTHER_EXPENSE, OTHER_INCOME, OTHER,
    ]


# ── Workflow ───────────────────────────────────────────────
class TaskType:
    HARVEST = "Harvest"
    TRANSPORT = "Transport"
    SELLING = "Selling"
    IRRIGATION = "Irrigation"
    FERTILIZING = "Fertilizing"
    SOWING = "Sowing"
    OTHER = "Other"
    ALL = [HARVEST, TRANSPORT, SELLING, IRRIGATION, FERTILIZING, SOWING, OTHER]


class TaskStatus:
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ALL = [PENDING, IN_PROGRESS, COMPLETED, CANCELLED]


class TaskPriority:
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    ALL = [LOW, MEDIUM, HIGH]


# ── Soil Types ─────────────────────────────────────────────
SOIL_TYPES = ["Loamy", "Sandy", "Clay", "Black Cotton", "Red", "Alluvial", "Laterite"]

# ── Indian States ──────────────────────────────────────────
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

# ── Languages ──────────────────────────────────────────────
LANGUAGES = ["Hindi", "English", "Marathi", "Gujarati", "Punjabi", "Tamil", "Telugu", "Kannada", "Bengali"]

# ── Common Crops ───────────────────────────────────────────
CROP_LIST = [
    "Wheat", "Rice", "Maize", "Onion", "Tomato", "Potato", "Cotton",
    "Soybean", "Sugarcane", "Bajra", "Jowar", "Groundnut", "Mustard",
    "Chickpea", "Lentil", "Turmeric", "Chilli", "Garlic", "Cauliflower",
    "Cabbage", "Brinjal", "Okra", "Spinach", "Grapes", "Mango",
]

# ── Collections ────────────────────────────────────────────
class Collections:
    USERS = "users"
    PLOTS = "plots"
    LEDGER = "ledger"
    WORKFLOW = "workflow"
    REFRESH_TOKENS = "refresh_tokens"
    RESET_TOKENS = "reset_tokens"
