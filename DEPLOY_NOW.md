# 🚀 DEPLOY NGAY BÂY GIỜ!

## ⚡ 3 bước đơn giản - 10 phút hoàn thành

---

## 🔴 BẠN GẶP LỖI GÌ?

### Lỗi: `404: NOT_FOUND` trên Vercel
**Nguyên nhân**: Vercel không thể chạy Python backend!

**Giải pháp**: Deploy backend riêng lên Railway, frontend lên Vercel

---

## ✅ GIẢI PHÁP - 3 BƯỚC

### 📍 BƯỚC 1: Deploy Backend (5 phút)

1. **Mở Railway**: https://railway.app/
2. **New Project** → **Deploy from GitHub**
3. Chọn repo **Shipwayyyy**
4. **⚠️ QUAN TRỌNG - Settings** (click icon bánh răng):
   - **Source → Root Directory**: `backend` ← PHẢI SET NÀY!
   - **Deploy → Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Add Variables** (tab Variables):
   ```
   MONGODB_URL=your-mongodb-atlas-connection-string
   SECRET_KEY=run-python-generate-secrets-py-to-get-this
   JWT_SECRET=run-python-generate-secrets-py-to-get-this
   NODE_ENV=production
   ```
6. **Deploy** và copy URL (ví dụ: `https://shipway.railway.app`)

💡 **Generate secrets:**
```bash
python generate-secrets.py
```

---

### 📍 BƯỚC 2: Cập nhật API URL (2 phút)

1. Mở `frontend/config/api.config.js`
2. Tìm dòng `production:` và thay:
   ```javascript
   production: {
       API_BASE_URL: 'https://YOUR-RAILWAY-URL/api/v1',  // ← Paste Railway URL
       UPLOAD_URL: 'https://YOUR-RAILWAY-URL/uploads'
   }
   ```
3. Save file
4. Push lên GitHub:
   ```bash
   git add .
   git commit -m "Update production API URL"
   git push
   ```

---

### 📍 BƯỚC 3: Deploy Frontend (3 phút)

**Cách 1: Vercel CLI (Nhanh hơn)**
```bash
npm install -g vercel
vercel login
vercel --prod
```

**Cách 2: Vercel Web UI**
1. Mở: https://vercel.com/new
2. Import repo **Shipwayyyy**
3. Settings để mặc định
4. Click **Deploy**

---

## ✅ KIỂM TRA

### Backend (Railway):
```
https://your-backend.railway.app/docs
```
→ Phải thấy Swagger UI

### Frontend (Vercel):
```
https://your-frontend.vercel.app
```
→ Phải thấy trang chủ và login/register hoạt động

---

## 🐛 GẶP LỖI?

### ❌ Railway: "start.sh not found" / "Could not determine how to build"
**Nguyên nhân**: Root Directory chưa được set!

**Fix**: 
1. Railway Settings → Source → Root Directory: `backend`
2. Redeploy

**Chi tiết**: Xem file `RAILWAY_DEPLOY_FIX.md`

### ❌ CORS Error
→ Đã fix sẵn trong code, push lại là được

### ❌ API không connect
→ Check `api.config.js` xem Railway URL đúng chưa

### ❌ MongoDB không kết nối được
→ Vào MongoDB Atlas → Network Access → Allow 0.0.0.0/0

---

## 📚 ĐỌC THÊM

- Chi tiết: `README_DEPLOY.md`
- Troubleshooting: `DEPLOYMENT_GUIDE.md`
- Quick guide: `QUICK_DEPLOY.md`

---

**🎉 XEM VIDEO HƯỚNG DẪN:** (Coming soon)

**💬 CẦN HELP?** 
- Check logs: Railway/Vercel dashboards
- Xem troubleshooting section trong README_DEPLOY.md

---

> **⏱️ Thời gian**: ~10 phút
> **💰 Chi phí**: $0 (Free tier)
> **🎯 Kết quả**: App live trên internet!
