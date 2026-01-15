# Changelog

All notable changes to Shipway project will be documented in this file.

## [1.0.0] - 2025-01-04

### Added

#### Backend
- ✅ Node.js + Express.js backend server
- ✅ MongoDB Atlas integration with Mongoose ODM
- ✅ User authentication system (Login, Register, Reset Password)
- ✅ OTP verification system with SMS support (Twilio)
- ✅ Role-based access control (Admin, User, Driver)
- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ Input validation with express-validator
- ✅ Error handling middleware
- ✅ CORS configuration
- ✅ Database seeding for admin account
- ✅ User management APIs
- ✅ Driver-specific features

#### Models
- ✅ User model with role support
- ✅ OTP model with TTL auto-expiration
- ✅ Indexes for optimized queries

#### Frontend
- ✅ Responsive authentication UI
- ✅ Login page with phone + password
- ✅ Registration with OTP verification
- ✅ Forgot password with OTP
- ✅ Role selection (User/Driver)
- ✅ API integration with backend
- ✅ Token-based authentication
- ✅ Local storage for session management
- ✅ Modern CSS styling with animations

#### Documentation
- ✅ Comprehensive backend documentation
- ✅ MongoDB Atlas setup guide
- ✅ Quick start guide
- ✅ API documentation
- ✅ Database schema documentation
- ✅ Deployment guides
- ✅ Troubleshooting section

#### Project Structure
- ✅ Separated backend and frontend folders
- ✅ Organized code structure
- ✅ Environment configuration files
- ✅ .gitignore for security
- ✅ README files for each component

### Security
- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ OTP rate limiting
- ✅ Input sanitization
- ✅ CORS protection
- ✅ Environment variables for secrets

### Features

#### Authentication
- Login with phone number
- Register with OTP verification
- Reset password with OTP
- JWT token management
- Auto-redirect based on role

#### User Management
- Create users with different roles
- View user profile
- Update user information
- Admin can manage all users
- Driver-specific profile fields

#### OTP System
- Generate 6-digit OTP
- SMS delivery via Twilio
- 5-minute expiration
- Max 5 verification attempts
- Auto-cleanup of expired OTPs

### Technical Specifications

#### Backend
- Node.js 18.x
- Express 4.18.2
- MongoDB with Mongoose 8.0.3
- JWT 9.0.2
- Bcrypt 2.4.3
- Twilio 4.19.0

#### Frontend
- Vanilla JavaScript (ES6 Modules)
- HTML5
- CSS3
- Fetch API for HTTP requests

#### Database
- MongoDB Atlas (Cloud)
- Collections: users, otps
- Indexes for performance
- TTL for auto-deletion

### API Endpoints

**Authentication**
- POST /api/auth/send-otp
- POST /api/auth/verify-otp
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/reset-password
- GET /api/auth/me

**Users**
- GET /api/users/profile
- PUT /api/users/profile
- GET /api/users (Admin)
- GET /api/users/:userId (Admin)
- PUT /api/users/:userId/status (Admin)
- DELETE /api/users/:userId (Admin)
- PUT /api/users/driver/info (Driver)
- GET /api/users/drivers (Admin)

### Known Issues
- None at this time

### Future Enhancements
See [README.md](README.md) Roadmap section

---

## Version History

- **1.0.0** (2025-01-04): Initial release
  - Full authentication system
  - MongoDB integration
  - Frontend-Backend integration
  - Comprehensive documentation

---

**Notes:**
- This is the first stable release
- All core features are implemented and tested
- Production-ready with proper security measures
- Full documentation provided

**Contributors:**
- Shipway Development Team

**License:**
Copyright © 2025 Công ty Cổ phần Shipway

