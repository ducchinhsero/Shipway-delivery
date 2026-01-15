# 🤝 Contributing to Shipway

Hướng dẫn cho team members về cách setup và contribute vào dự án.

## 📋 Setup cho Team Members

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Setup Backend

```bash
cd backend
npm install

# Tạo file .env từ .env.example
# Windows PowerShell:
Copy-Item .env.example .env

# Mac/Linux:
cp .env.example .env

# Chỉnh sửa .env với MongoDB URI của bạn
notepad .env  # hoặc code .env

# Seed admin account
npm run seed

# Chạy server
npm run dev
```

Backend sẽ chạy tại: http://localhost:5000

### 3. Setup Frontend

```bash
# Mở thư mục frontend
cd frontend

# Sử dụng Live Server (VS Code Extension)
# Hoặc:
python -m http.server 3000
```

Frontend sẽ chạy tại: http://localhost:3000 (hoặc 5500 với Live Server)

## 🔐 Environment Variables

### Backend (.env)

**QUAN TRỌNG**: File `.env` KHÔNG được commit vào Git!

Tạo file `backend/.env` với nội dung:

```env
# MongoDB - Lấy từ MongoDB Atlas của bạn
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/shipway

# JWT Secret - Tạo chuỗi random >= 32 ký tự
JWT_SECRET=your_very_long_secret_key_here_minimum_32_characters

# Server
PORT=5000
NODE_ENV=development

# Frontend
FRONTEND_URL=http://localhost:3000

# Admin mặc định
ADMIN_PHONE=+84391912441
ADMIN_PASSWORD=Admin@123456
```

## 📝 Git Workflow

### Branch Strategy

- `main` - Production code (protected)
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches

### Workflow

1. **Tạo branch mới từ develop**

```bash
git checkout develop
git pull origin develop
git checkout -b feature/ten-tinh-nang
```

2. **Làm việc và commit**

```bash
# Xem thay đổi
git status

# Add files
git add .

# Commit với message rõ ràng
git commit -m "feat: thêm chức năng ABC"
```

3. **Push lên remote**

```bash
git push origin feature/ten-tinh-nang
```

4. **Tạo Pull Request**

- Vào GitHub
- Tạo PR từ `feature/ten-tinh-nang` → `develop`
- Assign reviewer
- Đợi review và merge

### Commit Message Convention

```
<type>: <subject>

[optional body]
```

**Types:**
- `feat`: Tính năng mới
- `fix`: Sửa bug
- `docs`: Cập nhật documentation
- `style`: Format code, không thay đổi logic
- `refactor`: Refactor code
- `test`: Thêm tests
- `chore`: Cập nhật dependencies, config

**Examples:**
```bash
git commit -m "feat: thêm API endpoint đăng ký driver"
git commit -m "fix: sửa lỗi login không hoạt động"
git commit -m "docs: cập nhật README với hướng dẫn setup"
```

## ⚠️ KHÔNG Commit những file này

- ❌ `.env` files
- ❌ `node_modules/`
- ❌ IDE settings (`.vscode/`, `.idea/`)
- ❌ OS files (`.DS_Store`, `Thumbs.db`)
- ❌ Log files (`*.log`)
- ❌ Database files (`*.db`)

File `.gitignore` đã được cấu hình để tự động ignore các files này.

## ✅ PHẢI Commit những file này

- ✅ Source code (`*.js`, `*.html`, `*.css`)
- ✅ `package.json` và `package-lock.json`
- ✅ `.env.example` (template)
- ✅ Documentation (`*.md`)
- ✅ Configuration files (`server.js`, `config/*`)

## 🧪 Testing trước khi Push

```bash
# Chạy backend
cd backend
npm run dev

# Test các API endpoints
curl http://localhost:5000/api/health

# Chạy frontend và test UI
# Login, Register, Reset Password
```

## 🐛 Troubleshooting

### MongoDB Connection Error

```bash
# Kiểm tra MONGODB_URI trong .env
# Kiểm tra IP whitelist trong MongoDB Atlas
# Thử ping cluster
```

### Port đã được sử dụng

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### CORS Error

```bash
# Kiểm tra FRONTEND_URL trong backend/.env
# Restart backend server
```

## 📚 Documentation

- [README.md](README.md) - Tổng quan dự án
- [START_HERE.md](START_HERE.md) - Bắt đầu nhanh
- [QUICKSTART.md](docs/QUICKSTART.md) - Setup 10 phút
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Setup chi tiết
- [BACKEND_DOCUMENTATION.md](docs/BACKEND_DOCUMENTATION.md) - Backend docs
- [API_EXAMPLES.md](docs/API_EXAMPLES.md) - API examples

## 💬 Communication

- **Issues**: Tạo GitHub Issues cho bugs hoặc feature requests
- **Pull Requests**: Code review qua GitHub PRs
- **Questions**: Comment trong Issues hoặc PRs

## 🎯 Best Practices

1. **Luôn pull trước khi bắt đầu làm việc**
   ```bash
   git pull origin develop
   ```

2. **Commit thường xuyên với messages rõ ràng**

3. **Test kỹ trước khi push**

4. **Keep branches nhỏ và tập trung**

5. **Review code của người khác**

6. **Document code khi cần thiết**

7. **Follow coding conventions của dự án**

## 🔒 Security

- **KHÔNG BAO GIỜ** commit file `.env`
- **KHÔNG BAO GIỜ** commit passwords, API keys
- **KHÔNG BAO GIỜ** commit sensitive data
- Use `.env.example` để share configuration template

## 📞 Support

Nếu gặp vấn đề:
1. Check [Troubleshooting](#troubleshooting) section
2. Search trong Issues
3. Tạo Issue mới với:
   - Mô tả vấn đề
   - Steps to reproduce
   - Screenshots/logs
   - Environment info

---

**Happy Coding! 🚀**

