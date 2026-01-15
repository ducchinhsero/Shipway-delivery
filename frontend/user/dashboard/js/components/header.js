export function renderHeader() {
  const userName = localStorage.getItem('userName') || 'User';
  
  // Lấy chữ cái đầu tiên của tên để làm avatar
  const getInitials = (name) => {
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };
  
  const initials = getInitials(userName);
  
  return `
    <header class="main-header">
      <div class="header-left">
        <div class="logo">
          <img 
            src="../dashboard/images/logoshipway.png" 
            alt="Shipway Logo" 
            class="logo-img"
          />
          <span class="brand-name">Shipway</span>
        </div>
      </div>
      <div class="header-right">
        <button id="walletBtn" class="btn-wallet">
          <span class="btn-icon">💰</span>
          <span class="btn-text">Ví tiền</span>
        </button>

        <div class="user-profile">
          <div class="user-avatar" data-initials="${initials}">
            ${initials}
          </div>
          <span class="user-name">${userName}</span>
        </div>
        
        <button id="logoutBtn" class="btn-logout">Đăng xuất</button>
      </div>
    </header>
  `;
}

// Add logout functionality
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    // Xử lý nút Đăng xuất cũ
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        localStorage.clear();
        // Redirect to auth page
        window.location.href = '../../auth/index.html'; 
      });
    }

    // Xử lý nút Ví tiền
    const walletBtn = document.getElementById('walletBtn');
    if (walletBtn) {
      walletBtn.addEventListener('click', () => {
        window.location.href = '../wallet/index.html';
      });
    }
  }, 100);
});
