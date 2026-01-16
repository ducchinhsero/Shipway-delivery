#!/usr/bin/env python3
"""
Generate random secret keys for deployment
Run: python generate-secrets.py
"""
import secrets

print("=" * 60)
print("🔐 GENERATING SECRET KEYS FOR DEPLOYMENT")
print("=" * 60)
print()

secret_key = secrets.token_urlsafe(32)
jwt_secret = secrets.token_urlsafe(32)

print("Copy these values to your Railway/Render environment variables:")
print()
print(f"SECRET_KEY={secret_key}")
print()
print(f"JWT_SECRET={jwt_secret}")
print()
print("=" * 60)
print()
print("⚠️  IMPORTANT:")
print("   - Keep these values SECRET")
print("   - Do NOT commit to Git")
print("   - Use different keys for dev/staging/production")
print()
print("=" * 60)
