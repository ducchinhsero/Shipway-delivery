#!/usr/bin/env python3
"""
Script kiểm tra xem project đã sẵn sàng deploy chưa
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Kiểm tra file .env"""
    print("[*] Checking .env file...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("[X] File .env khong ton tai!")
        print("   Tạo file .env từ .env.example")
        return False
    
    # Check required variables
    required_vars = [
        "MONGO_URI",
        "SECRET_KEY",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN"
    ]
    
    with open(env_path) as f:
        content = f.read()
        
    missing = []
    for var in required_vars:
        if var not in content:
            missing.append(var)
    
    if missing:
        print(f"[X] Thieu cac bien: {', '.join(missing)}")
        return False
    
    # Check for placeholder values
    if "your-super-secret-key" in content:
        print("[X] SECRET_KEY van la placeholder!")
        print("   Generate new: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
        return False
    
    if "your_user:your_password" in content:
        print("[X] MONGO_URI van la placeholder!")
        return False
    
    print("[OK] File .env OK")
    return True


def check_requirements():
    """Kiểm tra dependencies"""
    print("\n[*] Checking requirements.txt...")
    req_path = Path("requirements.txt")
    
    if not req_path.exists():
        print("[X] File requirements.txt khong ton tai!")
        return False
    
    print("[OK] requirements.txt OK")
    return True


def check_structure():
    """Kiểm tra cấu trúc project"""
    print("\n[*] Checking project structure...")
    
    required_paths = [
        "app/main.py",
        "app/core/config.py",
        "app/core/security.py",
        "app/db/session.py",
        "app/db/models.py",
        "app/api/v1/auth.py",
        "app/api/v1/user.py",
        "run.py"
    ]
    
    missing = []
    for path in required_paths:
        if not Path(path).exists():
            missing.append(path)
    
    if missing:
        print(f"[X] Thieu cac file: {', '.join(missing)}")
        return False
    
    print("[OK] Project structure OK")
    return True


def check_gitignore():
    """Kiểm tra .gitignore"""
    print("\n[*] Checking .gitignore...")
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print("[!] File .gitignore khong ton tai!")
        return True  # Warning only
    
    with open(gitignore_path) as f:
        content = f.read()
    
    if ".env" not in content:
        print("[!] .env chua co trong .gitignore!")
        print("   Them .env vao .gitignore de khong commit sensitive data")
        return True
    
    print("[OK] .gitignore OK")
    return True


def check_migration_scripts():
    """Kiểm tra migration scripts"""
    print("\n[*] Checking migration scripts...")
    script_path = Path("scripts/migrate_add_plan_credit.py")
    
    if not script_path.exists():
        print("[!] Migration script khong ton tai")
        print("   Tao file scripts/migrate_add_plan_credit.py")
        return True  # Warning only
    
    print("[OK] Migration scripts OK")
    return True


def main():
    """Main function"""
    print("=" * 60)
    print("DEPLOYMENT READINESS CHECK")
    print("=" * 60)
    
    checks = [
        check_structure(),
        check_requirements(),
        check_env_file(),
        check_gitignore(),
        check_migration_scripts()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("[OK] DA SAN SANG DEPLOY!")
        print("\nNext steps:")
        print("1. Commit code to Git (neu chua)")
        print("2. Push to GitHub")
        print("3. Follow DEPLOYMENT_STEP_BY_STEP.md")
        print("4. SSH to server va clone repo")
        print("5. Follow deployment guide")
        return 0
    else:
        print("[X] CHUA SAN SANG DEPLOY!")
        print("\nVui long fix cac issues ben tren truoc khi deploy.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
