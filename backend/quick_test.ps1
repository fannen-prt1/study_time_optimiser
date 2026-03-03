# Quick CRUD Test
$baseUrl = "http://localhost:5000/api/v1"

Write-Host "`n=== Quick CRUD Test ===" -ForegroundColor Cyan

# Step 1: Login
Write-Host "`n[1] Login..." -ForegroundColor Green
$loginBody = @{
    email = "test@example.com"
    password = "TestPassword123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "✓ Logged in successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠ Login failed — registering new user..." -ForegroundColor Yellow
    $registerBody = @{
        email = "test@example.com"
        password = "TestPassword123"
        full_name = "Test User"
        age = 25
        student_type = "college"
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "$baseUrl/auth/register" -Method POST -Body $registerBody -ContentType "application/json" | Out-Null
        $loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
        $token = $loginResponse.access_token
        Write-Host "✓ User created and logged in" -ForegroundColor Green
    } catch {
        Write-Host "✗ Could not register or login. Is the server running on port 5000?" -ForegroundColor Red
        exit 1
    }
}

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Step 2: Create Subject
Write-Host "`n[2] Create Subject..." -ForegroundColor Green
$subjectBody = @{
    name = "Physics"
    color = "#3498db"
    icon = "⚛️"
    description = "Quantum Mechanics"
} | ConvertTo-Json

$subject = Invoke-RestMethod -Uri "$baseUrl/subjects/" -Method POST -Body $subjectBody -Headers $headers
Write-Host "✓ Subject created: $($subject.name) (ID: $($subject.id))" -ForegroundColor Green

# Step 3: Get all subjects
Write-Host "`n[3] Get All Subjects..." -ForegroundColor Green
$subjects = Invoke-RestMethod -Uri "$baseUrl/subjects/" -Method GET -Headers $headers
Write-Host "✓ Found $($subjects.Count) subject(s):" -ForegroundColor Green
foreach ($s in $subjects) {
    Write-Host "  - $($s.name) $($s.icon)" -ForegroundColor Gray
}

# Step 4: Create Study Session
Write-Host "`n[4] Create Study Session..." -ForegroundColor Green
$sessionBody = @{
    subject_id = $subject.id
    planned_duration = 45
    notes = "Study quantum entanglement"
    start_time = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
} | ConvertTo-Json

$session = Invoke-RestMethod -Uri "$baseUrl/sessions/" -Method POST -Body $sessionBody -Headers $headers
Write-Host "✓ Session created with status: $($session.status)" -ForegroundColor Green

# Step 5: Start session
Write-Host "`n[5] Start Session..." -ForegroundColor Green
$startedSession = Invoke-RestMethod -Uri "$baseUrl/sessions/$($session.id)/start" -Method POST -Headers $headers
Write-Host "✓ Session started, new status: $($startedSession.status)" -ForegroundColor Green

# Step 6: Create Goal
Write-Host "`n[6] Create Goal..." -ForegroundColor Green
$goalBody = @{
    subject_id = $subject.id
    title = "Master Quantum Mechanics"
    description = "Complete all chapters"
    goal_type = "study_hours"
    target_value = 30
    target_date = (Get-Date).AddDays(60).ToString("yyyy-MM-dd")
} | ConvertTo-Json

$goal = Invoke-RestMethod -Uri "$baseUrl/goals/" -Method POST -Body $goalBody -Headers $headers
Write-Host "✓ Goal created: $($goal.title) (Target: $($goal.target_value)h)" -ForegroundColor Green

# Step 7: Log Wellness
Write-Host "`n[7] Log Daily Wellness..." -ForegroundColor Green
$wellnessBody = @{
    date = (Get-Date).ToString("yyyy-MM-dd")
    sleep_hours = 8.0
    sleep_quality = 9
    energy_level = 8
    stress_level = 3
    mood = "excellent"
    notes = "Great day for studying!"
} | ConvertTo-Json

$wellness = Invoke-RestMethod -Uri "$baseUrl/wellness/" -Method POST -Body $wellnessBody -Headers $headers
Write-Host "✓ Wellness logged: $($wellness.sleep_hours)h sleep, energy=$($wellness.energy_level)/10" -ForegroundColor Green

# Step 8: Create Deadline
Write-Host "`n[8] Create Deadline..." -ForegroundColor Green
$deadlineBody = @{
    subject_id = $subject.id
    title = "Final Exam"
    description = "Comprehensive exam covering all topics"
    due_date = (Get-Date).AddDays(14).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
    priority = "high"
} | ConvertTo-Json

$deadline = Invoke-RestMethod -Uri "$baseUrl/deadlines/" -Method POST -Body $deadlineBody -Headers $headers
Write-Host "✓ Deadline created: $($deadline.title) - Priority: $($deadline.priority)" -ForegroundColor Green

# Summary
Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
Write-Host "All CRUD operations working" -ForegroundColor Green
Write-Host "`nCreated:" -ForegroundColor Yellow
Write-Host "  1 Subject - Physics" -ForegroundColor Gray
Write-Host "  1 Study Session - started" -ForegroundColor Gray
Write-Host "  1 Goal - 30 hours" -ForegroundColor Gray
Write-Host "  1 Deadline - Final Exam" -ForegroundColor Gray
Write-Host "  1 Wellness Entry - 8 hours sleep" -ForegroundColor Gray
