// order.service.js
import { adaptOrder } from './order.adapter.js';

export async function fetchOrders() {
  try {
    const token = localStorage.getItem('token');

    // ❌ Fetch cũ (API nội bộ)
    // const res = await fetch('/api/orders', {
    //   headers: {
    //     Authorization: `Bearer ${token}`
    //   }
    // });

    // ✅ Fetch mới: gọi API từ link cụ thể
    const res = await fetch(
    'https://mocki.io/v1/5cabedaf-4147-43fd-a5c1-eac2d87bbd85'
    );

    const data = await res.json();

     console.log('API /orders raw data:', data);

    return Array.isArray(data) ? data.map(adaptOrder) : [];

  } catch (err) {
    console.error('Fetch orders failed:', err);
    return [];
  }
}
