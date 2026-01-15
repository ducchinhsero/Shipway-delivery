"""
File upload service for handling images and documents
"""
import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from pathlib import Path


# Configuration
UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_FILES_PER_ORDER = 5


def ensure_upload_directory():
    """Create upload directory if it doesn't exist"""
    orders_dir = UPLOAD_DIR / "orders"
    orders_dir.mkdir(parents=True, exist_ok=True)
    return orders_dir


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file không được hỗ trợ. Chỉ chấp nhận: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Check file size (requires reading file, reset position after)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File quá lớn. Kích thước tối đa: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )


async def save_order_images(files: List[UploadFile], order_id: str) -> List[str]:
    """
    Save uploaded images for an order
    
    Args:
        files: List of uploaded files
        order_id: Order ID to associate images with
        
    Returns:
        List of saved file paths/URLs
        
    Raises:
        HTTPException: If validation fails
    """
    if len(files) > MAX_FILES_PER_ORDER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tối đa {MAX_FILES_PER_ORDER} ảnh cho mỗi đơn hàng"
        )
    
    # Ensure upload directory exists
    upload_dir = ensure_upload_directory()
    saved_paths = []
    
    for file in files:
        # Validate file
        validate_image_file(file)
        
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{order_id}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = upload_dir / unique_filename
        
        # Save file
        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Store relative path (in production, this would be a CDN URL)
            relative_path = f"/uploads/orders/{unique_filename}"
            saved_paths.append(relative_path)
            
        except Exception as e:
            # Clean up any successfully saved files
            for saved_path in saved_paths:
                try:
                    os.remove(UPLOAD_DIR / saved_path.lstrip("/"))
                except:
                    pass
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi khi lưu file: {str(e)}"
            )
    
    return saved_paths


async def delete_order_images(image_paths: List[str]) -> None:
    """
    Delete order images from storage
    
    Args:
        image_paths: List of image paths to delete
    """
    for path in image_paths:
        try:
            file_path = UPLOAD_DIR / path.lstrip("/")
            if file_path.exists():
                os.remove(file_path)
        except Exception as e:
            # Log error but don't raise exception
            print(f"Error deleting file {path}: {e}")


def get_full_image_url(path: str, base_url: str = "http://localhost:8000") -> str:
    """
    Convert relative path to full URL
    
    Args:
        path: Relative file path
        base_url: Base URL of the application
        
    Returns:
        Full URL to the image
    """
    if path.startswith("http"):
        return path
    return f"{base_url}{path}"
