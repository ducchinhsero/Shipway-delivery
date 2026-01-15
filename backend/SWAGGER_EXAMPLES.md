# 📚 Swagger API Examples

Tài liệu này cung cấp các ví dụ request/response cho từng API endpoint.

## 🔐 Authentication APIs

### 1. Send OTP

**Request:**

```json
POST /api/v1/auth/send-otp

{
  "phone": "+84123456789",
  "purpose": "register"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "OTP đã được gửi thành công",
  "expires_at": "2024-01-15T10:35:00",
  "otp": "123456"
}
```

> Note: Field `otp` chỉ xuất hiện trong development mode.

---

### 2. Verify OTP

**Request:**

```json
POST /api/v1/auth/verify-otp

{
  "phone": "+84123456789",
  "otp": "123456",
  "purpose": "register"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "OTP xác thực thành công"
}
```

**Response (Failed - Wrong OTP):**

```json
{
  "success": false,
  "message": "OTP không đúng. Còn 3 lần thử",
  "remaining_attempts": 3
}
```

---

### 3. Register

**Request:**

```json
POST /api/v1/auth/register

{
  "phone": "+84123456789",
  "name": "Nguyễn Văn A",
  "password": "123456",
  "otp": "123456",
  "role": "user",
  "email": "user@example.com"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Đăng ký thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYzEyMzQ1Njc4OTBhYmNkZWYwMTIzIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MDUwNTQ4MDB9.abc123def456",
  "user": {
    "_id": "65bc1234567890abcdef0123",
    "phone": "+84123456789",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "user@example.com",
    "is_active": true,
    "is_phone_verified": true,
    "avatar": null,
    "driver_info": null,
    "company_info": null,
    "last_login": "2024-01-15T10:30:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

### 4. Login

**Request:**

```json
POST /api/v1/auth/login

{
  "phone": "+84123456789",
  "password": "123456"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Đăng nhập thành công",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "65bc1234567890abcdef0123",
    "phone": "+84123456789",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "user@example.com",
    "is_active": true,
    "is_phone_verified": true,
    "avatar": null,
    "last_login": "2024-01-15T11:00:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

**Response (Failed - Wrong Password):**

```json
{
  "detail": "Mật khẩu không chính xác"
}
```

---

### 5. Reset Password

**Request:**

```json
POST /api/v1/auth/reset-password

{
  "phone": "+84123456789",
  "otp": "123456",
  "new_password": "newpass123"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Đặt lại mật khẩu thành công"
}
```

---

### 6. Get Current User (Protected)

**Request:**

```http
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Success):**

```json
{
  "success": true,
  "user": {
    "_id": "65bc1234567890abcdef0123",
    "phone": "+84123456789",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "user@example.com",
    "is_active": true,
    "is_phone_verified": true,
    "avatar": "https://example.com/avatar.jpg",
    "last_login": "2024-01-15T11:00:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

## 👤 User Management APIs

### 7. Update Profile (Protected)

**Request:**

```http
PUT /api/v1/user/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "name": "Nguyễn Văn B",
  "email": "newemail@example.com",
  "avatar": "https://example.com/new-avatar.jpg"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Cập nhật thông tin thành công",
  "user": {
    "_id": "65bc1234567890abcdef0123",
    "phone": "+84123456789",
    "name": "Nguyễn Văn B",
    "role": "user",
    "email": "newemail@example.com",
    "is_active": true,
    "is_phone_verified": true,
    "avatar": "https://example.com/new-avatar.jpg",
    "last_login": "2024-01-15T11:00:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:30:00"
  }
}
```

---

### 8. Get User Profile (Protected)

**Request:**

```http
GET /api/v1/user/profile/65bc1234567890abcdef0123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Success):**

```json
{
  "success": true,
  "user": {
    "_id": "65bc1234567890abcdef0123",
    "phone": "+84123456789",
    "name": "Nguyễn Văn A",
    "role": "user",
    "email": "user@example.com",
    "is_active": true,
    "is_phone_verified": true,
    "avatar": null,
    "last_login": "2024-01-15T11:00:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

## 🚨 Common Error Responses

### 400 Bad Request

```json
{
  "detail": "Số điện thoại đã được đăng ký"
}
```

### 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Tài khoản đã bị vô hiệu hóa"
}
```

### 404 Not Found

```json
{
  "detail": "Tài khoản không tồn tại"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "phone"],
      "msg": "Số điện thoại không hợp lệ",
      "type": "value_error"
    }
  ]
}
```

---

## 🔑 Authentication Flow Example

```
1. Send OTP for registration
   → POST /api/v1/auth/send-otp
   → Response: { "otp": "123456" }

2. Register with OTP
   → POST /api/v1/auth/register
   → Response: { "token": "eyJ..." }

3. Save token to localStorage/sessionStorage

4. Use token for protected requests
   → GET /api/v1/auth/me
   → Header: Authorization: Bearer eyJ...
   → Response: { "user": {...} }

5. Update profile
   → PUT /api/v1/user/profile
   → Header: Authorization: Bearer eyJ...
   → Response: { "user": {...} }
```

---

## 🧪 Test với cURL

### Register Flow

```bash
# Step 1: Send OTP
curl -X POST "http://localhost:8000/api/v1/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "purpose": "register"}'

# Step 2: Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "name": "Nguyen Van A",
    "password": "123456",
    "otp": "123456",
    "role": "user"
  }'

# Copy token from response
```

### Login and Access Protected Endpoint

```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "password": "123456"}' \
  | jq -r '.token')

# Get current user
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# Update profile
curl -X PUT "http://localhost:8000/api/v1/user/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "email": "new@example.com"}'
```

---

**Swagger UI**: http://localhost:8000/docs

**ReDoc**: http://localhost:8000/redoc
