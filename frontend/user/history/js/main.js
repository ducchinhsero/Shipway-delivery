import { fetchOrders } from './order.service.js';

const tbody = document.getElementById('orderTableBody');
const filterSelect = document.getElementById('statusFilter');
const orderCountEl = document.getElementById('orderCount');
const timeFilter = document.getElementById('timeFilter');
const nameFilterInput = document.getElementById('nameFilter');

let ALL_ORDERS = [];

function getStatusClass(status) {
  if (status === 'Đã giao') return 'delivered';
  if (status === 'Đang vận chuyển') return 'transit';
  return 'pending';
}

function isWithinDays(orderDate, days) {
  const now = new Date();
  const past = new Date();
  past.setDate(now.getDate() - days);
  return new Date(orderDate) >= past;
}

function getRecipientName(order) {
  return order.recipient_name || order.recipient?.name || '';
}

function renderTable(orders) {
  tbody.innerHTML = '';

  orders.forEach(order => {
    const statusClass = getStatusClass(order.status);

    tbody.innerHTML += `
      <tr class="right">
        <td><strong>${order.id}</strong></td>
        <td>${order.date}</td>
        <td>${getRecipientName(order)}</td>
        <td>
          <span class="status ${statusClass}">
            ${order.status}
          </span>
        </td>
        <td>${order.amount.toFixed(0)}₫</td>
        <td>
          <a href="/order/${order.id}">Chi tiết</a>
        </td>
      </tr>
    `;
  });
}

function updateOrderCount(list) {
  orderCountEl.textContent = `${list.length} đơn hàng tổng cộng`;
}

function applyFilters() {
  let result = [...ALL_ORDERS];

  // 1. Trạng thái
  if (filterSelect.value !== 'Tất cả trạng thái') {
    result = result.filter(o => o.status === filterSelect.value);
  }

  // 2. Thời gian
  if (timeFilter.value !== 'all') {
    const days = Number(timeFilter.value);
    result = result.filter(o => isWithinDays(o.date, days));
  }

  // 3. Tên người nhận
  const keyword = nameFilterInput.value.trim().toLowerCase();
  if (keyword) {
    result = result.filter(o =>
      getRecipientName(o).toLowerCase().includes(keyword)
    );
  }

  renderTable(result);
  updateOrderCount(result);
}

// events
filterSelect.addEventListener('change', applyFilters);
timeFilter.addEventListener('change', applyFilters);
nameFilterInput.addEventListener('input', applyFilters);

(async function init() {
  ALL_ORDERS = await fetchOrders();
  applyFilters();
})();
