/**
 * API Configuration
 * Tự động detect môi trường và sử dụng URL phù hợp
 */

const API_CONFIG = {
    // Development - local backend
    development: {
        API_BASE_URL: 'http://localhost:8000/api/v1',
        UPLOAD_URL: 'http://localhost:8000/uploads'
    },
    
    // Production - deployed backend
    production: {
        // TODO: Thay đổi URL này sau khi deploy backend lên Railway/Render
        API_BASE_URL: 'https://your-backend-app.railway.app/api/v1',
        UPLOAD_URL: 'https://your-backend-app.railway.app/uploads'
    }
};

// Auto-detect environment
const isProduction = window.location.hostname !== 'localhost' && 
                     window.location.hostname !== '127.0.0.1';

const currentConfig = isProduction ? API_CONFIG.production : API_CONFIG.development;

// Export config
window.API_BASE_URL = currentConfig.API_BASE_URL;
window.UPLOAD_URL = currentConfig.UPLOAD_URL;

console.log('[API Config]', {
    environment: isProduction ? 'production' : 'development',
    API_BASE_URL: window.API_BASE_URL,
    UPLOAD_URL: window.UPLOAD_URL
});
