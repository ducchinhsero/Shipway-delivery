# ============================================
# CREATE TEST USER FOR ORDER API
# ============================================

$BASE_URL = "http://localhost:8000/api/v1"
$AUTH_URL = "$BASE_URL/auth"

$TEST_PHONE = "0555555555"
$TEST_PASSWORD = "sieunhanvang"
$TEST_NAME = "Sieu Nhan Vang"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CREATING TEST USER" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "[1/2] Sending OTP..." -ForegroundColor Yellow

try {
    $otpBody = @{
        phone = $TEST_PHONE
        purpose = "register"
    } | ConvertTo-Json

    $otpResponse = Invoke-RestMethod -Uri "$AUTH_URL/send-otp" `
        -Method POST `
        -Body $otpBody `
        -ContentType "application/json"

    $OTP = $otpResponse.otp
    Write-Host "    OTP: $OTP" -ForegroundColor Green

    Write-Host "`n[2/2] Registering user (OTP will be verified during registration)..." -ForegroundColor Yellow

    $registerBody = @{
        phone = $TEST_PHONE
        password = $TEST_PASSWORD
        name = $TEST_NAME
        otp = $OTP
        role = "user"
    } | ConvertTo-Json

    $registerResponse = Invoke-RestMethod -Uri "$AUTH_URL/register" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json"

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  USER CREATED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Phone: $TEST_PHONE" -ForegroundColor White
    Write-Host "Password: $TEST_PASSWORD" -ForegroundColor White
    Write-Host "Name: $TEST_NAME" -ForegroundColor White
    Write-Host "`nBan co the chay test-order-api.ps1 bay gio!" -ForegroundColor Cyan
}
catch {
    Write-Host "`n[ERROR] Failed to create user: $_" -ForegroundColor Red
    
    # Kiem tra xem user da ton tai chua
    Write-Host "`nThu dang nhap voi user hien tai..." -ForegroundColor Yellow
    
    try {
        $loginBody = @{
            phone = $TEST_PHONE
            password = $TEST_PASSWORD
        } | ConvertTo-Json

        $loginResponse = Invoke-RestMethod -Uri "$AUTH_URL/login" `
            -Method POST `
            -Body $loginBody `
            -ContentType "application/json"

        Write-Host "`n[SUCCESS] User da ton tai!" -ForegroundColor Green
        Write-Host "Ban co the chay test-order-api.ps1 ngay!" -ForegroundColor Cyan
    }
    catch {
        Write-Host "`n[ERROR] User chua ton tai va khong tao duoc." -ForegroundColor Red
        Write-Host "Vui long tao user thu cong qua Swagger UI: http://localhost:8000/docs" -ForegroundColor Yellow
    }
}
