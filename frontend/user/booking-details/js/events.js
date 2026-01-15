import { togglePopup } from './ui.js';

export const initEventListeners = () => {
    document.addEventListener('click', (e) => {
        // 1. Kiểm tra nếu click vào ảnh có class clickable-img
        if (e.target.classList.contains('clickable-img')) {
            const imageSrc = e.target.src;
            togglePopup(imageSrc, true);
        }

        // 2. Click vào nút đóng hoặc vùng ngoài ảnh để đóng popup
        const isCloseBtn = e.target.id === 'closePopupBtn';
        const isOverlay = e.target.id === 'imagePopup';
        
        if (isCloseBtn || isOverlay) {
            togglePopup('', false);
        }
    });

    // Cuộn lên đầu trang
    const scrollBtn = document.getElementById('top');
    if (scrollBtn) {
        scrollBtn.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    }
};