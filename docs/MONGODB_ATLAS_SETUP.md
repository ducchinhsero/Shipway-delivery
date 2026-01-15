# 🗄️ Hướng dẫn cấu hình MongoDB Atlas cho Shipway

## Tổng quan

MongoDB Atlas là dịch vụ database cloud của MongoDB. Hướng dẫn này sẽ giúp bạn tạo và cấu hình database cho dự án Shipway.

## Bước 1: Tạo tài khoản MongoDB Atlas

1. Truy cập: https://www.mongodb.com/cloud/atlas/register
2. Đăng ký tài khoản mới hoặc đăng nhập nếu đã có

## Bước 2: Tạo Organization và Project

### Tạo Organization

1. Click vào avatar (góc phải trên) → **Organizations**
2. Click **Create New Organization**
3. Nhập tên: `Shipway`
4. Click **Next** → **Create Organization**

### Tạo Project

1. Trong Organization vừa tạo, click **New Project**
2. Nhập tên project: `shipway` (chữ thường)
3. Click **Next** → **Create Project**

## Bước 3: Tạo Cluster (Database)

1. Trong project `shipway`, click **Build a Database**
2. Chọn **FREE** (M0 Sandbox) - Đủ cho development
3. **Cloud Provider**: AWS (recommended)
4. **Region**: Chọn `Singapore (ap-southeast-1)` - Gần Việt Nam nhất
5. **Cluster Name**: Để mặc định hoặc đặt `Cluster0`
6. Click **Create**

⏱️ Chờ 3-5 phút để cluster được khởi tạo...

## Bước 4: Tạo Database User

1. Trên màn hình **Security Quickstart**, mục **How would you like to authenticate your connection?**
2. Chọn **Username and Password**
3. Nhập:
   - **Username**: `shipway_admin`
   - **Password**: Click **Autogenerate Secure Password** hoặc tự đặt
   - ⚠️ **LƯU LẠI PASSWORD** - Bạn sẽ cần nó sau!
4. Click **Create User**

## Bước 5: Cấu hình Network Access

1. Mục **Where would you like to connect from?**
2. Chọn **My Local Environment**
3. Click **Add My Current IP Address**
4. Hoặc để cho phép mọi IP (không khuyến khích cho production):
   - Click **Add IP Address**
   - Nhập: `0.0.0.0/0`
   - Description: `Allow all IPs (development only)`
5. Click **Finish and Close**

## Bước 6: Lấy Connection String

1. Click **Connect** trên cluster của bạn
2. Chọn **Drivers**
3. Driver: **Node.js**, Version: **4.1 or later**
4. Copy **Connection String**:

```
mongodb+srv://shipway_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

## Bước 7: Cấu hình trong dự án

### 7.1. Chỉnh sửa Connection String

Thay thế `<password>` bằng password thật:

```
mongodb+srv://shipway_admin:YourActualPassword123@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority
```

⚠️ **Quan trọng**: Thêm `/shipway` sau `.net` để chỉ định database name

### 7.2. Cập nhật file .env

Mở `backend/.env` và cập nhật:

```env
MONGODB_URI=mongodb+srv://shipway_admin:YourActualPassword123@cluster0.xxxxx.mongodb.net/shipway?retryWrites=true&w=majority
```

### 7.3. Test connection

```bash
cd backend
npm run dev
```

Nếu thành công, bạn sẽ thấy:

```
✅ MongoDB Connected: cluster0-shard-00-00.xxxxx.mongodb.net
📊 Database Name: shipway
🚀 Server is running on port 5000
```

## Bước 8: Seed Admin Account

```bash
npm run seed
```

Output:

```
✅ Admin account created successfully!
📱 Phone: +84987654321
🔑 Password: Admin@123456
```

## Bước 9: Verify trên MongoDB Atlas

1. Quay lại MongoDB Atlas Dashboard
2. Click **Browse Collections**
3. Bạn sẽ thấy:
   - Database: `shipway`
   - Collections:
     - `users` (1 document - admin)
     - `otps` (0 documents)

## Troubleshooting

### Lỗi: "Authentication failed"

**Nguyên nhân**: Username hoặc password sai

**Giải pháp**:
1. Vào **Database Access** trong Atlas
2. Edit user `shipway_admin`
3. Reset password hoặc tạo user mới

### Lỗi: "Connection timeout"

**Nguyên nhân**: IP chưa được whitelist

**Giải pháp**:
1. Vào **Network Access** trong Atlas
2. Thêm IP hiện tại hoặc `0.0.0.0/0`

### Lỗi: "Database name is missing"

**Nguyên nhân**: Thiếu `/shipway` trong connection string

**Giải pháp**:
- Đảm bảo connection string có format:
  ```
  mongodb+srv://.../@cluster.net/shipway?...
                                 ^^^^^^^^ Database name
  ```

### Lỗi: "MongoServerError: bad auth"

**Nguyên nhân**: Password chứa ký tự đặc biệt chưa được encode

**Giải pháp**:

Nếu password có ký tự đặc biệt (như `@`, `#`, `$`), cần encode chúng:

```javascript
// Ví dụ: password = "Pass@123"
// Phải encode thành: "Pass%40123"
```

Hoặc đặt lại password không có ký tự đặc biệt.

## Collections Structure

### users

```javascript
{
  "_id": ObjectId,
  "phone": "+84987654321",
  "name": "Shipway Administrator",
  "password": "$2a$10$...", // bcrypt hash
  "role": "admin",
  "isActive": true,
  "isPhoneVerified": true,
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

### otps

```javascript
{
  "_id": ObjectId,
  "phone": "+84123456789",
  "otp": "123456",
  "purpose": "register",
  "attempts": 0,
  "isUsed": false,
  "expiresAt": ISODate,
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## Best Practices

### Development

✅ Sử dụng Free Tier (M0)
✅ Whitelist IP cụ thể
✅ Tạo user với quyền `readWrite` trên database `shipway`

### Production

✅ Upgrade lên M10 trở lên (có auto-backup)
✅ Whitelist ONLY server IPs
✅ Enable **Two-Factor Authentication**
✅ Enable **Database Auditing**
✅ Setup **Monitoring & Alerts**
✅ Tạo **Backup** schedule

## Indexes

Các index đã được tự động tạo trong models:

### users collection

```javascript
{ phone: 1 }      // unique
{ email: 1 }
{ role: 1 }
{ createdAt: -1 }
```

### otps collection

```javascript
{ phone: 1, purpose: 1 }
{ expiresAt: 1 }           // TTL index
{ createdAt: 1 }
```

Để xem indexes:
1. MongoDB Atlas → Browse Collections
2. Chọn collection → Indexes tab

## Monitoring

### Metrics to watch

1. **Connections**: Số lượng connections đang active
2. **Operations**: Read/Write operations per second
3. **Network**: Data transfer
4. **Storage**: Database size

Access: Cluster → Metrics tab

## Backup & Restore

### Free Tier (M0)

- ❌ Không có auto-backup
- ✅ Có thể export manually:
  ```bash
  mongoexport --uri="mongodb+srv://..." --collection=users --out=users.json
  ```

### Paid Tier (M10+)

- ✅ Auto-backup daily
- ✅ Point-in-time restore
- ✅ Snapshot restore

## Support

- **MongoDB Docs**: https://docs.mongodb.com/
- **Atlas Docs**: https://docs.atlas.mongodb.com/
- **Community Forums**: https://community.mongodb.com/

---

**Last Updated**: January 4, 2025

