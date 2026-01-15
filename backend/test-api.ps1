# PowerShell script to test Shipway API

$BASE_URL = "http://localhost:8000/api/v1"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  SHIPWAY API TEST SUITE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "[TEST 1] Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 2: Send OTP
Write-Host "[TEST 2] Send OTP..." -ForegroundColor Yellow
$phone = "+84" + (Get-Random -Minimum 100000000 -Maximum 999999999)
Write-Host "Phone: $phone" -ForegroundColor Gray

$body = @{
    phone = $phone
    purpose = "register"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/send-otp" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    # Save OTP for later use
    $global:otp = $response.otp
    Write-Host "OTP saved: $global:otp" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 3: Verify OTP
Write-Host "[TEST 3] Verify OTP..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    otp = $global:otp
    purpose = "register"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/verify-otp" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 4: Register
Write-Host "[TEST 4] Register User..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    name = "Test User $(Get-Random -Minimum 1 -Maximum 1000)"
    password = "123456"
    otp = $global:otp
    role = "user"
    email = "test$(Get-Random -Minimum 1 -Maximum 1000)@example.com"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/register" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    # Save token for later use
    $global:token = $response.token
    $global:user_id = $response.user._id
    Write-Host "Token saved" -ForegroundColor Gray
    Write-Host "User ID: $global:user_id" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 5: Login
Write-Host "[TEST 5] Login..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    password = "123456"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/login" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    # Update token
    $global:token = $response.token
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 6: Get Current User (Protected)
Write-Host "[TEST 6] Get Current User (Protected)..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $global:token"
}

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/me" -Method Get -Headers $headers
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 7: Update Profile (Protected)
Write-Host "[TEST 7] Update Profile (Protected)..." -ForegroundColor Yellow

$body = @{
    name = "Updated Test User"
    email = "updated@example.com"
    avatar = "https://example.com/avatar.jpg"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/user/profile" -Method Put -Body $body -Headers $headers -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 8: Get User Profile by ID (Protected)
Write-Host "[TEST 8] Get User Profile by ID (Protected)..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/user/profile/$global:user_id" -Method Get -Headers $headers
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 9: Send OTP for Reset Password
Write-Host "[TEST 9] Send OTP for Reset Password..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    purpose = "reset-password"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/send-otp" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    # Save OTP for reset password
    $global:reset_otp = $response.otp
    Write-Host "Reset OTP saved: $global:reset_otp" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 10: Reset Password
Write-Host "[TEST 10] Reset Password..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    otp = $global:reset_otp
    new_password = "newpass123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/reset-password" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

# Test 11: Login with New Password
Write-Host "[TEST 11] Login with New Password..." -ForegroundColor Yellow

$body = @{
    phone = $phone
    password = "newpass123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/auth/login" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ SUCCESS:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
} catch {
    Write-Host "❌ FAILED:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  ALL TESTS COMPLETED!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test Phone: $phone" -ForegroundColor Gray
Write-Host "Latest Token: $global:token" -ForegroundColor Gray
Write-Host ""
Write-Host "Swagger UI: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "ReDoc: http://localhost:8000/redoc" -ForegroundColor Green
