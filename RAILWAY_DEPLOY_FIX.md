# 🚂 Fix Railway Deployment Error

## ❌ Lỗi bạn gặp phải:

```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

## 🔍 Nguyên nhân:

Railway đang tìm file ở **root directory** thay vì trong **backend/** folder.

---

## ✅ GIẢI PHÁP - 2 Cách

### 🎯 Cách 1: Set Root Directory trong Railway (RECOMMENDED)

#### Bước 1: Xóa deployment hiện tại (nếu có)
1. Vào Railway project của bạn
2. Click vào service → **Settings**
3. Scroll xuống → **Delete Service** (nếu cần)

#### Bước 2: Tạo service mới với Root Directory đúng
1. Railway Dashboard → **New Project**
2. **Deploy from GitHub repo**
3. Chọn repository **Shipwayyyy**
4. ⚠️ **QUAN TRỌNG**: Trước khi deploy, click **Settings** (icon bánh răng)

#### Bước 3: Cấu hình Service Settings
**Settings → Source:**
- ✅ **Root Directory**: `backend` ← QUAN TRỌNG!
- ✅ **Watch Paths**: `backend/**`

**Settings → Deploy:**
- **Build Command**: (để trống, Railway tự detect)
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

hoặc chỉ để trống, Railway sẽ dùng `Procfile`

#### Bước 4: Thêm Environment Variables
**Settings → Variables** → **+ New Variable**:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/shipway
SECRET_KEY=<run: python generate-secrets.py>
JWT_SECRET=<run: python generate-secrets.py>
NODE_ENV=production
```

**💡 Generate secrets:**
```bash
cd D:/Coding/Shipwayyyy
python generate-secrets.py
```

#### Bước 5: Deploy
- Click **Deploy** hoặc push code lên GitHub
- Railway sẽ tự động detect Python và build

---

### 🎯 Cách 2: Sử dụng Railway CLI

#### Bước 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Bước 2: Login
```bash
railway login
```

#### Bước 3: Link to project
```bash
cd D:/Coding/Shipwayyyy/backend
railway link
```

Chọn project của bạn từ danh sách.

#### Bước 4: Set Root Directory
```bash
# Railway CLI sẽ tự detect vì bạn đang ở trong backend/
railway up
```

#### Bước 5: Add Environment Variables
```bash
railway variables set MONGODB_URL="mongodb+srv://..."
railway variables set SECRET_KEY="your-secret-key"
railway variables set JWT_SECRET="your-jwt-secret"
railway variables set NODE_ENV="production"
```

---

## 🔍 Verify Setup

### Check 1: Root Directory đúng chưa?
Railway Dashboard → Settings → Source
```
Root Directory: backend ✅
```

### Check 2: Files có đúng không?
Railway sẽ tìm theo thứ tự:
1. ✅ `railway.toml` (đã tạo)
2. ✅ `nixpacks.toml` (đã tạo)
3. ✅ `Procfile` (đã tạo)
4. ✅ `start.sh` (đã tạo)
5. ✅ `requirements.txt` (có sẵn)

### Check 3: Build logs
Vào **Deployments** → Click deployment mới nhất → Xem logs:

**✅ Successful logs:**
```
Installing Python 3.11...
Installing dependencies from requirements.txt...
Successfully installed fastapi uvicorn...
Starting application...
```

**❌ Error logs:**
```
⚠ Script start.sh not found  ← Lỗi cũ
✖ Could not determine...
```
→ Root Directory chưa set đúng!

---

## 📋 Checklist Deploy Railway

- [ ] Push code mới (có `railway.toml`, `nixpacks.toml`, `start.sh`)
- [ ] Railway Settings → Root Directory = `backend`
- [ ] Railway Variables → Add all env vars
- [ ] Deploy và check logs
- [ ] Test endpoint: `https://your-app.railway.app/docs`
- [ ] Verify Swagger UI hiển thị

---

## 🐛 Vẫn gặp lỗi?

### Lỗi 1: Python version not found
**Fix**: Check `backend/runtime.txt`:
```
python-3.11.0
```

### Lỗi 2: Requirements install failed
**Fix**: Check `backend/requirements.txt` syntax

### Lỗi 3: Module 'app' not found
**Fix**: Verify structure:
```
backend/
  ├── app/
  │   ├── __init__.py  ← MUST exist
  │   └── main.py
  └── requirements.txt
```

### Lỗi 4: Port binding failed
**Fix**: Procfile phải dùng `$PORT`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Lỗi 5: MongoDB connection timeout
**Fix**: 
1. MongoDB Atlas → Network Access
2. Add IP: `0.0.0.0/0` (allow all)
3. Save

---

## 📸 Screenshots Guide

### 1. Set Root Directory
```
Railway Dashboard
  → Your Project
    → Settings (gear icon)
      → Source
        → Root Directory: backend ✅
        → Watch Paths: backend/**
```

### 2. Deploy Trigger
```
Settings
  → Triggers
    → Check: "Deploy on push to main"
```

### 3. Environment Variables
```
Settings
  → Variables
    → New Variable
      Name: MONGODB_URL
      Value: mongodb+srv://...
```

---

## ✅ Success Indicators

### 1. Build Success
Railway logs sẽ hiển thị:
```
✓ Python environment created
✓ Dependencies installed
✓ Build complete
✓ Starting server...
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 2. Deployment URL
Railway sẽ cung cấp URL:
```
https://shipway-production-abc123.up.railway.app
```

### 3. Test Endpoint
```bash
curl https://your-app.railway.app/health
```

Response:
```json
{
  "status": "healthy",
  "app": "Shipway API",
  "version": "1.0.0"
}
```

### 4. Swagger UI
Mở browser:
```
https://your-app.railway.app/docs
```
→ Phải thấy Swagger UI với list endpoints

---

## 🎯 Quick Commands

```bash
# 1. Commit new config files
git add backend/railway.toml backend/nixpacks.toml backend/start.sh
git commit -m "Add Railway deployment configs"
git push origin main

# 2. Check Railway logs
railway logs

# 3. Open deployed app
railway open

# 4. Check environment variables
railway variables
```

---

## 📞 Still Need Help?

### Check Railway Docs:
- https://docs.railway.app/deploy/deployments
- https://docs.railway.app/deploy/builds

### View Railway Community:
- Discord: https://discord.gg/railway
- Forum: https://help.railway.app/

### Debug Checklist:
1. ✅ Root Directory = `backend`
2. ✅ Environment variables set
3. ✅ Files pushed to GitHub
4. ✅ MongoDB Atlas IP whitelist
5. ✅ Railway build logs không có error

---

**🎉 After successful deploy:**

Copy Railway URL và update `frontend/config/api.config.js`:
```javascript
production: {
    API_BASE_URL: 'https://your-app.railway.app/api/v1',
    UPLOAD_URL: 'https://your-app.railway.app/uploads'
}
```

Sau đó deploy frontend lên Vercel!

---

**Last Updated**: 2026-01-16
