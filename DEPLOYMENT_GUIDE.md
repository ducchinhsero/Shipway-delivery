# 🚀 Hướng dẫn Deploy Shipway

## 📋 Tổng quan

Project Shipway sử dụng:
- **Frontend**: HTML/CSS/JavaScript (static files)
- **Backend**: Python/FastAPI
- **Database**: MongoDB Atlas

## 🎯 Chiến lược Deploy (Khuyến nghị)

### **Frontend → Vercel** (Miễn phí)
### **Backend → Railway/Render** (Miễn phí)
### **Database → MongoDB Atlas** (Miễn phí)

---

## 1️⃣ Deploy Backend lên Railway

### Bước 1: Tạo tài khoản Railway
1. Truy cập: https://railway.app/
2. Sign up with GitHub
3. Xác nhận email

### Bước 2: Deploy Backend
```bash
# Cài Railway CLI (optional)
npm install -g @railway/cli

# Hoặc deploy qua Web UI
```

**Deploy qua Railway Web UI:**
1. Click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Chọn repository `Shipwayyyy`
4. Railway sẽ tự động detect Python app
5. Thêm **Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://your-connection-string
   SECRET_KEY=your-secret-key-here
   JWT_SECRET=your-jwt-secret-here
   NODE_ENV=production
   ```

### Bước 3: Cấu hình Root Directory
1. Vào **Settings** → **Root Directory**
2. Set: `backend`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Bước 4: Lấy URL Backend
Sau khi deploy thành công, Railway sẽ cung cấp URL:
```
https://shipway-backend-production.up.railway.app
```

Copy URL này để dùng cho frontend!

---

## 2️⃣ Deploy Frontend lên Vercel

### Bước 1: Cập nhật API URL
Mở file `frontend/config/api.config.js` và thay:
```javascript
production: {
    API_BASE_URL: 'https://your-backend-app.railway.app/api/v1',
    UPLOAD_URL: 'https://your-backend-app.railway.app/uploads'
}
```

Thành URL Railway của bạn:
```javascript
production: {
    API_BASE_URL: 'https://shipway-backend-production.up.railway.app/api/v1',
    UPLOAD_URL: 'https://shipway-backend-production.up.railway.app/uploads'
}
```

### Bước 2: Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**Hoặc deploy qua Web UI:**
1. Truy cập: https://vercel.com/
2. Click **"Add New Project"**
3. Import repository `Shipwayyyy`
4. Vercel tự động phát hiện `vercel.json`
5. Click **"Deploy"**

### Bước 3: Lấy URL Frontend
Vercel sẽ cung cấp URL:
```
https://shipway-frontend.vercel.app
```

---

## 3️⃣ Cấu hình CORS cho Backend

Sau khi có URL Vercel, cần update CORS trong backend:

**File: `backend/app/main.py`**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://shipway-frontend.vercel.app",  # ← Thêm URL Vercel
        "https://*.vercel.app"  # Allow all Vercel preview URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Sau đó push code lên GitHub, Railway sẽ tự động redeploy.

---

## 4️⃣ Kiểm tra Deployment

### Backend (Railway)
Truy cập: `https://your-backend.railway.app/docs`
- ✅ Thấy Swagger UI
- ✅ Test API endpoints

### Frontend (Vercel)
Truy cập: `https://your-frontend.vercel.app`
- ✅ Trang load được
- ✅ API calls hoạt động
- ✅ Login/Register thành công

---

## 🔧 Troubleshooting

### ❌ Lỗi 404 trên Vercel
**Nguyên nhân**: Vercel không tìm thấy file index.html

**Giải pháp**: Đã fix trong `vercel.json` - route "/" → "frontend/index.html"

### ❌ CORS Error
**Nguyên nhân**: Backend chưa allow origin từ Vercel

**Giải pháp**: Update `allow_origins` trong `backend/app/main.py`

### ❌ API calls failed
**Nguyên nhân**: `API_BASE_URL` chưa đúng

**Giải pháp**: Check `frontend/config/api.config.js` và đảm bảo URL Railway đúng

### ❌ MongoDB connection failed
**Nguyên nhân**: Environment variables chưa set

**Giải pháp**: Thêm `MONGODB_URL` trong Railway settings

---

## 📊 Chi phí (Miễn phí!)

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Hobby | Free |
| Railway | Free Tier | Free (500 hours/month) |
| MongoDB Atlas | Free Tier | Free (512MB) |
| **Total** | | **$0/month** |

---

## 🎯 Alternative: Deploy Backend lên Render

Nếu không muốn dùng Railway:

1. Truy cập: https://render.com/
2. **New** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables (giống Railway)
6. Deploy!

---

## ✅ Checklist Deployment

- [ ] Backend deployed lên Railway/Render
- [ ] Database MongoDB Atlas đã setup
- [ ] Environment variables đã set đầy đủ
- [ ] Lấy được URL backend
- [ ] Update `api.config.js` với URL backend
- [ ] Update CORS trong backend
- [ ] Frontend deployed lên Vercel
- [ ] Test login/register hoạt động
- [ ] Test API calls thành công

---

**🎉 Done! Project đã live trên internet!**
