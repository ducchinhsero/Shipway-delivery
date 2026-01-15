# 📘 Tài liệu Backend - Shipway Transportation System

## 📋 Mục lục

1. [Tổng quan](#tổng-quan)
2. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
3. [Thiết kế Database](#thiết-kế-database)
4. [API Endpoints](#api-endpoints)
5. [Phân quyền và Bảo mật](#phân-quyền-và-bảo-mật)
6. [OTP System](#otp-system)
7. [Authentication Flow](#authentication-flow)
8. [Setup và Deployment](#setup-và-deployment)

---

## 🎯 Tổng quan

### Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| Node.js | >= 18.x | Runtime Environment |
| Express.js | ^4.18.2 | Web Framework |
| MongoDB | Cloud (Atlas) | Database |
| Mongoose | ^8.0.3 | ODM (Object Data Modeling) |
| JWT | ^9.0.2 | Token-based Authentication |
| Bcryptjs | ^2.4.3 | Password Hashing |
| Twilio | ^4.19.0 | SMS OTP Service |
| Express-validator | ^7.0.1 | Request Validation |

### Tính năng chính

- ✅ **Authentication**: Đăng ký, Đăng nhập, Đặt lại mật khẩu
- ✅ **OTP Verification**: Xác thực qua SMS (Twilio)
- ✅ **Role-based Access Control**: Admin, User, Driver
- ✅ **JWT Token**: Stateless authentication
- ✅ **Password Security**: Bcrypt hashing
- ✅ **Data Validation**: Express-validator
- ✅ **Error Handling**: Centralized error middleware

---

## 🏗️ Kiến trúc hệ thống

### Cấu trúc thư mục

```
backend/
├── src/
│   ├── config/              # Configuration files
│   │   └── database.js      # MongoDB connection
│   │
│   ├── models/              # Mongoose models
│   │   ├── User.model.js    # User schema & methods
│   │   └── OTP.model.js     # OTP schema & methods
│   │
│   ├── controllers/         # Route controllers
│   │   ├── auth.controller.js    # Authentication logic
│   │   └── user.controller.js    # User management
│   │
│   ├── services/            # Business logic
│   │   ├── auth.service.js       # Auth services
│   │   └── otp.service.js        # OTP services
│   │
│   ├── middleware/          # Express middlewares
│   │   ├── auth.middleware.js         # JWT verification
│   │   ├── error.middleware.js        # Error handling
│   │   └── validation.middleware.js   # Input validation
│   │
│   ├── routes/              # API routes
│   │   ├── auth.routes.js   # Auth endpoints
│   │   └── user.routes.js   # User endpoints
│   │
│   └── utils/               # Utilities
│       └── seed.js          # Database seeding
│
├── .env.template            # Environment template
├── .gitignore              # Git ignore rules
├── package.json            # Dependencies
├── server.js               # Entry point
└── README.md              # Backend README
```

### Luồng xử lý Request

```
Client Request
    ↓
Express Router
    ↓
Validation Middleware (if applicable)
    ↓
Authentication Middleware (if protected)
    ↓
Authorization Middleware (if role-based)
    ↓
Controller
    ↓
Service Layer
    ↓
Model/Database
    ↓
Response to Client
```

---

## 💾 Thiết kế Database

### MongoDB Collections

#### 1. **Users Collection**

Lưu trữ thông tin người dùng (Admin, User, Driver)

**Schema:**

```javascript
{
  _id: ObjectId,
  phone: String (unique, required),      // Số điện thoại (đăng nhập)
  name: String (required),               // Họ và tên
  password: String (hashed, required),   // Mật khẩu (bcrypt)
  role: String (enum),                   // 'admin' | 'user' | 'driver'
  email: String (optional),              // Email (không bắt buộc)
  
  // Status fields
  isActive: Boolean,                     // Tài khoản có hoạt động không
  isPhoneVerified: Boolean,              // Đã xác thực SĐT chưa
  
  avatar: String,                        // URL avatar
  
  // Driver specific fields
  driverInfo: {
    licenseNumber: String,               // Số bằng lái
    vehicleType: String,                 // 'motorbike'|'car'|'truck'|'van'
    vehiclePlate: String,                // Biển số xe
    isVerified: Boolean,                 // Tài xế đã được xác minh
    rating: Number,                      // Đánh giá (0-5)
    totalTrips: Number                   // Tổng số chuyến
  },
  
  // User/Partner specific fields
  companyInfo: {
    companyName: String,                 // Tên công ty
    taxCode: String,                     // Mã số thuế
    address: String                      // Địa chỉ công ty
  },
  
  lastLogin: Date,                       // Lần đăng nhập cuối
  refreshToken: String,                  // Refresh token (select: false)
  
  createdAt: Date,                       // Ngày tạo
  updatedAt: Date                        // Ngày cập nhật
}
```

**Indexes:**

```javascript
phone: 1 (unique)
email: 1
role: 1
createdAt: -1
```

**Validation Rules:**

- `phone`: Regex validation cho định dạng quốc tế
- `name`: 2-100 ký tự
- `password`: Tối thiểu 6 ký tự (hash trước khi lưu)
- `role`: Chỉ chấp nhận 'admin', 'user', 'driver'
- `email`: Email format validation (optional)

---

#### 2. **OTPs Collection**

Lưu trữ mã OTP để xác thực

**Schema:**

```javascript
{
  _id: ObjectId,
  phone: String (required),              // Số điện thoại nhận OTP
  otp: String (required),                // Mã OTP (6 chữ số)
  purpose: String (enum, required),      // 'register'|'reset-password'|'verify-phone'
  
  attempts: Number (default: 0),         // Số lần thử (max: 5)
  isUsed: Boolean (default: false),      // Đã sử dụng chưa
  
  expiresAt: Date (required, TTL),       // Thời gian hết hạn (auto delete)
  
  createdAt: Date,
  updatedAt: Date
}
```

**Indexes:**

```javascript
phone: 1, purpose: 1 (compound)
expiresAt: 1 (TTL index - auto delete when expired)
createdAt: 1
```

**TTL (Time To Live):**

- OTP tự động bị xóa khỏi database sau khi hết hạn
- Mặc định: 5 phút (có thể cấu hình qua `OTP_EXPIRE_MINUTES`)

**Business Rules:**

- Mỗi phone + purpose chỉ có 1 OTP active
- Tối đa 5 lần thử sai
- OTP được đánh dấu `isUsed = true` sau khi verify thành công

---

### Database Design Rationale

#### Tại sao tách User và OTP?

1. **Separation of Concerns**: OTP là dữ liệu tạm thời, User là dữ liệu vĩnh viễn
2. **Performance**: OTP tự động xóa (TTL), không làm phình to User collection
3. **Security**: OTP không lưu trong User, giảm rủi ro nếu bị breach
4. **Scalability**: Dễ dàng thay đổi OTP logic mà không ảnh hưởng User schema

#### Tại sao dùng Phone làm primary login?

- Phù hợp với thị trường Việt Nam (SMS OTP phổ biến)
- Dễ xác thực và giảm spam
- Không yêu cầu email (nhiều user không có/không muốn cung cấp)

---

## 🔌 API Endpoints

### Base URL

```
Development: http://localhost:5000/api
Production: https://api.shipway.vn/api
```

### Response Format

Tất cả API đều trả về format JSON chuẩn:

**Success Response:**

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error Response:**

```json
{
  "success": false,
  "message": "Error message",
  "errors": [ ... ] // Optional validation errors
}
```

---

### 🔐 Authentication Endpoints

#### 1. Send OTP

Gửi mã OTP đến số điện thoại

**Endpoint:** `POST /api/auth/send-otp`

**Body:**

```json
{
  "phone": "+84987654321",
  "purpose": "register" // 'register' | 'reset-password' | 'verify-phone'
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expiresAt": "2025-01-04T10:05:00.000Z",
  "otp": "123456" // Chỉ hiển thị trong development mode
}
```

**Error Cases:**

- `400`: Số điện thoại không hợp lệ
- `400`: Số điện thoại đã được đăng ký (nếu purpose = 'register')
- `404`: Tài khoản không tồn tại (nếu purpose = 'reset-password')
- `500`: Lỗi gửi SMS

---

#### 2. Verify OTP

Xác thực mã OTP

**Endpoint:** `POST /api/auth/verify-otp`

**Body:**

```json
{
  "phone": "+84987654321",
  "otp": "123456",
  "purpose": "register"
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

**Error Cases:**

- `400`: OTP không đúng (còn X lần thử)
- `400`: OTP đã hết hạn
- `400`: Vượt quá số lần thử

---

#### 3. Register

Đăng ký tài khoản mới

**Endpoint:** `POST /api/auth/register`

**Body:**

```json
{
  "phone": "+84987654321",
  "name": "Nguyễn Văn A",
  "password": "password123",
  "role": "user", // 'user' | 'driver' (không cho phép 'admin')
  "otp": "123456"
}
```

**Response:** `201 Created`

```json
{
  "success": true,
  "message": "Đăng ký thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "...",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "isActive": true,
    "isPhoneVerified": true,
    "createdAt": "..."
  }
}
```

**Validation:**

- Phone: Required, valid format
- Name: 2-100 ký tự
- Password: Tối thiểu 6 ký tự
- OTP: Required, 6 chữ số
- Role: 'user' hoặc 'driver' only

**Error Cases:**

- `400`: Thiếu thông tin bắt buộc
- `400`: Validation failed
- `400`: OTP không hợp lệ
- `400`: Số điện thoại đã tồn tại

---

#### 4. Login

Đăng nhập vào hệ thống

**Endpoint:** `POST /api/auth/login`

**Body:**

```json
{
  "phone": "+84987654321",
  "password": "password123"
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "Đăng nhập thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "...",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "lastLogin": "..."
  }
}
```

**Error Cases:**

- `400`: Thiếu số điện thoại hoặc mật khẩu
- `404`: Tài khoản không tồn tại
- `401`: Mật khẩu không chính xác
- `401`: Tài khoản đã bị vô hiệu hóa

---

#### 5. Reset Password

Đặt lại mật khẩu

**Endpoint:** `POST /api/auth/reset-password`

**Body:**

```json
{
  "phone": "+84987654321",
  "otp": "123456",
  "newPassword": "newpassword123"
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "Đặt lại mật khẩu thành công"
}
```

**Error Cases:**

- `400`: Thiếu thông tin
- `400`: OTP không hợp lệ
- `404`: Tài khoản không tồn tại

---

#### 6. Get Current User

Lấy thông tin user hiện tại (yêu cầu JWT)

**Endpoint:** `GET /api/auth/me`

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
{
  "success": true,
  "user": {
    "_id": "...",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "email@example.com",
    "avatar": null,
    "isActive": true,
    "isPhoneVerified": true,
    "lastLogin": "...",
    "createdAt": "..."
  }
}
```

**Error Cases:**

- `401`: Token không hợp lệ hoặc hết hạn
- `401`: Người dùng không tồn tại

---

### 👤 User Management Endpoints

#### 7. Get Profile

Lấy thông tin profile của user hiện tại

**Endpoint:** `GET /api/users/profile`

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK` (giống GET /api/auth/me)

---

#### 8. Update Profile

Cập nhật thông tin profile

**Endpoint:** `PUT /api/users/profile`

**Headers:**

```
Authorization: Bearer <token>
```

**Body:**

```json
{
  "name": "Nguyễn Văn B",
  "email": "newemail@example.com",
  "avatar": "https://...",
  "companyInfo": {
    "companyName": "ABC Company",
    "taxCode": "0123456789",
    "address": "123 Street, City"
  }
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "Cập nhật thông tin thành công",
  "user": { ... }
}
```

**Note:** Không cho phép cập nhật `phone`, `password`, `role`, `isActive`

---

#### 9. Get All Users (Admin Only)

Lấy danh sách tất cả users

**Endpoint:** `GET /api/users`

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Query Parameters:**

- `page` (default: 1): Số trang
- `limit` (default: 10): Số items per page
- `role`: Filter theo role ('admin', 'user', 'driver')
- `search`: Tìm kiếm theo tên hoặc số điện thoại

**Example:**

```
GET /api/users?page=1&limit=20&role=driver&search=nguyen
```

**Response:** `200 OK`

```json
{
  "success": true,
  "users": [ ... ],
  "totalPages": 5,
  "currentPage": 1,
  "total": 100
}
```

**Error Cases:**

- `401`: Chưa đăng nhập
- `403`: Không có quyền admin

---

#### 10. Get User by ID (Admin Only)

**Endpoint:** `GET /api/users/:userId`

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Response:** `200 OK`

```json
{
  "success": true,
  "user": { ... }
}
```

---

#### 11. Update User Status (Admin Only)

Kích hoạt/vô hiệu hóa tài khoản

**Endpoint:** `PUT /api/users/:userId/status`

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Body:**

```json
{
  "isActive": false
}
```

**Response:** `200 OK`

---

#### 12. Delete User (Admin Only)

**Endpoint:** `DELETE /api/users/:userId`

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Response:** `200 OK`

**Note:** Không cho phép xóa tài khoản admin

---

#### 13. Update Driver Info (Driver Only)

Cập nhật thông tin tài xế

**Endpoint:** `PUT /api/users/driver/info`

**Headers:**

```
Authorization: Bearer <driver_token>
```

**Body:**

```json
{
  "licenseNumber": "B2-12345678",
  "vehicleType": "motorbike",
  "vehiclePlate": "29A-12345"
}
```

**Response:** `200 OK`

---

#### 14. Get All Drivers (Admin Only)

**Endpoint:** `GET /api/users/drivers`

**Query Parameters:**

- `page`, `limit`: Pagination
- `isVerified`: Filter by verification status

**Response:** `200 OK`

---

## 🔒 Phân quyền và Bảo mật

### Role-Based Access Control (RBAC)

| Role | Quyền hạn |
|------|-----------|
| **admin** | - Toàn quyền quản lý hệ thống<br>- Xem/Sửa/Xóa users<br>- Kích hoạt/vô hiệu hóa tài khoản<br>- Xem báo cáo thống kê |
| **user** | - Sử dụng dịch vụ vận chuyển<br>- Cập nhật profile<br>- Xem lịch sử đơn hàng |
| **driver** | - Nhận đơn hàng<br>- Cập nhật thông tin xe/bằng lái<br>- Xem lịch sử chuyến đi |

### Authentication Flow

```
1. User gửi phone + password
2. Server verify credentials
3. Server tạo JWT token (payload: userId, role)
4. Client lưu token (localStorage/sessionStorage)
5. Mỗi request gửi kèm token trong header:
   Authorization: Bearer <token>
6. Server verify token bằng middleware
7. Nếu valid, tiếp tục xử lý request
8. Nếu invalid/expired, trả về 401 Unauthorized
```

### JWT Token Structure

**Payload:**

```json
{
  "userId": "507f1f77bcf86cd799439011",
  "role": "user",
  "iat": 1704355200,
  "exp": 1704960000
}
```

**Configuration:**

- Secret: `process.env.JWT_SECRET` (phải đủ mạnh, >= 32 ký tự)
- Expiration: 7 ngày (có thể config qua `JWT_EXPIRE`)

### Security Best Practices

#### 1. Password Security

- **Hashing Algorithm**: Bcrypt với salt rounds = 10
- **Minimum Length**: 6 ký tự
- **Storage**: Chỉ lưu hash, không bao giờ lưu plaintext
- **Select False**: Password field không được return mặc định

#### 2. OTP Security

- **Random Generation**: Math.random() (6 digits)
- **Expiration**: 5 phút
- **Rate Limiting**: Tối đa 5 lần thử
- **One-time Use**: Mark `isUsed = true` sau khi verify
- **Auto Cleanup**: TTL index tự động xóa OTP expired

#### 3. API Security

- **CORS**: Chỉ cho phép frontend domain
- **Rate Limiting**: Cần implement (express-rate-limit)
- **Input Validation**: Express-validator cho tất cả endpoints
- **SQL Injection**: Không áp dụng (NoSQL - MongoDB)
- **NoSQL Injection**: Mongoose sanitization

#### 4. Environment Variables

Không bao giờ commit file `.env` vào git

```bash
# .gitignore
.env
.env.local
.env.production
```

---

## 📱 OTP System

### OTP Flow

#### Registration Flow

```
1. User nhập số điện thoại
2. Frontend gọi POST /api/auth/send-otp
3. Backend:
   - Validate phone
   - Kiểm tra phone chưa đăng ký
   - Generate OTP (6 digits)
   - Lưu vào database
   - Gửi SMS qua Twilio
4. User nhập OTP + thông tin đăng ký
5. Frontend gọi POST /api/auth/register
6. Backend:
   - Verify OTP
   - Nếu valid, tạo user mới
   - Trả về JWT token
```

#### Reset Password Flow

```
1. User nhập số điện thoại
2. Frontend gọi POST /api/auth/send-otp (purpose: 'reset-password')
3. Backend:
   - Validate phone
   - Kiểm tra user tồn tại
   - Generate & send OTP
4. User nhập OTP + password mới
5. Frontend gọi POST /api/auth/reset-password
6. Backend:
   - Verify OTP
   - Hash password mới
   - Update user password
```

### Twilio Integration

**Setup:**

1. Tạo tài khoản Twilio: https://www.twilio.com
2. Lấy credentials:
   - Account SID
   - Auth Token
   - Phone Number
3. Cấu hình trong `.env`:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

**Development Mode:**

Nếu không config Twilio, hệ thống sẽ chạy mock mode:

- OTP được log ra console
- Không gửi SMS thật
- OTP được return trong response (chỉ development)

---

## 🚀 Setup và Deployment

### Development Setup

#### 1. Clone Repository

```bash
git clone <repo-url>
cd Shipwayyyy/backend
```

#### 2. Install Dependencies

```bash
npm install
```

#### 3. Environment Configuration

Tạo file `.env`:

```bash
cp .env.template .env
```

Cập nhật các biến:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/shipway

# JWT
JWT_SECRET=your_very_long_and_secure_secret_key_here_at_least_32_chars

# OTP
OTP_EXPIRE_MINUTES=5

# Twilio (Optional for development)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Server
PORT=5000
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
```

#### 4. Seed Admin Account

```bash
npm run seed
```

Output:

```
✅ Admin account created successfully!
📱 Phone: +84987654321
🔑 Password: Admin@123456
👤 Name: Shipway Administrator
```

#### 5. Start Development Server

```bash
npm run dev
```

Server chạy tại: http://localhost:5000

### MongoDB Atlas Setup

#### 1. Tạo Cluster

1. Đăng ký tài khoản MongoDB Atlas: https://www.mongodb.com/cloud/atlas
2. Tạo cluster mới (Free tier M0 đủ cho development)
3. Chọn region gần nhất (Singapore cho VN)

#### 2. Database Access

1. Database Access → Add New Database User
2. Username: `shipway_admin`
3. Password: (auto-generate hoặc tự đặt)
4. Role: Atlas Admin

#### 3. Network Access

1. Network Access → Add IP Address
2. Development: `0.0.0.0/0` (Allow from anywhere)
3. Production: Chỉ IP của server

#### 4. Get Connection String

1. Clusters → Connect → Connect your application
2. Driver: Node.js
3. Version: 4.1 or later
4. Copy connection string:

```
mongodb+srv://shipway_admin:<password>@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority
```

5. Replace `<password>` với password thật
6. Replace `shipway` với tên database (mặc định: `shipway`)

### Production Deployment

#### Option 1: VPS (Ubuntu/CentOS)

**1. Setup Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2 (Process Manager)
sudo npm install -g pm2
```

**2. Deploy Application**

```bash
# Clone repository
git clone <repo-url>
cd Shipwayyyy/backend

# Install dependencies
npm install --production

# Create .env file
nano .env
# (paste production environment variables)

# Seed admin
npm run seed

# Start with PM2
pm2 start server.js --name shipway-api

# Auto-start on reboot
pm2 startup
pm2 save
```

**3. Setup Nginx Reverse Proxy**

```bash
# Install Nginx
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/shipway-api
```

```nginx
server {
    listen 80;
    server_name api.shipway.vn;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/shipway-api /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

**4. SSL Certificate (Let's Encrypt)**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d api.shipway.vn

# Auto-renewal
sudo certbot renew --dry-run
```

#### Option 2: Heroku

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create shipway-api

# Set environment variables
heroku config:set MONGODB_URI=your_mongodb_uri
heroku config:set JWT_SECRET=your_jwt_secret
heroku config:set NODE_ENV=production
# ... (set all env vars)

# Deploy
git push heroku main

# Seed admin
heroku run npm run seed
```

#### Option 3: Docker

**Dockerfile:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 5000

CMD ["node", "server.js"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - JWT_SECRET=${JWT_SECRET}
      - NODE_ENV=production
    restart: unless-stopped
```

**Deploy:**

```bash
docker-compose up -d
```

### Environment Variables Checklist

#### Required

- [x] `MONGODB_URI` - MongoDB connection string
- [x] `JWT_SECRET` - JWT secret key (>= 32 chars)
- [x] `PORT` - Server port (default: 5000)
- [x] `NODE_ENV` - Environment (development/production)

#### Optional

- [ ] `OTP_EXPIRE_MINUTES` - OTP expiration time
- [ ] `JWT_EXPIRE` - JWT expiration time
- [ ] `TWILIO_ACCOUNT_SID` - Twilio credentials
- [ ] `TWILIO_AUTH_TOKEN`
- [ ] `TWILIO_PHONE_NUMBER`
- [ ] `FRONTEND_URL` - CORS allowed origin
- [ ] `ADMIN_PHONE` - Default admin phone
- [ ] `ADMIN_PASSWORD` - Default admin password
- [ ] `ADMIN_NAME` - Default admin name

---

## 📊 API Testing

### Using Postman

Import collection: `docs/Shipway_API.postman_collection.json`

### Using cURL

**Register:**

```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84987654321", "purpose": "register"}'

curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "name": "Test User",
    "password": "password123",
    "role": "user",
    "otp": "123456"
  }'
```

**Login:**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84987654321", "password": "password123"}'
```

**Get Profile:**

```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error

```
Error: connect ECONNREFUSED
```

**Solution:**

- Kiểm tra `MONGODB_URI` trong `.env`
- Kiểm tra Network Access trong MongoDB Atlas
- Kiểm tra Database User credentials

#### 2. JWT Token Invalid

```
Token không hợp lệ hoặc đã hết hạn
```

**Solution:**

- Kiểm tra `JWT_SECRET` khớp giữa môi trường
- Đảm bảo token chưa hết hạn (7 ngày)
- Format header: `Authorization: Bearer <token>`

#### 3. OTP Not Received

**Solution:**

- Development mode: Check console log
- Production: Kiểm tra Twilio credentials
- Kiểm tra số điện thoại format (+84...)

#### 4. CORS Error

```
Access to fetch has been blocked by CORS policy
```

**Solution:**

- Cập nhật `FRONTEND_URL` trong `.env`
- Kiểm tra CORS config trong `server.js`

---

## 📈 Future Enhancements

### Phase 2 Features

- [ ] **Refresh Token**: Implement refresh token mechanism
- [ ] **Rate Limiting**: Add express-rate-limit
- [ ] **Email OTP**: Alternative to SMS OTP
- [ ] **Social Login**: Google, Facebook OAuth
- [ ] **File Upload**: Cloudinary integration for avatars
- [ ] **Notification System**: Push notifications
- [ ] **Audit Logs**: Track user activities
- [ ] **Analytics**: Dashboard statistics

### Phase 3 Features

- [ ] **Order Management**: CRUD for shipments
- [ ] **Real-time Tracking**: Socket.io for live tracking
- [ ] **Payment Integration**: VNPay, Momo
- [ ] **Review System**: Driver ratings & feedback
- [ ] **Route Optimization**: Google Maps API
- [ ] **Multi-language**: i18n support

---

## 📞 Support

Nếu có vấn đề kỹ thuật, vui lòng tạo issue trên GitHub hoặc liên hệ:

- **Email**: support@shipway.vn
- **Documentation**: https://docs.shipway.vn
- **API Docs**: https://api.shipway.vn/docs

---

## 📄 License

Copyright © 2025 Shipway Transportation Company. All rights reserved.

---

**Last Updated**: January 4, 2025  
**Version**: 1.0.0  
**Author**: Shipway Development Team

