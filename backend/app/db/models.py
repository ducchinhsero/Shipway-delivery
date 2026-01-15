"""
Database models and operations
"""
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from enum import Enum
from app.core.security import hash_password, verify_password
from decimal import Decimal

# ==================== USER MODEL ====================

async def create_user(db: AsyncIOMotorDatabase, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new user
    
    Args:
        db: Database instance
        user_data: User data dictionary
        
    Returns:
        Created user document
    """
    # Hash password
    user_data['password'] = hash_password(user_data['password'])
    user_data['created_at'] = datetime.utcnow()
    user_data['updated_at'] = datetime.utcnow()
    
    # Initialize wallet info for new users
    if 'wallet_info' not in user_data:
        user_data['wallet_info'] = {
            "balance": 0,
            "total_topup": 0,
            "total_usage": 0
        }
    
    result = await db.users.insert_one(user_data)
    user = await db.users.find_one({"_id": result.inserted_id})
    
    return user


async def find_user_by_phone(db: AsyncIOMotorDatabase, phone: str) -> Optional[Dict[str, Any]]:
    """Find user by phone number"""
    return await db.users.find_one({"phone": phone})


async def find_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[Dict[str, Any]]:
    """Find user by ID"""
    try:
        return await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


async def update_user(db: AsyncIOMotorDatabase, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update user information
    
    Args:
        db: Database instance
        user_id: User ID
        update_data: Data to update
        
    Returns:
        Updated user document
    """
    update_data['updated_at'] = datetime.utcnow()
    
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    return await find_user_by_id(db, user_id)


async def update_user_password(db: AsyncIOMotorDatabase, phone: str, new_password: str) -> bool:
    """Update user password"""
    hashed_password = hash_password(new_password)
    
    result = await db.users.update_one(
        {"phone": phone},
        {"$set": {
            "password": hashed_password,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return result.modified_count > 0


async def verify_user_password(user: Dict[str, Any], password: str) -> bool:
    """Verify user password"""
    return verify_password(password, user['password'])


# ==================== OTP MODEL ====================

async def create_otp(db: AsyncIOMotorDatabase, otp_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new OTP record
    
    Args:
        db: Database instance
        otp_data: OTP data dictionary
        
    Returns:
        Created OTP document
    """
    # Delete existing OTPs for the same phone and purpose
    await db.otps.delete_many({
        "phone": otp_data['phone'],
        "purpose": otp_data['purpose']
    })
    
    otp_data['created_at'] = datetime.utcnow()
    otp_data['attempts'] = 0
    otp_data['is_used'] = False
    
    result = await db.otps.insert_one(otp_data)
    otp = await db.otps.find_one({"_id": result.inserted_id})
    
    return otp


async def find_latest_otp(
    db: AsyncIOMotorDatabase,
    phone: str,
    purpose: str
) -> Optional[Dict[str, Any]]:
    """
    Find the latest unused OTP for a phone and purpose
    
    Args:
        db: Database instance
        phone: Phone number
        purpose: OTP purpose (register, reset-password, verify-phone)
        
    Returns:
        OTP document if found, None otherwise
    """
    return await db.otps.find_one(
        {
            "phone": phone,
            "purpose": purpose,
            "is_used": False
        },
        sort=[("created_at", -1)]
    )


async def mark_otp_as_used(db: AsyncIOMotorDatabase, otp_id: ObjectId) -> bool:
    """Mark OTP as used"""
    result = await db.otps.update_one(
        {"_id": otp_id},
        {"$set": {"is_used": True}}
    )
    return result.modified_count > 0


async def increment_otp_attempts(db: AsyncIOMotorDatabase, otp_id: ObjectId) -> int:
    """
    Increment OTP verification attempts
    
    Returns:
        New attempt count
    """
    result = await db.otps.find_one_and_update(
        {"_id": otp_id},
        {"$inc": {"attempts": 1}},
        return_document=True
    )
    return result['attempts'] if result else 0


async def cleanup_expired_otps(db: AsyncIOMotorDatabase) -> int:
    """
    Clean up expired OTPs
    
    Returns:
        Number of deleted OTP records
    """
    result = await db.otps.delete_many({
        "expires_at": {"$lt": datetime.utcnow()}
    })
    return result.deleted_count


# ==================== WALLET & TRANSACTION MODELS ====================

async def create_transaction(
    db: AsyncIOMotorDatabase,
    transaction_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new transaction record
    
    Args:
        db: Database instance
        transaction_data: Transaction data dictionary
        
    Returns:
        Created transaction document
    """
    transaction_data['created_at'] = datetime.utcnow()
    transaction_data['updated_at'] = datetime.utcnow()
    
    result = await db.transactions.insert_one(transaction_data)
    transaction = await db.transactions.find_one({"_id": result.inserted_id})
    
    return transaction


async def get_user_transactions(
    db: AsyncIOMotorDatabase,
    user_id: str,
    limit: int = 50,
    skip: int = 0,
    transaction_type: Optional[str] = None
) -> list:
    """
    Get user's transaction history
    
    Args:
        db: Database instance
        user_id: User ID
        limit: Maximum number of transactions to return
        skip: Number of transactions to skip (for pagination)
        transaction_type: Filter by type (topup, usage, refund)
        
    Returns:
        List of transaction documents
    """
    query = {"user_id": user_id}
    if transaction_type:
        query["type"] = transaction_type
    
    cursor = db.transactions.find(query).sort("created_at", -1).skip(skip).limit(limit)
    transactions = await cursor.to_list(length=limit)
    
    return transactions


async def get_transaction_by_id(
    db: AsyncIOMotorDatabase,
    transaction_id: str
) -> Optional[Dict[str, Any]]:
    """Get transaction by ID"""
    try:
        return await db.transactions.find_one({"_id": ObjectId(transaction_id)})
    except Exception:
        return None


async def get_transaction_by_payment_id(
    db: AsyncIOMotorDatabase,
    payment_id: str
) -> Optional[Dict[str, Any]]:
    """Get transaction by payment ID (for webhook verification)"""
    return await db.transactions.find_one({"payment_id": payment_id})


async def update_transaction_status(
    db: AsyncIOMotorDatabase,
    transaction_id: str,
    status: str,
    payment_details: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Update transaction status
    
    Args:
        db: Database instance
        transaction_id: Transaction ID
        status: New status (pending, completed, failed, cancelled)
        payment_details: Additional payment details (optional)
        
    Returns:
        Updated transaction document
    """
    update_data = {
        "status": status,
        "updated_at": datetime.utcnow()
    }
    
    if payment_details:
        update_data["payment_details"] = payment_details
    
    if status == "completed":
        update_data["completed_at"] = datetime.utcnow()
    
    await db.transactions.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": update_data}
    )
    
    return await get_transaction_by_id(db, transaction_id)


async def get_wallet_info(
    db: AsyncIOMotorDatabase,
    user_id: str
) -> Optional[Dict[str, Any]]:
    """
    Get user's wallet information
    
    Args:
        db: Database instance
        user_id: User ID
        
    Returns:
        Wallet info with balance and statistics
    """
    user = await find_user_by_id(db, user_id)
    if not user:
        return None
    
    wallet_info = user.get('wallet_info', {})
    
    # Get recent transactions
    recent_transactions = await get_user_transactions(db, user_id, limit=5)
    
    # Calculate statistics
    total_topup = wallet_info.get('total_topup', 0)
    total_usage = wallet_info.get('total_usage', 0)
    current_balance = wallet_info.get('balance', 0)
    
    # Get pending transactions
    pending_transactions = await db.transactions.count_documents({
        "user_id": user_id,
        "status": "pending"
    })
    
    return {
        "user_id": user_id,
        "balance": current_balance,
        "total_topup": total_topup,
        "total_usage": total_usage,
        "pending_transactions": pending_transactions,
        "recent_transactions": recent_transactions
    }


async def add_to_wallet(
    db: AsyncIOMotorDatabase,
    user_id: str,
    amount: int
) -> Optional[Dict[str, Any]]:
    """
    Add money to user's wallet
    
    Args:
        db: Database instance
        user_id: User ID
        amount: Amount to add
        
    Returns:
        Updated user document
    """
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$inc": {
                "wallet_info.balance": amount,
                "wallet_info.total_topup": amount
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return await find_user_by_id(db, user_id)


async def use_from_wallet(
    db: AsyncIOMotorDatabase,
    user_id: str,
    amount: int
) -> Optional[Dict[str, Any]]:
    """
    Deduct money from user's wallet
    
    Args:
        db: Database instance
        user_id: User ID
        amount: Amount to deduct
        
    Returns:
        Updated user document or None if insufficient balance
    """
    user = await find_user_by_id(db, user_id)
    if not user:
        return None
    
    wallet_balance = user.get('wallet_info', {}).get('balance', 0)
    if wallet_balance < amount:
        return None  # Insufficient balance
    
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$inc": {
                "wallet_info.balance": -amount,
                "wallet_info.total_usage": amount
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return await find_user_by_id(db, user_id)


# ==================== ORDER MODEL ====================

async def generate_tracking_code(db: AsyncIOMotorDatabase) -> str:
    """
    Generate unique tracking code for order
    
    Args:
        db: Database instance
        
    Returns:
        Unique tracking code (format: SW + YYYYMMDD + sequential number)
    """
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"SW{today}"
    
    # Find the highest order number for today
    last_order = await db.orders.find_one(
        {"tracking_code": {"$regex": f"^{prefix}"}},
        sort=[("tracking_code", -1)]
    )
    
    if last_order:
        # Extract number and increment
        last_code = last_order["tracking_code"]
        last_number = int(last_code[len(prefix):])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:03d}"


async def create_order(db: AsyncIOMotorDatabase, order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new order
    
    Args:
        db: Database instance
        order_data: Order data dictionary
        
    Returns:
        Created order document
    """
    # Generate tracking code
    order_data['tracking_code'] = await generate_tracking_code(db)
    
    # Set timestamps
    order_data['created_at'] = datetime.utcnow()
    order_data['updated_at'] = datetime.utcnow()
    
    # Initialize status and history
    if 'status' not in order_data:
        order_data['status'] = 'pending'
    
    order_data['history'] = [{
        "status": order_data['status'],
        "timestamp": datetime.utcnow(),
        "note": "Đơn hàng được tạo"
    }]
    
    # Initialize flags
    order_data['is_reviewed'] = False
    order_data['is_paid'] = False
    
    # Insert order
    result = await db.orders.insert_one(order_data)
    order = await db.orders.find_one({"_id": result.inserted_id})
    
    return order


async def get_order_by_id(db: AsyncIOMotorDatabase, order_id: str) -> Optional[Dict[str, Any]]:
    """
    Get order by ID
    
    Args:
        db: Database instance
        order_id: Order ID
        
    Returns:
        Order document or None
    """
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
        return order
    except:
        return None


async def get_order_by_tracking_code(
    db: AsyncIOMotorDatabase,
    tracking_code: str
) -> Optional[Dict[str, Any]]:
    """
    Get order by tracking code
    
    Args:
        db: Database instance
        tracking_code: Tracking code
        
    Returns:
        Order document or None
    """
    return await db.orders.find_one({"tracking_code": tracking_code})


async def get_user_orders(
    db: AsyncIOMotorDatabase,
    user_id: str,
    status: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
) -> tuple[List[Dict[str, Any]], int]:
    """
    Get user's orders with pagination
    
    Args:
        db: Database instance
        user_id: User ID
        status: Filter by status (optional)
        limit: Number of orders to return
        skip: Number of orders to skip
        
    Returns:
        Tuple of (orders list, total count)
    """
    query = {"user_id": user_id}
    
    if status:
        query["status"] = status
    
    # Get total count
    total = await db.orders.count_documents(query)
    
    # Get paginated results
    cursor = db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    return orders, total


async def get_driver_orders(
    db: AsyncIOMotorDatabase,
    driver_id: str,
    status: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
) -> tuple[List[Dict[str, Any]], int]:
    """
    Get driver's assigned orders
    
    Args:
        db: Database instance
        driver_id: Driver ID
        status: Filter by status (optional)
        limit: Number of orders to return
        skip: Number of orders to skip
        
    Returns:
        Tuple of (orders list, total count)
    """
    query = {"driver_id": driver_id}
    
    if status:
        query["status"] = status
    
    total = await db.orders.count_documents(query)
    cursor = db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    return orders, total


async def update_order_status(
    db: AsyncIOMotorDatabase,
    order_id: str,
    new_status: str,
    note: Optional[str] = None,
    updated_by: Optional[str] = None
) -> bool:
    """
    Update order status and add to history
    
    Args:
        db: Database instance
        order_id: Order ID
        new_status: New status
        note: Optional note
        updated_by: User/Driver ID who updated
        
    Returns:
        True if successful, False otherwise
    """
    history_entry = {
        "status": new_status,
        "timestamp": datetime.utcnow(),
        "note": note,
        "updated_by": updated_by
    }
    
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "status": new_status,
                "updated_at": datetime.utcnow()
            },
            "$push": {"history": history_entry}
        }
    )
    
    return result.modified_count > 0


async def assign_driver_to_order(
    db: AsyncIOMotorDatabase,
    order_id: str,
    driver_id: str
) -> bool:
    """
    Assign a driver to an order
    
    Args:
        db: Database instance
        order_id: Order ID
        driver_id: Driver ID
        
    Returns:
        True if successful, False otherwise
    """
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "driver_id": driver_id,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return result.modified_count > 0


async def update_order_payment(
    db: AsyncIOMotorDatabase,
    order_id: str,
    is_paid: bool,
    payment_method: str
) -> bool:
    """
    Update order payment status
    
    Args:
        db: Database instance
        order_id: Order ID
        is_paid: Payment status
        payment_method: Payment method used
        
    Returns:
        True if successful, False otherwise
    """
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "is_paid": is_paid,
                "payment_method": payment_method,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return result.modified_count > 0


async def add_images_to_order(
    db: AsyncIOMotorDatabase,
    order_id: str,
    image_paths: List[str]
) -> bool:
    """
    Add images to an order
    
    Args:
        db: Database instance
        order_id: Order ID
        image_paths: List of image paths/URLs
        
    Returns:
        True if successful, False otherwise
    """
    result = await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$push": {"images": {"$each": image_paths}},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return result.modified_count > 0


async def delete_order(db: AsyncIOMotorDatabase, order_id: str) -> bool:
    """
    Delete an order (soft delete by setting status to cancelled)
    
    Args:
        db: Database instance
        order_id: Order ID
        
    Returns:
        True if successful, False otherwise
    """
    return await update_order_status(db, order_id, "cancelled", "Đơn hàng đã bị hủy")


async def get_available_orders(
    db: AsyncIOMotorDatabase,
    vehicle_type: Optional[str] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Get available orders for drivers (pending/confirmed orders without assigned driver)
    
    Args:
        db: Database instance
        vehicle_type: Filter by vehicle type (optional)
        limit: Number of orders to return
        
    Returns:
        List of available orders
    """
    query = {
        "driver_id": None,
        "status": {"$in": ["pending", "confirmed"]}
    }
    
    if vehicle_type:
        query["vehicle_type"] = vehicle_type
    
    cursor = db.orders.find(query).sort("created_at", -1).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    return orders