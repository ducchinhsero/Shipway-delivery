# 📦 Hướng Dẫn Sử Dụng Tính Năng Tạo Đơn Hàng

## 📋 Tổng Quan

Tính năng tạo đơn hàng đã được hoàn thiện với đầy đủ các chức năng:

### ✅ Backend API (Hoàn Chỉnh)
- ✅ Tạo đơn hàng với multipart/form-data
- ✅ Upload hình ảnh sản phẩm (tối đa 5 ảnh)
- ✅ Tính toán tự động khoảng cách và phí vận chuyển
- ✅ Tích hợp ví điện tử (tự động thanh toán nếu đủ tiền)
- ✅ Lưu trữ đơn hàng vào MongoDB
- ✅ API xem chi tiết đơn hàng
- ✅ API quản lý trạng thái đơn hàng

### ✅ Frontend (Hoàn Chỉnh)
- ✅ Form tạo đơn hàng với đầy đủ trường thông tin
- ✅ Tính khoảng cách và ước tính phí shipping tự động
- ✅ Upload và preview hình ảnh
- ✅ Validation đầy đủ
- ✅ Trang chi tiết đơn hàng kết nối với API thực

---

## 🚀 Cách Sử Dụng

### 1. **Khởi Động Backend**

```bash
cd backend
python run.py
```

Server sẽ chạy tại: `http://localhost:8000`

### 2. **Truy Cập Frontend**

Mở trình duyệt và truy cập:
```
http://localhost:8000/frontend/user/booking/index.html
```

### 3. **Tạo Đơn Hàng Mới**

#### Bước 1: Điền thông tin điểm lấy hàng
- **Địa chỉ lấy hàng**: Địa chỉ đầy đủ
- **Tên người gửi**: Tên người liên hệ
- **SĐT người gửi**: Số điện thoại (format: 0912345678)
- **Vĩ độ (Latitude)**: Tọa độ vĩ độ (ví dụ: 10.7329269)
- **Kinh độ (Longitude)**: Tọa độ kinh độ (ví dụ: 106.7172715)
- **Ghi chú điểm lấy hàng**: Ghi chú tùy chọn

#### Bước 2: Điền thông tin điểm giao hàng
- Tương tự như điểm lấy hàng

#### Bước 3: Thông tin hàng hóa
- **Tên hàng hóa**: Tên sản phẩm/hàng hóa
- **Trọng lượng**: Khối lượng tính bằng kg
- **Loại xe vận chuyển**: Chọn loại xe phù hợp
  - Xe máy (tối đa 30kg)
  - Xe ô tô (tối đa 300kg)
  - Xe van (tối đa 500kg)
  - Xe tải 500kg
  - Xe tải 1 tấn
- **Kích thước** (tùy chọn): Dài x Rộng x Cao (cm)

#### Bước 4: Tính phí vận chuyển
- Hệ thống sẽ **tự động tính** khi bạn nhập đủ thông tin:
  - Khoảng cách giữa 2 điểm
  - Phí vận chuyển ước tính

#### Bước 5: Thông tin bổ sung
- **Tiền thu hộ (COD)**: Số tiền cần thu hộ (tùy chọn)
- **Ghi chú đơn hàng**: Ghi chú thêm (tùy chọn)
- **Ảnh hàng hóa**: Upload tối đa 5 ảnh (tùy chọn)

#### Bước 6: Xác nhận
- Nhấn nút **"Xác nhận"**
- Hệ thống sẽ:
  1. Kiểm tra số dư ví
  2. Tạo đơn hàng
  3. Upload ảnh (nếu có)
  4. Tự động thanh toán nếu đủ tiền
  5. Chuyển đến trang chi tiết đơn hàng

### 4. **Xem Chi Tiết Đơn Hàng**

Sau khi tạo đơn thành công, bạn sẽ được chuyển đến trang chi tiết hiển thị:
- ✅ Mã vận đơn (tracking code)
- ✅ Trạng thái đơn hàng
- ✅ Thông tin điểm lấy/giao hàng
- ✅ Thông tin hàng hóa
- ✅ Thông tin tài xế (khi có)
- ✅ Tổng tiền
- ✅ Ảnh hàng hóa

---

## 📊 Cấu Trúc Dữ Liệu

### Order Schema

```javascript
{
  _id: ObjectId,
  tracking_code: "SW20240115001",
  user_id: "user_id",
  driver_id: "driver_id" | null,
  
  pickup_info: {
    address: string,
    lat: float,
    lng: float,
    contact_name: string,
    contact_phone: string,
    note: string
  },
  
  dropoff_info: {
    address: string,
    lat: float,
    lng: float,
    contact_name: string,
    contact_phone: string,
    note: string
  },
  
  product_name: string,
  images: [string],
  weight: float,
  length: float,
  width: float,
  height: float,
  vehicle_type: string,
  note: string,
  
  distance_km: float,
  shipping_fee: float,
  cod_amount: float,
  total_amount: float,
  
  payment_method: "wallet" | "cod" | "card",
  is_paid: boolean,
  
  status: "pending" | "confirmed" | "picking_up" | "picked_up" | "in_transit" | "delivering" | "delivered" | "cancelled" | "failed",
  history: [
    {
      status: string,
      timestamp: datetime,
      note: string,
      updated_by: string
    }
  ],
  
  is_reviewed: boolean,
  created_at: datetime,
  updated_at: datetime
}
```

---

## 💰 Bảng Giá Vận Chuyển

| Loại xe | Phí cơ bản | Giá/km | Khối lượng tối đa | Phụ phí (>50kg) |
|---------|-----------|--------|-------------------|-----------------|
| **Xe máy** | 15,000 VNĐ | 3,000 VNĐ | 30 kg | 0 |
| **Xe ô tô** | 30,000 VNĐ | 5,000 VNĐ | 300 kg | 500 VNĐ/kg |
| **Xe van** | 50,000 VNĐ | 7,000 VNĐ | 500 kg | 400 VNĐ/kg |
| **Xe tải 500kg** | 80,000 VNĐ | 10,000 VNĐ | 500 kg | 300 VNĐ/kg |
| **Xe tải 1 tấn** | 120,000 VNĐ | 15,000 VNĐ | 1000 kg | 200 VNĐ/kg |

**Phí COD:** 1% của số tiền COD (tối đa 50,000 VNĐ)

**Công thức:**
```
Shipping Fee = Base Fee + (Distance × Per KM) + Weight Surcharge + COD Fee
Total Amount = Shipping Fee + COD Amount
```

---

## 🔄 Quy Trình Xử Lý Đơn Hàng

```
1. USER tạo đơn hàng
   ↓
2. Hệ thống tính phí vận chuyển
   ↓
3. Kiểm tra số dư ví
   ↓
4. [Nếu đủ tiền]
   - Tự động trừ tiền từ ví
   - Chuyển trạng thái: pending → confirmed
   ↓
5. [Nếu không đủ tiền]
   - Giữ trạng thái: pending
   - Yêu cầu nạp thêm tiền
   ↓
6. DRIVER nhận đơn
   - Chuyển trạng thái: confirmed → picking_up
   ↓
7. DRIVER cập nhật trạng thái theo tiến trình
   - picking_up → picked_up → in_transit → delivering → delivered
```

---

## 📁 Cấu Trúc File

### Backend
```
backend/
├── app/
│   ├── api/v1/
│   │   ├── orders.py          # Order API endpoints
│   │   └── router.py          # API router (đã include orders)
│   ├── schemas/
│   │   └── order.py           # Order Pydantic schemas
│   ├── services/
│   │   ├── upload_service.py  # Upload hình ảnh
│   │   └── pricing_service.py # Tính phí vận chuyển
│   ├── db/
│   │   └── models.py          # Database functions (đã có order functions)
│   └── main.py                # Main app (đã mount static files)
└── uploads/orders/            # Thư mục lưu ảnh
```

### Frontend
```
frontend/user/
├── booking/                   # Form tạo đơn hàng
│   ├── index.html            # HTML (đã cập nhật đầy đủ trường)
│   ├── css/style.css         # CSS (đã thêm form-row, select, textarea)
│   └── js/main.js            # JavaScript (đã thêm tính phí, validation)
└── booking-details/          # Chi tiết đơn hàng
    ├── index.html
    └── js/
        ├── data.js           # Fetch data from API
        ├── main.js           # Initialize với API
        └── ui.js             # Render UI (đã cập nhật status mapping)
```

---

## 🔧 API Endpoints

### **Tạo đơn hàng**
```
POST /api/v1/orders
Content-Type: multipart/form-data
Authorization: Bearer {token}

Body (Form Data):
- pickup_address, pickup_lat, pickup_lng, pickup_contact_name, pickup_contact_phone, pickup_note
- dropoff_address, dropoff_lat, dropoff_lng, dropoff_contact_name, dropoff_contact_phone, dropoff_note
- product_name, weight, length, width, height, vehicle_type, note, cod_amount
- images (files, max 5)

Response:
{
  "success": true,
  "message": "Đơn hàng đã được tạo thành công",
  "order_id": "65a1b2c3d4e5f6789012345",
  "tracking_code": "SW20240115001",
  "total_amount": 545000,
  "payment_required": false
}
```

### **Xem chi tiết đơn hàng**
```
GET /api/v1/orders/{order_id}
Authorization: Bearer {token}

Response:
{
  "id": "65a1b2c3d4e5f6789012345",
  "tracking_code": "SW20240115001",
  "user_id": "...",
  "pickup_info": {...},
  "dropoff_info": {...},
  "product_name": "...",
  "images": [...],
  "weight": 5.5,
  "vehicle_type": "bike",
  "distance_km": 8.5,
  "shipping_fee": 45000,
  "total_amount": 545000,
  "status": "pending",
  ...
}
```

### **Danh sách đơn hàng**
```
GET /api/v1/orders?page=1&limit=10&status=pending
Authorization: Bearer {token}
```

---

## ✅ Validation Rules

### Frontend Validation:
- ✅ Tất cả trường bắt buộc phải được điền
- ✅ Số điện thoại: format 0912345678 hoặc +84912345678
- ✅ Vĩ độ: -90 đến 90
- ✅ Kinh độ: -180 đến 180
- ✅ Trọng lượng: số dương
- ✅ Loại xe phải được chọn

### Backend Validation:
- ✅ Kiểm tra khối lượng tối đa theo loại xe
- ✅ Validate format hình ảnh (.jpg, .jpeg, .png, .gif, .webp)
- ✅ Kiểm tra kích thước file (max 5MB/ảnh)
- ✅ Tối đa 5 ảnh/đơn hàng
- ✅ Kiểm tra số dư ví

---

## 🐛 Xử Lý Lỗi

### Lỗi phổ biến:

1. **"Không đủ tiền trong ví"**
   - Giải pháp: Nạp thêm tiền vào ví trước khi tạo đơn

2. **"Khối lượng vượt quá giới hạn"**
   - Giải pháp: Chọn loại xe phù hợp với khối lượng

3. **"File quá lớn"**
   - Giải pháp: Giảm kích thước ảnh xuống dưới 5MB

4. **"Không tìm thấy thông tin đơn hàng"**
   - Giải pháp: Kiểm tra lại order_id hoặc quay lại dashboard

---

## 🔐 Bảo Mật

- ✅ JWT Authentication cho tất cả API
- ✅ Kiểm tra quyền truy cập đơn hàng (chỉ owner/driver/admin)
- ✅ Validation đầy đủ ở cả frontend và backend
- ✅ File upload được validate định dạng và kích thước
- ✅ Không lưu thông tin nhạy cảm trong localStorage

---

## 📝 Ghi Chú Quan Trọng

1. **Tọa độ (Latitude/Longitude):**
   - Hiện tại cần nhập thủ công
   - Trong tương lai có thể tích hợp Google Maps API để tự động lấy tọa độ

2. **Ảnh hàng hóa:**
   - Không bắt buộc nhưng nên upload để tài xế dễ nhận diện
   - Ảnh được lưu tại server trong thư mục `uploads/orders/`

3. **Thanh toán tự động:**
   - Nếu có đủ tiền trong ví, đơn sẽ tự động được thanh toán và chuyển sang "confirmed"
   - Nếu không đủ, đơn giữ ở trạng thái "pending"

4. **Hủy đơn:**
   - Chỉ có thể hủy đơn ở trạng thái "pending" hoặc "confirmed"
   - Nếu đã thanh toán, tiền sẽ tự động hoàn lại ví

---

## 🎯 Tính Năng Đã Hoàn Thành

- [x] Form tạo đơn hàng với đầy đủ trường thông tin
- [x] Tính khoảng cách tự động (Haversine formula)
- [x] Tính phí vận chuyển tự động theo loại xe và khoảng cách
- [x] Upload và preview hình ảnh (tối đa 5 ảnh)
- [x] Validation đầy đủ ở frontend và backend
- [x] API tạo đơn hàng với multipart/form-data
- [x] Lưu trữ đơn hàng vào MongoDB
- [x] Tích hợp ví điện tử (tự động thanh toán)
- [x] Trang chi tiết đơn hàng kết nối với API
- [x] Hiển thị trạng thái đơn hàng real-time
- [x] Upload và hiển thị ảnh hàng hóa

---

## 🚀 Bước Tiếp Theo (Tùy Chọn)

### Cải tiến Frontend:
1. Tích hợp Google Maps API
   - Tự động lấy tọa độ khi nhập địa chỉ
   - Hiển thị bản đồ và route giữa 2 điểm
   - Autocomplete địa chỉ

2. Real-time tracking
   - WebSocket để cập nhật trạng thái real-time
   - Hiển thị vị trí tài xế trên bản đồ

3. Push notifications
   - Thông báo khi có tài xế nhận đơn
   - Thông báo khi trạng thái đơn thay đổi

### Cải tiến Backend:
1. Rate limiting
2. Caching với Redis
3. CDN cho ảnh
4. Email notifications
5. SMS notifications

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra console browser (F12) để xem lỗi
2. Kiểm tra log server
3. Đảm bảo backend đang chạy
4. Đảm bảo đã đăng nhập và có token hợp lệ

---

**Phiên bản:** 1.0.0  
**Ngày cập nhật:** 15/01/2026  
**Tác giả:** Shipway Development Team
