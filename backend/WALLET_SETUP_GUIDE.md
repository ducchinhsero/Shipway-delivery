# 💰 Wallet & Payment System - Setup Guide

**Version**: 1.0  
**Date**: 12/01/2026

---

## 📋 Tổng Quan

Hệ thống Wallet & Payment đã được triển khai đầy đủ với các tính năng:
- ✅ Xem số dư và thống kê ví
- ✅ Lịch sử giao dịch có phân trang
- ✅ Nạp tiền qua QR code (VietQR)
- ✅ Nạp tiền qua Momo/VNPay
- ✅ Webhook để verify payment

---

## 🚀 Quick Start

### **Bước 1: Setup Backend**

```powershell
# 1. Đổi tên folder (nếu chưa)
cd D:\Coding\Shipwayyyy
Rename-Item "backend-python" "backend"

# 2. Tạo virtual environment
cd backend
python -m venv venv

# 3. Kích hoạt venv
.\venv\Scripts\Activate

# 4. Cài đặt dependencies
pip install -r requirements.txt

# 5. Chạy server
python run.py
```

**Server sẽ chạy tại**: `http://localhost:8000`  
**Swagger Docs**: `http://localhost:8000/docs`

---

### **Bước 2: Test API**

```powershell
# Chạy test script tự động
.\test-wallet-api.ps1
```

Script sẽ test tất cả endpoints:
1. ✅ Đăng ký user
2. ✅ Login
3. ✅ Xem wallet
4. ✅ Tạo top-up request (QR)
5. ✅ Verify payment
6. ✅ Kiểm tra balance sau khi nạp
7. ✅ Xem transaction history
8. ✅ Test validation errors
9. ✅ Test Momo payment

---

## 📁 Files Created

### **1. Backend Files**

```
backend/
├── app/
│   ├── db/
│   │   └── models.py                      # ✅ Added wallet functions
│   ├── schemas/
│   │   └── wallet.py                      # ✅ NEW
│   ├── services/
│   │   └── payment_service.py             # ✅ NEW
│   └── api/v1/
│       ├── wallet.py                      # ✅ NEW
│       └── router.py                      # ✅ Updated
├── requirements.txt                        # ✅ Updated (added qrcode, Pillow)
├── test-wallet-api.ps1                    # ✅ NEW - Test script
├── WALLET_API_DOCUMENTATION.md            # ✅ NEW - API docs
└── WALLET_SETUP_GUIDE.md                  # ✅ NEW - This file
```

---

## 🔧 Configuration

### **Environment Variables**

Thêm vào `.env` (nếu cần):

```env
# Bank Account for QR Code
BANK_ID=970422
BANK_NAME=MB Bank
BANK_ACCOUNT_NO=0123456789
BANK_ACCOUNT_NAME=CONG TY SHIPWAY

# Momo Configuration
MOMO_PARTNER_CODE=your_partner_code
MOMO_ACCESS_KEY=your_access_key
MOMO_SECRET_KEY=your_secret_key

# VNPay Configuration
VNPAY_TMN_CODE=your_tmn_code
VNPAY_HASH_SECRET=your_hash_secret

# Payment Security
PAYMENT_SECRET_KEY=your_secret_key_here
```

---

## 📡 API Endpoints

### **Wallet Endpoints**

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/wallet` | Xem thông tin ví | ✅ |
| GET | `/api/v1/wallet/transactions` | Lịch sử giao dịch | ✅ |
| POST | `/api/v1/wallet/topup` | Tạo yêu cầu nạp tiền | ✅ |
| POST | `/api/v1/wallet/verify-payment` | Verify payment (webhook) | ❌ |

---

## 🧪 Manual Testing

### **Test 1: View Wallet**

```bash
# Login first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"+84123456789","password":"Test@123"}' \
  | jq -r '.access_token')

# Get wallet info
curl -s http://localhost:8000/api/v1/wallet \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Expected Output**:
```json
{
  "success": true,
  "wallet": {
    "user_id": "...",
    "balance": 0,
    "total_topup": 0,
    "total_usage": 0,
    "pending_transactions": 0,
    "recent_transactions": []
  }
}
```

---

### **Test 2: Create Top-Up (QR Code)**

```bash
curl -s -X POST http://localhost:8000/api/v1/wallet/topup \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "payment_method": "qr"
  }' | jq
```

**Expected Output**:
```json
{
  "success": true,
  "message": "Top-up request created successfully",
  "transaction_id": "...",
  "payment_id": "SW20260112...",
  "amount": 100000,
  "payment_method": "qr",
  "qr_code": "data:image/png;base64,...",
  "bank_info": {
    "bank_name": "MB Bank",
    "account_no": "0123456789",
    "account_name": "CONG TY SHIPWAY",
    "branch": "Ho Chi Minh",
    "amount": 100000,
    "content": "Nap tien Shipway SW20260112..."
  },
  "expires_at": "..."
}
```

**QR Code**: Copy base64 string và paste vào browser để xem QR code!

---

### **Test 3: Verify Payment**

```bash
# Save payment_id from previous step
PAYMENT_ID="SW20260112..."

# Simulate successful payment
curl -s -X POST http://localhost:8000/api/v1/wallet/verify-payment \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "'$PAYMENT_ID'",
    "status": "success",
    "transaction_code": "FT12345678"
  }' | jq
```

**Expected Output**:
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "transaction_id": "...",
  "new_balance": 100000
}
```

---

### **Test 4: Check Updated Balance**

```bash
curl -s http://localhost:8000/api/v1/wallet \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Expected**: `balance` should be 100,000 VND now!

---

### **Test 5: View Transaction History**

```bash
curl -s http://localhost:8000/api/v1/wallet/transactions \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Expected Output**:
```json
{
  "success": true,
  "total": 1,
  "transactions": [
    {
      "_id": "...",
      "user_id": "...",
      "amount": 100000,
      "type": "topup",
      "description": "Nạp tiền qua qr",
      "status": "completed",
      "payment_id": "SW20260112...",
      "payment_method": "qr",
      "created_at": "...",
      "updated_at": "...",
      "completed_at": "..."
    }
  ]
}
```

---

## 🎨 Frontend Integration

### **API Client Updates**

Thêm vào `shared/api.js`:

```javascript
// Wallet APIs
export const getWallet = async () => {
  return await apiRequest(API_CONFIG.ENDPOINTS.GET_WALLET);
};

export const getTransactions = async (limit = 50, skip = 0, type = null) => {
  let url = `${API_CONFIG.ENDPOINTS.GET_TRANSACTIONS}?limit=${limit}&skip=${skip}`;
  if (type) url += `&transaction_type=${type}`;
  return await apiRequest(url);
};

export const createTopUp = async (amount, paymentMethod) => {
  return await apiRequest(API_CONFIG.ENDPOINTS.CREATE_TOPUP, {
    method: 'POST',
    body: { amount, payment_method: paymentMethod }
  });
};
```

### **Config Updates**

Thêm vào `frontend/config/env.js`:

```javascript
ENDPOINTS: {
  // ... existing endpoints
  
  // Wallet
  GET_WALLET: '/wallet',
  GET_TRANSACTIONS: '/wallet/transactions',
  CREATE_TOPUP: '/wallet/topup'
}
```

---

## 🔍 Troubleshooting

### **Problem 1: QR Code không hiển thị**

**Solution**: Kiểm tra dependencies:
```bash
pip list | grep -i qrcode
pip list | grep -i pillow
```

Nếu chưa có, install lại:
```bash
pip install qrcode[pil]==7.4.2 Pillow==10.2.0
```

---

### **Problem 2: Payment không được verify**

**Check**:
1. Transaction có tồn tại không? (check MongoDB)
2. Payment ID có đúng không?
3. Status phải là "pending" trước khi verify

**Debug**:
```bash
# Check transactions in MongoDB
mongo
use shipway
db.transactions.find({payment_id: "SW20260112..."})
```

---

### **Problem 3: Balance không update**

**Check**:
1. Transaction status = "completed"?
2. `add_credit_to_user()` có được gọi không?
3. Check MongoDB: `db.users.findOne({_id: ...}).credit_info`

---

## 📊 Database Monitoring

### **Check Transactions**

```javascript
// In MongoDB
db.transactions.find().sort({created_at: -1}).limit(10)
```

### **Check User Balance**

```javascript
db.users.findOne({phone: "+84123456789"}).credit_info
```

### **Pending Transactions**

```javascript
db.transactions.find({status: "pending"})
```

---

## 🚀 Next Steps

### **1. Frontend UI** (Pending)
- [ ] Tạo Wallet page
- [ ] Hiển thị QR code
- [ ] Transaction history table
- [ ] Top-up form

### **2. Production Setup**
- [ ] Thêm real bank account info
- [ ] Tích hợp Momo/VNPay API thật
- [ ] Setup webhook URLs
- [ ] Add signature verification
- [ ] Add rate limiting

### **3. Monitoring**
- [ ] Transaction status monitoring
- [ ] Auto-expire pending transactions
- [ ] Daily balance reconciliation
- [ ] Alert system

---

## 📚 Documentation

- **API Docs**: `WALLET_API_DOCUMENTATION.md`
- **Swagger UI**: `http://localhost:8000/docs`
- **Test Script**: `test-wallet-api.ps1`

---

## ✅ Checklist

- [x] Transaction model created
- [x] Wallet schemas created
- [x] Payment service created
- [x] API endpoints implemented
- [x] QR code generation working
- [x] Payment verification working
- [x] Test script created
- [x] Documentation written
- [ ] Frontend integration
- [ ] Production deployment

---

**Status**: ✅ Backend Complete - Ready for Testing  
**Next**: Frontend Integration  
**Last Updated**: 12/01/2026
