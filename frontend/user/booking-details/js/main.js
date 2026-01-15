import { langData, fetchOrderData } from './data.js';
import { renderUI } from './ui.js';
import { initEventListeners } from './events.js';

document.addEventListener('DOMContentLoaded', async () => {
    // Get order_id from URL query params
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('order_id');

    if (!orderId) {
        alert('Không tìm thấy thông tin đơn hàng');
        window.location.href = '../dashboard/index.html';
        return;
    }

    try {
        // Show loading state
        document.getElementById('page-title').textContent = 'Đang tải...';

        // Fetch order data from API
        const orderData = await fetchOrderData(orderId);

        // Merge with langData
        const fullData = {
            ...langData,
            values: orderData
        };

        // Render UI with fetched data
        renderUI(fullData);
        initEventListeners();
    } catch (error) {
        alert('Không thể tải thông tin đơn hàng: ' + error.message);
        window.location.href = '../dashboard/index.html';
    }
});