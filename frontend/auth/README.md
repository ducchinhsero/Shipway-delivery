# 🔐 Authentication Feature

## 📁 Files Structure

```
auth/
├── index.html           # Auth UI (Login, Register, Reset Password)
├── auth.css             # Styles
├── auth.js              # Business logic (auth service)
├── auth.controller.js   # UI controller (DOM manipulation)
└── img/                 # Assets
    ├── logo.png
    └── background.jpeg
```

## 🎯 Features

### ✅ Login
- Phone number + password authentication
- Country code selector (+84, +1, +82, +81)
- Remember me functionality
- Error handling & validation

### ✅ Register
- Progressive form (step-by-step)
- OTP verification
- Role selection (User/Driver)
- Phone, Name, Password fields

### ✅ Reset Password
- OTP-based password reset
- Phone verification
- New password setup

## 🔗 Backend Integration

### Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/send-otp` | POST | Send OTP code |
| `/api/v1/auth/verify-otp` | POST | Verify OTP |
| `/api/v1/auth/reset-password` | POST | Reset password |

### Request/Response Format

**Login:**
```javascript
// Request
{
  "phone": "+84123456789",
  "password": "yourpassword"
}

// Response
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "_id": "user_id",
    "phone": "+84123456789",
    "name": "Your Name",
    "role": "user"
  }
}
```

**Register:**
```javascript
// Request
{
  "phone": "+84123456789",
  "name": "Your Name",
  "password": "yourpassword",
  "role": "user",
  "otp": "123456"
}

// Response
{
  "success": true,
  "token": "jwt_token_here",
  "user": { ... }
}
```

## 🏗️ Architecture

### Data Flow

```
User Input
    ↓
auth.controller.js (UI Controller)
    ↓
auth.js (Business Logic)
    ↓
../shared/api.js (HTTP Requests)
    ↓
Backend API (FastAPI)
```

### State Management

```
auth.js → authStore.setToken() → ../shared/auth-store.js
       → authStore.setUser()
       → eventBus.emit()    → ../shared/event-bus.js
```

## 🚀 Usage

### 1. Prerequisites

**Backend:**
```bash
cd backend
python run.py
# Server: http://localhost:8000
```

**Frontend:**
- Use Live Server extension in VSCode
- Or: `python -m http.server 5500`
- Open: `http://localhost:5500/auth/index.html`

### 2. Test Flow

**Register Flow:**
1. Click "Chưa có tài khoản? Đăng ký"
2. Select role (User/Driver)
3. Enter phone number
4. Click "Gửi mã OTP"
5. Check console for OTP code (development mode)
6. Enter OTP
7. Enter name and password
8. Click "Đăng ký"

**Login Flow:**
1. Enter phone + password
2. Click "Đăng nhập"
3. Redirect to dashboard

**Reset Password:**
1. Click "Quên mật khẩu?"
2. Enter phone number
3. Get OTP
4. Enter new password
5. Confirm

## 🔧 Configuration

**Backend URL** (`../config/env.js`):
```javascript
BASE_URL: 'http://localhost:8000/api/v1'
```

**Storage Keys:**
- Token: `shipway_token`
- User Data: `shipway_user`

## 🎨 UI Components

### Progressive Forms
Forms reveal fields step-by-step for better UX:

1. **Register:**
   - Phone → OTP Button
   - OTP verified → Name & Password fields appear
   - Click Register

2. **Reset Password:**
   - Phone → OTP Button
   - OTP verified → New Password field appears
   - Click Reset

### Country Code Selector
```html
<select id="loginCountry">
  <option value="+84">🇻🇳 +84</option>
  <option value="+1">🇺🇸 +1</option>
  <option value="+82">🇰🇷 +82</option>
  <option value="+81">🇯🇵 +81</option>
</select>
```

### OTP Notification
Development helper showing OTP codes:
```javascript
window.showOtpNotification(phone, otp);
```

## 📝 Code Examples

### Using Auth Service

```javascript
import { loginUser, registerUser, sendOtp } from './auth.js';

// Login
const response = await loginUser('+84123456789', 'password');

// Register
await sendOtp('+84123456789', { purpose: 'register' });
const result = await registerUser({
  phone: '+84123456789',
  name: 'User Name',
  password: 'password',
  role: 'user',
  otp: '123456'
});
```

### Using Auth Store

```javascript
import { authStore } from '../shared/auth-store.js';

// Check auth
if (authStore.isAuth()) {
  const user = authStore.getUser();
  const token = authStore.getToken();
}

// Logout
authStore.clear();
```

## 🐛 Troubleshooting

### Issue: Module not found
**Solution:** Ensure shared modules exist:
- `../shared/api.js`
- `../shared/auth-store.js`
- `../shared/event-bus.js`

### Issue: CORS error
**Solution:** Backend has CORS enabled. Check server is running.

### Issue: OTP not showing
**Solution:** Check browser console (development mode shows OTP)

### Issue: Can't login after register
**Solution:** Use the phone WITH country code (e.g., `+84123456789`)

## ✅ Testing Checklist

- [ ] Register new user
- [ ] Receive OTP in console
- [ ] Verify OTP
- [ ] Complete registration
- [ ] Login with credentials
- [ ] Token saved to localStorage
- [ ] User data saved
- [ ] Reset password flow
- [ ] Logout
- [ ] Form validation works
- [ ] Error messages display

## 📊 Status

- ✅ **UI**: Complete
- ✅ **Business Logic**: Complete
- ✅ **Backend Integration**: Complete
- ✅ **State Management**: Complete
- ✅ **Event System**: Complete
- ✅ **Error Handling**: Complete
- ✅ **Validation**: Complete

**Status: READY FOR USE** 🎉

## 🔜 Next Features

After Authentication is stable:
1. Dashboard integration
2. Protected routes
3. Token refresh
4. Session timeout
5. Multi-factor authentication

---

**Last Updated:** 2026-01-15
**Backend API:** http://localhost:8000/docs
**Status:** ✅ Production Ready
