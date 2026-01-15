# 📦 Order/Booking API Documentation

## Tổng quan

API này cung cấp các chức năng quản lý đơn hàng (booking) cho hệ thống giao hàng Shipway, bao gồm:
- ✅ Tạo đơn hàng mới với thông tin pickup/dropoff
- ✅ Upload hình ảnh sản phẩm
- ✅ Tính toán tự động phí vận chuyển
- ✅ Theo dõi trạng thái đơn hàng
- ✅ Quản lý đơn hàng cho người dùng và tài xế

---

## 🔐 Authentication

Hầu hết các endpoint yêu cầu JWT token trong header:

```http
Authorization: Bearer <your_jwt_token>
```

**Ngoại trừ:**
- `GET /api/v1/orders/tracking/{tracking_code}` - Public endpoint (không cần auth)

---

## 📋 API Endpoints

### 1. **Tạo đơn hàng mới**

**Endpoint:** `POST /api/v1/orders`

**Content-Type:** `multipart/form-data`

**Authentication:** Required (User)

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pickup_address` | string | ✅ | Địa chỉ lấy hàng |
| `pickup_lat` | float | ✅ | Latitude điểm lấy hàng |
| `pickup_lng` | float | ✅ | Longitude điểm lấy hàng |
| `pickup_contact_name` | string | ✅ | Tên người liên hệ (pickup) |
| `pickup_contact_phone` | string | ✅ | SĐT liên hệ (pickup) |
| `pickup_note` | string | ❌ | Ghi chú điểm lấy hàng |
| `dropoff_address` | string | ✅ | Địa chỉ giao hàng |
| `dropoff_lat` | float | ✅ | Latitude điểm giao hàng |
| `dropoff_lng` | float | ✅ | Longitude điểm giao hàng |
| `dropoff_contact_name` | string | ✅ | Tên người liên hệ (dropoff) |
| `dropoff_contact_phone` | string | ✅ | SĐT liên hệ (dropoff) |
| `dropoff_note` | string | ❌ | Ghi chú điểm giao hàng |
| `product_name` | string | ✅ | Tên sản phẩm/hàng hóa |
| `weight` | float | ✅ | Khối lượng (kg) |
| `vehicle_type` | string | ✅ | Loại xe: `bike`, `car`, `van`, `truck_500kg`, `truck_1000kg` |
| `note` | string | ❌ | Ghi chú đơn hàng |
| `cod_amount` | float | ❌ | Tiền thu hộ (COD), mặc định 0 |
| `images` | file[] | ❌ | Hình ảnh sản phẩm (tối đa 5 ảnh, mỗi ảnh ≤ 5MB) |

**Response:**

```json
{
  "success": true,
  "message": "Đơn hàng đã được tạo thành công",
  "order_id": "65a1b2c3d4e5f6789012345",
  "tracking_code": "SW20240115001",
  "total_amount": 545000,
  "payment_required": false
}
```

**Logic:**
- Tính toán tự động khoảng cách và phí vận chuyển
- Kiểm tra số dư ví người dùng
- Nếu đủ tiền → tự động thanh toán và chuyển trạng thái sang `confirmed`
- Nếu không đủ → trạng thái `pending`, yêu cầu nạp thêm tiền

**Curl Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "pickup_address=123 Nguyễn Văn Linh, Q.7, TP.HCM" \
  -F "pickup_lat=10.7329269" \
  -F "pickup_lng=106.7172715" \
  -F "pickup_contact_name=Nguyễn Văn A" \
  -F "pickup_contact_phone=0912345678" \
  -F "dropoff_address=456 Lê Văn Việt, Q.9, TP.HCM" \
  -F "dropoff_lat=10.8231271" \
  -F "dropoff_lng=106.7574535" \
  -F "dropoff_contact_name=Trần Thị B" \
  -F "dropoff_contact_phone=0987654321" \
  -F "product_name=Quần áo thời trang" \
  -F "weight=5.5" \
  -F "vehicle_type=bike" \
  -F "cod_amount=500000" \
  -F "images=@/path/to/image1.jpg" \
  -F "images=@/path/to/image2.jpg"
```

---

### 2. **Lấy danh sách đơn hàng của tôi**

**Endpoint:** `GET /api/v1/orders`

**Authentication:** Required (User)

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | ❌ | Lọc theo trạng thái |
| `page` | int | ❌ | Trang (mặc định: 1) |
| `limit` | int | ❌ | Số đơn/trang (mặc định: 10, max: 50) |

**Response:**

```json
{
  "total": 50,
  "page": 1,
  "limit": 10,
  "orders": [
    {
      "id": "65a1b2c3d4e5f6789012345",
      "tracking_code": "SW20240115001",
      "user_id": "65a1b2c3d4e5f678901234",
      "driver_id": null,
      "pickup_info": { ... },
      "dropoff_info": { ... },
      "product_name": "Quần áo thời trang",
      "images": ["http://localhost:8000/uploads/orders/img1.jpg"],
      "weight": 5.5,
      "vehicle_type": "bike",
      "distance_km": 8.5,
      "shipping_fee": 45000,
      "cod_amount": 500000,
      "total_amount": 545000,
      "payment_method": "wallet",
      "is_paid": true,
      "status": "pending",
      "history": [...],
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Curl Example:**

```bash
curl -X GET "http://localhost:8000/api/v1/orders?status=pending&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 3. **Xem chi tiết đơn hàng**

**Endpoint:** `GET /api/v1/orders/{order_id}`

**Authentication:** Required (Owner/Driver/Admin)

**Response:** Giống như object trong danh sách orders

**Curl Example:**

```bash
curl -X GET "http://localhost:8000/api/v1/orders/65a1b2c3d4e5f6789012345" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 4. **Theo dõi đơn hàng (Public)**

**Endpoint:** `GET /api/v1/orders/tracking/{tracking_code}`

**Authentication:** Not Required (Public)

**Response:** Thông tin đơn hàng đầy đủ

**Curl Example:**

```bash
curl -X GET "http://localhost:8000/api/v1/orders/tracking/SW20240115001"
```

---

### 5. **Cập nhật trạng thái đơn hàng**

**Endpoint:** `PATCH /api/v1/orders/{order_id}/status`

**Authentication:** Required (Owner/Driver/Admin)

**Request Body:**

```json
{
  "status": "picked_up",
  "note": "Đã lấy hàng thành công"
}
```

**Trạng thái hợp lệ:**
- `pending` - Chờ xác nhận
- `confirmed` - Đã xác nhận
- `picking_up` - Đang đến lấy hàng
- `picked_up` - Đã lấy hàng
- `in_transit` - Đang vận chuyển
- `delivering` - Đang giao hàng
- `delivered` - Đã giao hàng
- `cancelled` - Đã hủy
- `failed` - Giao hàng thất bại

**Response:**

```json
{
  "success": true,
  "message": "Cập nhật trạng thái thành công",
  "new_status": "picked_up"
}
```

**Quyền hạn:**
- **Owner:** Chỉ có thể hủy đơn (`cancelled`) nếu đơn ở trạng thái `pending` hoặc `confirmed`
- **Driver:** Có thể cập nhật trạng thái của đơn được giao
- **Admin:** Có thể cập nhật bất kỳ đơn nào

**Curl Example:**

```bash
curl -X PATCH "http://localhost:8000/api/v1/orders/65a1b2c3d4e5f6789012345/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "picked_up", "note": "Đã lấy hàng"}'
```

---

### 6. **Hủy đơn hàng**

**Endpoint:** `DELETE /api/v1/orders/{order_id}`

**Authentication:** Required (Owner/Admin)

**Response:**

```json
{
  "success": true,
  "message": "Đã hủy đơn hàng thành công",
  "refunded": true
}
```

**Logic:**
- Chỉ có thể hủy đơn ở trạng thái `pending` hoặc `confirmed`
- Nếu đã thanh toán → tự động hoàn tiền vào ví

**Curl Example:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/orders/65a1b2c3d4e5f6789012345" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🚗 Driver Endpoints

### 7. **Xem đơn hàng khả dụng (Driver)**

**Endpoint:** `GET /api/v1/orders/available/list`

**Authentication:** Required (Driver only)

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vehicle_type` | string | ❌ | Lọc theo loại xe |
| `limit` | int | ❌ | Số đơn tối đa (mặc định: 20, max: 50) |

**Response:** Danh sách các đơn hàng chưa có tài xế nhận

**Curl Example:**

```bash
curl -X GET "http://localhost:8000/api/v1/orders/available/list?vehicle_type=bike&limit=20" \
  -H "Authorization: Bearer DRIVER_TOKEN"
```

---

### 8. **Nhận đơn hàng (Driver)**

**Endpoint:** `POST /api/v1/orders/{order_id}/accept`

**Authentication:** Required (Driver only)

**Response:**

```json
{
  "success": true,
  "message": "Đã nhận đơn hàng thành công",
  "order_id": "65a1b2c3d4e5f6789012345",
  "tracking_code": "SW20240115001"
}
```

**Logic:**
- Gán tài xế vào đơn hàng
- Tự động chuyển trạng thái sang `picking_up`

**Curl Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/orders/65a1b2c3d4e5f6789012345/accept" \
  -H "Authorization: Bearer DRIVER_TOKEN"
```

---

## 💰 Bảng giá vận chuyển

| Loại xe | Phí cơ bản | Giá/km | Khối lượng tối đa | Phụ phí (>50kg) |
|---------|-----------|--------|-------------------|-----------------|
| **Bike** | 15,000 VNĐ | 3,000 VNĐ | 30 kg | 0 |
| **Car** | 30,000 VNĐ | 5,000 VNĐ | 300 kg | 500 VNĐ/kg |
| **Van** | 50,000 VNĐ | 7,000 VNĐ | 500 kg | 400 VNĐ/kg |
| **Truck 500kg** | 80,000 VNĐ | 10,000 VNĐ | 500 kg | 300 VNĐ/kg |
| **Truck 1000kg** | 120,000 VNĐ | 15,000 VNĐ | 1000 kg | 200 VNĐ/kg |

**Phí COD:** 1% của số tiền COD (tối đa 50,000 VNĐ)

**Công thức:**
```
Shipping Fee = Base Fee + (Distance × Per KM) + Weight Surcharge + COD Fee
Total Amount = Shipping Fee + COD Amount
```

---

## 📸 Upload hình ảnh

**Yêu cầu:**
- Định dạng: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Kích thước tối đa: **5MB/ảnh**
- Số lượng tối đa: **5 ảnh/đơn hàng**

**Lưu trữ:**
- Ảnh được lưu tại: `uploads/orders/`
- URL truy cập: `http://localhost:8000/uploads/orders/{filename}`

---

## 🔄 Order Status Flow

```
pending → confirmed → picking_up → picked_up → in_transit → delivering → delivered
   ↓
cancelled (chỉ từ pending/confirmed)
```

---

## ❌ Error Codes

| Status Code | Description |
|------------|-------------|
| `400` | Bad Request - Dữ liệu không hợp lệ |
| `401` | Unauthorized - Chưa đăng nhập |
| `403` | Forbidden - Không có quyền truy cập |
| `404` | Not Found - Không tìm thấy đơn hàng |
| `500` | Internal Server Error - Lỗi server |

---

## 📝 Notes

1. **Auto Payment:** Nếu user có đủ tiền trong ví, đơn hàng sẽ tự động thanh toán và chuyển sang `confirmed`
2. **Refund:** Khi hủy đơn đã thanh toán, tiền sẽ tự động hoàn lại ví
3. **Driver Assignment:** Chỉ tài xế mới có thể nhận đơn hàng
4. **Tracking:** Mã vận đơn có thể tra cứu công khai không cần đăng nhập
5. **History:** Mọi thay đổi trạng thái đều được ghi lại trong `history`

---

## 🧪 Testing

Xem file `test-order-api.ps1` để test tất cả các endpoint.

---

**Created:** 2024-01-15  
**Version:** 1.0.0  
**Author:** Shipway Development Team
