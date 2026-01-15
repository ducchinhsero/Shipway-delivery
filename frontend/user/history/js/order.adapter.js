// order.adapter.js

export function adaptOrder(apiOrder) {
  if (!apiOrder || typeof apiOrder !== 'object') {
    throw new Error('Invalid order data');
  }

  return {
    id: apiOrder.id ?? '—',

    date: apiOrder.date
      ? new Date(apiOrder.date).toLocaleDateString('vi-VN')
      : '',

    recipient: {
      name: apiOrder.recipient_name ?? apiOrder.recipient?.name ?? 'Chưa có'
    },

    status: apiOrder.status ?? 'Chờ xử lý',

    amount: Number(apiOrder.amount ?? apiOrder.total_amount ?? 0)
  };
}
