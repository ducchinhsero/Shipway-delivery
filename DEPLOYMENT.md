# 🚀 Shipway Deployment Guide

> Consolidated deployment documentation for Shipway project

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Production Configuration](#production-configuration)
6. [Deployment Steps](#deployment-steps)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### ✅ Code & Configuration
- [ ] All features tested locally
- [ ] No console errors or warnings
- [ ] Environment variables configured
- [ ] Database schema updated
- [ ] API endpoints documented
- [ ] Frontend builds successfully
- [ ] All tests passing

### ✅ Infrastructure
- [ ] MongoDB Atlas cluster created
- [ ] Network access configured (IP whitelist)
- [ ] Database user created with proper permissions
- [ ] Hosting service selected (Render, Railway, Vercel, etc.)
- [ ] Domain/subdomain configured (if applicable)
- [ ] SSL certificate setup

### ✅ Services
- [ ] Twilio account configured (OTP)
- [ ] Payment gateway configured (VNPay, Momo)
- [ ] Email service configured (if used)
- [ ] File storage configured (for uploads)

---

## Environment Setup

### Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
# MongoDB
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>?retryWrites=true&w=majority

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Twilio (OTP)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Payment Gateways
VNPAY_TMN_CODE=your_vnpay_code
VNPAY_HASH_SECRET=your_vnpay_secret
MOMO_PARTNER_CODE=your_momo_partner_code
MOMO_ACCESS_KEY=your_momo_access_key
MOMO_SECRET_KEY=your_momo_secret_key

# App Settings
APP_NAME=Shipway
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Frontend Environment Variables

Update `frontend/config/env.js`:

```javascript
export const API_CONFIG = {
  BASE_URL: 'https://your-backend-api.com/api/v1',  // Production API
  TIMEOUT: 30000,
  // ... other config
};
```

---

## Backend Deployment

### Option 1: Render.com

1. **Create Web Service**
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   - Add all variables from `.env`
   - Set `PORT` if required

3. **Auto-Deploy**
   - Enable auto-deploy on push to main branch

### Option 2: Railway.app

1. **New Project**
   - Import from GitHub
   - Railway auto-detects Python

2. **Configure**
   - Add environment variables
   - Set start command: `python run.py` or `uvicorn app.main:app`

3. **Domain**
   - Use provided railway.app domain or add custom domain

### Option 3: Google Cloud Run / AWS / Azure

See respective platform documentation for FastAPI deployment.

---

## Frontend Deployment

### Option 1: Vercel (Recommended for Static Sites)

1. **Import Project**
   ```bash
   vercel --prod
   ```

2. **Build Settings**
   - Framework Preset: None (static HTML/JS)
   - Build Command: (leave empty)
   - Output Directory: `frontend`

3. **Environment Variables**
   - Set API URLs in build environment

### Option 2: Netlify

1. **Drag & Drop**
   - Upload `frontend/` folder to Netlify

2. **Settings**
   - Publish directory: `frontend`
   - No build command needed

### Option 3: GitHub Pages

1. **Enable GitHub Pages**
   - Settings > Pages > Source: main branch / `frontend` folder

2. **Update Paths**
   - Ensure all paths are relative

---

## Production Configuration

### CORS Settings

In `backend/app/main.py`:

```python
origins = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Don't use ["*"] in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Security Checklist

- [ ] HTTPS enabled on all services
- [ ] CORS configured (no wildcard `*`)
- [ ] JWT secret is strong (32+ characters)
- [ ] Database credentials secured
- [ ] API keys in environment variables (not in code)
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] File upload validation and size limits

---

## Deployment Steps

### Step 1: Prepare Database

```bash
# Connect to MongoDB Atlas
# Create collections if they don't exist (app will auto-create)
# Run any migration scripts
cd backend/scripts
python migrate_add_plan_credit.py
```

### Step 2: Deploy Backend

```bash
# Option A: Render/Railway (use GUI)
# Option B: Manual server
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 3: Test Backend

```bash
# Test API
curl https://your-backend-api.com/api/v1/health

# Test authentication
curl -X POST https://your-backend-api.com/api/v1/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "purpose": "register"}'
```

### Step 4: Update Frontend Config

```javascript
// frontend/config/env.js
export const API_CONFIG = {
  BASE_URL: 'https://your-backend-api.com/api/v1',
  // ...
};
```

### Step 5: Deploy Frontend

```bash
# Vercel
cd frontend
vercel --prod

# Or Netlify
netlify deploy --prod --dir=frontend
```

### Step 6: Test Frontend

- [ ] Open production URL
- [ ] Test registration flow
- [ ] Test login
- [ ] Test creating order
- [ ] Test wallet operations
- [ ] Test all major features

---

## Post-Deployment Verification

### Backend Health Check

```bash
# Health endpoint
GET https://your-backend-api.com/health

# API docs
GET https://your-backend-api.com/docs
```

### Frontend Check

- [ ] All pages load without errors
- [ ] API calls work (check Network tab)
- [ ] Authentication flow works
- [ ] Protected routes redirect correctly
- [ ] Images and assets load
- [ ] Mobile responsive

### Database Check

- [ ] Connections working
- [ ] Data persisting correctly
- [ ] Indexes created
- [ ] Backup configured

---

## Troubleshooting

### Common Issues

**Issue: CORS Error**
```
Access to fetch at 'https://api...' from origin 'https://frontend...' 
has been blocked by CORS policy
```
**Solution**: Add frontend domain to backend CORS allowed origins

**Issue: 500 Internal Server Error**
**Solution**: Check backend logs, verify environment variables

**Issue: MongoDB Connection Failed**
**Solution**: 
- Check MONGODB_URI format
- Verify IP whitelist includes deployment server IP
- Test connection string

**Issue: OTP Not Sending**
**Solution**:
- Verify Twilio credentials
- Check Twilio account balance
- Verify phone number format

**Issue: Images Not Loading**
**Solution**:
- Check paths are relative
- Verify uploads directory accessible
- Check file permissions

### Logging & Monitoring

**Backend Logs:**
- Check hosting platform logs (Render/Railway)
- Add logging to critical functions
- Monitor error rates

**Frontend Errors:**
- Use browser console
- Implement error tracking (Sentry, LogRocket)
- Monitor API failure rates

---

## Maintenance

### Regular Tasks

- [ ] Monitor server health
- [ ] Check database size & performance
- [ ] Review error logs
- [ ] Update dependencies
- [ ] Backup database
- [ ] Test disaster recovery

### Updates & Rollback

```bash
# Deploy new version
git push origin main  # (if auto-deploy enabled)

# Rollback (Render/Railway)
# Use platform GUI to revert to previous deployment
```

---

## Quick Reference

| Service | URL | Notes |
|---------|-----|-------|
| Backend API | https://your-backend.com/api/v1 | FastAPI |
| Frontend | https://your-frontend.com | Static files |
| API Docs | https://your-backend.com/docs | Swagger UI |
| Database | MongoDB Atlas | Cloud hosted |
| Monitoring | Platform dashboard | Check logs |

---

## Support & Documentation

- **Setup**: See `SETUP_INSTRUCTIONS.md`
- **API**: See `backend/ORDER_API_DOCUMENTATION.md`, `backend/WALLET_API_DOCUMENTATION.md`
- **Frontend**: See `frontend/REORGANIZATION_SUMMARY.md`
- **Database**: See `docs/DATABASE_SCHEMA.md`

---

**Last Updated**: 2026-01-15
**Status**: ✅ Ready for Production
