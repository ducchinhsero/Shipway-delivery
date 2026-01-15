"""
User Management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserUpdateRequest, UpdateProfileResponse
from app.db import models
from typing import Dict, Any


router = APIRouter(
    prefix="/user",
    tags=["User Management"]
)


def convert_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chuyển đổi user document từ MongoDB sang format API response.
    
    Args:
        user: User document từ MongoDB (bao gồm ObjectId)
        
    Returns:
        Dict với _id đã được convert sang string và các field chuẩn hóa
        
    Note:
        - Helper function dùng chung cho tất cả user-related endpoints
        - Loại bỏ sensitive data như password, refresh_token
        - Chuẩn hóa format để consistent với API schema
    """
    user_dict = {
        "_id": str(user["_id"]),
        "phone": user["phone"],
        "name": user["name"],
        "role": user["role"],
        "email": user.get("email"),
        "is_active": user.get("is_active", True),
        "is_phone_verified": user.get("is_phone_verified", False),
        "avatar": user.get("avatar"),
        "driver_info": user.get("driver_info"),
        "company_info": user.get("company_info"),
        "last_login": user.get("last_login"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }
    return user_dict


@router.put(
    "/profile",
    response_model=UpdateProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật thông tin profile",
    description="""
    Cập nhật thông tin cá nhân của user đang đăng nhập.
    
    **Các field có thể cập nhật:**
    - `name`: Tên
    - `email`: Email
    - `avatar`: URL avatar
    
    **Các field KHÔNG thể cập nhật:**
    - `phone`: Số điện thoại (unique identifier)
    - `password`: Mật khẩu (dùng reset-password)
    - `role`: Vai trò (chỉ admin mới được đổi)
    
    **Yêu cầu:**
    - Header: `Authorization: Bearer <token>`
    """,
    responses={
        200: {"description": "Cập nhật thành công"},
        401: {"description": "Token không hợp lệ"},
        404: {"description": "User không tồn tại"}
    }
)
async def update_profile(
    payload: UserUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Cập nhật thông tin profile của user đang đăng nhập.
    
    Business Logic:
        1. Authenticate user qua JWT token
        2. Validate các field được gửi lên (Pydantic)
        3. Chỉ update các field được cung cấp (partial update)
        4. Cập nhật updated_at timestamp
        5. Trả về user info đã được cập nhật
        
    Args:
        payload: Request body chứa các field cần update (optional)
        current_user: User hiện tại từ JWT token (dependency)
        db: MongoDB database instance
        
    Returns:
        UpdateProfileResponse chứa user info đã cập nhật
        
    Raises:
        HTTPException 401: Token không hợp lệ
        HTTPException 404: User không tồn tại
        
    Updatable Fields:
        - name: Tên đầy đủ
        - email: Email (optional)
        - avatar: URL ảnh đại diện
        
    Non-updatable Fields:
        - phone: Unique identifier (không thể đổi)
        - password: Dùng /auth/reset-password
        - role: Chỉ admin mới có quyền đổi
        - wallet_info: Dùng /wallet endpoints
        
    Security:
        - User chỉ có thể update profile của chính mình
        - Sensitive fields được protect
        
    Example:
        Request Headers:
        ```
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
        
        Request Body:
        ```json
        {
            "name": "Nguyễn Văn B",
            "email": "newmail@example.com",
            "avatar": "https://example.com/avatar.jpg"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "Cập nhật thông tin thành công",
            "user": {
                "_id": "507f1f77bcf86cd799439011",
                "phone": "+84987654321",
                "name": "Nguyễn Văn B",
                "email": "newmail@example.com",
                "avatar": "https://example.com/avatar.jpg",
                "updated_at": "2025-01-08T10:35:00Z"
            }
        }
        ```
    """
    # Prepare update data (only include provided fields)
    update_data = {}
    
    if payload.name is not None:
        update_data["name"] = payload.name
    
    if payload.email is not None:
        update_data["email"] = payload.email
    
    if payload.avatar is not None:
        update_data["avatar"] = payload.avatar
    
    # If no fields to update
    if not update_data:
        return {
            "success": True,
            "message": "Không có thay đổi nào",
            "user": convert_user_response(current_user)
        }
    
    # Update user
    updated_user = await models.update_user(
        db,
        str(current_user["_id"]),
        update_data
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không thể cập nhật thông tin"
        )
    
    return {
        "success": True,
        "message": "Cập nhật thông tin thành công",
        "user": convert_user_response(updated_user)
    }


@router.get(
    "/profile/{user_id}",
    response_model=UpdateProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Xem profile user khác (Admin)",
    description="""
    Xem thông tin profile của user khác.
    
    **Yêu cầu:**
    - Đang đăng nhập
    - Header: `Authorization: Bearer <token>`
    
    **Lưu ý:**
    - User thường chỉ xem được profile của chính mình
    - Admin có thể xem profile của bất kỳ ai
    """,
    responses={
        200: {"description": "Thành công"},
        401: {"description": "Chưa đăng nhập"},
        403: {"description": "Không có quyền truy cập"},
        404: {"description": "User không tồn tại"}
    }
)
async def get_user_profile(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Xem thông tin profile của user khác (với kiểm tra quyền).
    
    Business Logic:
        1. Authenticate user qua JWT token
        2. Kiểm tra quyền truy cập:
           - User thường: Chỉ xem được profile của chính mình
           - Admin: Có thể xem profile của bất kỳ ai
        3. Tìm user theo user_id
        4. Trả về thông tin user
        
    Args:
        user_id: MongoDB ObjectId của user cần xem (path parameter)
        current_user: User hiện tại từ JWT token
        db: MongoDB database instance
        
    Returns:
        UpdateProfileResponse chứa user info
        
    Raises:
        HTTPException 401: Chưa đăng nhập
        HTTPException 403: Không có quyền xem profile này
        HTTPException 404: User không tồn tại
        
    Authorization:
        - Own profile: Allowed for all authenticated users
        - Other profiles: Admin only
        
    Use Cases:
        - User xem profile của chính mình
        - Admin xem profile của bất kỳ user nào (quản lý)
        - Driver xem profile của partner (nếu có permission)
        
    Example:
        Request:
        ```
        GET /api/v1/user/profile/507f1f77bcf86cd799439011
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
        
        Response (Success):
        ```json
        {
            "success": true,
            "user": {
                "_id": "507f1f77bcf86cd799439011",
                "phone": "+84987654321",
                "name": "Nguyễn Văn A",
                "role": "user",
                "email": "user@example.com"
            }
        }
        ```
        
        Response (Forbidden):
        ```json
        {
            "detail": "Bạn không có quyền xem thông tin này"
        }
        ```
    """
    # Check permission: only allow viewing own profile or admin can view all
    if str(current_user["_id"]) != user_id and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem thông tin này"
        )
    
    # Find user
    user = await models.find_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại"
        )
    
    return {
        "success": True,
        "user": convert_user_response(user)
    }
