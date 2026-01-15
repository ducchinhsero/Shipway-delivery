"""
Wallet API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.api.deps import get_current_user, get_database
from app.schemas.user import UserResponse
from app.schemas.wallet import (
    WalletResponse,
    WalletInfo,
    TransactionListResponse,
    TransactionResponse,
    TopUpRequest,
    TopUpResponse,
    PaymentVerificationRequest,
    PaymentVerificationResponse
)
from app.db.models import (
    get_wallet_info,
    get_user_transactions,
    create_transaction,
    get_transaction_by_payment_id,
    update_transaction_status,
    add_to_wallet
)
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/", response_model=WalletResponse)
async def get_wallet(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get wallet information
    
    Returns:
        - balance: Current balance
        - total_topup: Total amount topped up
        - total_usage: Total amount used
        - pending_transactions: Number of pending transactions
        - recent_transactions: List of recent transactions
    """
    wallet_info = await get_wallet_info(db, str(current_user.id))
    
    if not wallet_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    # Convert recent transactions
    recent_transactions = []
    for tx in wallet_info.get('recent_transactions', []):
        tx_dict = {
            "_id": str(tx['_id']),
            "user_id": tx['user_id'],
            "amount": tx['amount'],
            "type": tx['type'],
            "description": tx.get('description'),
            "status": tx['status'],
            "payment_id": tx.get('payment_id'),
            "payment_method": tx.get('payment_method'),
            "payment_details": tx.get('payment_details'),
            "created_at": tx['created_at'],
            "updated_at": tx['updated_at'],
            "completed_at": tx.get('completed_at')
        }
        recent_transactions.append(TransactionResponse(**tx_dict))
    
    wallet = WalletInfo(
        user_id=wallet_info['user_id'],
        balance=wallet_info['balance'],
        total_topup=wallet_info['total_topup'],
        total_usage=wallet_info['total_usage'],
        pending_transactions=wallet_info['pending_transactions'],
        recent_transactions=recent_transactions
    )
    
    return WalletResponse(wallet=wallet)


@router.get("/transactions", response_model=TransactionListResponse)
async def get_transactions(
    limit: int = 50,
    skip: int = 0,
    transaction_type: str = None,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get transaction history
    
    Query Parameters:
        - limit: Maximum number of transactions (default: 50, max: 100)
        - skip: Number of transactions to skip (for pagination)
        - transaction_type: Filter by type (topup, usage, refund)
    
    Returns:
        List of transactions
    """
    # Limit validation
    if limit > 100:
        limit = 100
    
    transactions = await get_user_transactions(
        db,
        str(current_user.id),
        limit=limit,
        skip=skip,
        transaction_type=transaction_type
    )
    
    # Convert to response format
    transaction_list = []
    for tx in transactions:
        tx_dict = {
            "_id": str(tx['_id']),
            "user_id": tx['user_id'],
            "amount": tx['amount'],
            "type": tx['type'],
            "description": tx.get('description'),
            "status": tx['status'],
            "payment_id": tx.get('payment_id'),
            "payment_method": tx.get('payment_method'),
            "payment_details": tx.get('payment_details'),
            "created_at": tx['created_at'],
            "updated_at": tx['updated_at'],
            "completed_at": tx.get('completed_at')
        }
        transaction_list.append(TransactionResponse(**tx_dict))
    
    return TransactionListResponse(
        total=len(transaction_list),
        transactions=transaction_list
    )


@router.post("/topup", response_model=TopUpResponse)
async def create_topup(
    request: TopUpRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a top-up request
    
    Request Body:
        - amount: Amount to top up (VND)
        - payment_method: Payment method (qr, bank_transfer, momo, vnpay)
    
    Returns:
        - transaction_id: Transaction ID
        - payment_id: Payment ID
        - qr_code: QR code image (for bank transfer)
        - payment_url: Payment URL (for momo, vnpay)
        - bank_info: Bank information (for bank transfer)
        - expires_at: Payment expiration time
    """
    payment_service = PaymentService()
    
    # Create payment based on method
    if request.payment_method in ['qr', 'bank_transfer']:
        payment_info = payment_service.create_bank_transfer_payment(
            amount=request.amount,
            user_id=str(current_user.id)
        )
    elif request.payment_method == 'momo':
        payment_info = payment_service.create_momo_payment(
            amount=request.amount,
            user_id=str(current_user.id),
            order_info=f"Nap tien Shipway - {current_user.name}"
        )
    elif request.payment_method == 'vnpay':
        payment_info = payment_service.create_vnpay_payment(
            amount=request.amount,
            user_id=str(current_user.id),
            order_info=f"Nap tien Shipway - {current_user.name}"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment method"
        )
    
    # Create transaction record
    transaction_data = {
        "user_id": str(current_user.id),
        "amount": request.amount,
        "type": "topup",
        "description": f"Nạp tiền qua {request.payment_method}",
        "status": "pending",
        "payment_id": payment_info['payment_id'],
        "payment_method": request.payment_method,
        "payment_details": {
            "expires_at": payment_info['expires_at'].isoformat()
        }
    }
    
    transaction = await create_transaction(db, transaction_data)
    
    return TopUpResponse(
        transaction_id=str(transaction['_id']),
        payment_id=payment_info['payment_id'],
        amount=request.amount,
        payment_method=request.payment_method,
        qr_code=payment_info.get('qr_code'),
        payment_url=payment_info.get('payment_url'),
        bank_info=payment_info.get('bank_info'),
        expires_at=payment_info['expires_at']
    )


@router.post("/verify-payment", response_model=PaymentVerificationResponse)
async def verify_payment(
    request: PaymentVerificationRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Verify payment (webhook endpoint)
    
    This endpoint is called by payment gateways to notify payment status.
    In production, this should be properly secured with signature verification.
    
    Request Body:
        - payment_id: Payment ID
        - status: Payment status (success, failed)
        - transaction_code: Transaction code from bank
        - payment_time: Payment time
        - signature: Security signature
    
    Returns:
        - success: Whether verification was successful
        - message: Verification message
        - transaction_id: Transaction ID
        - new_balance: New wallet balance
    """
    # Find transaction by payment ID
    transaction = await get_transaction_by_payment_id(db, request.payment_id)
    
    if not transaction:
        return PaymentVerificationResponse(
            success=False,
            message="Transaction not found"
        )
    
    # Check if transaction is already completed
    if transaction['status'] == 'completed':
        return PaymentVerificationResponse(
            success=False,
            message="Transaction already completed"
        )
    
    # Verify signature (in production)
    # if request.signature:
    #     is_valid = PaymentService.verify_payment_signature(
    #         payment_id=request.payment_id,
    #         amount=transaction['amount'],
    #         status=request.status,
    #         signature=request.signature
    #     )
    #     if not is_valid:
    #         return PaymentVerificationResponse(
    #             success=False,
    #             message="Invalid signature"
    #         )
    
    # Update transaction status
    if request.status == 'success':
        # Update transaction
        payment_details = {
            "transaction_code": request.transaction_code,
            "payment_time": request.payment_time.isoformat() if request.payment_time else None
        }
        
        await update_transaction_status(
            db,
            str(transaction['_id']),
            'completed',
            payment_details
        )
        
        # Add credit to user
        user = await add_to_wallet(
            db,
            transaction['user_id'],
            transaction['amount']
        )
        
        new_balance = user['wallet_info']['balance']
        
        return PaymentVerificationResponse(
            success=True,
            message="Payment verified successfully",
            transaction_id=str(transaction['_id']),
            new_balance=new_balance
        )
    else:
        # Payment failed
        await update_transaction_status(
            db,
            str(transaction['_id']),
            'failed'
        )
        
        return PaymentVerificationResponse(
            success=False,
            message="Payment failed"
        )
