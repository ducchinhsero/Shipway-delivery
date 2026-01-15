# 🔐 Environment Variables Guide

## 📋 Overview

File `.env` chứa các biến môi trường quan trọng cho ứng dụng. **KHÔNG BAO GIỜ** commit file này vào Git.

---

## 🚀 Quick Setup

### Development (Local)

```bash
# 1. Copy template
cp env.example.txt .env

# 2. Edit file
nano .env

# 3. Fill in required values (tối thiểu)
MONGO_URI=mongodb://localhost:27017
DB_NAME=shipway
SECRET_KEY=dev-secret-key-change-in-production

# 4. Start app
python run.py
```

### Production

```bash
# 1. Copy template
cp env.example.txt .env

# 2. Edit file
nano .env

# 3. Fill in ALL production values
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/shipway?retryWrites=true
DB_NAME=shipway
SECRET_KEY=<generate-strong-secret>
TWILIO_ACCOUNT_SID=<your-sid>
TWILIO_AUTH_TOKEN=<your-token>
TWILIO_PHONE_NUMBER=<your-number>

# 4. Generate strong SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📝 All Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://...` |
| `DB_NAME` | Database name | `shipway` |
| `SECRET_KEY` | JWT secret key (32+ chars) | `<generate-unique>` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `APP_NAME` | Application name | `Shipway API` | `My App` |
| `NODE_ENV` | Environment | `development` | `production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry | `1440` (1 day) | `10080` (7 days) |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` | `HS256` |
| `OTP_EXPIRE_MINUTES` | OTP expiry | `5` | `10` |
| `OTP_MAX_ATTEMPTS` | Max OTP attempts | `5` | `3` |
| `HOST` | Server host | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Server port | `8000` | `8080` |

### Twilio Variables (SMS OTP)

| Variable | Required | Description |
|----------|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Production only | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Production only | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Production only | Twilio verified phone (+format) |

**Note**: Nếu không có Twilio credentials, OTP sẽ được trả về trong response (development mode only).

---

## 🔧 Configuration by Environment

### Development (Local)

```env
# Minimal setup for local development
NODE_ENV=development
MONGO_URI=mongodb://localhost:27017
DB_NAME=shipway
SECRET_KEY=dev-secret-not-for-production

# Twilio optional (OTP will return in response)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

**Features:**
- ✅ Local MongoDB
- ✅ OTP in response (no SMS)
- ✅ Hot reload
- ✅ Debug logs

### Staging

```env
NODE_ENV=staging
MONGO_URI=mongodb+srv://staging_user:password@cluster0.xxxxx.mongodb.net/shipway_staging?retryWrites=true
DB_NAME=shipway_staging
SECRET_KEY=<unique-staging-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Use Twilio test credentials
TWILIO_ACCOUNT_SID=<test-sid>
TWILIO_AUTH_TOKEN=<test-token>
TWILIO_PHONE_NUMBER=<test-number>

HOST=0.0.0.0
PORT=8000
```

**Features:**
- ✅ MongoDB Atlas (staging cluster)
- ✅ Twilio test credentials
- ✅ Similar to production
- ✅ Safe for testing

### Production

```env
NODE_ENV=production
MONGO_URI=mongodb+srv://prod_user:STRONG_PASSWORD@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority
DB_NAME=shipway
SECRET_KEY=<STRONG-32-CHAR-SECRET>
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256

OTP_EXPIRE_MINUTES=5
OTP_MAX_ATTEMPTS=5

# Production Twilio
TWILIO_ACCOUNT_SID=<production-sid>
TWILIO_AUTH_TOKEN=<production-token>
TWILIO_PHONE_NUMBER=<production-number>

HOST=0.0.0.0
PORT=8000
WORKERS=4
```

**Features:**
- ✅ MongoDB Atlas (production cluster)
- ✅ Production Twilio (real SMS)
- ✅ Strong security
- ✅ High availability

---

## 🔐 Security Best Practices

### 1. SECRET_KEY

**❌ BAD:**
```env
SECRET_KEY=123456
SECRET_KEY=my-secret-key
SECRET_KEY=your-super-secret-key-change-this
```

**✅ GOOD:**
```env
# Generate with:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output:
SECRET_KEY=xQR9KpT5vN2mL8wY4bH7jF3nA6sD1gK9
```

### 2. MongoDB Connection

**❌ BAD:**
```env
# Weak password
MONGO_URI=mongodb+srv://admin:123456@cluster.mongodb.net/

# No auth source
MONGO_URI=mongodb://user:pass@host:27017/db

# Exposed credentials
MONGO_URI=mongodb+srv://myemail@gmail.com:mypassword@...
```

**✅ GOOD:**
```env
# Strong password + auth params
MONGO_URI=mongodb+srv://shipway_prod:Kj9#mL2$pQ5@xR8&cluster0.mongodb.net/shipway?retryWrites=true&w=majority&authSource=admin

# Use environment-specific users
# - Development: dev_user
# - Staging: staging_user
# - Production: prod_user
```

### 3. Twilio Credentials

**❌ BAD:**
```env
# Using test credentials in production
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=test_token_123456
```

**✅ GOOD:**
```env
# Production credentials from Twilio console
TWILIO_ACCOUNT_SID=ACa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TWILIO_AUTH_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TWILIO_PHONE_NUMBER=+84987654321
```

### 4. File Permissions

```bash
# Set strict permissions for .env
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (only owner can read/write)

# Owner should be the user running the app
sudo chown app_user:app_user .env
```

### 5. Backup

```bash
# Backup .env to secure location
sudo cp .env /root/.env.backup.$(date +%Y%m%d)
sudo chmod 600 /root/.env.backup.*

# List backups
ls -la /root/.env.backup.*
```

---

## 🧪 Testing Configuration

### Verify .env is loaded

```python
# Test script: test_config.py
from app.core.config import settings

print(f"MongoDB: {settings.get_mongodb_url()}")
print(f"DB Name: {settings.get_db_name()}")
print(f"JWT Secret: {settings.get_jwt_secret()[:10]}...")
print(f"Twilio SID: {settings.TWILIO_ACCOUNT_SID[:10] if settings.TWILIO_ACCOUNT_SID else 'Not set'}...")
```

Run:
```bash
python test_config.py
```

### Check MongoDB Connection

```python
# Test MongoDB connection
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def test_mongo():
    client = AsyncIOMotorClient(settings.get_mongodb_url())
    try:
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        
        db = client[settings.get_db_name()]
        collections = await db.list_collection_names()
        print(f"Collections: {collections}")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    finally:
        client.close()

asyncio.run(test_mongo())
```

---

## 🔄 Rotation & Updates

### When to Rotate

- **SECRET_KEY**: Every 6 months or after security incident
- **MongoDB Password**: Every 3-6 months
- **Twilio Token**: If compromised

### How to Rotate SECRET_KEY

```bash
# 1. Generate new key
NEW_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# 2. Update .env
nano .env
# Change SECRET_KEY to new value

# 3. Restart service
sudo systemctl restart shipway-api

# 4. Test
curl https://apishipway.lpwanmapper.com/health

# 5. All existing tokens will be invalidated
# Users need to login again
```

### How to Update MongoDB

```bash
# 1. Update password in MongoDB Atlas
# 2. Update MONGO_URI in .env with new password
# 3. Restart service
sudo systemctl restart shipway-api
```

---

## 📊 Environment Variables Priority

FastAPI loads environment variables in this order:

1. **System environment variables** (highest priority)
2. **`.env` file** (in project root)
3. **Default values** in `config.py` (lowest priority)

Example:
```python
# config.py
class Settings(BaseSettings):
    SECRET_KEY: str = "default-key"  # Used if not in .env or system env
    
    class Config:
        env_file = ".env"
```

---

## 🐛 Troubleshooting

### Issue 1: "ValidationError: MONGO_URI Extra inputs are not permitted"

**Cause**: Typo in variable name in `.env`

**Fix:**
```bash
# Check for typos
cat .env | grep MONGO

# Should be MONGO_URI, not MONGODB_URI (unless using old format)
```

### Issue 2: "SECRET_KEY not found"

**Cause**: `.env` file not in correct location

**Fix:**
```bash
# .env must be in backend-python/ directory
cd backend-python
ls -la .env

# If not found, create it
cp env.example.txt .env
```

### Issue 3: "MongoDB connection timeout"

**Cause**: Wrong connection string or IP not whitelisted

**Fix:**
```bash
# 1. Check connection string
cat .env | grep MONGO_URI

# 2. Go to MongoDB Atlas
# 3. Network Access → Add IP: 0.0.0.0/0 (all) or specific IP

# 4. Test connection
python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
async def test():
    client = AsyncIOMotorClient('YOUR_MONGO_URI')
    await client.admin.command('ping')
    print('Connected!')
asyncio.run(test())
"
```

### Issue 4: "Twilio authentication failed"

**Cause**: Wrong credentials or test credentials in production

**Fix:**
```bash
# 1. Verify credentials in Twilio console
# 2. Check .env values
cat .env | grep TWILIO

# 3. Make sure no extra spaces
TWILIO_ACCOUNT_SID=ACxxxx   # ❌ (space before value)
TWILIO_ACCOUNT_SID=ACxxxx    # ✅
```

---

## 📚 References

- **Pydantic Settings**: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- **MongoDB Connection Strings**: https://www.mongodb.com/docs/manual/reference/connection-string/
- **Twilio Credentials**: https://console.twilio.com/
- **JWT Best Practices**: https://datatracker.ietf.org/doc/html/rfc8725

---

## ✅ Checklist

Before deploying:

- [ ] `.env` file created from template
- [ ] `SECRET_KEY` generated (32+ chars)
- [ ] MongoDB connection string configured
- [ ] MongoDB IP whitelist updated
- [ ] Twilio credentials added (production)
- [ ] File permissions set (`chmod 600 .env`)
- [ ] `.env` added to `.gitignore`
- [ ] Configuration tested locally
- [ ] Backup created

---

**Last updated**: January 8, 2025  
**Version**: 2.0.0
