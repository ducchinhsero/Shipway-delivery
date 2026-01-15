const statusLabels = {
  'FINDING_DRIVER': 'Tìm tài xế',
  'IN_TRANSIT': 'Đang vận chuyển',
  'COMPLETED': 'Hoàn thành',
  'CANCELLED': 'Đã hủy'
};

export function statusBadge(status) {
  const label = statusLabels[status] || status;
  return `<span class="status-badge ${status}">${label}</span>`;
}
