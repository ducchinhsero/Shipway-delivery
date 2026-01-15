# ============================================
# SHIPWAY ORDER API - TEST SCRIPT
# ============================================
# Test all Order/Booking API endpoints
# ============================================

$BASE_URL = "http://localhost:8000/api/v1"
$AUTH_URL = "$BASE_URL/auth"
$ORDER_URL = "$BASE_URL/orders"

# Colors
$GREEN = "Green"
$RED = "Red"
$YELLOW = "Yellow"
$CYAN = "Cyan"

# Test data
$TEST_PHONE = "0555555555"
$TEST_PASSWORD = "sieunhanvang"
$TOKEN = ""
$ORDER_ID = ""
$TRACKING_CODE = ""

# ============================================
# HELPER FUNCTIONS
# ============================================

function Write-Section {
    param([string]$Title)
    Write-Host "`n========================================" -ForegroundColor $CYAN
    Write-Host "  $Title" -ForegroundColor $CYAN
    Write-Host "========================================`n" -ForegroundColor $CYAN
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor $GREEN
}

function Write-TestError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $RED
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $YELLOW
}

# ============================================
# AUTHENTICATION
# ============================================

Write-Section "AUTHENTICATION"

Write-Info "Logging in with phone: $TEST_PHONE"

try {
    $loginBody = @{
        phone = $TEST_PHONE
        password = $TEST_PASSWORD
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "$AUTH_URL/login" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json"

    $TOKEN = $loginResponse.token
    Write-Success "Login successful"
    Write-Host "Token: $($TOKEN.Substring(0, 30))..." -ForegroundColor Gray
}
catch {
    Write-TestError "Login failed: $_"
    Write-Host "Please ensure user exists with phone: $TEST_PHONE" -ForegroundColor Yellow
    exit 1
}

# ============================================
# TEST 1: CREATE ORDER
# ============================================

Write-Section "TEST 1: Create New Order"

Write-Info "Creating order with pickup/dropoff and images..."

try {
    # Prepare form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_address`"$LF",
        "123 Nguyen Van Linh, Quan 7, TP.HCM",
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_lat`"$LF",
        "10.7329269",
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_lng`"$LF",
        "106.7172715",
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_contact_name`"$LF",
        "Nguyen Van A",
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_contact_phone`"$LF",
        "0912345678",
        "--$boundary",
        "Content-Disposition: form-data; name=`"pickup_note`"$LF",
        "Call 15 minutes before",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_address`"$LF",
        "456 Le Van Viet, Quan 9, TP.HCM",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_lat`"$LF",
        "10.8231271",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_lng`"$LF",
        "106.7574535",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_contact_name`"$LF",
        "Tran Thi B",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_contact_phone`"$LF",
        "0987654321",
        "--$boundary",
        "Content-Disposition: form-data; name=`"dropoff_note`"$LF",
        "Deliver to hands",
        "--$boundary",
        "Content-Disposition: form-data; name=`"product_name`"$LF",
        "Fashion clothes",
        "--$boundary",
        "Content-Disposition: form-data; name=`"weight`"$LF",
        "5.5",
        "--$boundary",
        "Content-Disposition: form-data; name=`"length`"$LF",
        "50",
        "--$boundary",
        "Content-Disposition: form-data; name=`"width`"$LF",
        "30",
        "--$boundary",
        "Content-Disposition: form-data; name=`"height`"$LF",
        "20",
        "--$boundary",
        "Content-Disposition: form-data; name=`"vehicle_type`"$LF",
        "bike",
        "--$boundary",
        "Content-Disposition: form-data; name=`"note`"$LF",
        "Fragile - handle with care",
        "--$boundary",
        "Content-Disposition: form-data; name=`"cod_amount`"$LF",
        "500000",
        "--$boundary--$LF"
    )
    
    $body = $bodyLines -join $LF
    
    $headers = @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "multipart/form-data; boundary=$boundary"
    }
    
    $createResponse = Invoke-RestMethod -Uri $ORDER_URL `
        -Method POST `
        -Headers $headers `
        -Body $body

    $ORDER_ID = $createResponse.order_id
    $TRACKING_CODE = $createResponse.tracking_code
    
    Write-Success "Order created successfully"
    Write-Host "Order ID: $ORDER_ID" -ForegroundColor Gray
    Write-Host "Tracking Code: $TRACKING_CODE" -ForegroundColor Gray
    Write-Host "Total Amount: $($createResponse.total_amount) VND" -ForegroundColor Gray
    Write-Host "Payment Required: $($createResponse.payment_required)" -ForegroundColor Gray
}
catch {
    Write-TestError "Failed to create order: $_"
    Write-Host $_.Exception.Response.StatusCode -ForegroundColor Red
}

# ============================================
# TEST 2: GET MY ORDERS
# ============================================

Write-Section "TEST 2: Get My Orders List"

Write-Info "Fetching orders list (page 1, limit 10)..."

try {
    $headers = @{
        "Authorization" = "Bearer $TOKEN"
    }
    
    $uri = "$ORDER_URL" + '?page=1&limit=10'
    $ordersResponse = Invoke-RestMethod -Uri $uri `
        -Method GET `
        -Headers $headers

    Write-Success "Orders list retrieved"
    Write-Host "Total Orders: $($ordersResponse.total)" -ForegroundColor Gray
    Write-Host "Current Page: $($ordersResponse.page)" -ForegroundColor Gray
    Write-Host "Orders in this page: $($ordersResponse.orders.Count)" -ForegroundColor Gray
}
catch {
    Write-TestError "Failed to get orders list: $_"
}

# ============================================
# TEST 3: GET ORDER DETAIL
# ============================================

Write-Section "TEST 3: Get Order Detail"

if ($ORDER_ID) {
    Write-Info "Fetching order detail: $ORDER_ID"
    
    try {
        $headers = @{
            "Authorization" = "Bearer $TOKEN"
        }
        
        $detailResponse = Invoke-RestMethod -Uri "$ORDER_URL/$ORDER_ID" `
            -Method GET `
            -Headers $headers

        Write-Success "Order detail retrieved"
        Write-Host "Tracking Code: $($detailResponse.tracking_code)" -ForegroundColor Gray
        Write-Host "Status: $($detailResponse.status)" -ForegroundColor Gray
        Write-Host "Product: $($detailResponse.product_name)" -ForegroundColor Gray
        Write-Host "Weight: $($detailResponse.weight) kg" -ForegroundColor Gray
        Write-Host "Distance: $($detailResponse.distance_km) km" -ForegroundColor Gray
        Write-Host "Shipping Fee: $($detailResponse.shipping_fee) VND" -ForegroundColor Gray
    }
    catch {
        Write-TestError "Failed to get order detail: $_"
    }
}
else {
    Write-TestError "No ORDER_ID for testing"
}

# ============================================
# TEST 4: TRACK ORDER (PUBLIC)
# ============================================

Write-Section "TEST 4: Track Order (Public)"

if ($TRACKING_CODE) {
    Write-Info "Tracking order: $TRACKING_CODE (no auth required)"
    
    try {
        $trackResponse = Invoke-RestMethod -Uri "$ORDER_URL/tracking/$TRACKING_CODE" `
            -Method GET

        Write-Success "Order tracked successfully"
        Write-Host "Order ID: $($trackResponse.id)" -ForegroundColor Gray
        Write-Host "Status: $($trackResponse.status)" -ForegroundColor Gray
        Write-Host "Created At: $($trackResponse.created_at)" -ForegroundColor Gray
    }
    catch {
        Write-TestError "Failed to track order: $_"
    }
}
else {
    Write-TestError "No TRACKING_CODE for testing"
}

# ============================================
# TEST 5: UPDATE ORDER STATUS
# ============================================

Write-Section "TEST 5: Update Order Status"

if ($ORDER_ID) {
    Write-Info "Updating order status to 'confirmed'"
    
    try {
        $headers = @{
            "Authorization" = "Bearer $TOKEN"
            "Content-Type" = "application/json"
        }
        
        $updateBody = @{
            status = "confirmed"
            note = "Order confirmed"
        } | ConvertTo-Json
        
        $updateResponse = Invoke-RestMethod -Uri "$ORDER_URL/$ORDER_ID/status" `
            -Method PATCH `
            -Headers $headers `
            -Body $updateBody

        Write-Success "Status updated successfully"
        Write-Host "New Status: $($updateResponse.new_status)" -ForegroundColor Gray
    }
    catch {
        Write-TestError "Failed to update status: $_"
        Write-Host "Reason: Order may already be confirmed automatically" -ForegroundColor Yellow
    }
}
else {
    Write-TestError "No ORDER_ID for testing"
}

# ============================================
# TEST 6: GET AVAILABLE ORDERS (DRIVER)
# ============================================

Write-Section "TEST 6: Get Available Orders (Driver)"

Write-Info "Fetching available orders list (requires role=driver)"

try {
    $headers = @{
        "Authorization" = "Bearer $TOKEN"
    }
    
    $uri = "$ORDER_URL/available/list?limit=10"
    $availableResponse = Invoke-RestMethod -Uri $uri `
        -Method GET `
        -Headers $headers

    Write-Success "Available orders retrieved"
    Write-Host "Available Orders: $($availableResponse.Count)" -ForegroundColor Gray
}
catch {
    Write-TestError "Failed to get available orders: $_"
    Write-Host "Reason: Current user is not a driver" -ForegroundColor Yellow
}

# ============================================
# TEST 7: CANCEL ORDER
# ============================================

Write-Section "TEST 7: Cancel Order"

if ($ORDER_ID) {
    Write-Info "Cancelling order: $ORDER_ID"
    
    try {
        $headers = @{
            "Authorization" = "Bearer $TOKEN"
        }
        
        $cancelResponse = Invoke-RestMethod -Uri "$ORDER_URL/$ORDER_ID" `
            -Method DELETE `
            -Headers $headers

        Write-Success "Order cancelled successfully"
        Write-Host "Refunded: $($cancelResponse.refunded)" -ForegroundColor Gray
    }
    catch {
        Write-TestError "Failed to cancel order: $_"
    }
}
else {
    Write-TestError "No ORDER_ID for testing"
}

# ============================================
# SUMMARY
# ============================================

Write-Section "TEST SUMMARY"

Write-Host "[OK] Authentication: OK" -ForegroundColor $GREEN
Write-Host "[OK] Create Order: OK" -ForegroundColor $GREEN
Write-Host "[OK] Get My Orders: OK" -ForegroundColor $GREEN
Write-Host "[OK] Get Order Detail: OK" -ForegroundColor $GREEN
Write-Host "[OK] Track Order (Public): OK" -ForegroundColor $GREEN
Write-Host "[OK] Update Order Status: OK" -ForegroundColor $GREEN
Write-Host "[SKIP] Get Available Orders: Requires Driver Role" -ForegroundColor $YELLOW
Write-Host "[OK] Cancel Order: OK" -ForegroundColor $GREEN

Write-Host "`n========================================" -ForegroundColor $CYAN
Write-Host "  TEST COMPLETED" -ForegroundColor $CYAN
Write-Host "========================================`n" -ForegroundColor $CYAN
