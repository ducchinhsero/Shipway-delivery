# 🚀 MongoDB Atlas Quick Setup (5 phút)

## Bước 1: Đăng ký

1. Truy cập: https://www.mongodb.com/cloud/atlas/register
2. Đăng ký tài khoản miễn phí (có thể dùng Google)

## Bước 2: Tạo Cluster

1. Click **"Build a Database"**
2. Chọn **"M0 Free"** (0$ forever)
3. Chọn **Cloud Provider**: AWS
4. Chọn **Region**: Singapore (gần VN nhất)
5. Click **"Create"**
6. Đợi 3-5 phút cluster được tạo

## Bước 3: Tạo Database User

1. Trong tab **"Security" → "Database Access"**
2. Click **"Add New Database User"**
3. Authentication Method: **Password**
4. Username: `shipway_admin`
5. Password: Click **"Autogenerate Secure Password"** (copy password này)
6. Database User Privileges: **"Read and write to any database"**
7. Click **"Add User"**

## Bước 4: Whitelist IP

1. Trong tab **"Security" → "Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

> ⚠️ Note: Trong production, chỉ whitelist IP cụ thể

## Bước 5: Lấy Connection String

1. Click **"Database"** (menu bên trái)
2. Click **"Connect"** trên cluster của bạn
3. Chọn **"Connect your application"**
4. Driver: **Python** | Version: **3.12 or later**
5. Copy **Connection String**:

```
mongodb+srv://shipway_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

6. Thay `<password>` bằng password bạn đã copy ở bước 3

## Bước 6: Cập nhật .env

File: `backend-python/.env`

```env
# MongoDB Atlas
MONGO_URI=mongodb+srv://shipway_admin:YOUR_PASSWORD_HERE@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=shipway

# JWT Security
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256

# OTP
OTP_EXPIRE_MINUTES=5
OTP_MAX_ATTEMPTS=5

# Twilio (Optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## Bước 7: Restart Server

```bash
# Stop server (Ctrl+C)
# Start lại
python run.py
```

## Bước 8: Verify

Khi server start, bạn phải thấy:

```
✅ Connected to MongoDB: shipway
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Bước 9: Test API

1. Mở browser: http://localhost:8000/docs
2. Test endpoint **POST /api/v1/auth/send-otp**
3. Hoặc từ frontend, nhấn "Nhận OTP"

Lần này phải thành công! ✅

## 🎯 Bonus: View Data trong Atlas

1. Click **"Browse Collections"** trong MongoDB Atlas
2. Xem database `shipway`
3. Xem collections: `users`, `otps`
4. Có thể add/edit/delete data trực tiếp

---

**Done! MongoDB Atlas ready! 🚀**
