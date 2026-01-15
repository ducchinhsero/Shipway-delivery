"""
Order/Booking API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from typing import List, Optional
from bson import ObjectId

from app.api.deps import get_current_user
from app.db.session import get_database
from app.db import models as db_models
from app.schemas.order import (
    CreateOrderRequest, CreateOrderResponse, OrderResponse, OrderListResponse,
    UpdateOrderStatusRequest, VehicleType, OrderStatus, PaymentMethod, LocationInfo
)
from app.services.upload_service import save_order_images, delete_order_images
from app.services.pricing_service import calculate_distance, calculate_shipping_fee, validate_vehicle_for_weight
from app.core.exceptions import AppException
from motor.motor_asyncio import AsyncIOMotorDatabase


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    # Order data as JSON
    pickup_address: str = Form(...),
    pickup_lat: float = Form(...),
    pickup_lng: float = Form(...),
    pickup_contact_name: str = Form(...),
    pickup_contact_phone: str = Form(...),
    pickup_note: Optional[str] = Form(None),
    
    dropoff_address: str = Form(...),
    dropoff_lat: float = Form(...),
    dropoff_lng: float = Form(...),
    dropoff_contact_name: str = Form(...),
    dropoff_contact_phone: str = Form(...),
    dropoff_note: Optional[str] = Form(None),
    
    product_name: str = Form(...),
    weight: float = Form(...),
    length: Optional[float] = Form(None),
    width: Optional[float] = Form(None),
    height: Optional[float] = Form(None),
    vehicle_type: str = Form(...),
    note: Optional[str] = Form(None),
    cod_amount: float = Form(0),
    
    # Images as files
    images: List[UploadFile] = File(None),
    
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new delivery order/booking
    
    **Multipart Form Data Required:**
    - pickup_* fields: Pickup location information
    - dropoff_* fields: Dropoff location information  
    - product_name: Name of the product/package
    - weight: Weight in kilograms
    - length: Length in centimeters (optional)
    - width: Width in centimeters (optional)
    - height: Height in centimeters (optional)
    - vehicle_type: Type of vehicle (bike, car, van, truck_500kg, truck_1000kg)
    - cod_amount: Cash on delivery amount (optional, default 0)
    - images: Product images (optional, max 5 files)
    """
    try:
        # Validate vehicle type enum
        try:
            vehicle_enum = VehicleType(vehicle_type)
        except ValueError:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Loại xe không hợp lệ. Chỉ chấp nhận: {', '.join([v.value for v in VehicleType])}"
            )
        
        # Validate weight for vehicle type
        if not validate_vehicle_for_weight(weight, vehicle_enum):
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Khối lượng {weight}kg vượt quá giới hạn cho loại xe {vehicle_type}"
            )
        
        # Build location info
        pickup_info = {
            "address": pickup_address,
            "lat": pickup_lat,
            "lng": pickup_lng,
            "contact_name": pickup_contact_name,
            "contact_phone": pickup_contact_phone,
            "note": pickup_note
        }
        
        dropoff_info = {
            "address": dropoff_address,
            "lat": dropoff_lat,
            "lng": dropoff_lng,
            "contact_name": dropoff_contact_name,
            "contact_phone": dropoff_contact_phone,
            "note": dropoff_note
        }
        
        # Calculate distance
        distance_km = calculate_distance(
            pickup_lat, pickup_lng,
            dropoff_lat, dropoff_lng
        )
        
        # Calculate pricing
        pricing = calculate_shipping_fee(
            distance_km=distance_km,
            weight=weight,
            vehicle_type=vehicle_enum,
            cod_amount=cod_amount
        )
        
        # Check if user has sufficient balance
        user = await db_models.find_user_by_id(db, str(current_user["_id"]))
        if not user:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Người dùng không tồn tại"
            )
        
        user_balance = user.get('wallet_info', {}).get('balance', 0)
        total_amount = pricing['total_amount']
        
        # Create order data
        order_data = {
            "user_id": str(current_user["_id"]),
            "driver_id": None,
            "pickup_info": pickup_info,
            "dropoff_info": dropoff_info,
            "product_name": product_name,
            "images": [],  # Will be added after order creation
            "weight": weight,
            "length": length,
            "width": width,
            "height": height,
            "vehicle_type": vehicle_type,
            "note": note,
            "distance_km": distance_km,
            "shipping_fee": pricing['shipping_fee'],
            "cod_amount": cod_amount,
            "total_amount": total_amount,
            "payment_method": PaymentMethod.WALLET.value,  # Default to wallet
            "is_paid": False,
            "status": OrderStatus.PENDING.value
        }
        
        # Create order
        order = await db_models.create_order(db, order_data)
        order_id = str(order["_id"])
        
        # Upload images if provided
        if images and len(images) > 0:
            # Filter out empty files
            valid_images = [img for img in images if img.filename]
            if valid_images:
                try:
                    image_paths = await save_order_images(valid_images, order_id)
                    await db_models.add_images_to_order(db, order_id, image_paths)
                except Exception as e:
                    # Order created but image upload failed
                    # Don't fail the entire request
                    print(f"Image upload failed: {e}")
        
        # Check if payment is required
        payment_required = True
        if user_balance >= total_amount:
            # Sufficient balance - auto-pay and confirm order
            await db_models.use_credit_from_user(db, str(current_user["_id"]), total_amount)
            await db_models.update_order_payment(db, order_id, True, PaymentMethod.WALLET.value)
            await db_models.update_order_status(
                db, order_id, OrderStatus.CONFIRMED.value,
                f"Đã thanh toán {total_amount:,.0f} VNĐ từ ví",
                str(current_user["_id"])
            )
            payment_required = False
        
        return CreateOrderResponse(
            success=True,
            message="Đơn hàng đã được tạo thành công" if not payment_required else "Đơn hàng đã được tạo. Vui lòng nạp thêm tiền để xác nhận.",
            order_id=order_id,
            tracking_code=order["tracking_code"],
            total_amount=total_amount,
            payment_required=payment_required
        )
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.get("", response_model=OrderListResponse)
async def get_my_orders(
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get current user's orders with pagination
    
    **Query Parameters:**
    - status: Filter by order status (optional)
    - page: Page number (default: 1)
    - limit: Items per page (default: 10, max: 50)
    """
    try:
        skip = (page - 1) * limit
        orders, total = await db_models.get_user_orders(
            db,
            str(current_user["_id"]),
            status_filter,
            limit,
            skip
        )
        
        # Convert ObjectId to string for response
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return OrderListResponse(
            total=total,
            page=page,
            limit=limit,
            orders=[OrderResponse(**order) for order in orders]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get detailed information of a specific order
    
    **Path Parameters:**
    - order_id: Order ID
    """
    try:
        order = await db_models.get_order_by_id(db, order_id)
        
        if not order:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Đơn hàng không tồn tại"
            )
        
        # Check if user owns this order or is the assigned driver
        user_id = str(current_user["_id"])
        is_owner = order["user_id"] == user_id
        is_driver = order.get("driver_id") == user_id
        is_admin = current_user.get("role") == "admin"
        
        if not (is_owner or is_driver or is_admin):
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Bạn không có quyền xem đơn hàng này"
            )
        
        order["_id"] = str(order["_id"])
        return OrderResponse(**order)
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.get("/tracking/{tracking_code}", response_model=OrderResponse)
async def track_order(
    tracking_code: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Track order by tracking code (public endpoint - no auth required)
    
    **Path Parameters:**
    - tracking_code: Order tracking code (e.g., SW20240115001)
    """
    try:
        order = await db_models.get_order_by_tracking_code(db, tracking_code)
        
        if not order:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Không tìm thấy đơn hàng với mã vận đơn này"
            )
        
        order["_id"] = str(order["_id"])
        return OrderResponse(**order)
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.patch("/{order_id}/status", response_model=dict)
async def update_order_status_endpoint(
    order_id: str,
    request: UpdateOrderStatusRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update order status
    
    **Path Parameters:**
    - order_id: Order ID
    
    **Permissions:**
    - Owner can cancel pending/confirmed orders
    - Driver can update assigned order status
    - Admin can update any order
    """
    try:
        order = await db_models.get_order_by_id(db, order_id)
        
        if not order:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Đơn hàng không tồn tại"
            )
        
        user_id = str(current_user["_id"])
        user_role = current_user.get("role", "user")
        is_owner = order["user_id"] == user_id
        is_driver = order.get("driver_id") == user_id
        is_admin = user_role == "admin"
        
        # Authorization checks
        if request.status == OrderStatus.CANCELLED:
            # Only owner can cancel their own orders (if not yet picked up)
            if not is_owner and not is_admin:
                raise AppException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    message="Chỉ chủ đơn hàng mới có thể hủy"
                )
            if order["status"] not in ["pending", "confirmed"]:
                raise AppException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Không thể hủy đơn hàng đã được lấy"
                )
        elif is_driver:
            # Driver can only update their assigned orders
            pass
        elif not is_admin:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Bạn không có quyền cập nhật trạng thái đơn hàng này"
            )
        
        # Update status
        success = await db_models.update_order_status(
            db, order_id, request.status.value,
            request.note, user_id
        )
        
        if not success:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Không thể cập nhật trạng thái đơn hàng"
            )
        
        return {
            "success": True,
            "message": "Cập nhật trạng thái thành công",
            "new_status": request.status.value
        }
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.delete("/{order_id}", response_model=dict)
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Cancel an order (only owner can cancel pending/confirmed orders)
    
    **Path Parameters:**
    - order_id: Order ID
    """
    try:
        order = await db_models.get_order_by_id(db, order_id)
        
        if not order:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Đơn hàng không tồn tại"
            )
        
        user_id = str(current_user["_id"])
        is_owner = order["user_id"] == user_id
        is_admin = current_user.get("role") == "admin"
        
        if not is_owner and not is_admin:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Bạn không có quyền hủy đơn hàng này"
            )
        
        if order["status"] not in ["pending", "confirmed"]:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Không thể hủy đơn hàng đã được lấy"
            )
        
        # Refund if already paid
        if order.get("is_paid"):
            await db_models.add_credit_to_user(db, order["user_id"], order["total_amount"])
        
        # Cancel order
        success = await db_models.delete_order(db, order_id)
        
        if not success:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Không thể hủy đơn hàng"
            )
        
        return {
            "success": True,
            "message": "Đã hủy đơn hàng thành công",
            "refunded": order.get("is_paid", False)
        }
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


# ==================== DRIVER ENDPOINTS ====================

@router.get("/available/list", response_model=List[OrderResponse])
async def get_available_orders(
    vehicle_type: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get available orders for drivers (orders without assigned driver)
    
    **Query Parameters:**
    - vehicle_type: Filter by vehicle type (optional)
    - limit: Maximum number of orders (default: 20, max: 50)
    
    **Permissions:** Only drivers can access this endpoint
    """
    try:
        # Check if user is a driver
        if current_user.get("role") != "driver":
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Chỉ tài xế mới có thể xem đơn hàng khả dụng"
            )
        
        orders = await db_models.get_available_orders(db, vehicle_type, limit)
        
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return [OrderResponse(**order) for order in orders]
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )


@router.post("/{order_id}/accept", response_model=dict)
async def accept_order(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Accept an order (driver only)
    
    **Path Parameters:**
    - order_id: Order ID
    
    **Permissions:** Only drivers can accept orders
    """
    try:
        # Check if user is a driver
        if current_user.get("role") != "driver":
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Chỉ tài xế mới có thể nhận đơn hàng"
            )
        
        order = await db_models.get_order_by_id(db, order_id)
        
        if not order:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Đơn hàng không tồn tại"
            )
        
        if order.get("driver_id"):
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Đơn hàng đã được tài xế khác nhận"
            )
        
        if order["status"] not in ["pending", "confirmed"]:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Đơn hàng không ở trạng thái có thể nhận"
            )
        
        # Assign driver
        driver_id = str(current_user["_id"])
        success = await db_models.assign_driver_to_order(db, order_id, driver_id)
        
        if not success:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Không thể nhận đơn hàng"
            )
        
        # Update status to picking_up
        await db_models.update_order_status(
            db, order_id, OrderStatus.PICKING_UP.value,
            "Tài xế đang đến lấy hàng", driver_id
        )
        
        return {
            "success": True,
            "message": "Đã nhận đơn hàng thành công",
            "order_id": order_id,
            "tracking_code": order["tracking_code"]
        }
        
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )
