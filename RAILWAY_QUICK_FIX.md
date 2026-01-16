# ⚡ Railway Quick Fix - "start.sh not found"

## 🔴 Lỗi:
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

---

## ✅ FIX NGAY (2 phút)

### Bước 1: Push files mới
```bash
cd D:/Coding/Shipwayyyy
git add .
git commit -m "Add Railway deployment configs"
git push origin main
```

Files đã được tạo sẵn:
- ✅ `backend/railway.toml`
- ✅ `backend/nixpacks.toml`
- ✅ `backend/start.sh`
- ✅ `backend/Procfile` (updated)

### Bước 2: Set Root Directory trong Railway

**Cách làm:**

1. Vào Railway Dashboard: https://railway.app/
2. Click vào **Project của bạn**
3. Click vào **Service** (hoặc tên app)
4. Click icon **⚙️ Settings** (góc trên)
5. Tìm section **"Source"**
6. **Root Directory**: Điền `backend`
7. **Watch Paths**: Điền `backend/**`
8. Click **Save** hoặc Railway tự save

### Bước 3: Redeploy
- Railway sẽ tự động redeploy sau khi set Root Directory
- Hoặc click **Redeploy** manually

---

## 🎯 Visual Guide

```
Railway Dashboard
    ↓
Your Project
    ↓
Service (click vào)
    ↓
⚙️ Settings (góc trên phải)
    ↓
📁 Source Section
    ↓
Root Directory: [backend]  ← ĐIỀN VÀO ĐÂY
Watch Paths: [backend/**]
    ↓
✅ Deploy lại
```

---

## ✅ Kiểm tra thành công

### 1. Build Logs
Vào **Deployments** → Click deployment mới → Xem logs:

**Thành công:**
```
✓ Installing Python 3.11
✓ Installing dependencies
✓ Build complete
✓ Starting application
INFO: Uvicorn running on http://0.0.0.0:XXXX
```

### 2. Test URL
Mở browser:
```
https://your-app.railway.app/docs
```
→ Phải thấy Swagger UI

### 3. Health Check
```bash
curl https://your-app.railway.app/health
```
→ Phải trả về JSON

---

## 🐛 Vẫn lỗi?

### Option A: Xóa và tạo lại service
1. Settings → Delete Service
2. New → Deploy from GitHub
3. Chọn repo
4. **NGAY TỪ ĐẦU**: Set Root Directory = `backend`
5. Deploy

### Option B: Dùng Railway CLI
```bash
npm install -g @railway/cli
railway login
cd backend
railway up
```

---

## 📄 Chi tiết đầy đủ

Xem file: `RAILWAY_DEPLOY_FIX.md`

---

**⏱️ Thời gian fix: 2 phút**
**🎯 Sau khi fix: Backend sẽ chạy ngon lành!**
