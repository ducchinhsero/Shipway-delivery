# 🔄 Onboarding Integration with Auth System

## ✅ What Changed

### Before (Mock System)
```javascript
// Used fake auth
localStorage.setItem("shipway_user", JSON.stringify(user));
function login(role = "shipper") { /* mock */ }
```

**Problems:**
- ❌ Different localStorage keys than real auth
- ❌ No JWT token
- ❌ Couldn't access real dashboard
- ❌ Mock data not compatible with backend

### After (Real Auth Integration)
```javascript
// Uses production auth
import { authStore } from '../shared/auth-store.js';
authStore.isAuthenticated()
authStore.getUser()
authStore.logout()
```

**Benefits:**
- ✅ Same auth system across all pages
- ✅ JWT token managed properly
- ✅ Can access real dashboard after login
- ✅ Compatible with backend API

---

## 🎯 How It Works Now

### User Flow

1. **User visits Onboarding** (`frontend/onboarding/index.html`)
   - If NOT logged in: Shows "Đăng nhập" and "Đăng ký" buttons
   - If logged in: Shows "Dashboard" and "Đăng xuất" buttons

2. **User clicks "Đăng nhập"**
   - Redirects to `frontend/auth/index.html`
   - User logs in with real backend
   - Backend returns JWT token
   - Token saved in localStorage

3. **User returns to Onboarding**
   - `authStore` detects token
   - Header updates to show Dashboard button
   - Clicking Dashboard goes to real dashboard

4. **User clicks "Đăng xuất"**
   - Calls `authStore.logout()`
   - Clears token and user data
   - Page reloads, back to logged-out state

---

## 🔧 Technical Details

### Auth Store Integration

```javascript
import { authStore } from '../shared/auth-store.js';

// Check auth status
if (authStore.isAuthenticated()) {
  const user = authStore.getUser();
  console.log(user.name, user.role);
}

// Logout
authStore.logout();
```

### Storage Keys (Standardized)

| Key | Purpose | Example |
|-----|---------|---------|
| `auth:token` | JWT token | `eyJhbGciOiJIUzI1...` |
| `auth:user` | User data | `{"id": 1, "name": "...", "role": "user"}` |
| `auth:isAuthenticated` | Auth flag | `true` / `false` |

**Old mock keys removed:**
- ❌ `shipway_user` (no longer used)

---

## 📝 Files Modified

1. **`frontend/onboarding/js/main.js`**
   - Replaced mock auth with real auth
   - Integrated with `authStore`
   - Dynamic dashboard URL based on role
   - Clean logout function

2. **`frontend/onboarding/index.html`**
   - Updated script tag (removed `defer`, using ES6 modules)

---

## 🧪 Testing

### Test Logged-Out State
1. Clear localStorage: `localStorage.clear()`
2. Visit `frontend/onboarding/index.html`
3. Should see: "Đăng nhập" and "Đăng ký" buttons

### Test Logged-In State
1. Login via `frontend/auth/index.html`
2. Return to `frontend/onboarding/index.html`
3. Should see: "Dashboard" and "Đăng xuất" buttons
4. Click "Dashboard" → Goes to user dashboard
5. Click "Đăng xuất" → Logs out, page reloads

### Test Role-Based Dashboard
- User role → `frontend/user/dashboard/`
- Driver role → `frontend/driver/dashboard/`

---

## 🎨 UI States

### Not Logged In
```
[Trang chủ] [Về chúng tôi] [Đăng nhập] [Đăng ký]
```

### Logged In (User)
```
[Trang chủ] [Về chúng tôi] [Dashboard] [Đăng xuất]
                            ↓
                    user/dashboard/
```

### Logged In (Driver)
```
[Trang chủ] [Về chúng tôi] [Dashboard] [Đăng xuất]
                            ↓
                    driver/dashboard/
```

---

## ⚠️ Breaking Changes

### Removed Functions
- ❌ `login(role)` - Use real auth instead
- ❌ `loadUserFromStorage()` - Handled by authStore
- ❌ `AppState` object - Replaced by authStore

### Migration Guide

**If you were using mock login in console:**

Before:
```javascript
login("shipper")  // ❌ No longer works
```

After:
```javascript
// Must login through frontend/auth/index.html
// Or manually set in console (for testing):
localStorage.setItem('auth:token', 'your-jwt-token');
localStorage.setItem('auth:user', JSON.stringify({
  id: 1,
  name: 'Test User',
  role: 'user'
}));
location.reload();
```

---

## 🚀 Benefits

1. **Consistency**: Same auth across all pages
2. **Security**: Real JWT tokens, not mock data
3. **Scalability**: Easy to add new protected features
4. **Maintainability**: Single source of truth for auth
5. **User Experience**: Seamless navigation between pages

---

## 📚 Related Files

- `frontend/shared/auth-store.js` - Auth state management
- `frontend/shared/auth-guard.js` - Route protection
- `frontend/shared/api.js` - API calls with auth
- `frontend/auth/` - Login/Register pages

---

**Last Updated**: 2026-01-15
**Status**: ✅ Integrated with production auth
