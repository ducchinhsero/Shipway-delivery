# 🚀 Hướng dẫn Setup Shipway - Chi tiết từng bước

## 📌 Tổng quan

Tài liệu này hướng dẫn chi tiết cách setup và chạy dự án Shipway từ đầu. Thời gian ước tính: **15-20 phút**.

## 📋 Yêu cầu hệ thống

### Bắt buộc
- ✅ **Node.js** >= 18.x ([Download](https://nodejs.org/))
- ✅ **Git** ([Download](https://git-scm.com/))
- ✅ **MongoDB Atlas Account** (Free) ([Sign up](https://www.mongodb.com/cloud/atlas))

### Khuyến nghị
- ✅ **VS Code** với extensions:
  - Live Server
  - ESLint
  - MongoDB for VS Code
- ✅ **Postman** để test API ([Download](https://www.postman.com/))
- ✅ **MongoDB Compass** để xem database ([Download](https://www.mongodb.com/products/compass))

## 🎯 Bước 1: Clone Repository

```bash
# Clone project
git clone <repository-url>
cd Shipwayyyy

# Kiểm tra cấu trúc
dir  # Windows
ls   # Mac/Linux
```

Bạn sẽ thấy:
```
├── backend/
├── frontend/
├── docs/
├── README.md
└── ...
```

## 🗄️ Bước 2: Setup MongoDB Atlas

### 2.1. Tạo tài khoản

1. Truy cập: https://www.mongodb.com/cloud/atlas/register
2. Đăng ký với email hoặc Google account
3. Xác nhận email

### 2.2. Tạo Organization & Project

1. Sau khi login, click **"New Project"**
2. Project Name: `shipway`
3. Click **"Next"** → **"Create Project"**

### 2.3. Tạo Database Cluster

1. Click **"Build a Database"**
2. Chọn **"FREE"** (M0 Sandbox)
3. **Cloud Provider**: AWS
4. **Region**: `ap-southeast-1` (Singapore) - Gần VN nhất
5. **Cluster Name**: `Cluster0` (hoặc tùy chọn)
6. Click **"Create"**

⏱️ Đợi 3-5 phút để cluster khởi tạo...

### 2.4. Tạo Database User

Khi cluster sẵn sàng, màn hình **Security Quickstart** hiện ra:

1. **Authentication Method**: Username and Password
2. **Username**: `shipway_admin`
3. **Password**: Click **"Autogenerate Secure Password"**
4. ⚠️ **COPY VÀ LƯU PASSWORD** vào notepad
5. Click **"Create User"**

### 2.5. Whitelist IP Address

1. Mục **"Where would you like to connect from?"**
2. Click **"Add My Current IP Address"**
3. Hoặc để development: Add IP `0.0.0.0/0` (Allow all)
4. Click **"Finish and Close"**

### 2.6. Lấy Connection String

1. Click **"Connect"** trên cluster
2. Chọn **"Drivers"**
3. Driver: **Node.js**, Version: **4.1 or later**
4. Copy connection string:

```
mongodb+srv://shipway_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

5. **QUAN TRỌNG**: 
   - Thay `<password>` bằng password thật
   - Thêm `/shipway` sau `.net` để chỉ định database name

Kết quả cuối cùng:
```
mongodb+srv://shipway_admin:YourPassword123@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority
```

📝 **Lưu connection string này**, bạn sẽ cần ở bước sau!

## 🔧 Bước 3: Setup Backend

### 3.1. Install Dependencies

```bash
cd backend
npm install
```

Đợi npm install xong (khoảng 1-2 phút)...

### 3.2. Tạo file .env

**Windows:**
```bash
copy .env.template .env
```

**Mac/Linux:**
```bash
cp .env.template .env
```

### 3.3. Cấu hình .env

Mở file `backend/.env` bằng text editor và cập nhật:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# MongoDB Configuration
MONGODB_URI=mongodb+srv://shipway_admin:YourPassword123@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority

# JWT Configuration
JWT_SECRET=shipway_super_secret_key_minimum_32_characters_long_for_security
JWT_EXPIRE=7d

# OTP Configuration
OTP_EXPIRE_MINUTES=5

# Twilio Configuration (Optional - để trống nếu chưa có)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Admin Default Credentials
ADMIN_PHONE=+84987654321
ADMIN_PASSWORD=Admin@123456
ADMIN_NAME=Shipway Administrator
```

⚠️ **Quan trọng**:
- `MONGODB_URI`: Paste connection string từ bước 2.6
- `JWT_SECRET`: Phải >= 32 ký tự (đã có sẵn trong template)
- `TWILIO_*`: Để trống nếu chưa có tài khoản Twilio (OTP sẽ hiển thị trong console)

### 3.4. Seed Database

Tạo tài khoản admin mặc định:

```bash
npm run seed
```

Kết quả:
```
✅ MongoDB Connected: cluster0-shard-00-00.xxxxx.mongodb.net
📊 Database Name: shipway
✅ Admin account created successfully!
📱 Phone: +84987654321
🔑 Password: Admin@123456
👤 Name: Shipway Administrator

⚠️ Please change the default password after first login!
```

### 3.5. Chạy Backend Server

```bash
npm run dev
```

Kết quả:
```
✅ MongoDB Connected: cluster0...
📊 Database Name: shipway
🚀 Server is running on port 5000
🌍 Environment: development
```

✅ **Backend đã sẵn sàng!**

Để test, mở browser: http://localhost:5000/api/health

Bạn sẽ thấy:
```json
{
  "status": "OK",
  "message": "Shipway API is running",
  "timestamp": "2025-01-04T..."
}
```

## 💻 Bước 4: Setup Frontend

### 4.1. Mở terminal mới

Giữ backend server chạy, mở terminal/command prompt mới

### 4.2. Kiểm tra config

Mở file `frontend/config/env.js`:

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:5000/api',  // ✅ Đúng
  // ...
};
```

Nếu backend chạy ở port khác, cập nhật `BASE_URL`.

### 4.3. Chạy Frontend

**Option A: VS Code Live Server (Khuyến nghị)**

1. Mở VS Code
2. Install extension: **Live Server** (by Ritwick Dey)
3. Right-click file `frontend/index.html`
4. Chọn **"Open with Live Server"**
5. Browser tự động mở tại http://localhost:5500 hoặc http://127.0.0.1:5500

**Option B: Python HTTP Server**

```bash
cd frontend
python -m http.server 3000
```

Mở browser: http://localhost:3000

**Option C: Node.js http-server**

```bash
cd frontend
npx http-server -p 3000
```

Mở browser: http://localhost:3000

✅ **Frontend đã sẵn sàng!**

## 🧪 Bước 5: Test hệ thống

### 5.1. Test Login với Admin

1. Mở frontend: http://localhost:3000
2. Nhập:
   - **Số điện thoại**: `987654321` (hoặc `+84987654321`)
   - **Mật khẩu**: `Admin@123456`
3. Click **"Đăng nhập"**

Nếu thành công, bạn sẽ được redirect (hiện tại sẽ lỗi 404 vì chưa có dashboard page - đây là bình thường)

### 5.2. Test Đăng ký User mới

1. Click **"Chưa có tài khoản? Đăng ký"**
2. Chọn role: **"Đối tác vận chuyển"**
3. Nhập số điện thoại: `0123456789`
4. Click **"Gửi mã OTP"**
5. Mở **Browser Console** (F12) để xem OTP:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 MÃ OTP ĐÃ ĐƯỢC GỬI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Số điện thoại: +840123456789
   🔐 Mã OTP: 123456
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

6. Nhập OTP vào form
7. Nhập **Họ và tên** và **Mật khẩu**
8. Click **"Đăng ký"**

Nếu thành công: "Đăng ký thành công" → Chuyển về màn hình login

### 5.3. Test API với cURL

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"phone\": \"+84987654321\", \"password\": \"Admin@123456\"}"
```

(Trên Mac/Linux, thay `^` bằng `\`)

### 5.4. Verify Database

1. Mở MongoDB Atlas Dashboard
2. Click **"Browse Collections"**
3. Bạn sẽ thấy:
   - Database: `shipway`
   - Collection: `users` (có 2 documents: admin + user mới)
   - Collection: `otps` (có thể trống hoặc có OTP chưa expire)

## ✅ Hoàn thành!

Bạn đã setup thành công:
- ✅ Backend API chạy tại http://localhost:5000
- ✅ Frontend chạy tại http://localhost:3000 (hoặc 5500)
- ✅ MongoDB Atlas database
- ✅ Admin account
- ✅ Test user account

## 🔧 Troubleshooting

### Backend không chạy

**Lỗi: "Error connecting to MongoDB"**

**Nguyên nhân**: Connection string sai hoặc IP chưa được whitelist

**Giải pháp**:
1. Kiểm tra `MONGODB_URI` trong `.env`
2. Đảm bảo đã thay `<password>` bằng password thật
3. Đảm bảo có `/shipway` sau `.net`
4. Vào MongoDB Atlas → Network Access → Add IP `0.0.0.0/0`

---

**Lỗi: "Port 5000 already in use"**

**Giải pháp**:

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Mac/Linux:
```bash
lsof -ti:5000 | xargs kill -9
```

Hoặc đổi PORT trong `.env`:
```env
PORT=5001
```

---

**Lỗi: "JWT_SECRET must be at least 32 characters"**

**Giải pháp**: Cập nhật `JWT_SECRET` trong `.env` với chuỗi >= 32 ký tự

### Frontend không kết nối được Backend

**Lỗi: CORS error trong console**

**Giải pháp**:
1. Kiểm tra `FRONTEND_URL` trong `backend/.env`
2. Restart backend server
3. Đảm bảo backend đang chạy

---

**Lỗi: "Failed to fetch"**

**Giải pháp**:
1. Kiểm tra `BASE_URL` trong `frontend/config/env.js`
2. Đảm bảo backend đang chạy tại URL đó
3. Mở http://localhost:5000/api/health để verify

### OTP không nhận được

**Development mode**: OTP được log ra console (F12)

**Production**: Cần cấu hình Twilio:
1. Đăng ký tài khoản Twilio
2. Lấy Account SID, Auth Token, Phone Number
3. Cập nhật trong `.env`
4. Restart backend

### MongoDB Atlas

**Lỗi: "Authentication failed"**

**Giải pháp**:
1. Vào Database Access trong Atlas
2. Edit user `shipway_admin`
3. Reset password
4. Cập nhật `.env` với password mới

---

**Lỗi: "Connection timeout"**

**Giải pháp**:
1. Vào Network Access trong Atlas
2. Add IP `0.0.0.0/0` (cho development)
3. Hoặc add IP hiện tại của bạn

## 📚 Tài liệu tham khảo

- [README.md](README.md) - Tổng quan dự án
- [QUICKSTART.md](docs/QUICKSTART.md) - Quick start 10 phút
- [BACKEND_DOCUMENTATION.md](docs/BACKEND_DOCUMENTATION.md) - Chi tiết Backend
- [MONGODB_ATLAS_SETUP.md](docs/MONGODB_ATLAS_SETUP.md) - Chi tiết MongoDB
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Cấu trúc dự án

## 🆘 Cần giúp đỡ?

1. Đọc [Troubleshooting](#troubleshooting) ở trên
2. Kiểm tra logs:
   - Backend: Terminal chạy `npm run dev`
   - Frontend: Browser Console (F12)
3. Kiểm tra MongoDB Atlas: Browse Collections
4. Tạo issue trên GitHub với:
   - Mô tả lỗi
   - Screenshots
   - Logs/Error messages

## 🎉 Next Steps

Sau khi setup xong:

1. **Explore API**: Dùng Postman test các endpoints
2. **Customize**: Chỉnh sửa UI, thêm features
3. **Deploy**: Đọc deployment guides trong docs
4. **Twilio**: Setup SMS OTP thật
5. **Dashboard**: Tạo dashboard pages cho từng role

---

**Last Updated**: January 4, 2025  
**Estimated Time**: 15-20 minutes  
**Difficulty**: Beginner-friendly ⭐⭐

**Good luck! 🚀**

