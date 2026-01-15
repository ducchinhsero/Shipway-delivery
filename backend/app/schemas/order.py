"""
Order schemas for booking/shipment management
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


# ==================== ENUMS ====================

class VehicleType(str, Enum):
    """Vehicle types for delivery"""
    BIKE = "bike"           # Xe máy
    CAR = "car"             # Xe ô tô 4 chỗ
    VAN = "van"             # Xe van 7 chỗ
    TRUCK_500KG = "truck_500kg"   # Xe tải 500kg
    TRUCK_1000KG = "truck_1000kg" # Xe tải 1 tấn


class OrderStatus(str, Enum):
    """Order status stages"""
    PENDING = "pending"           # Chờ xác nhận
    CONFIRMED = "confirmed"       # Đã xác nhận
    PICKING_UP = "picking_up"     # Đang đến lấy hàng
    PICKED_UP = "picked_up"       # Đã lấy hàng
    IN_TRANSIT = "in_transit"     # Đang vận chuyển
    DELIVERING = "delivering"     # Đang giao hàng
    DELIVERED = "delivered"       # Đã giao hàng
    CANCELLED = "cancelled"       # Đã hủy
    FAILED = "failed"             # Giao hàng thất bại


class PaymentMethod(str, Enum):
    """Payment methods"""
    WALLET = "wallet"       # Ví điện tử
    COD = "cod"             # Tiền mặt
    CARD = "card"           # Thẻ ngân hàng


# ==================== LOCATION SCHEMAS ====================

class LocationInfo(BaseModel):
    """Location information for pickup/dropoff"""
    address: str = Field(..., min_length=5, max_length=500, description="Địa chỉ đầy đủ")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    contact_name: str = Field(..., min_length=2, max_length=100, description="Tên người liên hệ")
    contact_phone: str = Field(..., pattern=r"^(0|\+84)[0-9]{9,10}$", description="SĐT liên hệ")
    note: Optional[str] = Field(None, max_length=500, description="Ghi chú địa điểm")

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Nguyễn Văn Linh, Phường Tân Phú, Quận 7, TP.HCM",
                "lat": 10.7329269,
                "lng": 106.7172715,
                "contact_name": "Nguyễn Văn A",
                "contact_phone": "0912345678",
                "note": "Gọi trước khi đến 15 phút"
            }
        }


# ==================== ORDER REQUEST SCHEMAS ====================

class CreateOrderRequest(BaseModel):
    """Request schema for creating a new order"""
    # Pickup & Dropoff locations
    pickup_info: LocationInfo = Field(..., description="Thông tin điểm lấy hàng")
    dropoff_info: LocationInfo = Field(..., description="Thông tin điểm giao hàng")
    
    # Product information
    product_name: str = Field(..., min_length=2, max_length=200, description="Tên hàng hóa")
    weight: float = Field(..., gt=0, le=10000, description="Khối lượng (kg)")
    
    # Dimensions (kích thước)
    length: Optional[float] = Field(None, gt=0, le=1000, description="Chiều dài (cm)")
    width: Optional[float] = Field(None, gt=0, le=1000, description="Chiều rộng (cm)")
    height: Optional[float] = Field(None, gt=0, le=1000, description="Chiều cao (cm)")
    
    vehicle_type: VehicleType = Field(..., description="Loại xe vận chuyển")
    
    # Optional fields
    note: Optional[str] = Field(None, max_length=1000, description="Ghi chú đơn hàng")
    cod_amount: float = Field(0, ge=0, description="Tiền thu hộ (COD)")
    
    # Images will be uploaded separately via multipart/form-data
    
    class Config:
        json_schema_extra = {
            "example": {
                "pickup_info": {
                    "address": "123 Nguyễn Văn Linh, Q.7, TP.HCM",
                    "lat": 10.7329269,
                    "lng": 106.7172715,
                    "contact_name": "Nguyễn Văn A",
                    "contact_phone": "0912345678",
                    "note": "Gọi trước 15 phút"
                },
                "dropoff_info": {
                    "address": "456 Lê Văn Việt, Q.9, TP.HCM",
                    "lat": 10.8231271,
                    "lng": 106.7574535,
                    "contact_name": "Trần Thị B",
                    "contact_phone": "0987654321",
                    "note": "Giao tận tay"
                },
                "product_name": "Quần áo thời trang",
                "weight": 5.5,
                "length": 50,
                "width": 30,
                "height": 20,
                "vehicle_type": "bike",
                "note": "Hàng dễ vỡ, cẩn thận",
                "cod_amount": 500000
            }
        }


class UpdateOrderStatusRequest(BaseModel):
    """Request to update order status"""
    status: OrderStatus = Field(..., description="Trạng thái mới")
    note: Optional[str] = Field(None, max_length=500, description="Ghi chú cập nhật")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "picked_up",
                "note": "Đã lấy hàng thành công"
            }
        }


# ==================== ORDER RESPONSE SCHEMAS ====================

class OrderHistoryItem(BaseModel):
    """Single history entry"""
    status: OrderStatus
    timestamp: datetime
    note: Optional[str] = None
    updated_by: Optional[str] = None  # user_id or driver_id

    class Config:
        json_schema_extra = {
            "example": {
                "status": "picked_up",
                "timestamp": "2024-01-15T10:30:00Z",
                "note": "Đã lấy hàng",
                "updated_by": "driver_123"
            }
        }


class OrderResponse(BaseModel):
    """Complete order information"""
    id: str = Field(alias="_id")
    tracking_code: str
    user_id: str
    driver_id: Optional[str] = None
    
    # Location info
    pickup_info: Dict[str, Any]
    dropoff_info: Dict[str, Any]
    
    # Product info
    product_name: str
    images: List[str] = []
    weight: float
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    vehicle_type: VehicleType
    note: Optional[str] = None
    
    # Pricing
    distance_km: float
    shipping_fee: float
    cod_amount: float
    total_amount: float
    
    # Payment
    payment_method: PaymentMethod
    is_paid: bool
    
    # Status
    status: OrderStatus
    history: List[Dict[str, Any]] = []
    is_reviewed: bool = False
    
    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "65a1b2c3d4e5f6789012345",
                "tracking_code": "SW20240115001",
                "user_id": "65a1b2c3d4e5f678901234",
                "driver_id": None,
                "pickup_info": {
                    "address": "123 Nguyễn Văn Linh, Q.7",
                    "lat": 10.7329269,
                    "lng": 106.7172715,
                    "contact_name": "Nguyễn Văn A",
                    "contact_phone": "0912345678"
                },
                "dropoff_info": {
                    "address": "456 Lê Văn Việt, Q.9",
                    "lat": 10.8231271,
                    "lng": 106.7574535,
                    "contact_name": "Trần Thị B",
                    "contact_phone": "0987654321"
                },
                "product_name": "Quần áo thời trang",
                "images": [
                    "https://storage.shipway.com/orders/img1.jpg",
                    "https://storage.shipway.com/orders/img2.jpg"
                ],
                "weight": 5.5,
                "vehicle_type": "bike",
                "note": "Hàng dễ vỡ",
                "distance_km": 8.5,
                "shipping_fee": 45000,
                "cod_amount": 500000,
                "total_amount": 545000,
                "payment_method": "wallet",
                "is_paid": True,
                "status": "pending",
                "history": [],
                "is_reviewed": False,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        }


class OrderListResponse(BaseModel):
    """Paginated list of orders"""
    total: int
    page: int
    limit: int
    orders: List[OrderResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 50,
                "page": 1,
                "limit": 10,
                "orders": []
            }
        }


class CreateOrderResponse(BaseModel):
    """Response after creating an order"""
    success: bool
    message: str
    order_id: str
    tracking_code: str
    total_amount: float
    payment_required: bool

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Đơn hàng đã được tạo thành công",
                "order_id": "65a1b2c3d4e5f6789012345",
                "tracking_code": "SW20240115001",
                "total_amount": 545000,
                "payment_required": True
            }
        }
