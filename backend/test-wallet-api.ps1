# Test Wallet & Payment API
# PowerShell script to test all wallet endpoints

$BASE_URL = "http://localhost:8000/api/v1"
$TEST_PHONE = "+84987654321"
$TEST_PASSWORD = "Test@123"
$TEST_NAME = "Wallet Test User"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  WALLET & PAYMENT API TEST" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Green

# Helper function to make HTTP requests
function Invoke-ApiRequest {
    param(
        [string]$Method,
        [string]$Endpoint,
        [object]$Body,
        [string]$Token
    )
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    if ($Token) {
        $headers["Authorization"] = "Bearer $Token"
    }
    
    $params = @{
        Method = $Method
        Uri = "$BASE_URL$Endpoint"
        Headers = $headers
    }
    
    if ($Body) {
        $params["Body"] = ($Body | ConvertTo-Json -Depth 10)
    }
    
    try {
        $response = Invoke-RestMethod @params
        return $response
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json
        return @{
            error = $true
            status = $statusCode
            message = $errorBody
        }
    }
}

# Test 1: Send OTP
Write-Host "[TEST 1] Send OTP for Registration" -ForegroundColor Yellow
$otpResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/send-otp" -Body @{
    phone = $TEST_PHONE
    purpose = "register"
}

if ($otpResponse.success) {
    Write-Host "  ✓ OTP sent successfully" -ForegroundColor Green
    Write-Host "  OTP Code: $($otpResponse.otp)" -ForegroundColor Cyan
    $OTP_CODE = $otpResponse.otp
} else {
    Write-Host "  ✗ Failed to send OTP" -ForegroundColor Red
    Write-Host "  Error: $($otpResponse.message)" -ForegroundColor Red
    exit 1
}

# Test 2: Register User
Write-Host "`n[TEST 2] Register New User" -ForegroundColor Yellow
$registerResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/register" -Body @{
    phone = $TEST_PHONE
    name = $TEST_NAME
    password = $TEST_PASSWORD
    role = "user"
    otp = $OTP_CODE
}

if ($registerResponse.success) {
    Write-Host "  ✓ User registered successfully" -ForegroundColor Green
    $TOKEN = $registerResponse.access_token
} else {
    # User might already exist, try login
    Write-Host "  ⚠ Registration failed, trying login..." -ForegroundColor Yellow
    
    $loginResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/login" -Body @{
        username = $TEST_PHONE
        password = $TEST_PASSWORD
    }
    
    if ($loginResponse.access_token) {
        Write-Host "  ✓ Login successful" -ForegroundColor Green
        $TOKEN = $loginResponse.access_token
    } else {
        Write-Host "  ✗ Failed to login" -ForegroundColor Red
        exit 1
    }
}

Write-Host "  Token: $($TOKEN.Substring(0, 20))..." -ForegroundColor Cyan

# Test 3: Get Wallet Info
Write-Host "`n[TEST 3] Get Wallet Info" -ForegroundColor Yellow
$walletResponse = Invoke-ApiRequest -Method GET -Endpoint "/wallet" -Token $TOKEN

if ($walletResponse.success) {
    Write-Host "  ✓ Wallet info retrieved" -ForegroundColor Green
    Write-Host "  Balance: $($walletResponse.wallet.balance) VND" -ForegroundColor Cyan
    Write-Host "  Total Top-up: $($walletResponse.wallet.total_topup) VND" -ForegroundColor Cyan
    Write-Host "  Total Usage: $($walletResponse.wallet.total_usage) VND" -ForegroundColor Cyan
    Write-Host "  Pending Transactions: $($walletResponse.wallet.pending_transactions)" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Failed to get wallet info" -ForegroundColor Red
}

# Test 4: Create Top-Up Request (QR Code)
Write-Host "`n[TEST 4] Create Top-Up Request (QR Code)" -ForegroundColor Yellow
$topupResponse = Invoke-ApiRequest -Method POST -Endpoint "/wallet/topup" -Token $TOKEN -Body @{
    amount = 100000
    payment_method = "qr"
}

if ($topupResponse.success) {
    Write-Host "  ✓ Top-up request created" -ForegroundColor Green
    Write-Host "  Transaction ID: $($topupResponse.transaction_id)" -ForegroundColor Cyan
    Write-Host "  Payment ID: $($topupResponse.payment_id)" -ForegroundColor Cyan
    Write-Host "  Amount: $($topupResponse.amount) VND" -ForegroundColor Cyan
    Write-Host "  Bank: $($topupResponse.bank_info.bank_name)" -ForegroundColor Cyan
    Write-Host "  Account: $($topupResponse.bank_info.account_no)" -ForegroundColor Cyan
    Write-Host "  Content: $($topupResponse.bank_info.content)" -ForegroundColor Cyan
    Write-Host "  QR Code: [Generated]" -ForegroundColor Cyan
    $PAYMENT_ID = $topupResponse.payment_id
} else {
    Write-Host "  ✗ Failed to create top-up request" -ForegroundColor Red
}

# Test 5: Get Transaction History (Before Payment)
Write-Host "`n[TEST 5] Get Transaction History (Before Payment)" -ForegroundColor Yellow
$transactionsResponse = Invoke-ApiRequest -Method GET -Endpoint "/wallet/transactions?limit=5" -Token $TOKEN

if ($transactionsResponse.success) {
    Write-Host "  ✓ Transactions retrieved" -ForegroundColor Green
    Write-Host "  Total: $($transactionsResponse.total)" -ForegroundColor Cyan
    
    foreach ($tx in $transactionsResponse.transactions) {
        $statusColor = if ($tx.status -eq "completed") { "Green" } elseif ($tx.status -eq "pending") { "Yellow" } else { "Red" }
        Write-Host "    - [$($tx.status)] $($tx.type): $($tx.amount) VND - $($tx.description)" -ForegroundColor $statusColor
    }
} else {
    Write-Host "  ✗ Failed to get transactions" -ForegroundColor Red
}

# Test 6: Verify Payment (Simulate)
Write-Host "`n[TEST 6] Verify Payment (Simulate Bank Transfer)" -ForegroundColor Yellow
$verifyResponse = Invoke-ApiRequest -Method POST -Endpoint "/wallet/verify-payment" -Body @{
    payment_id = $PAYMENT_ID
    status = "success"
    transaction_code = "FT" + (Get-Random -Minimum 10000000 -Maximum 99999999)
    payment_time = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
}

if ($verifyResponse.success) {
    Write-Host "  ✓ Payment verified successfully" -ForegroundColor Green
    Write-Host "  New Balance: $($verifyResponse.new_balance) VND" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Payment verification failed" -ForegroundColor Red
    Write-Host "  Message: $($verifyResponse.message)" -ForegroundColor Red
}

# Test 7: Get Wallet Info (After Payment)
Write-Host "`n[TEST 7] Get Wallet Info (After Payment)" -ForegroundColor Yellow
$walletAfterResponse = Invoke-ApiRequest -Method GET -Endpoint "/wallet" -Token $TOKEN

if ($walletAfterResponse.success) {
    Write-Host "  ✓ Wallet info retrieved" -ForegroundColor Green
    Write-Host "  New Balance: $($walletAfterResponse.wallet.balance) VND" -ForegroundColor Green
    Write-Host "  Total Top-up: $($walletAfterResponse.wallet.total_topup) VND" -ForegroundColor Cyan
    Write-Host "  Total Usage: $($walletAfterResponse.wallet.total_usage) VND" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Failed to get wallet info" -ForegroundColor Red
}

# Test 8: Get Transaction History (After Payment)
Write-Host "`n[TEST 8] Get Transaction History (After Payment)" -ForegroundColor Yellow
$transactionsAfterResponse = Invoke-ApiRequest -Method GET -Endpoint "/wallet/transactions?limit=5" -Token $TOKEN

if ($transactionsAfterResponse.success) {
    Write-Host "  ✓ Transactions retrieved" -ForegroundColor Green
    Write-Host "  Total: $($transactionsAfterResponse.total)" -ForegroundColor Cyan
    
    foreach ($tx in $transactionsAfterResponse.transactions) {
        $statusColor = if ($tx.status -eq "completed") { "Green" } elseif ($tx.status -eq "pending") { "Yellow" } else { "Red" }
        Write-Host "    - [$($tx.status)] $($tx.type): $($tx.amount) VND - $($tx.description)" -ForegroundColor $statusColor
    }
} else {
    Write-Host "  ✗ Failed to get transactions" -ForegroundColor Red
}

# Test 9: Test Invalid Amount
Write-Host "`n[TEST 9] Test Invalid Amount (should fail)" -ForegroundColor Yellow
$invalidResponse = Invoke-ApiRequest -Method POST -Endpoint "/wallet/topup" -Token $TOKEN -Body @{
    amount = 15000  # Not multiple of 10,000
    payment_method = "qr"
}

if ($invalidResponse.error) {
    Write-Host "  ✓ Validation error as expected" -ForegroundColor Green
    Write-Host "  Error: Amount must be multiple of 10,000 VND" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Should have failed validation" -ForegroundColor Red
}

# Test 10: Test Different Payment Methods
Write-Host "`n[TEST 10] Test Momo Payment Method" -ForegroundColor Yellow
$momoResponse = Invoke-ApiRequest -Method POST -Endpoint "/wallet/topup" -Token $TOKEN -Body @{
    amount = 200000
    payment_method = "momo"
}

if ($momoResponse.success) {
    Write-Host "  ✓ Momo top-up request created" -ForegroundColor Green
    Write-Host "  Payment URL: $($momoResponse.payment_url)" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Failed to create momo request" -ForegroundColor Red
}

# Summary
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All wallet & payment endpoints tested!" -ForegroundColor Green
Write-Host "  Test User: $TEST_PHONE" -ForegroundColor Cyan
Write-Host "  Final Balance: $($walletAfterResponse.wallet.balance) VND" -ForegroundColor Green
Write-Host "`n  Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Check Swagger UI: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  2. View documentation: WALLET_API_DOCUMENTATION.md" -ForegroundColor White
Write-Host "  3. Test with Postman/Thunder Client" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Green
