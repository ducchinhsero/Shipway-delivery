export const OrderStatus = {
  DELIVERED: 'Đã giao',
  IN_TRANSIT: 'Đang vận chuyển',
  PENDING: 'Chờ xử lý'
};

export const MOCK_ORDERS = [
  {
    id: '#SW-9024',
    date: '24 Tháng 10, 2023',
    recipient: { name: 'John Doe', initials: 'JD' },
    status: OrderStatus.DELIVERED,
    amount: 45.00
  },
  {
    id: '#SW-8942',
    date: '22 Tháng 10, 2023',
    recipient: { name: 'Alice Smith', initials: 'AS' },
    status: OrderStatus.IN_TRANSIT,
    amount: 122.50
  },
  {
    id: '#SW-8910',
    date: '21 Tháng 10, 2023',
    recipient: { name: 'Michael Brown', initials: 'MB' },
    status: OrderStatus.PENDING,
    amount: 18.25
  },
  {
    id: '#SW-8801',
    date: '18 Tháng 10, 2023',
    recipient: { name: 'Sarah Jenkins', initials: 'SJ' },
    status: OrderStatus.DELIVERED,
    amount: 64.00
  },
  {
    id: '#SW-8799',
    date: '15 Tháng 10, 2023',
    recipient: { name: 'Robert King', initials: 'RK' },
    status: OrderStatus.DELIVERED,
    amount: 210.30
  }
];
