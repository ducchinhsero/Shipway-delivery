# 📡 API Examples - Shipway

Tài liệu này cung cấp các ví dụ cụ thể để test API của Shipway.

## 🔧 Setup

### Base URL
```
Development: http://localhost:5000/api
Production: https://api.shipway.vn/api
```

### Headers
```
Content-Type: application/json
Authorization: Bearer <token>  // For protected routes
```

## 📝 Examples

### 1. Health Check

**Request:**
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "OK",
  "message": "Shipway API is running",
  "timestamp": "2025-01-04T10:30:00.000Z"
}
```

---

### 2. Send OTP (Register)

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "purpose": "register"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expiresAt": "2025-01-04T10:35:00.000Z",
  "otp": "123456"
}
```

**Note**: `otp` chỉ hiển thị trong development mode

---

### 3. Verify OTP

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "otp": "123456",
    "purpose": "register"
  }'
```

**Response (Success):**
```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

**Response (Failed):**
```json
{
  "success": false,
  "message": "OTP không đúng. Còn 4 lần thử",
  "remainingAttempts": 4
}
```

---

### 4. Register User

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "password": "password123",
    "role": "user",
    "otp": "123456"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Đăng ký thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "isActive": true,
    "isPhoneVerified": true,
    "createdAt": "2025-01-04T10:30:00.000Z",
    "updatedAt": "2025-01-04T10:30:00.000Z"
  }
}
```

---

### 5. Login

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Đăng nhập thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "lastLogin": "2025-01-04T10:30:00.000Z"
  }
}
```

---

### 6. Send OTP (Reset Password)

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "purpose": "reset-password"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expiresAt": "2025-01-04T10:35:00.000Z"
}
```

---

### 7. Reset Password

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84987654321",
    "otp": "123456",
    "newPassword": "newpassword123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Đặt lại mật khẩu thành công"
}
```

---

### 8. Get Current User (Protected)

**Request:**
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**
```json
{
  "success": true,
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": null,
    "isActive": true,
    "isPhoneVerified": true,
    "avatar": null,
    "lastLogin": "2025-01-04T10:30:00.000Z",
    "createdAt": "2025-01-04T10:00:00.000Z",
    "updatedAt": "2025-01-04T10:30:00.000Z"
  }
}
```

---

### 9. Get Profile (Protected)

**Request:**
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <token>"
```

**Response:** (Same as Get Current User)

---

### 10. Update Profile (Protected)

**Request:**
```bash
curl -X PUT http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyễn Văn B",
    "email": "nguyenvanb@example.com",
    "companyInfo": {
      "companyName": "ABC Company",
      "taxCode": "0123456789",
      "address": "123 Đường ABC, TP.HCM"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Cập nhật thông tin thành công",
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn B",
    "email": "nguyenvanb@example.com",
    "companyInfo": {
      "companyName": "ABC Company",
      "taxCode": "0123456789",
      "address": "123 Đường ABC, TP.HCM"
    }
  }
}
```

---

### 11. Update Driver Info (Driver Only)

**Request:**
```bash
curl -X PUT http://localhost:5000/api/users/driver/info \
  -H "Authorization: Bearer <driver_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "licenseNumber": "B2-12345678",
    "vehicleType": "motorbike",
    "vehiclePlate": "29A-12345"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Cập nhật thông tin tài xế thành công",
  "user": {
    "_id": "...",
    "phone": "+84123456789",
    "name": "Tài Xế A",
    "role": "driver",
    "driverInfo": {
      "licenseNumber": "B2-12345678",
      "vehicleType": "motorbike",
      "vehiclePlate": "29A-12345",
      "isVerified": false,
      "rating": 0,
      "totalTrips": 0
    }
  }
}
```

---

### 12. Get All Users (Admin Only)

**Request:**
```bash
curl -X GET "http://localhost:5000/api/users?page=1&limit=10&role=user" \
  -H "Authorization: Bearer <admin_token>"
```

**Response:**
```json
{
  "success": true,
  "users": [
    {
      "_id": "...",
      "phone": "+84987654321",
      "name": "User 1",
      "role": "user",
      "isActive": true,
      "createdAt": "..."
    },
    {
      "_id": "...",
      "phone": "+84987654322",
      "name": "User 2",
      "role": "user",
      "isActive": true,
      "createdAt": "..."
    }
  ],
  "totalPages": 5,
  "currentPage": 1,
  "total": 50
}
```

---

### 13. Get User by ID (Admin Only)

**Request:**
```bash
curl -X GET http://localhost:5000/api/users/65a1b2c3d4e5f6g7h8i9j0k1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response:**
```json
{
  "success": true,
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "user@example.com",
    "isActive": true,
    "isPhoneVerified": true,
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

---

### 14. Update User Status (Admin Only)

**Request:**
```bash
curl -X PUT http://localhost:5000/api/users/65a1b2c3d4e5f6g7h8i9j0k1/status \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "isActive": false
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Cập nhật trạng thái thành công",
  "user": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "phone": "+84987654321",
    "name": "Nguyễn Văn A",
    "isActive": false
  }
}
```

---

### 15. Delete User (Admin Only)

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/users/65a1b2c3d4e5f6g7h8i9j0k1 \
  -H "Authorization: Bearer <admin_token>"
```

**Response:**
```json
{
  "success": true,
  "message": "Xóa người dùng thành công"
}
```

---

### 16. Get All Drivers (Admin Only)

**Request:**
```bash
curl -X GET "http://localhost:5000/api/users/drivers?page=1&limit=10&isVerified=true" \
  -H "Authorization: Bearer <admin_token>"
```

**Response:**
```json
{
  "success": true,
  "drivers": [
    {
      "_id": "...",
      "phone": "+84123456789",
      "name": "Tài Xế A",
      "role": "driver",
      "driverInfo": {
        "licenseNumber": "B2-12345678",
        "vehicleType": "motorbike",
        "vehiclePlate": "29A-12345",
        "isVerified": true,
        "rating": 4.5,
        "totalTrips": 100
      },
      "createdAt": "..."
    }
  ],
  "totalPages": 3,
  "currentPage": 1,
  "total": 30
}
```

---

## 🔴 Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Vui lòng điền đầy đủ thông tin",
  "errors": [
    {
      "field": "phone",
      "message": "Số điện thoại là bắt buộc"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Không có quyền truy cập. Vui lòng đăng nhập"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Role 'user' không có quyền truy cập tài nguyên này"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Tài khoản không tồn tại"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Lỗi server",
  "stack": "..." // Only in development
}
```

---

## 🧪 Testing Workflow

### 1. Register Flow

```bash
# Step 1: Send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "purpose": "register"}'

# Step 2: Register with OTP
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "name": "Test User",
    "password": "test123",
    "role": "user",
    "otp": "123456"
  }'
```

### 2. Login Flow

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "password": "test123"}'

# Save token from response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Get profile
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Reset Password Flow

```bash
# Step 1: Send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "purpose": "reset-password"}'

# Step 2: Reset password
curl -X POST http://localhost:5000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "otp": "123456",
    "newPassword": "newpassword123"
  }'

# Step 3: Login with new password
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "password": "newpassword123"}'
```

---

## 📦 Postman Collection

Import this JSON to Postman:

```json
{
  "info": {
    "name": "Shipway API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000/api"
    },
    {
      "key": "token",
      "value": ""
    }
  ]
}
```

---

## 💡 Tips

### Windows CMD
Sử dụng `^` để xuống dòng:
```cmd
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"phone\": \"+84987654321\", \"password\": \"Admin@123456\"}"
```

### PowerShell
Sử dụng backtick `` ` ``:
```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"phone": "+84987654321", "password": "Admin@123456"}'
```

### Mac/Linux
Sử dụng `\`:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84987654321", "password": "Admin@123456"}'
```

---

**Last Updated**: January 4, 2025  
**Version**: 1.0.0

