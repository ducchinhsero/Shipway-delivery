# 🗄️ Database Schema Design - Shipway

## 📊 Overview

Shipway sử dụng **MongoDB Atlas** (NoSQL) với 2 collections chính:
- `users` - Lưu trữ người dùng (Admin, User, Driver)
- `otps` - Lưu trữ mã OTP tạm thời

## 🏗️ Entity Relationship Diagram (Text)

```
┌─────────────────┐
│     USERS       │
│  (Collection)   │
├─────────────────┤
│ _id (PK)        │
│ phone (Unique)  │
│ name            │
│ password        │
│ role            │
│ email           │
│ isActive        │
│ isPhoneVerified │
│ avatar          │
│ driverInfo      │◄────────── (Embedded Document)
│ companyInfo     │◄────────── (Embedded Document)
│ lastLogin       │
│ refreshToken    │
│ createdAt       │
│ updatedAt       │
└─────────────────┘

┌─────────────────┐
│      OTPS       │
│  (Collection)   │
├─────────────────┤
│ _id (PK)        │
│ phone           │────┐
│ otp             │    │
│ purpose         │    │ (Reference - not FK)
│ attempts        │    │ Liên kết logic
│ isUsed          │    │ với users.phone
│ expiresAt (TTL) │    │
│ createdAt       │    │
│ updatedAt       │────┘
└─────────────────┘
```

---

## 📋 Collection Schemas

### 1. Users Collection

#### Collection Name: `users`

#### Purpose
Lưu trữ tất cả người dùng trong hệ thống với 3 roles:
- **admin**: Quản trị viên
- **user**: Đối tác vận chuyển
- **driver**: Tài xế

#### Schema Definition

```javascript
{
  // === BASIC INFO ===
  _id: ObjectId,                    // MongoDB auto-generated ID
  phone: String,                    // Số điện thoại (login identifier)
  name: String,                     // Họ và tên
  password: String,                 // Bcrypt hashed password
  role: String,                     // 'admin' | 'user' | 'driver'
  email: String | null,             // Email (optional)
  
  // === STATUS ===
  isActive: Boolean,                // Tài khoản có hoạt động không
  isPhoneVerified: Boolean,         // Đã xác thực SĐT qua OTP
  avatar: String | null,            // URL to avatar image
  
  // === DRIVER SPECIFIC (Embedded Document) ===
  driverInfo: {
    licenseNumber: String | null,   // Số bằng lái
    vehicleType: String | null,     // 'motorbike' | 'car' | 'truck' | 'van'
    vehiclePlate: String | null,    // Biển số xe
    isVerified: Boolean,            // Admin đã verify driver
    rating: Number,                 // Đánh giá 0-5 sao
    totalTrips: Number              // Tổng số chuyến đã chạy
  },
  
  // === USER/PARTNER SPECIFIC (Embedded Document) ===
  companyInfo: {
    companyName: String | null,     // Tên công ty
    taxCode: String | null,         // Mã số thuế
    address: String | null          // Địa chỉ công ty
  },
  
  // === SYSTEM FIELDS ===
  lastLogin: Date | null,           // Lần login cuối
  refreshToken: String | null,      // JWT refresh token (select: false)
  
  // === TIMESTAMPS ===
  createdAt: Date,                  // Auto by Mongoose timestamps
  updatedAt: Date                   // Auto by Mongoose timestamps
}
```

#### Field Details

| Field | Type | Required | Unique | Default | Notes |
|-------|------|----------|--------|---------|-------|
| _id | ObjectId | Yes | Yes | Auto | MongoDB ID |
| phone | String | Yes | Yes | - | Format: `+84XXXXXXXXX` |
| name | String | Yes | No | - | 2-100 characters |
| password | String | Yes | No | - | Bcrypt hash (select: false) |
| role | String | Yes | No | 'user' | Enum: admin/user/driver |
| email | String | No | No | null | Valid email format |
| isActive | Boolean | No | No | true | Account status |
| isPhoneVerified | Boolean | No | No | false | OTP verified |
| avatar | String | No | No | null | Image URL |
| driverInfo.licenseNumber | String | No | No | null | Driver only |
| driverInfo.vehicleType | String | No | No | null | Enum values |
| driverInfo.vehiclePlate | String | No | No | null | Driver only |
| driverInfo.isVerified | Boolean | No | No | false | Admin verified |
| driverInfo.rating | Number | No | No | 0 | 0-5 range |
| driverInfo.totalTrips | Number | No | No | 0 | Count |
| companyInfo.companyName | String | No | No | null | User/Partner only |
| companyInfo.taxCode | String | No | No | null | User/Partner only |
| companyInfo.address | String | No | No | null | User/Partner only |
| lastLogin | Date | No | No | null | Updated on login |
| refreshToken | String | No | No | null | select: false |
| createdAt | Date | Yes | No | Auto | Mongoose timestamp |
| updatedAt | Date | Yes | No | Auto | Mongoose timestamp |

#### Validation Rules

**Phone:**
```javascript
validate: {
  validator: function(v) {
    return /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/.test(v);
  },
  message: 'Số điện thoại không hợp lệ'
}
```

**Email:**
```javascript
validate: {
  validator: function(v) {
    if (!v) return true; // Optional
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  },
  message: 'Email không hợp lệ'
}
```

**Name:**
- Min length: 2 characters
- Max length: 100 characters
- Required

**Password:**
- Min length: 6 characters
- Required
- Automatically hashed before save

**Role:**
- Enum: ['admin', 'user', 'driver']
- Default: 'user'

**Vehicle Type:**
- Enum: ['motorbike', 'car', 'truck', 'van']
- Optional

#### Indexes

```javascript
// Primary Indexes
phone: 1 (unique)           // Fast lookup by phone, unique constraint

// Secondary Indexes
email: 1                    // Search by email
role: 1                     // Filter by role
createdAt: -1               // Sort by newest first

// Compound Indexes (Future)
{ role: 1, isActive: 1 }    // Active users by role
{ 'driverInfo.isVerified': 1, role: 1 }  // Verified drivers
```

#### Pre-save Middleware

**Password Hashing:**
```javascript
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});
```

#### Methods

**Compare Password:**
```javascript
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};
```

**To Safe Object:**
```javascript
userSchema.methods.toSafeObject = function() {
  const obj = this.toObject();
  delete obj.password;
  delete obj.refreshToken;
  delete obj.__v;
  return obj;
};
```

---

### 2. OTPs Collection

#### Collection Name: `otps`

#### Purpose
Lưu trữ mã OTP tạm thời cho:
- Đăng ký tài khoản (register)
- Đặt lại mật khẩu (reset-password)
- Xác thực số điện thoại (verify-phone)

#### Schema Definition

```javascript
{
  _id: ObjectId,                    // MongoDB auto-generated ID
  phone: String,                    // Số điện thoại nhận OTP
  otp: String,                      // Mã OTP (6 chữ số)
  purpose: String,                  // 'register' | 'reset-password' | 'verify-phone'
  
  attempts: Number,                 // Số lần thử verify (max: 5)
  isUsed: Boolean,                  // Đã sử dụng OTP chưa
  
  expiresAt: Date,                  // Thời gian hết hạn (TTL index)
  
  createdAt: Date,                  // Mongoose timestamp
  updatedAt: Date                   // Mongoose timestamp
}
```

#### Field Details

| Field | Type | Required | Default | TTL | Notes |
|-------|------|----------|---------|-----|-------|
| _id | ObjectId | Yes | Auto | - | MongoDB ID |
| phone | String | Yes | - | - | International format |
| otp | String | Yes | - | - | 6-digit code |
| purpose | String | Yes | - | - | Enum: 3 values |
| attempts | Number | No | 0 | - | Max: 5 |
| isUsed | Boolean | No | false | - | One-time use |
| expiresAt | Date | Yes | +5min | Yes | Auto-delete |
| createdAt | Date | Yes | Auto | - | Timestamp |
| updatedAt | Date | Yes | Auto | - | Timestamp |

#### Validation Rules

**Purpose:**
```javascript
enum: {
  values: ['register', 'reset-password', 'verify-phone'],
  message: 'Purpose không hợp lệ'
}
```

**Attempts:**
```javascript
type: Number,
default: 0,
max: 5  // Tối đa 5 lần thử
```

**OTP Format:**
- 6 chữ số
- Random generated
- Example: "123456"

#### Indexes

```javascript
// Compound Index
{ phone: 1, purpose: 1 }    // Find OTP by phone and purpose

// TTL Index (Auto-delete expired documents)
{ expiresAt: 1 }            // expires: 0 (delete when expiresAt < now)

// Sort Index
{ createdAt: 1 }            // Get latest OTP
```

#### TTL (Time To Live)

**Auto-Cleanup:**
```javascript
expiresAt: {
  type: Date,
  required: true,
  index: { expires: 0 }  // TTL index
}
```

- MongoDB tự động xóa documents khi `expiresAt < current time`
- Check interval: ~60 seconds
- Expiration time: 5 phút (có thể config qua `OTP_EXPIRE_MINUTES`)

#### Methods

**Is Expired:**
```javascript
otpSchema.methods.isExpired = function() {
  return new Date() > this.expiresAt;
};
```

**Is Attempts Exceeded:**
```javascript
otpSchema.methods.isAttemptsExceeded = function() {
  return this.attempts >= 5;
};
```

---

## 🔄 Data Flow Diagrams

### User Registration Flow

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │
       │ 1. POST /api/auth/send-otp
       │    { phone, purpose: 'register' }
       ▼
┌─────────────┐
│   Backend   │
│     API     │
└──────┬──────┘
       │
       │ 2. Check if phone exists in users
       │
       ▼
┌─────────────┐      NO
│    users    │──────────────┐
│ collection  │              │
└─────────────┘              │
                             │
                             │ 3. Generate OTP
                             │    Save to otps collection
                             ▼
                      ┌─────────────┐
                      │    otps     │
                      │ collection  │
                      └──────┬──────┘
                             │
                             │ 4. Send SMS via Twilio
                             │
                             ▼
                      ┌─────────────┐
                      │   Client    │
                      │ (Gets OTP)  │
                      └──────┬──────┘
                             │
                             │ 5. POST /api/auth/register
                             │    { phone, name, password, otp }
                             ▼
                      ┌─────────────┐
                      │   Backend   │
                      │ Verify OTP  │
                      └──────┬──────┘
                             │
                             │ 6. If valid OTP:
                             │    Create user in users collection
                             │    Mark OTP as used
                             ▼
                      ┌─────────────┐
                      │    users    │
                      │ collection  │
                      │ (New User)  │
                      └─────────────┘
```

### OTP Lifecycle

```
┌──────────────────────────────────────────────────────┐
│                    OTP LIFECYCLE                     │
└──────────────────────────────────────────────────────┘

1. CREATE
   ├─ Generate 6-digit random code
   ├─ Save to otps collection
   ├─ expiresAt = now + 5 minutes
   └─ attempts = 0, isUsed = false

2. VERIFY (Multiple Attempts Possible)
   ├─ User inputs OTP
   ├─ Backend checks:
   │  ├─ OTP exists?
   │  ├─ Not expired?
   │  ├─ Not used?
   │  └─ Attempts < 5?
   │
   ├─ If INCORRECT:
   │  ├─ Increment attempts++
   │  └─ If attempts >= 5: Delete OTP
   │
   └─ If CORRECT:
      ├─ Mark isUsed = true
      └─ Proceed with action (register/reset)

3. AUTO-CLEANUP
   ├─ MongoDB TTL index
   ├─ Check every ~60 seconds
   └─ Delete if expiresAt < now
```

---

## 📈 Data Growth Estimation

### Users Collection

**Assumptions:**
- 1,000 users/month
- Average document size: ~2 KB

**Growth:**

| Time | Users | Size | Notes |
|------|-------|------|-------|
| 1 month | 1,000 | ~2 MB | Minimal |
| 6 months | 6,000 | ~12 MB | Light |
| 1 year | 12,000 | ~24 MB | Still small |
| 3 years | 36,000 | ~72 MB | Manageable |

### OTPs Collection

**Assumptions:**
- 5,000 OTP requests/month
- TTL: 5 minutes
- Average document size: ~500 bytes

**Steady State:**
- ~17 OTPs at any given time (5 min window)
- Size: ~8.5 KB
- **Self-cleaning** via TTL

**Note:** OTPs collection sẽ luôn nhỏ do TTL auto-cleanup!

---

## 🔍 Query Patterns

### Common Queries

**1. Find User by Phone (Login)**
```javascript
db.users.findOne({ phone: "+84987654321" });
// Index: phone (unique) - O(1)
```

**2. Get All Active Users by Role**
```javascript
db.users.find({ 
  role: "driver", 
  isActive: true 
}).sort({ createdAt: -1 });
// Index: role + isActive (compound) - O(log n)
```

**3. Find Valid OTP**
```javascript
db.otps.findOne({ 
  phone: "+84987654321",
  purpose: "register",
  isUsed: false
}).sort({ createdAt: -1 });
// Index: { phone: 1, purpose: 1 } - O(log n)
```

**4. Get Verified Drivers**
```javascript
db.users.find({ 
  role: "driver",
  "driverInfo.isVerified": true,
  isActive: true
}).sort({ "driverInfo.rating": -1 });
// Index: driverInfo.isVerified + role (compound)
```

**5. Search Users by Name or Phone**
```javascript
db.users.find({
  $or: [
    { name: { $regex: "nguyen", $options: "i" } },
    { phone: { $regex: "0123", $options: "i" } }
  ]
});
// Text search - consider adding text index later
```

---

## 🔒 Security Considerations

### Password Security
- ✅ Bcrypt hashing (10 salt rounds)
- ✅ Never returned in queries (select: false)
- ✅ Min length: 6 characters
- ✅ Hashed before save (pre-save middleware)

### OTP Security
- ✅ 6-digit random code
- ✅ 5-minute expiration (TTL)
- ✅ Max 5 verification attempts
- ✅ One-time use (isUsed flag)
- ✅ Auto-cleanup via TTL
- ✅ Purpose-specific (can't reuse for different action)

### Phone Number
- ✅ Unique index (prevent duplicates)
- ✅ Validation regex
- ✅ International format support

### Sensitive Data
- ✅ refreshToken: select: false
- ✅ password: select: false
- ✅ No plaintext secrets in database

---

## 🛠️ Maintenance Tasks

### Regular Tasks

**Daily:**
- ✅ Auto: TTL cleanup (MongoDB automatic)

**Weekly:**
- Check index performance
- Monitor collection sizes

**Monthly:**
- Review slow queries
- Optimize indexes if needed
- Archive old inactive users (optional)

### Backup Strategy

**MongoDB Atlas Auto-Backup:**
- Continuous backup (paid tier)
- Point-in-time restore
- Manual snapshot before major changes

**Manual Backup:**
```bash
# Export users
mongoexport --uri="mongodb+srv://..." \
  --collection=users \
  --out=users_backup.json

# Export otps (if needed)
mongoexport --uri="mongodb+srv://..." \
  --collection=otps \
  --out=otps_backup.json
```

---

## 📊 Performance Optimization

### Indexes Strategy

**Current Indexes:**
```javascript
// users collection
{ phone: 1 }          // Primary lookup
{ email: 1 }          // Optional search
{ role: 1 }           // Filter by role
{ createdAt: -1 }     // Sort newest

// otps collection
{ phone: 1, purpose: 1 }  // Compound lookup
{ expiresAt: 1 }          // TTL cleanup
{ createdAt: 1 }          // Sort
```

**Future Indexes (When Needed):**
```javascript
// users collection
{ role: 1, isActive: 1 }                    // Active users by role
{ 'driverInfo.isVerified': 1, role: 1 }     // Verified drivers
{ lastLogin: -1 }                           // Sort by activity

// Text search
db.users.createIndex({ name: "text" });
```

### Query Performance Tips

1. **Always use indexes** - Check with `explain()`
2. **Limit results** - Use `.limit()` for pagination
3. **Project only needed fields** - Use `.select()`
4. **Avoid regex** on large datasets - Consider text index
5. **Use lean()** for read-only - Skip Mongoose overhead

---

## 🔄 Migration Strategy

### Version 1.0.0 (Current)
- users collection
- otps collection
- Basic indexes

### Future Migrations

**v1.1.0 - Add Text Search:**
```javascript
db.users.createIndex({ name: "text", email: "text" });
```

**v1.2.0 - Add Compound Indexes:**
```javascript
db.users.createIndex({ role: 1, isActive: 1 });
db.users.createIndex({ "driverInfo.isVerified": 1, role: 1 });
```

**v2.0.0 - Add New Collections:**
- orders collection
- shipments collection
- reviews collection

---

## 📚 References

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Mongoose Schema Guide](https://mongoosejs.com/docs/guide.html)
- [MongoDB Indexes](https://docs.mongodb.com/manual/indexes/)
- [TTL Indexes](https://docs.mongodb.com/manual/core/index-ttl/)

---

**Last Updated**: January 4, 2025  
**Version**: 1.0.0  
**Schema Version**: 1

