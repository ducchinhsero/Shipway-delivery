import { statusBadge } from "./statusBadge.js";

export function orderItem(order) {
  return `
    <div class="order-item">
      <div class="item-id" data-label="Mã">${order.order_code}</div>
      <div class="item-date" data-label="Ngày đặt">${order.created_at}</div>
      <div class="item-product" data-label="Tên hàng">${order.product_name}</div>
      <div class="item-weight" data-label="Khối lượng">${order.weight}</div>
      <div class="item-price" data-label="Giá">${order.price}</div>
      <div class="item-status" data-label="Trạng thái">${statusBadge(order.status)}</div>
      <div class="item-actions" data-label="Chi tiết">

        <button 
            class="btn-action" 
            title="Chi tiết"
            onclick="window.location.href='../booking-details/index.html?id=${order.order_code}'"
        >
            ⋮
        </button>

      </div>
    </div>
  `;
}
