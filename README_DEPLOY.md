# 🚀 Deploy Shipway lên Production

## ⚠️ VẤN ĐỀ BẠN GẶP PHẢI

Bạn đã deploy lên Vercel nhưng gặp lỗi **404: NOT_FOUND** vì:
- Vercel chủ yếu hỗ trợ **Node.js/Static sites**
- Backend của bạn là **Python/FastAPI**
- Vercel không thể chạy Python backend

## ✅ GIẢI PHÁP (Architecture đúng)

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Vercel    │─────▶│   Railway   │─────▶│  MongoDB    │
│  (Frontend) │      │  (Backend)  │      │   Atlas     │
└─────────────┘      └─────────────┘      └─────────────┘
   Static HTML         Python/FastAPI      Database
```

---

## 📝 HƯỚNG DẪN DEPLOY CHI TIẾT

### 🔹 BƯỚC 1: Deploy Backend lên Railway

#### 1.1. Tạo tài khoản Railway
- Truy cập: https://railway.app/
- Sign up with GitHub (miễn phí)

#### 1.2. Deploy Backend
1. Click **"New Project"** 
2. Chọn **"Deploy from GitHub repo"**
3. Authorize Railway access GitHub
4. Chọn repository **"Shipwayyyy"**

#### 1.3. Cấu hình Project
**Settings → General:**
- **Root Directory**: `backend`

**Settings → Deploy:**
- **Start Command**: 
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

#### 1.4. Thêm Environment Variables
**Settings → Variables** → Add Variable:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/shipway?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_SECRET=your-jwt-secret-at-least-32-characters-long
NODE_ENV=production
PORT=8000
```

💡 **Tạo SECRET_KEY ngẫu nhiên:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### 1.5. Deploy
- Railway sẽ tự động build và deploy
- Đợi 2-3 phút
- Lấy **Public URL**: Ví dụ `https://shipway-production.up.railway.app`

#### 1.6. Kiểm tra Backend
Mở browser và truy cập:
```
https://your-backend-url.railway.app/docs
```
→ Phải thấy Swagger UI

---

### 🔹 BƯỚC 2: Cập nhật Frontend Config

#### 2.1. Update API Base URL
Mở file **`frontend/config/api.config.js`** và sửa:

```javascript
production: {
    // Thay YOUR_RAILWAY_URL bằng URL Railway của bạn
    API_BASE_URL: 'https://shipway-production.up.railway.app/api/v1',
    UPLOAD_URL: 'https://shipway-production.up.railway.app/uploads'
}
```

#### 2.2. Commit và Push
```bash
git add .
git commit -m "Update production API URL"
git push origin main
```

---

### 🔹 BƯỚC 3: Deploy Frontend lên Vercel

#### Option A: Vercel CLI (Recommended)
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd D:/Coding/Shipwayyyy
vercel --prod
```

Vercel sẽ hỏi:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name?** → shipway (hoặc tên khác)
- **Directory?** → `./` (press Enter)
- **Override settings?** → No

#### Option B: Vercel Web UI
1. Truy cập: https://vercel.com/new
2. Click **"Import Git Repository"**
3. Chọn **"Shipwayyyy"**
4. **Framework Preset**: Other
5. **Root Directory**: Để trống (`.`)
6. **Build Command**: Để trống
7. **Output Directory**: Để trống
8. **Install Command**: Để trống
9. Click **"Deploy"**

#### 3.2. Lấy URL Frontend
Vercel sẽ cho bạn URL như:
```
https://shipway.vercel.app
hoặc
https://shipway-abc123.vercel.app
```

---

### 🔹 BƯỚC 4: Kiểm tra Production

#### 4.1. Kiểm tra Backend
```bash
curl https://your-backend.railway.app/health
```
Phải trả về: `{"status":"healthy",...}`

#### 4.2. Kiểm tra Frontend
Mở browser:
```
https://your-frontend.vercel.app
```
- ✅ Trang load được
- ✅ Có thể đăng ký/đăng nhập
- ✅ API calls hoạt động

#### 4.3. Test Full Flow
1. Mở DevTools (F12) → Network tab
2. Click "Đăng ký" hoặc "Đăng nhập"
3. Check API request đi đến Railway URL
4. Nếu thành công → Done! 🎉

---

## 🐛 TROUBLESHOOTING

### ❌ Lỗi: 404 Not Found trên Vercel

**Nguyên nhân**: Vercel không tìm thấy index.html

**Giải pháp**: Đã fix trong `vercel.json` - routes đã được cấu hình đúng

**Kiểm tra**:
```bash
# File vercel.json đã tồn tại?
ls vercel.json

# Nội dung có đúng không?
cat vercel.json
```

---

### ❌ Lỗi: CORS Policy Error

**Nguyên nhân**: Backend chưa allow frontend URL

**Giải pháp**: Đã update trong `backend/app/main.py` - CORS cho phép `*.vercel.app`

**Nếu vẫn lỗi**:
1. Vào Railway → Variables
2. Thêm variable:
   ```
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
3. Update `backend/app/main.py`:
   ```python
   allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(",")
   ```

---

### ❌ Lỗi: API calls failed (Network Error)

**Nguyên nhân**: 
- API URL sai trong config
- Backend chưa chạy

**Kiểm tra**:
```bash
# 1. Backend có chạy không?
curl https://your-backend.railway.app/health

# 2. API config đúng chưa?
cat frontend/config/api.config.js
```

**Giải pháp**:
- Đảm bảo Railway URL đúng
- Commit và push lại nếu sửa config

---

### ❌ Lỗi: Cannot connect to MongoDB

**Nguyên nhân**: 
- MONGODB_URL sai
- MongoDB chưa whitelist IP Railway

**Giải pháp**:
1. Vào MongoDB Atlas
2. **Network Access** → **Add IP Address**
3. Chọn **"Allow access from anywhere"** (0.0.0.0/0)
4. Save

---

### ❌ Lỗi: JWT/SECRET_KEY not set

**Nguyên nhân**: Environment variables chưa được set

**Giải pháp**:
1. Vào Railway → Settings → Variables
2. Thêm đầy đủ:
   ```
   SECRET_KEY=...
   JWT_SECRET=...
   MONGODB_URL=...
   ```

---

## 💰 CHI PHÍ

| Service | Plan | Chi phí | Giới hạn |
|---------|------|---------|----------|
| **Vercel** | Hobby | **FREE** | Unlimited bandwidth |
| **Railway** | Free Tier | **FREE** | $5 credit/month (~500 hours) |
| **MongoDB Atlas** | Free Tier | **FREE** | 512MB storage |
| **TOTAL** | | **$0/month** | 🎉 |

⚠️ **Lưu ý**: Railway free tier có giới hạn 500 hours/month. Nếu app luôn chạy 24/7 thì:
- 1 tháng = 720 hours
- Vượt quá 500 hours → Bị tính phí hoặc app sleep

**Giải pháp**: Dùng Railway cron/schedule hoặc nâng cấp lên plan $5/month.

---

## 📁 FILES ĐÃ TẠO

```
Shipwayyyy/
├── vercel.json              ← Vercel config
├── .vercelignore            ← Ignore Python files
├── frontend/
│   └── config/
│       └── api.config.js    ← Auto-detect environment
├── backend/
│   ├── Procfile            ← Railway/Heroku config
│   ├── railway.json         ← Railway config
│   └── runtime.txt          ← Python version
└── DEPLOYMENT_GUIDE.md      ← Chi tiết hơn
```

---

## ✅ CHECKLIST DEPLOYMENT

**Backend (Railway):**
- [ ] Tạo project trên Railway
- [ ] Connect GitHub repo
- [ ] Set root directory = `backend`
- [ ] Add environment variables
- [ ] Deploy thành công
- [ ] Test `/docs` endpoint

**Frontend (Vercel):**
- [ ] Update `api.config.js` với Railway URL
- [ ] Push code lên GitHub
- [ ] Deploy to Vercel
- [ ] Test trang chủ load được

**Integration:**
- [ ] Test login/register
- [ ] Test API calls từ frontend
- [ ] Check CORS không bị lỗi
- [ ] Test upload files (nếu có)

---

## 🎯 NEXT STEPS

Sau khi deploy thành công:

1. **Custom Domain** (Optional):
   - Vercel: Settings → Domains → Add domain
   - Railway: Settings → Domains → Add custom domain

2. **Monitoring**:
   - Railway có built-in metrics
   - Vercel Analytics (free)

3. **Backup**:
   - MongoDB Atlas có auto-backup
   - Export database định kỳ

4. **Security**:
   - Giới hạn CORS origins (không dùng "*")
   - Enable rate limiting
   - Add API key authentication

---

## 📚 TÀI LIỆU THAM KHẢO

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MongoDB Atlas](https://www.mongodb.com/docs/atlas/)

---

**🎉 Chúc bạn deploy thành công!**

Nếu gặp vấn đề, check lại từng bước hoặc xem logs:
- Railway: Deployments → View logs
- Vercel: Deployments → View logs
