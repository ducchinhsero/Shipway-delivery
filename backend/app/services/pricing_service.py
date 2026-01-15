"""
Pricing service for calculating shipping fees
"""
from typing import Dict, Any
from app.schemas.order import VehicleType
import math


# Base pricing configuration (VND)
PRICING_CONFIG = {
    VehicleType.BIKE: {
        "base_fee": 15000,      # Phí cơ bản
        "per_km": 3000,         # Giá mỗi km
        "max_weight": 30,       # Khối lượng tối đa (kg)
        "weight_surcharge": 0   # Phụ phí theo cân nặng
    },
    VehicleType.CAR: {
        "base_fee": 30000,
        "per_km": 5000,
        "max_weight": 300,
        "weight_surcharge": 500  # 500 VND/kg nếu > 50kg
    },
    VehicleType.VAN: {
        "base_fee": 50000,
        "per_km": 7000,
        "max_weight": 500,
        "weight_surcharge": 400
    },
    VehicleType.TRUCK_500KG: {
        "base_fee": 80000,
        "per_km": 10000,
        "max_weight": 500,
        "weight_surcharge": 300
    },
    VehicleType.TRUCK_1000KG: {
        "base_fee": 120000,
        "per_km": 15000,
        "max_weight": 1000,
        "weight_surcharge": 200
    }
}


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lng1: First location coordinates
        lat2, lng2: Second location coordinates
        
    Returns:
        Distance in kilometers
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)


def calculate_shipping_fee(
    distance_km: float,
    weight: float,
    vehicle_type: VehicleType,
    cod_amount: float = 0
) -> Dict[str, Any]:
    """
    Calculate shipping fee based on distance, weight, and vehicle type
    
    Args:
        distance_km: Distance in kilometers
        weight: Package weight in kg
        vehicle_type: Type of vehicle
        cod_amount: COD amount (if any)
        
    Returns:
        Dict containing fee breakdown
    """
    config = PRICING_CONFIG[vehicle_type]
    
    # Validate weight
    if weight > config["max_weight"]:
        raise ValueError(
            f"Khối lượng vượt quá giới hạn cho loại xe {vehicle_type.value}. "
            f"Tối đa: {config['max_weight']}kg"
        )
    
    # Base fee + distance fee
    base_fee = config["base_fee"]
    distance_fee = distance_km * config["per_km"]
    
    # Weight surcharge (if applicable)
    weight_surcharge = 0
    if weight > 50 and config["weight_surcharge"] > 0:
        excess_weight = weight - 50
        weight_surcharge = excess_weight * config["weight_surcharge"]
    
    # COD fee (1% of COD amount, max 50,000 VND)
    cod_fee = 0
    if cod_amount > 0:
        cod_fee = min(cod_amount * 0.01, 50000)
    
    # Total shipping fee
    shipping_fee = base_fee + distance_fee + weight_surcharge + cod_fee
    
    # Round to nearest 1000 VND
    shipping_fee = math.ceil(shipping_fee / 1000) * 1000
    
    return {
        "base_fee": base_fee,
        "distance_fee": distance_fee,
        "weight_surcharge": weight_surcharge,
        "cod_fee": cod_fee,
        "shipping_fee": shipping_fee,
        "total_amount": shipping_fee + cod_amount
    }


def validate_vehicle_for_weight(weight: float, vehicle_type: VehicleType) -> bool:
    """
    Check if vehicle type can handle the given weight
    
    Args:
        weight: Package weight in kg
        vehicle_type: Type of vehicle
        
    Returns:
        True if valid, False otherwise
    """
    config = PRICING_CONFIG[vehicle_type]
    return weight <= config["max_weight"]


def suggest_vehicle_type(weight: float) -> VehicleType:
    """
    Suggest appropriate vehicle type based on weight
    
    Args:
        weight: Package weight in kg
        
    Returns:
        Suggested vehicle type
    """
    if weight <= 30:
        return VehicleType.BIKE
    elif weight <= 300:
        return VehicleType.CAR
    elif weight <= 500:
        return VehicleType.VAN
    elif weight <= 500:
        return VehicleType.TRUCK_500KG
    else:
        return VehicleType.TRUCK_1000KG
