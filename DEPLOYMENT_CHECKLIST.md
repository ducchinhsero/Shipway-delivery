# ✅ Deployment Checklist

## 📦 Files đã chuẩn bị sẵn

### Configuration
- [x] `vercel.json` - Vercel routing config
- [x] `.vercelignore` - Ignore Python files
- [x] `backend/Procfile` - Railway/Heroku config
- [x] `backend/railway.json` - Railway deployment config
- [x] `backend/runtime.txt` - Python version specification
- [x] `frontend/config/api.config.js` - Auto-detect environment

### Documentation
- [x] `DEPLOY_NOW.md` - Quick start (3 bước)
- [x] `QUICK_DEPLOY.md` - Deploy trong 10 phút
- [x] `README_DEPLOY.md` - Chi tiết + troubleshooting
- [x] `DEPLOYMENT_GUIDE.md` - Hướng dẫn từng bước
- [x] `DEPLOYMENT_SUMMARY.md` - Tổng quan architecture

### Utilities
- [x] `generate-secrets.py` - Generate SECRET_KEY & JWT_SECRET

### Code Updates
- [x] CORS config updated in `backend/app/main.py`
- [x] API config script added to `frontend/index.html`

---

## 🎯 TODO - Deployment Steps

### Backend (Railway/Render)
- [ ] Generate secret keys: `python generate-secrets.py`
- [ ] Create Railway account
- [ ] Deploy backend from GitHub
- [ ] Set root directory = `backend`
- [ ] Add environment variables
- [ ] Copy backend URL

### Frontend (Vercel)
- [ ] Update `frontend/config/api.config.js` với backend URL
- [ ] Commit & push to GitHub
- [ ] Deploy to Vercel
- [ ] Copy frontend URL

### Testing
- [ ] Test backend: `https://backend-url/docs`
- [ ] Test frontend: `https://frontend-url/`
- [ ] Test login/register flow
- [ ] Test API calls (check DevTools Network)
- [ ] Test CORS (no errors in console)

### Optional
- [ ] Setup custom domain
- [ ] Enable monitoring/analytics
- [ ] Setup error tracking
- [ ] Configure CI/CD pipeline
- [ ] Setup automated backups

---

## 📊 Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Railway | https://railway.app | Backend hosting |
| Vercel | https://vercel.com | Frontend hosting |
| MongoDB Atlas | https://cloud.mongodb.com | Database |

| Environment Variable | Example | Required |
|---------------------|---------|----------|
| `MONGODB_URL` | `mongodb+srv://...` | ✅ Yes |
| `SECRET_KEY` | `generated-32-chars` | ✅ Yes |
| `JWT_SECRET` | `generated-32-chars` | ✅ Yes |
| `NODE_ENV` | `production` | ✅ Yes |
| `PORT` | `8000` | ⚠️ Railway auto-sets |

---

## 🚨 Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| 404 on Vercel | Already fixed in `vercel.json` |
| CORS Error | Already fixed in `main.py` |
| API fails | Check `api.config.js` URL |
| MongoDB fails | Whitelist 0.0.0.0/0 in Atlas |
| Secrets error | Run `generate-secrets.py` |

---

## 🎯 Success Criteria

✅ Backend `/docs` shows Swagger UI
✅ Frontend homepage loads
✅ Login/Register works
✅ API calls succeed (no CORS errors)
✅ Orders can be created
✅ Wallet shows balance

---

**Status**: Ready to deploy! 🚀
**Next**: Follow `DEPLOY_NOW.md`
