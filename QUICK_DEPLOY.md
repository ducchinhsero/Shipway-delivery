# ⚡ Quick Deploy Guide

## 🎯 Deploy ngay trong 10 phút!

### 1️⃣ Deploy Backend lên Railway (5 phút)

1. **Truy cập Railway**: https://railway.app/
2. Click **"Start a New Project"**
3. Chọn **"Deploy from GitHub repo"**
4. Chọn repo `Shipwayyyy`
5. **Settings**:
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Add Variables** (tab Variables):
   ```
   MONGODB_URL=your-mongodb-connection-string
   SECRET_KEY=your-secret-key-minimum-32-characters
   JWT_SECRET=your-jwt-secret-minimum-32-characters
   NODE_ENV=production
   PORT=8000
   ```

7. **Deploy** và đợi Railway build xong

8. **Copy URL**: Ví dụ: `https://shipway-production.up.railway.app`

---

### 2️⃣ Cập nhật API Config (1 phút)

Mở file `frontend/config/api.config.js` và sửa:

```javascript
production: {
    API_BASE_URL: 'https://your-backend-url.railway.app/api/v1',  // ← Paste Railway URL
    UPLOAD_URL: 'https://your-backend-url.railway.app/uploads'
}
```

---

### 3️⃣ Cập nhật CORS (1 phút)

Mở `backend/app/main.py` line 77-83:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://*.vercel.app",  # ← Thêm dòng này
        "*"  # Temporary - nên giới hạn sau
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push lên GitHub, Railway tự động redeploy.

---

### 4️⃣ Deploy Frontend lên Vercel (3 phút)

**Option A: Vercel CLI**
```bash
npm install -g vercel
vercel login
vercel --prod
```

**Option B: Vercel Web UI**
1. Truy cập: https://vercel.com/new
2. Import repository `Shipwayyyy`
3. Framework Preset: **Other**
4. Root Directory: **`.`** (để trống)
5. Build Command: **Để trống**
6. Output Directory: **Để trống**
7. Click **Deploy**

---

### ✅ Kiểm tra

**Backend**: `https://your-backend.railway.app/docs`
- Nên thấy Swagger UI

**Frontend**: `https://your-frontend.vercel.app`
- Nên thấy trang chủ

---

## 🐛 Lỗi thường gặp

### ❌ Vercel 404
**Fix**: Đã có file `vercel.json` - redeploy là được

### ❌ CORS Error
**Fix**: Đã update `allow_origins` ở bước 3

### ❌ API không connect được
**Fix**: Check `api.config.js` - đảm bảo URL Railway đúng

---

## 🚀 Done!

Bây giờ app của bạn đã live trên internet:
- Frontend: https://your-app.vercel.app
- Backend API: https://your-backend.railway.app/api/v1
- API Docs: https://your-backend.railway.app/docs
