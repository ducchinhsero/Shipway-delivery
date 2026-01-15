# Shipway Frontend

Frontend application cho hệ thống quản lý vận chuyển Shipway.

## Công nghệ

- **HTML5** - Markup
- **CSS3** - Styling
- **Vanilla JavaScript** - Logic (ES6 Modules)

## Cấu trúc thư mục

```
frontend/
├── assets/
│   ├── css/
│   │   └── auth.css          # Styles cho authentication
│   └── js/
│       ├── api.js            # API calls & HTTP client
│       ├── auth.service.js   # Authentication services
│       └── auth.controller.js # UI controllers
├── config/
│   └── env.js                # Environment configuration
├── img/
│   └── ...                   # Images & assets
└── index.html                # Main entry point
```

## Cài đặt & Chạy

### Development

1. **Cấu hình API URL**

Mở `config/env.js` và cập nhật `BASE_URL`:

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:5000/api',  // Backend API URL
  // ...
};
```

2. **Chạy với Live Server**

Có thể sử dụng:

- **VS Code Live Server Extension** (Recommended)
  - Install extension: Live Server
  - Right click `index.html` → Open with Live Server
  
- **Python HTTP Server**
  ```bash
  python -m http.server 3000
  ```
  
- **Node.js http-server**
  ```bash
  npm install -g http-server
  http-server -p 3000
  ```

3. **Truy cập**

Mở trình duyệt: `http://localhost:3000`

## Tính năng

### Authentication

- ✅ **Đăng nhập**: Số điện thoại + Mật khẩu
- ✅ **Đăng ký**: OTP verification
- ✅ **Quên mật khẩu**: Reset via OTP
- ✅ **Phân quyền**: User / Driver roles

### API Integration

Tất cả các chức năng đã được tích hợp với Backend API:

- Send OTP
- Verify OTP
- Register
- Login
- Reset Password

### Local Storage

- `shipway_token`: JWT token
- `shipway_user`: User data

## Environment Variables

Cấu hình trong `config/env.js`:

```javascript
{
  BASE_URL: 'http://localhost:5000/api',  // Backend API
  TIMEOUT: 30000,                         // Request timeout
  ENDPOINTS: { ... }                      // API endpoints
}
```

## Build cho Production

### Option 1: Serve tĩnh

Upload tất cả files lên web server (Nginx, Apache, etc.)

**Nginx config:**

```nginx
server {
    listen 80;
    server_name shipway.vn;
    root /var/www/shipway/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Option 2: Netlify / Vercel

```bash
# netlify.toml
[build]
  publish = "frontend"
  command = "echo 'No build needed'"
```

Deploy:
```bash
netlify deploy --prod
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Copyright © 2025 Shipway Transportation Company

