"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.api.deps import get_db, get_current_user
from app.schemas.user import (
    UserRegisterRequest, UserLoginRequest, TokenResponse,
    UserResponse, UserProfileResponse
)
from app.schemas.otp import (
    SendOTPRequest, SendOTPResponse,
    VerifyOTPRequest, VerifyOTPResponse,
    ResetPasswordRequest, ResetPasswordResponse
)
from app.db import models
from app.services import otp_service
from app.core.security import create_access_token
from datetime import datetime
from typing import Dict, Any


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def convert_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chuyển đổi user document từ MongoDB sang format API response.
    
    Args:
        user: User document từ MongoDB (bao gồm ObjectId)
        
    Returns:
        Dict với _id đã được convert sang string và các field chuẩn hóa
        
    Note:
        - Chuyển ObjectId thành string để serialize JSON
        - Thêm default values cho các optional fields
        - Loại bỏ sensitive data (password, refresh_token)
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
        "wallet_info": user.get("wallet_info"),
        "last_login": user.get("last_login"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }
    return user_dict


@router.post(
    "/send-otp",
    response_model=SendOTPResponse,
    status_code=status.HTTP_200_OK,
    summary="Gửi mã OTP",
    description="""
    Gửi mã OTP 6 chữ số đến số điện thoại.
    
    **Mục đích sử dụng:**
    - `register`: Đăng ký tài khoản mới
    - `reset-password`: Đặt lại mật khẩu
    - `verify-phone`: Xác thực số điện thoại
    
    **Lưu ý:**
    - OTP có hiệu lực 5 phút
    - Mỗi số điện thoại chỉ có 1 OTP active cho mỗi mục đích
    - Trong development mode, OTP sẽ được trả về trong response để test
    """,
    responses={
        200: {"description": "OTP đã được gửi thành công"},
        400: {"description": "Số điện thoại không hợp lệ hoặc đã tồn tại"},
        404: {"description": "Tài khoản không tồn tại (khi reset password)"}
    }
)
async def send_otp(
    payload: SendOTPRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Gửi mã OTP 6 chữ số đến số điện thoại qua SMS (Twilio).
    
    Business Logic:
        1. Kiểm tra xem số điện thoại đã tồn tại chưa (nếu purpose=register)
        2. Kiểm tra tài khoản có tồn tại không (nếu purpose=reset-password)
        3. Tạo OTP 6 chữ số random
        4. Lưu OTP vào database với TTL 5 phút
        5. Gửi OTP qua SMS (hoặc trả về trong response nếu development mode)
    
    Args:
        payload: Request body chứa phone và purpose
        db: MongoDB database instance (dependency injection)
        
    Returns:
        SendOTPResponse với success status và message
        
    Raises:
        HTTPException 400: Số điện thoại đã tồn tại (register)
        HTTPException 404: Tài khoản không tồn tại (reset-password)
        
    Example:
        Request:
        ```json
        {
            "phone": "+84987654321",
            "purpose": "register"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "OTP đã được gửi đến +84987654321",
            "otp": "123456"  // Chỉ có trong development mode
        }
        ```
    """
    # Check user existence based on purpose
    user = await models.find_user_by_phone(db, payload.phone)
    
    if payload.purpose == "register" and user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số điện thoại đã được đăng ký"
        )
    
    if payload.purpose == "reset-password" and not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tài khoản không tồn tại"
        )
    
    # Create and send OTP
    result = await otp_service.create_and_send_otp(
        db,
        payload.phone,
        payload.purpose
    )
    
    return result


@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse,
    status_code=status.HTTP_200_OK,
    summary="Xác thực mã OTP",
    description="""
    Xác thực mã OTP đã được gửi đến số điện thoại.
    
    **Quy tắc:**
    - Mỗi OTP chỉ được sử dụng 1 lần
    - Tối đa 5 lần thử sai
    - OTP hết hạn sau 5 phút
    - Sau khi hết hạn hoặc vượt quá số lần thử, OTP sẽ bị xóa
    """,
    responses={
        200: {"description": "OTP xác thực thành công"},
        400: {"description": "OTP không đúng, hết hạn hoặc đã được sử dụng"}
    }
)
async def verify_otp(
    payload: VerifyOTPRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Xác thực mã OTP đã được gửi đến số điện thoại.
    
    Business Logic:
        1. Tìm OTP trong database theo phone và purpose
        2. Kiểm tra OTP có hết hạn không (5 phút)
        3. Kiểm tra số lần thử (max 5 lần)
        4. So sánh OTP nhập vào với OTP trong database
        5. Đánh dấu OTP đã sử dụng hoặc tăng số lần thử sai
        
    Args:
        payload: Request body chứa phone, otp, purpose
        db: MongoDB database instance
        
    Returns:
        VerifyOTPResponse với success status
        
    Raises:
        HTTPException 400: OTP không đúng, hết hạn, hoặc vượt quá số lần thử
        
    Example:
        Request:
        ```json
        {
            "phone": "+84987654321",
            "otp": "123456",
            "purpose": "register"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "OTP xác thực thành công"
        }
        ```
    """
    result = await otp_service.verify_otp_code(
        db,
        payload.phone,
        payload.otp,
        payload.purpose
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản",
    description="""
    Tạo tài khoản mới với số điện thoại và mật khẩu.
    
    **Quy trình:**
    1. Gọi `/send-otp` với purpose=`register` để nhận OTP
    2. Người dùng nhập OTP
    3. Gọi endpoint này với đầy đủ thông tin + OTP
    
    **Trả về:**
    - JWT token để xác thực các request sau
    - Thông tin user vừa tạo
    
    **Lưu ý:**
    - OTP phải được xác thực trước khi đăng ký
    - Số điện thoại phải unique
    - Mật khẩu tối thiểu 6 ký tự
    """,
    responses={
        201: {"description": "Đăng ký thành công"},
        400: {"description": "Thông tin không hợp lệ hoặc số điện thoại đã tồn tại"}
    }
)
async def register(
    payload: UserRegisterRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Đăng ký tài khoản mới sau khi xác thực OTP.
    
    Business Logic:
        1. Xác thực OTP (purpose=register)
        2. Kiểm tra số điện thoại chưa tồn tại
        3. Hash password bằng bcrypt
        4. Tạo user mới với role mặc định là 'user'
        5. Set is_phone_verified=True (vì đã verify OTP)
        6. Khởi tạo plan='free', max_trips=10, credit_balance=0
        7. Generate JWT token
        8. Trả về token và thông tin user
        
    Args:
        payload: Request body chứa phone, name, password, otp, role (optional)
        db: MongoDB database instance
        
    Returns:
        TokenResponse chứa JWT token và user info
        
    Raises:
        HTTPException 400: OTP không hợp lệ hoặc số điện thoại đã tồn tại
        
    Security:
        - Password được hash bằng bcrypt (không lưu plaintext)
        - JWT token chứa user_id và role
        - Token expire sau 7 ngày (configurable)
        
    Example:
        Request:
        ```json
        {
            "phone": "+84987654321",
            "name": "Nguyễn Văn A",
            "password": "matkhau123",
            "otp": "123456",
            "role": "user"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "Đăng ký thành công",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "_id": "507f1f77bcf86cd799439011",
                "phone": "+84987654321",
                "name": "Nguyễn Văn A",
                "role": "user",
                "plan": "free",
                "max_trips": 10,
                "credit_balance": 0
            }
        }
        ```
    """
    # Verify OTP first
    otp_result = await otp_service.verify_otp_code(
        db,
        payload.phone,
        payload.otp,
        "register"
    )
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=otp_result["message"]
        )
    
    # Check if user already exists
    existing_user = await models.find_user_by_phone(db, payload.phone)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số điện thoại đã được đăng ký"
        )
    
    # Create user
    user_data = {
        "phone": payload.phone,
        "name": payload.name,
        "password": payload.password,
        "role": payload.role or "user",
        "email": payload.email,
        "is_active": True,
        "is_phone_verified": True,  # Since we verified OTP
        "avatar": None,
        "driver_info": None,
        "company_info": None,
        "last_login": datetime.utcnow()
    }
    
    user = await models.create_user(db, user_data)
    
    # Generate JWT token
    token = create_access_token({
        "user_id": str(user["_id"]),
        "role": user["role"]
    })
    
    return {
        "success": True,
        "message": "Đăng ký thành công",
        "token": token,
        "user": convert_user_response(user)
    }


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập",
    description="""
    Đăng nhập bằng số điện thoại và mật khẩu.
    
    **Trả về:**
    - JWT token để xác thực các request sau
    - Thông tin user
    
    **Lưu ý:**
    - Token có hiệu lực 7 ngày
    - Cần gửi token trong header: `Authorization: Bearer <token>`
    """,
    responses={
        200: {"description": "Đăng nhập thành công"},
        401: {"description": "Sai thông tin đăng nhập"},
        403: {"description": "Tài khoản đã bị vô hiệu hóa"}
    }
)
async def login(
    payload: UserLoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Đăng nhập tài khoản bằng số điện thoại và mật khẩu.
    
    Business Logic:
        1. Tìm user theo số điện thoại
        2. Kiểm tra tài khoản có active không
        3. Verify password với bcrypt
        4. Cập nhật last_login timestamp
        5. Generate JWT token mới
        6. Trả về token và thông tin user
        
    Args:
        payload: Request body chứa phone và password
        db: MongoDB database instance
        
    Returns:
        TokenResponse chứa JWT token và user info
        
    Raises:
        HTTPException 401: Sai thông tin đăng nhập
        HTTPException 403: Tài khoản đã bị vô hiệu hóa
        
    Security:
        - Password verification dùng bcrypt
        - Token chứa user_id và role để authorization
        - Token expire sau 7 ngày (default)
        
    Example:
        Request:
        ```json
        {
            "phone": "+84987654321",
            "password": "matkhau123"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "Đăng nhập thành công",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "_id": "507f1f77bcf86cd799439011",
                "phone": "+84987654321",
                "name": "Nguyễn Văn A",
                "role": "user",
                "last_login": "2025-01-08T10:30:00Z"
            }
        }
        ```
    """
    # Find user
    user = await models.find_user_by_phone(db, payload.phone)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản không tồn tại"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    # Verify password
    is_valid = await models.verify_user_password(user, payload.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mật khẩu không chính xác"
        )
    
    # Update last login
    await models.update_user(db, str(user["_id"]), {
        "last_login": datetime.utcnow()
    })
    user["last_login"] = datetime.utcnow()
    
    # Generate JWT token
    token = create_access_token({
        "user_id": str(user["_id"]),
        "role": user["role"]
    })
    
    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "token": token,
        "user": convert_user_response(user)
    }


@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
    status_code=status.HTTP_200_OK,
    summary="Đặt lại mật khẩu",
    description="""
    Đặt lại mật khẩu khi quên mật khẩu.
    
    **Quy trình:**
    1. Gọi `/send-otp` với purpose=`reset-password`
    2. Người dùng nhập OTP
    3. Gọi endpoint này với OTP + mật khẩu mới
    
    **Lưu ý:**
    - OTP phải được xác thực
    - Mật khẩu mới tối thiểu 6 ký tự
    """,
    responses={
        200: {"description": "Đặt lại mật khẩu thành công"},
        400: {"description": "OTP không hợp lệ"},
        404: {"description": "Tài khoản không tồn tại"}
    }
)
async def reset_password(
    payload: ResetPasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Đặt lại mật khẩu khi quên mật khẩu (sau khi xác thực OTP).
    
    Business Logic:
        1. Xác thực OTP (purpose=reset-password)
        2. Tìm user theo số điện thoại
        3. Hash mật khẩu mới bằng bcrypt
        4. Cập nhật mật khẩu trong database
        5. OTP sẽ bị đánh dấu đã sử dụng
        
    Args:
        payload: Request body chứa phone, otp, new_password
        db: MongoDB database instance
        
    Returns:
        ResetPasswordResponse với success status
        
    Raises:
        HTTPException 400: OTP không hợp lệ
        HTTPException 404: Tài khoản không tồn tại
        HTTPException 500: Không thể cập nhật mật khẩu
        
    Security:
        - Yêu cầu OTP verification trước khi reset
        - Password mới được hash bằng bcrypt
        - OTP chỉ dùng được 1 lần
        
    Example:
        Request:
        ```json
        {
            "phone": "+84987654321",
            "otp": "123456",
            "new_password": "matkhaumoi123"
        }
        ```
        
        Response:
        ```json
        {
            "success": true,
            "message": "Đặt lại mật khẩu thành công"
        }
        ```
    """
    # Verify OTP
    otp_result = await otp_service.verify_otp_code(
        db,
        payload.phone,
        payload.otp,
        "reset-password"
    )
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=otp_result["message"]
        )
    
    # Find user
    user = await models.find_user_by_phone(db, payload.phone)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tài khoản không tồn tại"
        )
    
    # Update password
    success = await models.update_user_password(db, payload.phone, payload.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể cập nhật mật khẩu"
        )
    
    return {
        "success": True,
        "message": "Đặt lại mật khẩu thành công"
    }


@router.get(
    "/me",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin user hiện tại",
    description="""
    Lấy thông tin profile của user đang đăng nhập.
    
    **Yêu cầu:**
    - Header: `Authorization: Bearer <token>`
    
    **Trả về:**
    - Thông tin đầy đủ của user
    """,
    responses={
        200: {"description": "Thành công"},
        401: {"description": "Token không hợp lệ hoặc hết hạn"},
        404: {"description": "User không tồn tại"}
    }
)
async def get_me(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Lấy thông tin profile của user đang đăng nhập (Protected endpoint).
    
    Business Logic:
        1. Parse JWT token từ Authorization header
        2. Validate token và lấy user_id
        3. Tìm user trong database
        4. Trả về thông tin đầy đủ của user
        
    Args:
        current_user: User object từ JWT token (dependency injection)
        
    Returns:
        UserProfileResponse chứa thông tin user đầy đủ
        
    Raises:
        HTTPException 401: Token không hợp lệ hoặc hết hạn
        HTTPException 404: User không tồn tại
        
    Security:
        - Yêu cầu JWT token trong Authorization header
        - Format: "Authorization: Bearer <token>"
        
    Example:
        Request Headers:
        ```
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
        
        Response:
        ```json
        {
            "success": true,
            "user": {
                "_id": "507f1f77bcf86cd799439011",
                "phone": "+84987654321",
                "name": "Nguyễn Văn A",
                "email": "user@example.com",
                "role": "user",
                "plan": "premium",
                "used_trips": 45,
                "max_trips": 999999,
                "credit_balance": 150000,
                "is_active": true,
                "is_phone_verified": true,
                "last_login": "2025-01-08T10:30:00Z"
            }
        }
        ```
    """
    return {
        "success": True,
        "user": convert_user_response(current_user)
    }
