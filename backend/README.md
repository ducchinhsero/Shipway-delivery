# Shipway Backend API - FastAPI

Backend API được xây dựng bằng **FastAPI** với **MongoDB**, đầy đủ **Swagger documentation**.

## 🎯 Tính năng

- ✅ **Authentication**: Đăng ký, đăng nhập, đặt lại mật khẩu
- ✅ **OTP Verification**: Xác thực OTP qua SMS (Twilio)
- ✅ **User Management**: Quản lý profile người dùng
- ✅ **JWT Authentication**: Bảo mật API với JWT token
- ✅ **Swagger Documentation**: API docs tự động tại `/docs`
- ✅ **Role-based Access**: Phân quyền user/driver/admin

## 📁 Cấu trúc project

```
app/
├── main.py                 # FastAPI app chính
├── core/
│   ├── config.py           # Cấu hình từ .env
│   └── security.py         # JWT, password hashing
├── db/
│   ├── session.py          # MongoDB connection
│   └── models.py           # Database operations
├── schemas/                # Pydantic schemas (Swagger)
│   ├── user.py
│   └── otp.py
├── api/
│   ├── deps.py             # Dependencies (auth, db)
│   └── v1/
│       ├── auth.py         # Auth endpoints
│       ├── user.py         # User endpoints
│       └── router.py       # Router tổng
└── services/
    └── otp_service.py      # OTP logic
```

## 🚀 Cài đặt

### 1. Cài đặt Python dependencies

```bash
cd backend-python
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Sửa file `.env`:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=shipway

# JWT Secret (BẮT BUỘC THAY ĐỔI)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Twilio (Optional - nếu muốn gửi SMS thật)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 3. Chạy MongoDB

Đảm bảo MongoDB đang chạy:

```bash
# Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Hoặc cài đặt trực tiếp
mongod
```

### 4. Chạy server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

Sau khi chạy server, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔑 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint           | Mô tả                        | Auth Required |
|--------|--------------------|------------------------------|---------------|
| POST   | `/send-otp`        | Gửi mã OTP                   | ❌             |
| POST   | `/verify-otp`      | Xác thực OTP                 | ❌             |
| POST   | `/register`        | Đăng ký tài khoản            | ❌             |
| POST   | `/login`           | Đăng nhập                    | ❌             |
| POST   | `/reset-password`  | Đặt lại mật khẩu             | ❌             |
| GET    | `/me`              | Lấy thông tin user hiện tại  | ✅             |

### User Management (`/api/v1/user`)

| Method | Endpoint              | Mô tả                    | Auth Required |
|--------|-----------------------|--------------------------|---------------|
| PUT    | `/profile`            | Cập nhật profile         | ✅             |
| GET    | `/profile/{user_id}`  | Xem profile user khác    | ✅             |

## 🧪 Test API

### 1. Đăng ký tài khoản

**Bước 1: Gửi OTP**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "purpose": "register"
  }'
```

**Bước 2: Đăng ký**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "name": "Nguyen Van A",
    "password": "123456",
    "otp": "123456",
    "role": "user"
  }'
```

### 2. Đăng nhập

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+84123456789",
    "password": "123456"
  }'
```

Response:

```json
{
  "success": true,
  "message": "Đăng nhập thành công",
  "token": "eyJhbGci...",
  "user": {...}
}
```

### 3. Sử dụng JWT token

Thêm token vào header:

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGci..."
```

## 🔒 Authentication Flow

```
1. User request OTP:
   POST /api/v1/auth/send-otp
   -> SMS sent (or printed in dev mode)

2. User register with OTP:
   POST /api/v1/auth/register
   -> Verify OTP -> Create user -> Return JWT token

3. User login:
   POST /api/v1/auth/login
   -> Verify password -> Return JWT token

4. Use JWT for protected endpoints:
   Authorization: Bearer <token>
```

## 📝 Swagger Rules (BẮT BUỘC)

Khi thêm API mới, **BẮT BUỘC**:

1. ✅ Có `summary` và `description`
2. ✅ Có `response_model` (Pydantic)
3. ✅ Có `responses` với status codes
4. ✅ Có `tags` để group API
5. ✅ Có `example` trong schemas

**Example:**

```python
@router.post(
    "/endpoint",
    response_model=ResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Mô tả ngắn gọn",
    description="Mô tả chi tiết về API này...",
    tags=["Tag Name"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request"}
    }
)
async def my_endpoint(payload: RequestSchema):
    ...
```

## 🛠️ Development

### Database Models

Tất cả database operations nằm trong `app/db/models.py`:

```python
from app.db import models

# User operations
user = await models.create_user(db, user_data)
user = await models.find_user_by_phone(db, phone)
user = await models.update_user(db, user_id, update_data)

# OTP operations
otp = await models.create_otp(db, otp_data)
otp = await models.find_latest_otp(db, phone, purpose)
```

### Schemas

Định nghĩa request/response schemas trong `app/schemas/`:

```python
from pydantic import BaseModel, Field

class MyRequest(BaseModel):
    field: str = Field(..., example="value", description="...")

class MyResponse(BaseModel):
    success: bool = True
    data: Any
```

## 🔧 Production Deployment

1. **Thay đổi JWT_SECRET**:
   ```env
   JWT_SECRET=generate-strong-random-secret-key
   ```

2. **Cấu hình CORS**:
   ```python
   # app/main.py
   allow_origins=["https://yourdomain.com"]
   ```

3. **Chạy với production server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Sử dụng MongoDB Atlas** (cloud):
   ```env
   MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net
   ```

## 📞 Support

Nếu có vấn đề, hãy check:

1. MongoDB đã chạy chưa?
2. File `.env` đã cấu hình đúng chưa?
3. Dependencies đã cài đầy đủ chưa?
4. Swagger docs: http://localhost:8000/docs

---

**Happy Coding! 🚀**
