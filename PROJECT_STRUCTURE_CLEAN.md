# 📁 Shipway Project Structure (Clean)

> Updated: 2026-01-15 - After reorganization & cleanup

## 🌳 Directory Tree

```
Shipwayyyy/
│
├── 📁 backend/                      Python FastAPI Backend
│   ├── app/
│   │   ├── api/v1/                  API endpoints
│   │   │   ├── auth.py             Authentication
│   │   │   ├── orders.py           Order management
│   │   │   ├── wallet.py           Wallet & payments
│   │   │   ├── subscription.py     Subscription plans
│   │   │   └── user.py             User management
│   │   ├── core/                   Core functionality
│   │   │   ├── config.py           Configuration
│   │   │   ├── security.py         Auth & hashing
│   │   │   └── exceptions.py       Custom exceptions
│   │   ├── db/                     Database
│   │   │   ├── models.py           MongoDB operations
│   │   │   └── session.py          DB connection
│   │   ├── schemas/                Pydantic schemas
│   │   │   ├── order.py
│   │   │   ├── wallet.py
│   │   │   ├── user.py
│   │   │   └── ...
│   │   ├── services/               Business logic
│   │   │   ├── otp_service.py      OTP/Twilio
│   │   │   ├── payment_service.py  Payments (VNPay, Momo)
│   │   │   ├── pricing_service.py  Fee calculation
│   │   │   └── upload_service.py   File uploads
│   │   └── main.py                 FastAPI app
│   ├── scripts/                    Utility scripts
│   │   └── migrate_add_plan_credit.py
│   ├── uploads/orders/             User uploads
│   ├── requirements.txt            Python dependencies
│   ├── run.py                      Server starter
│   ├── env.example.txt             Environment template
│   ├── *.ps1                       Test scripts
│   └── *_DOCUMENTATION.md          Feature docs
│
├── 📁 frontend/                     Frontend Application
│   ├── auth/                       Authentication (PUBLIC)
│   │   ├── index.html
│   │   ├── auth.js
│   │   ├── auth.controller.js
│   │   ├── auth.css
│   │   └── img/
│   ├── user/                       User Features (PROTECTED)
│   │   ├── dashboard/              Order management
│   │   ├── booking/                Create order
│   │   ├── wallet/                 Wallet & payments
│   │   ├── history/                Order history
│   │   ├── booking-details/        Order details
│   │   └── verify-identity/        KYC
│   ├── onboarding/                 Welcome flow (PUBLIC)
│   │   ├── index.html
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   ├── shared/                     Shared modules
│   │   ├── api.js                  API service
│   │   ├── auth-store.js           Auth state
│   │   ├── auth-guard.js           Route protection
│   │   ├── event-bus.js            Event system
│   │   ├── header.html/js/css      Common header
│   │   └── footer.html             Common footer
│   ├── config/                     Configuration
│   │   └── env.js                  API endpoints
│   ├── index.html                  Dev menu
│   ├── README.md                   Frontend guide
│   ├── REORGANIZATION_SUMMARY.md   Architecture docs
│   └── STRUCTURE_ANALYSIS.md       Analysis
│
├── 📁 docs/                         Documentation
│   ├── API_EXAMPLES.md             API usage examples
│   ├── BACKEND_DOCUMENTATION.md    Backend overview
│   ├── DATABASE_SCHEMA.md          DB structure
│   ├── MONGODB_ATLAS_SETUP.md      MongoDB setup
│   ├── QUICKSTART.md               Quick start guide
│   ├── AUTH_IMPLEMENTATION_PLAN.md Auth details
│   ├── AUTH_INTEGRATION_SUMMARY.md Auth summary
│   ├── INDEX.md                    Docs index
│   └── database schema diagram.png Visual schema
│
├── 📄 README.md                     Main project readme
├── 📄 CHANGELOG.md                  Version history
├── 📄 CONTRIBUTING.md               Contribution guide
├── 📄 SETUP_INSTRUCTIONS.md         Setup guide
├── 📄 DEPLOYMENT.md                 Deployment guide (unified)
├── 📄 PROJECT_STRUCTURE.md          Old structure doc
├── 📄 PROJECT_STRUCTURE_CLEAN.md    This file
├── 📄 SUMMARY.md                    Project summary
├── 📄 MONGODB_QUICK_SETUP.md        Quick MongoDB guide
├── 📄 CLEANUP_PLAN.md               Cleanup analysis
└── 📄 .gitignore                    Git ignore rules
```

## 📊 File Statistics

| Category | Count | Notes |
|----------|-------|-------|
| Python files | 25+ | Backend code |
| JavaScript files | 30+ | Frontend code |
| HTML files | 20+ | Frontend pages |
| CSS files | 20+ | Styles |
| Documentation | 25+ | Markdown files |
| Test scripts | 4 | PowerShell scripts |

## 🎯 Key Features by Location

### Backend (`backend/`)

| Feature | Files | Status |
|---------|-------|--------|
| Authentication | `api/v1/auth.py`, `core/security.py` | ✅ Ready |
| Order Management | `api/v1/orders.py`, `schemas/order.py` | ✅ Ready |
| Wallet & Payments | `api/v1/wallet.py`, `services/payment_service.py` | ✅ Ready |
| User Management | `api/v1/user.py`, `schemas/user.py` | ✅ Ready |
| Subscriptions | `api/v1/subscription.py` | ✅ Ready |

### Frontend (`frontend/`)

| Feature | Location | Status |
|---------|----------|--------|
| Login/Register | `auth/` | ✅ Ready |
| Dashboard | `user/dashboard/` | ✅ Ready (backend connected) |
| Create Order | `user/booking/` | 🔨 WIP |
| Wallet | `user/wallet/` | ✅ Ready (backend connected) |
| Order History | `user/history/` | 🔨 WIP |
| Order Details | `user/booking-details/` | 🔨 WIP |
| KYC | `user/verify-identity/` | 🔨 WIP |
| Onboarding | `onboarding/` | 🔨 WIP |

## 🔒 Protected Routes

All pages in `frontend/user/` are protected with:
- Authentication check (redirect to login if not authenticated)
- Role verification (user role required)
- Auto-implemented via `shared/auth-guard.js`

## 📝 Documentation Index

### Getting Started
1. `README.md` - Project overview
2. `SETUP_INSTRUCTIONS.md` - Local setup
3. `docs/QUICKSTART.md` - Quick start
4. `MONGODB_QUICK_SETUP.md` - Database setup

### Development
1. `backend/README.md` - Backend guide
2. `frontend/README.md` - Frontend guide
3. `docs/BACKEND_DOCUMENTATION.md` - Backend API
4. `frontend/REORGANIZATION_SUMMARY.md` - Frontend architecture

### Features
1. `backend/ORDER_API_DOCUMENTATION.md` - Order API
2. `backend/WALLET_API_DOCUMENTATION.md` - Wallet API
3. `docs/AUTH_IMPLEMENTATION_PLAN.md` - Auth details
4. `docs/DATABASE_SCHEMA.md` - Database

### Deployment
1. `DEPLOYMENT.md` - Complete deployment guide
2. `backend/ENV_VARIABLES.md` - Environment vars
3. `backend/QUICKSTART.md` - Backend quick start

## 🧹 What Was Cleaned Up

### Removed (20+ files/folders)
- ❌ Temporary scripts (add-auth-protection.ps1, update-paths.ps1, etc.)
- ❌ Empty folders (assets/, img/, shell-app/, admin/, driver/)
- ❌ Wrong files (package-lock.json in Python project)
- ❌ Duplicate docs (7 deployment docs → 1 unified)
- ❌ Old analysis files

### Consolidated
- ✅ 7 deployment docs → `DEPLOYMENT.md`
- ✅ Frontend docs → `docs/` folder
- ✅ Test scripts → backend folder

## 🚀 Quick Navigation

### For Developers
```bash
# Backend
cd backend/
python run.py                    # Start backend server
.\create-test-user.ps1          # Create test user
.\test-order-api-clean.ps1      # Test order API

# Frontend
cd frontend/
# Open index.html in browser or use Live Server
```

### For Documentation
```bash
# Main docs
cat README.md                    # Project overview
cat SETUP_INSTRUCTIONS.md        # How to setup
cat DEPLOYMENT.md                # How to deploy

# API docs
http://localhost:8000/docs       # Swagger UI (when backend running)
```

### For Testing
```bash
# Backend tests
cd backend/
.\test-api.ps1                   # Test auth API
.\test-wallet-api.ps1            # Test wallet API
.\test-order-api-clean.ps1       # Test order API

# Frontend
# Open frontend/index.html and navigate through features
```

## 📦 Dependencies

### Backend
- **Python**: 3.9+
- **FastAPI**: Web framework
- **MongoDB**: Database (Atlas)
- **Pydantic**: Data validation
- **See**: `backend/requirements.txt`

### Frontend
- **Vanilla JavaScript**: No framework
- **ES6 Modules**: Modern JS
- **CSS3**: Custom styles
- **No build step**: Pure HTML/CSS/JS

## 🎯 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend API | ✅ 95% | Core features ready |
| Frontend Auth | ✅ 100% | Complete |
| Frontend Dashboard | ✅ 90% | Backend connected |
| Frontend Wallet | ✅ 85% | Backend connected |
| Frontend Booking | 🔨 70% | Need backend integration |
| Documentation | ✅ 90% | Comprehensive |
| Testing | 🔨 60% | Scripts available |
| Deployment | 📝 0% | Guide ready, not deployed |

## 🔗 Related Files

- **Old structure**: `PROJECT_STRUCTURE.md` (outdated)
- **Cleanup analysis**: `CLEANUP_PLAN.md`
- **Frontend analysis**: `frontend/STRUCTURE_ANALYSIS.md`
- **Change log**: `CHANGELOG.md`

---

**Last Updated**: 2026-01-15
**Status**: ✅ Clean & Organized
**Next**: Continue feature development or deploy
