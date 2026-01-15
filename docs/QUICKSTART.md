# ⚡ Quick Start - Shipway

Hướng dẫn nhanh để chạy dự án Shipway trong 10 phút.

## 📋 Prerequisites

- ✅ Node.js >= 18.x
- ✅ Git
- ✅ MongoDB Atlas account
- ✅ Text editor (VS Code recommended)

## 🚀 Setup trong 10 phút

### Step 1: Clone Repository (1 phút)

```bash
git clone <repository-url>
cd Shipwayyyy
```

### Step 2: Setup MongoDB Atlas (3 phút)

1. Truy cập: https://www.mongodb.com/cloud/atlas
2. Tạo account (nếu chưa có)
3. Tạo **FREE Cluster**:
   - Cloud: AWS
   - Region: Singapore
   - Cluster: Cluster0
4. Tạo **Database User**:
   - Username: `shipway_admin`
   - Password: (Autogenerate & SAVE IT)
5. **Network Access**: Add `0.0.0.0/0` (for development)
6. **Connect** → **Drivers** → Copy connection string

Chi tiết: [MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)

### Step 3: Setup Backend (3 phút)

```bash
# 1. Vào thư mục backend
cd backend

# 2. Install dependencies
npm install

# 3. Tạo file .env
cp .env.template .env

# 4. Chỉnh sửa .env
# Mở .env và cập nhật:
# - MONGODB_URI (paste connection string từ Atlas)
# - JWT_SECRET (ít nhất 32 ký tự)

# 5. Seed admin account
npm run seed

# 6. Chạy server
npm run dev
```

Nếu thành công:
```
✅ MongoDB Connected: cluster0...
📊 Database Name: shipway
🚀 Server is running on port 5000
```

### Step 4: Setup Frontend (2 phút)

```bash
# 1. Mở terminal mới
cd frontend

# 2. Cấu hình API URL
# Mở frontend/config/env.js
# Kiểm tra BASE_URL: 'http://localhost:5000/api'

# 3. Chạy frontend
# Option A: VS Code Live Server (Recommended)
# - Install extension: Live Server
# - Right click index.html → Open with Live Server

# Option B: Python
python -m http.server 3000

# Option C: Node http-server
npx http-server -p 3000
```

### Step 5: Test (1 phút)

1. Mở browser: http://localhost:3000
2. Click **"Chưa có tài khoản? Đăng ký"**
3. Chọn role: **Đối tác vận chuyển**
4. Nhập số điện thoại: `0987654321`
5. Click **"Gửi mã OTP"**
6. Kiểm tra Console (F12) để lấy OTP
7. Nhập OTP và thông tin còn lại
8. Click **"Đăng ký"**

Hoặc login với admin account:
```
Phone: +84987654321
Password: Admin@123456
```

## 🎉 Hoàn thành!

Bạn đã có:
- ✅ Backend API chạy tại http://localhost:5000
- ✅ Frontend chạy tại http://localhost:3000
- ✅ MongoDB Atlas database
- ✅ Admin account để test

## 📝 Environment Variables Checklist

### Backend (.env)

```env
✅ MONGODB_URI=mongodb+srv://shipway_admin:password@cluster.mongodb.net/shipway
✅ JWT_SECRET=your_minimum_32_character_secret_key_here
✅ PORT=5000
✅ NODE_ENV=development
✅ FRONTEND_URL=http://localhost:3000

# Optional (for SMS OTP)
⬜ TWILIO_ACCOUNT_SID=
⬜ TWILIO_AUTH_TOKEN=
⬜ TWILIO_PHONE_NUMBER=
```

### Frontend (config/env.js)

```javascript
✅ BASE_URL: 'http://localhost:5000/api'
```

## 🧪 Test API

### Sử dụng cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Login admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84987654321", "password": "Admin@123456"}'

# Send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+84123456789", "purpose": "register"}'
```

### Sử dụng Postman

1. Import API collection (nếu có)
2. Set environment:
   - `base_url`: `http://localhost:5000/api`

## 🐛 Common Issues

### Backend không chạy

**Error**: `Error connecting to MongoDB`

**Fix**:
1. Kiểm tra MONGODB_URI trong .env
2. Kiểm tra Network Access trong Atlas (whitelist IP)
3. Kiểm tra username/password

---

**Error**: `Port 5000 already in use`

**Fix**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Hoặc đổi PORT trong .env
PORT=5001
```

### Frontend không hiển thị

**Error**: CORS error

**Fix**:
1. Kiểm tra FRONTEND_URL trong backend/.env
2. Restart backend server

---

**Error**: API calls fail

**Fix**:
1. Kiểm tra BASE_URL trong frontend/config/env.js
2. Đảm bảo backend đang chạy
3. Mở F12 → Network tab để debug

### MongoDB Atlas

**Error**: "Authentication failed"

**Fix**:
1. Vào Database Access → Edit user
2. Reset password
3. Cập nhật .env với password mới

## 📚 Next Steps

- [ ] Đọc [Backend Documentation](BACKEND_DOCUMENTATION.md)
- [ ] Tìm hiểu API endpoints
- [ ] Setup Twilio cho SMS OTP thật
- [ ] Customize frontend UI
- [ ] Deploy lên production

## 💡 Tips

### Development

- Sử dụng **nodemon** để auto-restart backend
- Dùng **VS Code Live Server** cho frontend
- Bật **MongoDB Compass** để xem database

### Testing

- OTP được log ra console (F12)
- Development mode: OTP hiển thị trong response
- Sử dụng admin account để test admin features

### Debugging

- Check backend logs: Terminal running `npm run dev`
- Check frontend errors: Browser Console (F12)
- Check MongoDB data: Atlas → Browse Collections

## 🆘 Need Help?

1. Đọc [BACKEND_DOCUMENTATION.md](BACKEND_DOCUMENTATION.md)
2. Đọc [MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)
3. Check [README.md](../README.md)
4. Create GitHub issue

---

**Last Updated**: January 4, 2025  
**Estimated Time**: 10 minutes  
**Difficulty**: Easy ⭐

