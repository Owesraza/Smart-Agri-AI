# SmartAgri AI – Backend API (Phase 2)

**FastAPI + MongoDB Atlas + JWT Authentication**

---

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your MongoDB URL and JWT secret
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app + lifespan
│   ├── config/settings.py      # Pydantic BaseSettings
│   ├── database/connection.py  # Motor async MongoDB client
│   ├── models/                 # DB field documentation
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── common.py           # Shared: APIResponse, Pagination
│   │   ├── user.py             # User register/login/update schemas
│   │   └── domain.py           # Plot, Ledger, Workflow schemas
│   ├── routers/                # FastAPI route handlers
│   │   ├── auth.py             # /api/v1/auth/*
│   │   ├── users.py            # /api/v1/users/*
│   │   ├── plots.py            # /api/v1/plots/*
│   │   ├── ledger.py           # /api/v1/ledger/*
│   │   ├── workflow.py         # /api/v1/workflow/*
│   │   ├── market.py           # /api/v1/market/* (mock)
│   │   ├── weather.py          # /api/v1/weather/* (mock)
│   │   ├── analytics.py        # /api/v1/analytics/*
│   │   └── dashboard.py        # /api/v1/dashboard/*
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── domain_service.py   # Plot + Ledger + Workflow
│   │   └── analytics_service.py
│   ├── authentication/jwt_handler.py  # JWT + bcrypt
│   ├── middleware/logging_middleware.py
│   ├── dependencies/auth.py    # get_current_user, require_role
│   ├── utils/
│   │   ├── exceptions.py       # Custom exceptions + handlers
│   │   ├── validators.py       # Phone, password validators
│   │   └── helpers.py          # Serializer, pagination
│   └── constants/constants.py  # Roles, statuses, crops
├── requirements.txt
├── .env
└── README.md
```

---

## 🔐 Authentication Flow

```
POST /api/v1/auth/register  →  Create account
POST /api/v1/auth/login     →  Get access_token + refresh_token
GET  /api/v1/users/me       →  Authorization: Bearer <access_token>
POST /api/v1/auth/refresh   →  { refresh_token } → new tokens
POST /api/v1/auth/logout    →  Invalidate refresh token
```

---

## 📋 API Endpoints Summary

| Module     | Base URL               | Methods |
|------------|------------------------|---------|
| Auth       | `/api/v1/auth`         | POST    |
| Users      | `/api/v1/users`        | GET, PATCH, DELETE |
| Plots      | `/api/v1/plots`        | GET, POST, PUT, DELETE |
| Ledger     | `/api/v1/ledger`       | GET, POST, PUT, DELETE |
| Workflow   | `/api/v1/workflow`     | GET, POST, PUT, PATCH, DELETE |
| Market     | `/api/v1/market`       | GET (mock) |
| Weather    | `/api/v1/weather`      | GET (mock) |
| Analytics  | `/api/v1/analytics`    | GET |
| Dashboard  | `/api/v1/dashboard`    | GET |

---

## 🧪 Test with Swagger

1. Open http://localhost:8000/docs
2. Click **POST /api/v1/auth/register** → register
3. Click **POST /api/v1/auth/login** → copy `access_token`
4. Click **Authorize** (🔒) → paste token as `Bearer <token>`
5. All protected routes now work

---

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGODB_URL` | MongoDB Atlas connection string |
| `DATABASE_NAME` | Database name (default: `smartagri_db`) |
| `JWT_SECRET_KEY` | Secret key for signing JWTs |
| `JWT_ALGORITHM` | Algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL (default: 30) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL (default: 7) |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) |

---

## 📦 Phase 3 – AI Integration (Upcoming)

The following endpoints are placeholder-ready for Phase 3:
- `POST /api/v1/ai/recommend` – Sell/hold recommendation
- `POST /api/v1/ai/chat` – Gemini AI chat assistant
- `GET /api/v1/market/prices` – Replace mock with AGMARKNET live API
- `GET /api/v1/weather/today` – Already connected to OpenWeatherMap in frontend
