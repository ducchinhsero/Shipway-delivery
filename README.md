# 🚚 Shipway - Hệ thống Quản lý Vận chuyển

Hệ thống quản lý vận chuyển toàn diện cho Công ty Cổ phần Shipway, bao gồm chức năng đăng nhập, đăng ký, quên mật khẩu với xác thực OTP và phân quyền người dùng.

## 📋 Tổng quan

Shipway là nền tảng kết nối đối tác vận chuyển với tài xế, cung cấp giải pháp logistics hiệu quả cho các doanh nghiệp.

### Tính năng chính

- ✅ **Authentication System**
  - Đăng ký tài khoản với OTP verification
  - Đăng nhập với số điện thoại
  - Quên mật khẩu với OTP reset
  
- ✅ **Role-based Access Control**
  - **Admin**: Quản trị viên hệ thống
  - **User**: Đối tác sử dụng dịch vụ vận chuyển
  - **Driver**: Tài xế đăng ký

- ✅ **OTP System**
  - SMS OTP qua Twilio
  - Hạn chế số lần thử (max 5)
  - Auto-expire sau 5 phút

- ✅ **Swagger Documentation**
  - API docs tự động tại `/docs`
  - ReDoc tại `/redoc`
  - Try it out directly

## 🏗️ Kiến trúc

```
Shipwayyyy/
├── backend/              # FastAPI + Python + MongoDB (PORT 8000)
│   ├── app/
│   │   ├── main.py      # FastAPI entry point
│   │   ├── core/        # Config & Security
│   │   ├── db/          # Database models & session
│   │   ├── schemas/     # Pydantic schemas (Swagger)
│   │   ├── api/         # API endpoints (v1)
│   │   └── services/    # Business logic
│   ├── requirements.txt
│   └── run.py
│
├── frontend/            # Vanilla JS (HTML/CSS/JS)
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   ├── config/
│   ├── img/
│   └── index.html
│
└── docs/                # Documentation
    ├── BACKEND_DOCUMENTATION.md
    └── DATABASE_SCHEMA.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- MongoDB (local hoặc Atlas)
- Twilio account (optional for SMS OTP)

### Backend Setup

```bash
# 1. Cài đặt dependencies
cd backend
pip install -r requirements.txt

# 2. Cấu hình môi trường
# Tạo file .env với nội dung:
MONGO_URI=mongodb://tvlic:tvlic123456@192.168.111.9:27017/shipway?authSource=testcoveragedb
DB_NAME=shipway
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 3. Chạy server
python run.py
# Server chạy tại http://localhost:8000
# Swagger UI tại http://localhost:8000/docs
```

### Frontend Setup

```bash
# Chạy với Live Server
cd frontend
# Mở index.html với VS Code Live Server (port 5500)
# hoặc:
python -m http.server 5500

# Frontend chạy tại http://localhost:5500
```

## 📚 Documentation

### 🚀 Getting Started

- **[Backend README](backend-python/README.md)** - Complete backend setup guide
- **[Backend QUICKSTART](backend-python/QUICKSTART.md)** - 5-minute quick start guide
- **[Frontend README](frontend/README.md)** - Frontend setup guide

### 📖 Development Guides

- **[Backend Documentation](docs/BACKEND_DOCUMENTATION.md)** - API, Database, Security details
- **[Swagger Examples](backend-python/SWAGGER_EXAMPLES.md)** - API examples with request/response
- **[Migration Guide](backend-python/MIGRATION_GUIDE.md)** - Node.js vs FastAPI comparison
- **[Database Schema](docs/DATABASE_SCHEMA.md)** - MongoDB schema design
- **[API Examples](docs/API_EXAMPLES.md)** - Additional API examples

### 🚢 Deployment & Production

- **[🎯 Production Deploy Checklist](PRODUCTION_DEPLOY_CHECKLIST.md)** - Quick deploy guide ⭐
- **[📋 Infrastructure Handover](INFRASTRUCTURE_HANDOVER.md)** - Complete production docs
- **[🌐 Frontend Deployment](frontend/DEPLOYMENT.md)** - Frontend deploy guide
- **[📦 Deployment Files](DEPLOYMENT_FILES.md)** - Files to upload/ignore
- **[🔧 MongoDB Setup](MONGODB_QUICK_SETUP.md)** - MongoDB Atlas setup

### 🆕 New Features

- **[Plan & Credit System](backend-python/PLAN_CREDIT_SYSTEM.md)** - Subscription & credits feature
- **[Credit Migration Plan](backend-python/MIGRATION_PLAN_CREDIT.md)** - DB migration guide

### 🔍 Analysis & Reference

- **[APISHIPWAY Analysis](APISHIPWAY_ANALYSIS.md)** - Previous Flask app analysis
- **[Project Structure](PROJECT_STRUCTURE.md)** - Codebase structure
- **[Project Summary](backend-python/PROJECT_SUMMARY.md)** - Backend project overview
- **[Changelog](CHANGELOG.md)** - Version history

### 📡 API Documentation

**Development:**
- **Swagger UI**: http://localhost:8000/docs 🎉
- **ReDoc**: http://localhost:8000/redoc

**Production:**
- **Swagger UI**: https://apishipway.lpwanmapper.com/apidocs/ 🌐
- **API Base**: https://apishipway.lpwanmapper.com/

### API Endpoints

**Authentication (`/api/v1/auth`):**

```
POST   /api/v1/auth/send-otp          # Gửi OTP
POST   /api/v1/auth/verify-otp        # Xác thực OTP
POST   /api/v1/auth/register          # Đăng ký tài khoản
POST   /api/v1/auth/login             # Đăng nhập
POST   /api/v1/auth/reset-password    # Đặt lại mật khẩu
GET    /api/v1/auth/me                # Lấy thông tin user (Protected)
```

**User Management (`/api/v1/user`):**

```
PUT    /api/v1/user/profile           # Cập nhật profile (Protected)
GET    /api/v1/user/profile/:userId   # Xem profile user khác (Protected)
```

**Subscription & Credits (`/api/v1/subscription`):** 🆕

```
GET    /api/v1/subscription/plan      # Xem plan hiện tại (Protected)
PUT    /api/v1/subscription/plan      # Cập nhật plan (Admin only)
GET    /api/v1/subscription/credit    # Xem số dư credit (Protected)
PUT    /api/v1/subscription/credit    # Cập nhật credit (Admin only)
```

## 🔐 Environment Variables

### Backend (.env)

```env
# MongoDB
MONGO_URI=mongodb://tvlic:tvlic123456@192.168.111.9:27017/shipway?authSource=testcoveragedb
DB_NAME=shipway

# JWT Security
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256

# OTP
OTP_EXPIRE_MINUTES=5
OTP_MAX_ATTEMPTS=5

# Twilio (Optional - for SMS)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Frontend (config/env.js)

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api/v1',
  // ...
};
```

## 🗄️ Database Schema

### Users Collection

```javascript
{
  phone: String (unique),         // +84987654321
  name: String,                   // Nguyễn Văn A
  password: String (hashed),      // bcrypt hash
  role: String,                   // 'admin' | 'user' | 'driver'
  is_active: Boolean,
  is_phone_verified: Boolean,
  
  // Subscription & Credits (NEW) 🆕
  plan: String,                   // 'free' | 'basic' | 'premium' | 'enterprise'
  used_trips: Number,             // Số chuyến đã dùng trong kỳ
  max_trips: Number,              // Giới hạn chuyến theo plan
  credit_balance: Number,         // Số dư credit (VND)
  
  // Driver specific
  driver_info: {
    license_number: String,
    vehicle_type: String,
    vehicle_plate: String,
    is_verified: Boolean,
    rating: Number,
    total_trips: Number
  },
  
  // User/Partner specific
  company_info: {
    company_name: String,
    tax_code: String,
    address: String
  },
  
  last_login: Date,
  created_at: Date,
  updated_at: Date
}
```

### OTPs Collection

```javascript
{
  phone: String,
  otp: String,                    // 6-digit code
  purpose: String,                // 'register' | 'reset-password' | 'verify-phone'
  attempts: Number,               // Max: 5
  is_used: Boolean,
  expires_at: Date,               // TTL index - auto delete
  created_at: Date
}
```

## 🧪 Testing

### Test API với Swagger UI

1. Mở http://localhost:8000/docs
2. Click "Try it out" trên bất kỳ endpoint nào
3. Nhập request body
4. Click "Execute"
5. Xem response

### Test API với PowerShell

```powershell
# Chạy test suite tự động
cd backend
.\test-api.ps1
```

### Test API với cURL

```bash
# Send OTP
curl -X POST http://localhost:8000/api/v1/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "purpose": "register"}'

# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "name": "Test User",
    "password": "123456",
    "otp": "123456",
    "role": "user"
  }'
```

## 🚢 Production Deployment

### 🌐 Production URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **API Production** | https://apishipway.lpwanmapper.com/ | Main API backend |
| **Swagger Docs** | https://apishipway.lpwanmapper.com/apidocs/ | API documentation |
| **File Server** | https://file.lpwanmapper.com/ | Python files & resources |

### 📚 Deployment Documentation

#### Quick Reference

- **[🎯 Production Deploy Checklist](PRODUCTION_DEPLOY_CHECKLIST.md)** - Step-by-step deployment guide
- **[📋 Infrastructure Handover](INFRASTRUCTURE_HANDOVER.md)** - Complete infrastructure documentation
- **[🌐 Frontend Deployment](frontend/DEPLOYMENT.md)** - Frontend deployment guide
- **[📦 Deployment Files](DEPLOYMENT_FILES.md)** - What files to upload

#### Backend Deployment (Quick)

```bash
# 1. Clone repository
git clone <repo-url>
cd Shipwayyyy/backend-python

# 2. Setup virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
nano .env  # Add production values

# 5. Run with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Production systemd service (recommended)
# See PRODUCTION_DEPLOY_CHECKLIST.md for full setup
```

#### Frontend Deployment (Quick)

```bash
# Deploy with Nginx (recommended)
# See frontend/DEPLOYMENT.md for full guide

# Or deploy with Netlify
cd frontend
netlify deploy --prod

# Or deploy with Vercel
vercel --prod
```

### 🔒 Environment Requirements

**Production .env (Backend):**

```env
# MongoDB Atlas (Production)
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/shipway?retryWrites=true
DB_NAME=shipway

# JWT (GENERATE NEW SECRET!)
SECRET_KEY=<generate-strong-32-char-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Twilio (Production)
TWILIO_ACCOUNT_SID=<production-sid>
TWILIO_AUTH_TOKEN=<production-token>
TWILIO_PHONE_NUMBER=<production-number>

# Generate secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Frontend Config:**

Frontend tự động phát hiện môi trường (không cần chỉnh sửa):
- Development (localhost) → `http://localhost:8000/api/v1`
- Production → `https://apishipway.lpwanmapper.com/api/v1`

## 📊 Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Language |
| FastAPI | 0.109.0 | Web framework |
| MongoDB | Cloud | Database |
| Motor | 3.3.2 | Async MongoDB driver |
| Pydantic | 2.5.3 | Validation & Swagger |
| JWT | 3.3.0 | Authentication |
| Passlib | 1.7.4 | Password hashing |
| Twilio | 8.11.1 | SMS OTP |

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript (ES6 Modules)

## 🔒 Security

- ✅ Password hashing với Bcrypt
- ✅ JWT token authentication (24h expiry)
- ✅ OTP rate limiting (5 attempts max)
- ✅ Input validation với Pydantic (auto)
- ✅ CORS protection
- ✅ Environment variables cho sensitive data
- ✅ MongoDB injection prevention
- ✅ Token expiration handling

## 📈 Roadmap

### Phase 2

- [ ] Refresh token mechanism
- [ ] Rate limiting middleware
- [ ] Email OTP alternative
- [ ] Social login (Google, Facebook)
- [ ] File upload (Cloudinary)

### Phase 3

- [ ] Order management system
- [ ] Real-time tracking (WebSocket)
- [ ] Payment integration (VNPay, Momo)
- [ ] Review system
- [ ] Route optimization (Google Maps API)

## 🎯 Why FastAPI?

- ✅ **Auto Swagger**: API docs tự động, không cần viết tay
- ✅ **Type Safety**: Python type hints → autocomplete tốt hơn
- ✅ **Performance**: Nhanh như Go, Java (async native)
- ✅ **Validation**: Pydantic validate request tự động
- ✅ **Modern**: Async/await, dependency injection
- ✅ **Easy Testing**: Swagger UI có nút "Try it out"

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

- **Email**: support@shipway.vn
- **Documentation**: Xem thư mục `docs/` và `backend/`
- **Swagger UI**: http://localhost:8000/docs
- **Issues**: Tạo issue trên GitHub

## 📄 License

Copyright © 2025 Công ty Cổ phần Shipway. All rights reserved.

---

**Phiên bản**: 2.0.0 (FastAPI)
**Cập nhật**: 08/01/2025  
**Team**: Shipway Development Team

**Backend**: FastAPI + Python + MongoDB  
**Swagger**: http://localhost:8000/docs 🚀
