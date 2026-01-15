import { renderHeader } from "../components/header.js";
import { orderItem } from "../components/orderItem.js";
import { authGuard } from "../../../../shared/auth-guard.js";

// Backend API integration
const API_BASE = 'http://localhost:8000/api/v1';

// Render header
document.getElementById("header").innerHTML = renderHeader();

const orderList = document.getElementById("orderList");

let allOrders = [];
let currentFilter = 'ALL';
let isLoading = false;

// Render orders function
function renderOrders(orders) {
  if (isLoading) {
    orderList.innerHTML = '<div class="empty-state"><p>Đang tải...</p></div>';
    return;
  }

  if (orders.length === 0) {
    orderList.innerHTML = '<div class="empty-state"><p>Không có đơn hàng nào</p></div>';
    return;
  }
  orderList.innerHTML = orders.map(orderItem).join("");
}

// Fetch orders from backend
async function fetchOrders() {
  try {
    isLoading = true;
    renderOrders([]);

    const user = authGuard.getCurrentUser();
    const token = localStorage.getItem('token');

    if (!token) {
      throw new Error('No authentication token');
    }

    const response = await fetch(`${API_BASE}/orders`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    allOrders = data.orders || data || [];
    
    isLoading = false;
    applyFilter();
  } catch (error) {
    console.error('[Dashboard] Error fetching orders:', error);
    isLoading = false;
    orderList.innerHTML = `<div class="empty-state"><p style="color: red;">Lỗi: ${error.message}</p></div>`;
  }
}

// Apply current filter
function applyFilter() {
  if (currentFilter === "ALL") {
    renderOrders(allOrders);
  } else {
    const filtered = allOrders.filter(o => o.status === currentFilter);
    renderOrders(filtered);
  }
}

// Initial fetch
fetchOrders();

// Filter functionality
const filterButtons = document.querySelectorAll(".filter-btn");

filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    // Remove active class from all buttons
    filterButtons.forEach(b => b.classList.remove("active"));
    
    // Add active class to clicked button
    btn.classList.add("active");
    
    // Get status and filter
    const status = btn.dataset.status;
    currentFilter = status;
    
    applyFilter();
  });
});

// Create order button
document.querySelector(".btn-create-order")?.addEventListener("click", () => {
  window.location.href = '../booking/index.html'; // Updated path
});
