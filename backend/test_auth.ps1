# Test Authentication System
# This script tests all authentication endpoints

$baseUrl = "http://localhost:5000/api/v1/auth"

Write-Host "`n=== Testing Authentication System ===" -ForegroundColor Cyan

# Test 1: Register a new user
Write-Host "`n[1] Testing User Registration..." -ForegroundColor Yellow
$registerData = @{
    email = "test@example.com"
    password = "TestPassword123"
    full_name = "Test User"
    age = 22
    student_type = "college"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "$baseUrl/register" -Method Post -Body $registerData -ContentType "application/json"
    Write-Host "✅ Registration successful!" -ForegroundColor Green
    Write-Host "User ID: $($registerResponse.id)" -ForegroundColor Gray
    Write-Host "Email: $($registerResponse.email)" -ForegroundColor Gray
    Write-Host "Is Verified: $($registerResponse.is_verified)" -ForegroundColor Gray
} catch {
    $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "❌ Registration failed: $($errorDetail.detail)" -ForegroundColor Red
    if ($errorDetail.detail -eq "Email already registered") {
        Write-Host "   (This is expected if you've run the test before)" -ForegroundColor Gray
    }
}

# Test 2: Login
Write-Host "`n[2] Testing Login..." -ForegroundColor Yellow
$loginData = @{
    email = "test@example.com"
    password = "TestPassword123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "✅ Login successful!" -ForegroundColor Green
    Write-Host "Access Token: $($loginResponse.access_token.Substring(0,20))..." -ForegroundColor Gray
    Write-Host "Refresh Token: $($loginResponse.refresh_token.Substring(0,20))..." -ForegroundColor Gray
    Write-Host "Expires In: $($loginResponse.expires_in) seconds" -ForegroundColor Gray
    
    $accessToken = $loginResponse.access_token
    $refreshToken = $loginResponse.refresh_token
} catch {
    $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "❌ Login failed: $($errorDetail.detail)" -ForegroundColor Red
    exit 1
}

# Test 3: Get current user info (protected endpoint)
Write-Host "`n[3] Testing Protected Endpoint (Get Current User)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    $userResponse = Invoke-RestMethod -Uri "$baseUrl/me" -Method Get -Headers $headers
    Write-Host "✅ Protected endpoint accessible!" -ForegroundColor Green
    Write-Host "User: $($userResponse.full_name) ($($userResponse.email))" -ForegroundColor Gray
    Write-Host "Student Type: $($userResponse.student_type)" -ForegroundColor Gray
    Write-Host "Age: $($userResponse.age)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Failed to access protected endpoint" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Test 4: Refresh Token
Write-Host "`n[4] Testing Token Refresh..." -ForegroundColor Yellow
$refreshData = @{
    refresh_token = $refreshToken
} | ConvertTo-Json

try {
    $refreshResponse = Invoke-RestMethod -Uri "$baseUrl/refresh" -Method Post -Body $refreshData -ContentType "application/json"
    Write-Host "✅ Token refresh successful!" -ForegroundColor Green
    Write-Host "New Access Token: $($refreshResponse.access_token.Substring(0,20))..." -ForegroundColor Gray
    Write-Host "New Refresh Token: $($refreshResponse.refresh_token.Substring(0,20))..." -ForegroundColor Gray
} catch {
    Write-Host "❌ Token refresh failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Test 5: Request Password Reset
Write-Host "`n[5] Testing Password Reset Request..." -ForegroundColor Yellow
$resetRequestData = @{
    email = "test@example.com"
} | ConvertTo-Json

try {
    $resetRequestResponse = Invoke-RestMethod -Uri "$baseUrl/request-password-reset" -Method Post -Body $resetRequestData -ContentType "application/json"
    Write-Host "✅ Password reset request sent!" -ForegroundColor Green
    Write-Host "$($resetRequestResponse.message)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Password reset request failed" -ForegroundColor Red
}

# Test 6: Invalid Login (wrong password)
Write-Host "`n[6] Testing Invalid Login (Wrong Password)..." -ForegroundColor Yellow
$invalidLoginData = @{
    email = "test@example.com"
    password = "WrongPassword123"
} | ConvertTo-Json

try {
    $invalidResponse = Invoke-RestMethod -Uri "$baseUrl/login" -Method Post -Body $invalidLoginData -ContentType "application/json"
    Write-Host "❌ Should have failed but didn't!" -ForegroundColor Red
} catch {
    $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "✅ Correctly rejected invalid credentials!" -ForegroundColor Green
    Write-Host "Error: $($errorDetail.detail)" -ForegroundColor Gray
}

# Test 7: Access protected endpoint without token
Write-Host "`n[7] Testing Protected Endpoint Without Token..." -ForegroundColor Yellow
try {
    $noAuthResponse = Invoke-RestMethod -Uri "$baseUrl/me" -Method Get
    Write-Host "❌ Should have failed but didn't!" -ForegroundColor Red
} catch {
    Write-Host "✅ Correctly rejected request without token!" -ForegroundColor Green
}

# Test 8: Logout
Write-Host "`n[8] Testing Logout..." -ForegroundColor Yellow
$logoutData = @{
    refresh_token = $refreshToken
} | ConvertTo-Json

try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    $logoutResponse = Invoke-RestMethod -Uri "$baseUrl/logout" -Method Post -Body $logoutData -ContentType "application/json" -Headers $headers
    Write-Host "✅ Logout successful!" -ForegroundColor Green
    Write-Host "$($logoutResponse.message)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Logout failed" -ForegroundColor Red
}

Write-Host "`n=== Authentication Tests Complete ===" -ForegroundColor Cyan
Write-Host "`nNote: Check backend terminal for verification/reset token links (dev mode)" -ForegroundColor Yellow
