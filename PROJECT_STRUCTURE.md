# 📁 Cấu trúc dự án Shipway

## Tổng quan

Dự án Shipway được tổ chức thành các thư mục rõ ràng, tách biệt frontend và backend.

```
Shipwayyyy/
│
├── backend/                    # Backend API (Node.js + Express + MongoDB)
│   ├── src/
│   │   ├── config/            # Configuration files
│   │   │   └── database.js    # MongoDB connection config
│   │   │
│   │   ├── models/            # Mongoose models
│   │   │   ├── User.model.js  # User schema (Admin, User, Driver)
│   │   │   └── OTP.model.js   # OTP schema with TTL
│   │   │
│   │   ├── controllers/       # Route handlers
│   │   │   ├── auth.controller.js   # Authentication logic
│   │   │   └── user.controller.js   # User management
│   │   │
│   │   ├── services/          # Business logic layer
│   │   │   ├── auth.service.js      # Auth operations
│   │   │   └── otp.service.js       # OTP generation & verification
│   │   │
│   │   ├── middleware/        # Express middlewares
│   │   │   ├── auth.middleware.js        # JWT verification
│   │   │   ├── error.middleware.js       # Error handling
│   │   │   └── validation.middleware.js  # Input validation
│   │   │
│   │   ├── routes/            # API routes
│   │   │   ├── auth.routes.js      # /api/auth/*
│   │   │   └── user.routes.js      # /api/users/*
│   │   │
│   │   └── utils/             # Utility functions
│   │       └── seed.js        # Database seeding script
│   │
│   ├── .env.template          # Environment variables template
│   ├── .gitignore            # Git ignore rules for backend
│   ├── package.json          # Backend dependencies
│   ├── server.js             # Main entry point
│   ├── server.example.js     # Example mock server (no MongoDB)
│   └── README.md             # Backend documentation
│
├── frontend/                  # Frontend application (HTML/CSS/JS)
│   ├── assets/
│   │   ├── css/
│   │   │   └── auth.css      # Styles for authentication pages
│   │   │
│   │   └── js/
│   │       ├── api.js              # HTTP client & API calls
│   │       ├── auth.service.js     # Authentication services
│   │       └── auth.controller.js  # UI controllers & event handlers
│   │
│   ├── config/
│   │   └── env.js            # Frontend configuration (API URL)
│   │
│   ├── img/                  # Images and assets
│   │   ├── Dcm.png          # Logo
│   │   └── Screenshot_1.jpeg # Background image
│   │
│   ├── index.html            # Main entry point
│   └── README.md             # Frontend documentation
│
├── docs/                      # Documentation
│   ├── BACKEND_DOCUMENTATION.md   # Comprehensive backend docs
│   ├── MONGODB_ATLAS_SETUP.md     # MongoDB Atlas setup guide
│   └── QUICKSTART.md              # Quick start guide (10 minutes)
│
├── .gitignore                # Global git ignore
├── CHANGELOG.md              # Version history
├── PROJECT_STRUCTURE.md      # This file
└── README.md                 # Main project documentation
```

## Chi tiết các thành phần

### Backend (`/backend`)

#### Entry Point
- **server.js**: Main application entry point, khởi động Express server và kết nối MongoDB

#### Source Code (`/src`)

**Config**
- `database.js`: MongoDB connection và configuration

**Models**
- `User.model.js`: Schema cho users với role-based fields
- `OTP.model.js`: Schema cho OTP với auto-expiration

**Controllers**
- `auth.controller.js`: Xử lý authentication requests (login, register, OTP, etc.)
- `user.controller.js`: Xử lý user management (profile, update, admin operations)

**Services**
- `auth.service.js`: Business logic cho authentication
- `otp.service.js`: OTP generation, sending (Twilio), verification

**Middleware**
- `auth.middleware.js`: JWT verification, role authorization
- `error.middleware.js`: Centralized error handling
- `validation.middleware.js`: Input validation rules

**Routes**
- `auth.routes.js`: Authentication endpoints
- `user.routes.js`: User management endpoints

**Utils**
- `seed.js`: Script để tạo admin account mặc định

#### Configuration Files
- `.env.template`: Template cho environment variables
- `package.json`: Dependencies và scripts
- `.gitignore`: Files cần ignore

### Frontend (`/frontend`)

#### Main Files
- **index.html**: Entry point, chứa HTML structure cho authentication pages

#### Assets (`/assets`)

**CSS**
- `auth.css`: Styles cho login, register, reset password pages

**JavaScript**
- `api.js`: HTTP client, API calls, localStorage management
- `auth.service.js`: Authentication services (login, register, OTP)
- `auth.controller.js`: UI controllers, event handlers, form validation

#### Config
- `env.js`: Frontend configuration (API URL, storage keys)

#### Images
- `Dcm.png`: Logo
- `Screenshot_1.jpeg`: Background image

### Documentation (`/docs`)

- **BACKEND_DOCUMENTATION.md**: 
  - Kiến trúc hệ thống
  - Database design
  - API specifications
  - Security guidelines
  - Deployment guides

- **MONGODB_ATLAS_SETUP.md**:
  - Step-by-step MongoDB Atlas setup
  - Database configuration
  - Connection string setup
  - Troubleshooting

- **QUICKSTART.md**:
  - Quick setup guide (10 minutes)
  - Common issues và solutions
  - Testing instructions

### Root Files

- **README.md**: Main project documentation
- **CHANGELOG.md**: Version history và changes
- **PROJECT_STRUCTURE.md**: This file
- **.gitignore**: Global git ignore rules

## File Naming Conventions

### Backend
- Models: `*.model.js` (e.g., `User.model.js`)
- Controllers: `*.controller.js`
- Services: `*.service.js`
- Routes: `*.routes.js`
- Middleware: `*.middleware.js`

### Frontend
- Controllers: `*.controller.js`
- Services: `*.service.js`
- Styles: `*.css`

## Technology Stack

### Backend
```
├── express          # Web framework
├── mongoose         # MongoDB ODM
├── jsonwebtoken     # JWT authentication
├── bcryptjs         # Password hashing
├── twilio           # SMS OTP
├── express-validator # Input validation
├── cors             # CORS middleware
└── dotenv           # Environment variables
```

### Frontend
```
├── Vanilla JavaScript (ES6 Modules)
├── HTML5
├── CSS3
└── Fetch API
```

## Data Flow

### Authentication Flow

```
Frontend                Backend                 MongoDB
   |                       |                       |
   |--[POST /register]---->|                       |
   |                       |--[Create User]------->|
   |                       |<---[User Created]-----|
   |<--[Token + User]------|                       |
   |                       |                       |
   |--[POST /login]------->|                       |
   |                       |--[Find User]--------->|
   |                       |<---[User Data]--------|
   |                       |--[Verify Password]--->|
   |<--[Token + User]------|                       |
   |                       |                       |
   [Store Token in localStorage]
```

### OTP Flow

```
Frontend                Backend                 Twilio
   |                       |                       |
   |--[POST /send-otp]---->|                       |
   |                       |--[Generate OTP]-------|
   |                       |--[Send SMS]---------->|
   |<--[Success]-----------|                       |
   |                       |                       |
   |--[POST /verify-otp]-->|                       |
   |                       |--[Check OTP]----------|
   |<--[Valid/Invalid]-----|                       |
```

## Environment Variables

### Backend (.env)
```
PORT                 # Server port (5000)
NODE_ENV            # Environment (development/production)
MONGODB_URI         # MongoDB connection string
JWT_SECRET          # JWT secret key (min 32 chars)
JWT_EXPIRE          # Token expiration (7d)
OTP_EXPIRE_MINUTES  # OTP validity (5)
TWILIO_*            # Twilio credentials (optional)
FRONTEND_URL        # CORS allowed origin
ADMIN_*             # Default admin credentials
```

### Frontend (config/env.js)
```javascript
BASE_URL            # Backend API URL
TIMEOUT             # Request timeout
ENDPOINTS           # API endpoint paths
STORAGE_KEYS        # LocalStorage key names
```

## Scripts

### Backend
```bash
npm start          # Start production server
npm run dev        # Start development server (nodemon)
npm run seed       # Seed database with admin account
```

### Frontend
```bash
# No build scripts needed (vanilla JS)
# Use any static file server
```

## Ports

| Service | Port | URL |
|---------|------|-----|
| Backend API | 5000 | http://localhost:5000 |
| Frontend | 3000 | http://localhost:3000 |
| Example Server | 5001 | http://localhost:5001 |

## Database Collections

### users
- Stores user accounts (Admin, User, Driver)
- Indexes: phone (unique), email, role, createdAt

### otps
- Stores OTP codes temporarily
- TTL index: Auto-delete after expiration
- Indexes: phone+purpose, expiresAt, createdAt

## API Routes

### Public Routes
```
POST /api/auth/send-otp
POST /api/auth/verify-otp
POST /api/auth/register
POST /api/auth/login
POST /api/auth/reset-password
```

### Protected Routes
```
GET  /api/auth/me                    [All authenticated users]
GET  /api/users/profile              [All authenticated users]
PUT  /api/users/profile              [All authenticated users]
PUT  /api/users/driver/info          [Driver only]
GET  /api/users                      [Admin only]
GET  /api/users/:userId              [Admin only]
PUT  /api/users/:userId/status       [Admin only]
DELETE /api/users/:userId            [Admin only]
GET  /api/users/drivers              [Admin only]
```

## Security Measures

✅ Password hashing (bcrypt)
✅ JWT authentication
✅ OTP verification
✅ Rate limiting on OTP attempts
✅ Input validation
✅ CORS configuration
✅ Environment variables for secrets
✅ MongoDB injection prevention
✅ Select false on sensitive fields

## Development Workflow

1. **Start Backend**
   ```bash
   cd backend
   npm run dev
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   # Use Live Server or http-server
   ```

3. **Make Changes**
   - Backend: Auto-restart với nodemon
   - Frontend: Auto-reload với Live Server

4. **Test**
   - Use browser console for frontend debugging
   - Use Postman/cURL for API testing
   - Check MongoDB Atlas for data

## Deployment Structure

### Production
```
/var/www/shipway/
├── backend/           # Backend on same or different server
│   └── (uploaded via git/ftp)
│
├── frontend/          # Frontend on web server
│   └── (uploaded to Nginx/Apache/Netlify)
│
└── .env              # Production environment variables
```

## Additional Notes

- Frontend và Backend có thể deploy riêng biệt
- MongoDB Atlas ở cloud, accessible từ anywhere
- Frontend chỉ cần static file server
- Backend cần Node.js runtime
- Communication qua REST API
- CORS được config để allow frontend domain

---

**Last Updated**: January 4, 2025  
**Version**: 1.0.0  
**Maintained by**: Shipway Development Team

