# 💰 Wallet & Payment API Documentation

**Version**: 1.0  
**Base URL**: `http://localhost:8000/api/v1`  
**Date**: 12/01/2026

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Payment Methods](#payment-methods)
5. [Testing Guide](#testing-guide)
6. [Error Codes](#error-codes)

---

## 🎯 Overview

Hệ thống Wallet & Payment cho phép người dùng:
- ✅ Xem số dư tài khoản
- ✅ Xem lịch sử giao dịch
- ✅ Nạp tiền qua QR code (VietQR)
- ✅ Nạp tiền qua Momo, VNPay
- ✅ Tự động cộng tiền sau khi thanh toán

---

## 🔐 Authentication

Tất cả endpoints (trừ `verify-payment`) yêu cầu JWT token:

```http
Authorization: Bearer <your_jwt_token>
```

---

## 📡 Endpoints

### 1. Get Wallet Info

**Endpoint**: `GET /api/v1/wallet`  
**Auth**: Required  
**Description**: Lấy thông tin ví và số dư

**Response 200**:
```json
{
  "success": true,
  "wallet": {
    "user_id": "60d5ec49f1b2c72b8c8e4f1a",
    "balance": 500000,
    "total_topup": 1000000,
    "total_usage": 500000,
    "pending_transactions": 0,
    "recent_transactions": [
      {
        "_id": "...",
        "user_id": "...",
        "amount": 100000,
        "type": "topup",
        "description": "Nạp tiền qua qr",
        "status": "completed",
        "payment_id": "SW20260112120000ABCD",
        "payment_method": "qr",
        "created_at": "2026-01-12T08:00:00Z",
        "updated_at": "2026-01-12T08:05:00Z",
        "completed_at": "2026-01-12T08:05:00Z"
      }
    ]
  }
}
```

**Example**:
```bash
curl -X GET http://localhost:8000/api/v1/wallet \
  -H "Authorization: Bearer <token>"
```

---

### 2. Get Transaction History

**Endpoint**: `GET /api/v1/wallet/transactions`  
**Auth**: Required  
**Description**: Lấy lịch sử giao dịch

**Query Parameters**:
- `limit` (int, optional): Số lượng transactions (default: 50, max: 100)
- `skip` (int, optional): Bỏ qua N transactions (pagination)
- `transaction_type` (string, optional): Lọc theo loại (`topup`, `usage`, `refund`)

**Response 200**:
```json
{
  "success": true,
  "total": 25,
  "transactions": [
    {
      "_id": "...",
      "user_id": "...",
      "amount": 100000,
      "type": "topup",
      "description": "Nạp tiền qua qr",
      "status": "completed",
      "payment_id": "SW20260112120000ABCD",
      "payment_method": "qr",
      "payment_details": {
        "transaction_code": "FT12345678",
        "payment_time": "2026-01-12T08:05:00Z"
      },
      "created_at": "2026-01-12T08:00:00Z",
      "updated_at": "2026-01-12T08:05:00Z",
      "completed_at": "2026-01-12T08:05:00Z"
    }
  ]
}
```

**Example**:
```bash
# Lấy 20 transactions gần nhất
curl -X GET "http://localhost:8000/api/v1/wallet/transactions?limit=20" \
  -H "Authorization: Bearer <token>"

# Lấy transactions loại topup
curl -X GET "http://localhost:8000/api/v1/wallet/transactions?transaction_type=topup" \
  -H "Authorization: Bearer <token>"

# Pagination - trang 2
curl -X GET "http://localhost:8000/api/v1/wallet/transactions?limit=20&skip=20" \
  -H "Authorization: Bearer <token>"
```

---

### 3. Create Top-Up Request

**Endpoint**: `POST /api/v1/wallet/topup`  
**Auth**: Required  
**Description**: Tạo yêu cầu nạp tiền

**Request Body**:
```json
{
  "amount": 100000,
  "payment_method": "qr"
}
```

**Fields**:
- `amount` (int, required): Số tiền nạp (VND)
  - Min: 10,000 VND
  - Max: 100,000,000 VND
  - Phải chia hết cho 10,000
- `payment_method` (string, required): Phương thức thanh toán
  - `qr` hoặc `bank_transfer`: Chuyển khoản ngân hàng (có QR code)
  - `momo`: Ví Momo
  - `vnpay`: VNPay

**Response 200 (QR/Bank Transfer)**:
```json
{
  "success": true,
  "message": "Top-up request created successfully",
  "transaction_id": "60d5ec49f1b2c72b8c8e4f1b",
  "payment_id": "SW20260112120000ABCD",
  "amount": 100000,
  "payment_method": "qr",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "bank_info": {
    "bank_name": "MB Bank",
    "account_no": "0123456789",
    "account_name": "CONG TY SHIPWAY",
    "branch": "Ho Chi Minh",
    "amount": 100000,
    "content": "Nap tien Shipway SW20260112120000ABCD"
  },
  "expires_at": "2026-01-12T08:15:00Z"
}
```

**Response 200 (Momo/VNPay)**:
```json
{
  "success": true,
  "message": "Top-up request created successfully",
  "transaction_id": "60d5ec49f1b2c72b8c8e4f1b",
  "payment_id": "SW20260112120000ABCD",
  "amount": 100000,
  "payment_method": "momo",
  "payment_url": "https://test-payment.momo.vn/v2/gateway/pay?...",
  "qr_code": null,
  "bank_info": null,
  "expires_at": "2026-01-12T08:15:00Z"
}
```

**Error 400** (Invalid amount):
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "amount"],
      "msg": "Amount must be multiple of 10,000 VND"
    }
  ]
}
```

**Examples**:
```bash
# Nạp tiền qua QR code
curl -X POST http://localhost:8000/api/v1/wallet/topup \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "payment_method": "qr"
  }'

# Nạp tiền qua Momo
curl -X POST http://localhost:8000/api/v1/wallet/topup \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 200000,
    "payment_method": "momo"
  }'
```

---

### 4. Verify Payment (Webhook)

**Endpoint**: `POST /api/v1/wallet/verify-payment`  
**Auth**: Not required (public endpoint for payment gateways)  
**Description**: Xác nhận thanh toán (được gọi bởi payment gateway)

**Request Body**:
```json
{
  "payment_id": "SW20260112120000ABCD",
  "status": "success",
  "transaction_code": "FT12345678",
  "payment_time": "2026-01-12T08:05:00Z",
  "signature": "abc123..."
}
```

**Fields**:
- `payment_id` (string, required): Payment ID từ bước top-up
- `status` (string, required): `success` hoặc `failed`
- `transaction_code` (string, optional): Mã giao dịch từ ngân hàng
- `payment_time` (datetime, optional): Thời gian thanh toán
- `signature` (string, optional): Chữ ký bảo mật

**Response 200** (Success):
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "transaction_id": "60d5ec49f1b2c72b8c8e4f1b",
  "new_balance": 600000
}
```

**Response 200** (Failed):
```json
{
  "success": false,
  "message": "Payment failed"
}
```

**Response 200** (Not found):
```json
{
  "success": false,
  "message": "Transaction not found"
}
```

**Example**:
```bash
# Verify payment thành công
curl -X POST http://localhost:8000/api/v1/wallet/verify-payment \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "SW20260112120000ABCD",
    "status": "success",
    "transaction_code": "FT12345678",
    "payment_time": "2026-01-12T08:05:00Z"
  }'

# Verify payment thất bại
curl -X POST http://localhost:8000/api/v1/wallet/verify-payment \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "SW20260112120000ABCD",
    "status": "failed"
  }'
```

---

## 💳 Payment Methods

### 1. QR Code (VietQR)

**Cách hoạt động**:
1. User tạo top-up request
2. Backend generate QR code theo chuẩn VietQR
3. User scan QR bằng app ngân hàng
4. Chuyển khoản với nội dung chứa `payment_id`
5. Bank gửi webhook về backend (hoặc manual verify)
6. Backend cộng tiền vào tài khoản

**Ưu điểm**:
- ✅ Không cần tích hợp phức tạp
- ✅ Miễn phí
- ✅ Hỗ trợ hầu hết ngân hàng VN

**Nhược điểm**:
- ⚠️ Cần verify thủ công hoặc tích hợp bank API
- ⚠️ Thời gian xử lý chậm hơn

### 2. Momo

**Cách hoạt động**:
1. User tạo top-up request với `payment_method: "momo"`
2. Backend tạo payment URL qua Momo API
3. User được redirect đến Momo payment page
4. User thanh toán trên Momo
5. Momo gửi IPN (Instant Payment Notification) về backend
6. Backend verify và cộng tiền

**Ưu điểm**:
- ✅ Tự động verify
- ✅ Nhanh
- ✅ Phổ biến

**Nhược điểm**:
- ⚠️ Phí giao dịch
- ⚠️ Cần đăng ký merchant

### 3. VNPay

Tương tự Momo, dùng cho thẻ ATM/Credit card.

---

## 🧪 Testing Guide

### Setup

1. **Đổi tên folder backend**:
```bash
cd D:\Coding\Shipwayyyy
Rename-Item "backend-python" "backend"
```

2. **Cài đặt dependencies**:
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

3. **Chạy server**:
```bash
python run.py
# Server: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Test Flow

**1. Đăng ký/Đăng nhập**:
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "name": "Test User",
    "password": "Test@123",
    "role": "user",
    "otp": "123456"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "+84123456789",
    "password": "Test@123"
  }'

# Save token
TOKEN="<your_token_here>"
```

**2. Xem wallet**:
```bash
curl -X GET http://localhost:8000/api/v1/wallet \
  -H "Authorization: Bearer $TOKEN"
```

**3. Tạo top-up request**:
```bash
curl -X POST http://localhost:8000/api/v1/wallet/topup \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "payment_method": "qr"
  }'

# Save payment_id từ response
PAYMENT_ID="<payment_id_here>"
```

**4. Verify payment (simulate)**:
```bash
curl -X POST http://localhost:8000/api/v1/wallet/verify-payment \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "'$PAYMENT_ID'",
    "status": "success",
    "transaction_code": "FT12345678"
  }'
```

**5. Kiểm tra balance mới**:
```bash
curl -X GET http://localhost:8000/api/v1/wallet \
  -H "Authorization: Bearer $TOKEN"
```

**6. Xem transaction history**:
```bash
curl -X GET http://localhost:8000/api/v1/wallet/transactions \
  -H "Authorization: Bearer $TOKEN"
```

---

## ❌ Error Codes

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Pydantic validation failed |
| 500 | Internal Server Error | Server error |

**Common Validation Errors**:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "amount"],
      "msg": "Amount must be multiple of 10,000 VND",
      "input": 15000
    }
  ]
}
```

---

## 📊 Database Schema

### Transaction Collection

```javascript
{
  _id: ObjectId,
  user_id: String,
  amount: Number,
  type: String,  // topup, usage, refund
  description: String,
  status: String,  // pending, completed, failed, cancelled
  payment_id: String,
  payment_method: String,  // qr, bank_transfer, momo, vnpay
  payment_details: {
    transaction_code: String,
    payment_time: Date,
    expires_at: String
  },
  created_at: Date,
  updated_at: Date,
  completed_at: Date
}
```

### User.credit_info

```javascript
{
  credit_balance: Number,     // Số dư hiện tại
  total_credit_added: Number, // Tổng đã nạp
  total_credit_used: Number   // Tổng đã dùng
}
```

---

## 🚀 Production Considerations

### Security

1. **Webhook Signature Verification**:
   - Verify signature từ payment gateway
   - Prevent replay attacks

2. **Rate Limiting**:
   - Limit số lần tạo top-up request
   - Prevent abuse

3. **Amount Validation**:
   - Min/Max limits
   - Multiple of 10,000 VND

### Monitoring

1. **Transaction Status**:
   - Monitor pending transactions
   - Auto-expire after 15 minutes
   - Alert for failed transactions

2. **Balance Reconciliation**:
   - Daily balance check
   - Compare with transaction history

---

## 📞 Support

**Documentation**: `/docs` (Swagger UI)  
**API Version**: v1  
**Last Updated**: 12/01/2026
