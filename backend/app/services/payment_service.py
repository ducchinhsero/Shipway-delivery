"""
Payment Service - QR Code Generation & Payment Gateway Integration
"""
import io
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import qrcode
from qrcode.image.pure import PyPNGImage


class PaymentService:
    """Payment service for handling top-up transactions"""
    
    # Bank account information (replace with real bank account)
    BANK_INFO = {
        "bank_id": "970422",  # MB Bank
        "bank_name": "MB Bank",
        "account_no": "0123456789",
        "account_name": "CONG TY SHIPWAY",
        "branch": "Ho Chi Minh"
    }
    
    # Payment gateway configurations (mock for demo)
    MOMO_CONFIG = {
        "partner_code": "MOMO_PARTNER_CODE",
        "access_key": "MOMO_ACCESS_KEY",
        "secret_key": "MOMO_SECRET_KEY",
        "endpoint": "https://test-payment.momo.vn/v2/gateway/api/create"
    }
    
    VNPAY_CONFIG = {
        "tmn_code": "VNPAY_TMN_CODE",
        "hash_secret": "VNPAY_HASH_SECRET",
        "endpoint": "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    }
    
    @staticmethod
    def generate_payment_id() -> str:
        """Generate unique payment ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = secrets.token_hex(4).upper()
        return f"SW{timestamp}{random_str}"
    
    @staticmethod
    def generate_qr_code_vietqr(
        amount: int,
        payment_id: str,
        description: str = "Nap tien Shipway"
    ) -> str:
        """
        Generate VietQR code for bank transfer
        
        Args:
            amount: Amount in VND
            payment_id: Unique payment ID
            description: Transaction description
            
        Returns:
            Base64 encoded QR code image
        """
        # VietQR format: bankId|accountNo|accountName|amount|description|template
        bank_info = PaymentService.BANK_INFO
        
        # Format payment description with payment ID
        payment_description = f"{description} {payment_id}"
        
        # VietQR data string
        qr_data = (
            f"{bank_info['bank_id']}|"
            f"{bank_info['account_no']}|"
            f"{bank_info['account_name']}|"
            f"{amount}|"
            f"{payment_description}|"
            f"qr_only"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def create_bank_transfer_payment(
        amount: int,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Create bank transfer payment
        
        Args:
            amount: Amount in VND
            user_id: User ID
            
        Returns:
            Payment information with QR code
        """
        payment_id = PaymentService.generate_payment_id()
        description = f"Nap tien Shipway"
        
        # Generate QR code
        qr_code = PaymentService.generate_qr_code_vietqr(
            amount=amount,
            payment_id=payment_id,
            description=description
        )
        
        # Bank info
        bank_info = {
            "bank_name": PaymentService.BANK_INFO['bank_name'],
            "account_no": PaymentService.BANK_INFO['account_no'],
            "account_name": PaymentService.BANK_INFO['account_name'],
            "branch": PaymentService.BANK_INFO['branch'],
            "amount": amount,
            "content": f"{description} {payment_id}"
        }
        
        # Payment expires in 15 minutes
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        return {
            "payment_id": payment_id,
            "qr_code": qr_code,
            "bank_info": bank_info,
            "expires_at": expires_at
        }
    
    @staticmethod
    def create_momo_payment(
        amount: int,
        user_id: str,
        order_info: str
    ) -> Dict[str, Any]:
        """
        Create Momo payment (mock implementation)
        
        Args:
            amount: Amount in VND
            user_id: User ID
            order_info: Order information
            
        Returns:
            Payment URL and information
        """
        payment_id = PaymentService.generate_payment_id()
        
        # Mock Momo payment URL
        payment_url = (
            f"https://test-payment.momo.vn/v2/gateway/pay?"
            f"partnerCode={PaymentService.MOMO_CONFIG['partner_code']}&"
            f"orderId={payment_id}&"
            f"amount={amount}&"
            f"orderInfo={order_info}"
        )
        
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        return {
            "payment_id": payment_id,
            "payment_url": payment_url,
            "qr_code": None,  # Momo has its own QR in their page
            "expires_at": expires_at
        }
    
    @staticmethod
    def create_vnpay_payment(
        amount: int,
        user_id: str,
        order_info: str
    ) -> Dict[str, Any]:
        """
        Create VNPay payment (mock implementation)
        
        Args:
            amount: Amount in VND
            user_id: User ID
            order_info: Order information
            
        Returns:
            Payment URL and information
        """
        payment_id = PaymentService.generate_payment_id()
        
        # Mock VNPay payment URL
        payment_url = (
            f"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?"
            f"vnp_TmnCode={PaymentService.VNPAY_CONFIG['tmn_code']}&"
            f"vnp_TxnRef={payment_id}&"
            f"vnp_Amount={amount * 100}&"  # VNPay uses cents
            f"vnp_OrderInfo={order_info}"
        )
        
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        return {
            "payment_id": payment_id,
            "payment_url": payment_url,
            "qr_code": None,
            "expires_at": expires_at
        }
    
    @staticmethod
    def verify_payment_signature(
        payment_id: str,
        amount: int,
        status: str,
        signature: str,
        secret_key: str = "SHIPWAY_SECRET_KEY"
    ) -> bool:
        """
        Verify payment signature from webhook
        
        Args:
            payment_id: Payment ID
            amount: Amount
            status: Payment status
            signature: Signature from payment gateway
            secret_key: Secret key for verification
            
        Returns:
            True if signature is valid
        """
        # Create signature
        data = f"{payment_id}{amount}{status}{secret_key}"
        expected_signature = hashlib.sha256(data.encode()).hexdigest()
        
        return signature == expected_signature
    
    @staticmethod
    def generate_payment_signature(
        payment_id: str,
        amount: int,
        status: str,
        secret_key: str = "SHIPWAY_SECRET_KEY"
    ) -> str:
        """
        Generate payment signature for webhook
        
        Args:
            payment_id: Payment ID
            amount: Amount
            status: Payment status
            secret_key: Secret key
            
        Returns:
            Payment signature
        """
        data = f"{payment_id}{amount}{status}{secret_key}"
        return hashlib.sha256(data.encode()).hexdigest()
