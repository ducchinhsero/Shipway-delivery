// Static labels for the page
export const langData = {
    header: {
        title: "Chi tiết đơn hàng",
        brand: "Shipway",
        wallet: "💰 Ví tiền",
        logout: "Đăng xuất",
        statusTexts: {
            pending: "Chờ xác nhận",
            confirmed: "Đã xác nhận",
            picking_up: "Đang đến lấy hàng",
            picked_up: "Đã lấy hàng",
            in_transit: "Đang vận chuyển",
            delivering: "Đang giao hàng",
            delivered: "Đã giao hàng",
            cancelled: "Đã hủy",
            failed: "Giao hàng thất bại"
        },
        back: "Quay lại",
        footer: "© 2017 - 2026 - Công ty Cổ phần Shipway"
    },

    labels: {
        orderId: "Mã vận đơn",
        pickup: "Điểm nhận hàng",
        delivery: "Điểm trả hàng",
        type: "Tên hàng hóa",
        size: "Kích thước",
        weight: "Trọng lượng",
        driver: "Tài xế",
        driverPhone: "SĐT tài xế",
        cost: "Tổng tiền",
        date: "Ngày tạo",
        images: "Ảnh hàng hoá"
    }
};

// Fetch order data from API
export async function fetchOrderData(orderId) {
    const token = localStorage.getItem("access_token");
    const API_BASE_URL = window.location.origin;

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/orders/${orderId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Không thể tải thông tin đơn hàng');
        }

        const order = await response.json();
        
        // Transform API data to match UI format
        return {
            orderId: order.tracking_code,
            status: order.status,
            pickup: `${order.pickup_info.address}\nNgười gửi: ${order.pickup_info.contact_name}\nSĐT: ${order.pickup_info.contact_phone}`,
            delivery: `${order.dropoff_info.address}\nNgười nhận: ${order.dropoff_info.contact_name}\nSĐT: ${order.dropoff_info.contact_phone}`,
            type: order.product_name,
            size: order.length && order.width && order.height 
                ? `${order.length} x ${order.width} x ${order.height} cm` 
                : "Không có thông tin",
            weight: `${order.weight} kg`,
            driver: order.driver_id || "Chưa có",
            driverPhone: order.driver_id ? "**********" : "Chưa có",
            cost: `${order.total_amount.toLocaleString('vi-VN')} VNĐ`,
            date: new Date(order.created_at).toLocaleString('vi-VN'),
            confirm_images: order.images && order.images.length > 0 
                ? order.images.map(img => img.startsWith('http') ? img : `${API_BASE_URL}/${img}`)
                : []
        };
    } catch (error) {
        console.error('Error fetching order:', error);
        throw error;
    }
}