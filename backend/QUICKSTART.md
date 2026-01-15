# 🚀 Quick Start Guide

## Bước 1: Cài đặt môi trường

### 1.1 Cài đặt Python (nếu chưa có)

```bash
# Check Python version (cần >= 3.8)
python --version

# Hoặc
python3 --version
```

### 1.2 Tạo virtual environment (khuyên dùng)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Bước 2: Cấu hình

### 2.1 Tạo file .env

```bash
# Copy từ example
cp .env.example .env
```

### 2.2 Sửa file .env

**BẮT BUỘC** phải thay đổi:

```env
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

Tạo JWT secret ngẫu nhiên:

```bash
# Sử dụng Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Tùy chọn** (nếu muốn gửi SMS thật):

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

> ⚠️ Nếu không cấu hình Twilio, OTP sẽ được in ra console trong development mode.

## Bước 3: Chạy MongoDB

### Option 1: Docker (khuyên dùng)

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Option 2: MongoDB Atlas (Cloud - Free)

1. Đăng ký tại https://www.mongodb.com/cloud/atlas
2. Tạo cluster miễn phí
3. Lấy connection string
4. Cập nhật trong `.env`:

```env
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net
```

### Option 3: Cài đặt local

- Windows: https://www.mongodb.com/try/download/community
- Linux: `sudo apt install mongodb`
- Mac: `brew install mongodb-community`

## Bước 4: Chạy server

### Cách 1: Sử dụng run script

```bash
python run.py
```

### Cách 2: Sử dụng uvicorn trực tiếp

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Bước 5: Kiểm tra

Server đang chạy tại: **http://localhost:8000**

### Kiểm tra health:

```bash
curl http://localhost:8000/health
```

### Mở Swagger UI:

Truy cập: **http://localhost:8000/docs**

## 🧪 Test API

### 1. Test gửi OTP

Trong Swagger UI (`/docs`):

1. Mở endpoint `POST /api/v1/auth/send-otp`
2. Click "Try it out"
3. Nhập:
   ```json
   {
     "phone": "+84123456789",
     "purpose": "register"
   }
   ```
4. Click "Execute"
5. Xem response và OTP (trong development mode)

### 2. Test đăng ký

1. Mở endpoint `POST /api/v1/auth/register`
2. Nhập:
   ```json
   {
     "phone": "+84123456789",
     "name": "Nguyen Van A",
     "password": "123456",
     "otp": "123456",
     "role": "user"
   }
   ```
3. Click "Execute"
4. **Copy JWT token** từ response

### 3. Test API có authentication

1. Click nút **"Authorize" 🔒** ở góc phải trên Swagger UI
2. Paste JWT token (format: `Bearer <token>` hoặc chỉ `<token>`)
3. Click "Authorize"
4. Bây giờ bạn có thể test các API yêu cầu authentication như `/api/v1/auth/me`

## ⚠️ Troubleshooting

### Lỗi: "No module named 'app'"

```bash
# Đảm bảo bạn đang ở thư mục backend-python
cd backend-python

# Chạy lại
python run.py
```

### Lỗi: "Could not connect to MongoDB"

```bash
# Kiểm tra MongoDB đang chạy
# Docker:
docker ps | grep mongodb

# Local:
# Windows: kiểm tra service "MongoDB"
# Linux/Mac:
sudo systemctl status mongodb
```

### Lỗi: "pydantic.errors.PydanticUserError"

```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt
```

### OTP không được gửi

- Trong development mode, OTP sẽ được in ra console/terminal
- Check logs trong terminal nơi bạn chạy server
- Nếu muốn gửi SMS thật, cần cấu hình Twilio

## 📝 Next Steps

1. ✅ Test tất cả API endpoints trong Swagger
2. ✅ Đọc [README.md](README.md) để hiểu chi tiết
3. ✅ Tham khảo [backend readme](../backend/readme%20for%20backend.md) để hiểu coding rules
4. ✅ Bắt đầu phát triển frontend hoặc thêm features mới

## 🎉 Done!

Backend API đã sẵn sàng! Swagger documentation: **http://localhost:8000/docs**

Happy Coding! 🚀
