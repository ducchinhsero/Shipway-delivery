const getInitials = (name) => {
    if (!name) return "?";
    const parts = name.trim().split(/\s+/);
    return (parts[0][0] + (parts[parts.length - 1][0] || "")).toUpperCase();
};

export const renderUI = (langData) => {
    const uiMap = {
        'web-title': langData.header.title,
        'brand': langData.header.brand,
        'walletBtn': langData.header.wallet,
        'user-name': langData.header.userName,
        'logoutBtn': langData.header.logout,
        'page-title': langData.header.title,
        'order-status': langData.header.status1,
        'backBtn': langData.header.back,
        'footer': langData.header.footer,
        'label-order-id': langData.labels.orderId,
        'order-id': langData.values.orderId,
        'label-pickup': langData.labels.pickup,
        'pickup-location': langData.values.pickup,
        'label-delivery': langData.labels.delivery,
        'delivery-location': langData.values.delivery,
        'label-type': langData.labels.type,
        'type': langData.values.type,
        'label-size': langData.labels.size,
        'size': langData.values.size,
        'label-weight': langData.labels.weight,
        'weight': langData.values.weight,
        'label-driver-name': langData.labels.driver,
        'driver-name': langData.values.driver,
        'label-driver-phone': langData.labels.driverPhone,
        'driver-phone': langData.values.driverPhone,
        'label-cost': langData.labels.cost,
        'cost': langData.values.cost,
        'label-date': langData.labels.date,
        'date-create': langData.values.date,
        'label-image': langData.labels.images
    };

    Object.entries(uiMap).forEach(([id, text]) => {
        const el = document.getElementById(id);
        if (el) el.innerText = text;
    });

    // 1. Xử lý tên người dùng
    const name = langData.header.userName || "Guest User"; 

    const nameEl = document.getElementById('user-name');
    if (nameEl) {
        nameEl.innerText = name;
    }

    const avatarEl = document.getElementById('user-avatar');
    if (avatarEl) {
        avatarEl.innerText = getInitials(name === "Guest User" ? "?" : name);
    }

    // Xử lý logic trạng thái đơn hàng đặc thù
    const statusBox = document.querySelector('.status');
    const orderStatus = langData.values.status;
    if (statusBox) {
        // Map status to state class
        const statusClassMap = {
            'pending': 'state-1',
            'confirmed': 'state-1',
            'picking_up': 'state-2',
            'picked_up': 'state-2',
            'in_transit': 'state-2',
            'delivering': 'state-2',
            'delivered': 'state-3',
            'cancelled': 'state-4',
            'failed': 'state-4'
        };
        statusBox.className = `status ${statusClassMap[orderStatus] || 'state-1'}`;
        document.getElementById('order-status').innerText = langData.header.statusTexts[orderStatus] || orderStatus;
    }

    // Ẩn hiện SĐT tài xế theo trạng thái đơn
    const phoneElement = document.getElementById('driver-phone');

    if (phoneElement) {
        if (orderStatus === 'delivered' && langData.values.driver !== "Chưa có") {
            phoneElement.innerText = langData.values.driverPhone;
            phoneElement.style.color = "#000000"; 
        } else {
            phoneElement.innerText = "**********"; 
        }
    }

    // Render từng Image Item dựa trên mảng confirm_images
    const images = langData.values.confirm_images || []; // Mảng [url1, url2, url3]

    // Hide all image containers first
    for (let i = 1; i <= 3; i++) {
        const imgEl = document.getElementById(`image-container-${i}`);
        if (imgEl) {
            imgEl.style.display = "none";
        }
    }

    // Show images if available
    if (images.length > 0) {
        images.forEach((src, index) => {
            if (index < 3) { // Only show first 3 images
                const imgEl = document.getElementById(`image-container-${index + 1}`);
                if (imgEl) {
                    imgEl.src = src;
                    imgEl.style.display = "block";
                }
            }
        });
    } else {
        // Show placeholder if no images
        const imgEl = document.getElementById(`image-container-1`);
        if (imgEl) {
            imgEl.src = "img/box.jpg";
            imgEl.style.display = "block";
        }
    }

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

    // Xử lý nút Quay lại
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.location.href = '../dashboard/index.html';
      });
    }

};

export const togglePopup = (src = '', show = false) => {
    const popup = document.getElementById("imagePopup");
    const imgFull = document.getElementById("imgFull");
    if (popup) {
        popup.style.display = show ? "flex" : "none";
        if (show && imgFull) imgFull.src = src;
    }
};