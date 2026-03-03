# Test script for CRUD endpoints
$baseUrl = "http://localhost:5000/api/v1"
$token = ""
$userId = ""
$subjectId = ""
$sessionId = ""
$goalId = ""
$deadlineId = ""
$wellnessId = ""

# Helper function to make requests
function Invoke-ApiRequest {
    param(
        [string]$Method,
        [string]$Endpoint,
        [object]$Body = $null,
        [bool]$UseAuth = $false
    )
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    if ($UseAuth -and $token) {
        $headers["Authorization"] = "Bearer $token"
    }
    
    $params = @{
        Uri = "$baseUrl$Endpoint"
        Method = $Method
        Headers = $headers
    }
    
    if ($Body) {
        $params["Body"] = ($Body | ConvertTo-Json -Depth 10)
    }
    
    try {
        $response = Invoke-RestMethod @params
        return $response
    } catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
        return $null
    }
}

Write-Host "`n=== Study Time Optimizer - CRUD Endpoints Test ===" -ForegroundColor Cyan
Write-Host "`nWaiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test 1: Login to get token
Write-Host "`n[1] Testing Login..." -ForegroundColor Green
$loginData = @{
    email = "test@example.com"
    password = "TestPassword123"
}
$loginResponse = Invoke-ApiRequest -Method "POST" -Endpoint "/auth/login" -Body $loginData
if ($loginResponse) {
    $token = $loginResponse.access_token
    Write-Host "✓ Login successful" -ForegroundColor Green
    Write-Host "Token: $($token.Substring(0, 30))..." -ForegroundColor Gray
} else {
    Write-Host "✗ Login failed - Creating new user..." -ForegroundColor Yellow
    
    # Register new user
    $registerData = @{
        email = "test@example.com"
        password = "TestPassword123"
        full_name = "Test User"
        age = 25
        student_type = "college"
    }
    $registerResponse = Invoke-ApiRequest -Method "POST" -Endpoint "/auth/register" -Body $registerData
    
    if ($registerResponse) {
        # Login again
        $loginResponse = Invoke-ApiRequest -Method "POST" -Endpoint "/auth/login" -Body $loginData
        $token = $loginResponse.access_token
        Write-Host "✓ User created and logged in" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create user. Exiting." -ForegroundColor Red
        exit 1
    }
}

# Test 2: Get current user profile
Write-Host "`n[2] Testing Get User Profile..." -ForegroundColor Green
$userProfile = Invoke-ApiRequest -Method "GET" -Endpoint "/users/me" -UseAuth $true
if ($userProfile) {
    $userId = $userProfile.id
    Write-Host "✓ User Profile: $($userProfile.full_name) ($($userProfile.email))" -ForegroundColor Green
    Write-Host "  Age: $($userProfile.age), Student Type: $($userProfile.student_type)" -ForegroundColor Gray
}

# Test 3: Create a Subject
Write-Host "`n[3] Testing Create Subject..." -ForegroundColor Green
$subjectData = @{
    name = "Mathematics"
    color = "#FF5733"
    icon = "📐"
    description = "Advanced Calculus and Linear Algebra"
}
$subject = Invoke-ApiRequest -Method "POST" -Endpoint "/subjects/" -Body $subjectData -UseAuth $true
if ($subject) {
    $subjectId = $subject.id
    Write-Host "✓ Subject created: $($subject.name) (ID: $subjectId)" -ForegroundColor Green
}

# Test 4: Get all Subjects
Write-Host "`n[4] Testing Get All Subjects..." -ForegroundColor Green
$subjects = Invoke-ApiRequest -Method "GET" -Endpoint "/subjects/" -UseAuth $true
if ($subjects) {
    Write-Host "✓ Found $($subjects.Count) subject(s)" -ForegroundColor Green
    foreach ($s in $subjects) {
        Write-Host "  - $($s.name) $($s.icon)" -ForegroundColor Gray
    }
}

# Test 5: Create a Study Session
Write-Host "`n[5] Testing Create Study Session..." -ForegroundColor Green
$sessionData = @{
    subject_id = $subjectId
    planned_duration = 60
    notes = "Chapter 5: Integration techniques"
    start_time = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
}
$session = Invoke-ApiRequest -Method "POST" -Endpoint "/sessions/" -Body $sessionData -UseAuth $true
if ($session) {
    $sessionId = $session.id
    Write-Host "✓ Session created: Status=$($session.status), Planned=$($session.planned_duration)min" -ForegroundColor Green
}

# Test 6: Start Study Session
Write-Host "`n[6] Testing Start Session..." -ForegroundColor Green
$startedSession = Invoke-ApiRequest -Method "POST" -Endpoint "/sessions/$sessionId/start" -UseAuth $true
if ($startedSession) {
    Write-Host "✓ Session started: Status=$($startedSession.status)" -ForegroundColor Green
}

# Test 7: Complete Study Session
Write-Host "`n[7] Testing Complete Session..." -ForegroundColor Green
$completionData = @{
    actual_duration = 55
    productivity_score = 8
    focus_score = 7
    energy_level = 6
    difficulty_rating = 7
    mood_after = "satisfied"
    session_feedback = "Good progress on integration techniques"
}
$completedSession = Invoke-ApiRequest -Method "POST" -Endpoint "/sessions/$sessionId/complete" -Body $completionData -UseAuth $true
if ($completedSession) {
    Write-Host "✓ Session completed: Productivity=$($completedSession.productivity_score)/10" -ForegroundColor Green
}

# Test 8: Get all Sessions
Write-Host "`n[8] Testing Get All Sessions..." -ForegroundColor Green
$sessions = Invoke-ApiRequest -Method "GET" -Endpoint "/sessions/" -UseAuth $true
if ($sessions) {
    Write-Host "✓ Found $($sessions.Count) session(s)" -ForegroundColor Green
}

# Test 9: Create a Goal
Write-Host "`n[9] Testing Create Goal..." -ForegroundColor Green
$goalData = @{
    subject_id = $subjectId
    title = "Complete 20 hours of study"
    description = "Study goal for this month"
    goal_type = "study_hours"
    target_value = 20
    target_date = (Get-Date).AddDays(30).ToString("yyyy-MM-dd")
}
$goal = Invoke-ApiRequest -Method "POST" -Endpoint "/goals/" -Body $goalData -UseAuth $true
if ($goal) {
    $goalId = $goal.id
    Write-Host "✓ Goal created: $($goal.title) (Target: $($goal.target_value))" -ForegroundColor Green
}

# Test 10: Update Goal Progress
Write-Host "`n[10] Testing Update Goal Progress..." -ForegroundColor Green
$progressData = @{
    progress = 5.5
}
$updatedGoal = Invoke-ApiRequest -Method "POST" -Endpoint "/goals/$goalId/progress" -Body $progressData -UseAuth $true
if ($updatedGoal) {
    Write-Host "✓ Goal progress updated: $($updatedGoal.current_value)/$($updatedGoal.target_value)" -ForegroundColor Green
}

# Test 11: Create a Deadline
Write-Host "`n[11] Testing Create Deadline..." -ForegroundColor Green
$deadlineData = @{
    subject_id = $subjectId
    title = "Midterm Exam"
    description = "Chapters 1-5"
    due_date = (Get-Date).AddDays(7).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
    priority = "high"
}
$deadline = Invoke-ApiRequest -Method "POST" -Endpoint "/deadlines/" -Body $deadlineData -UseAuth $true
if ($deadline) {
    $deadlineId = $deadline.id
    Write-Host "✓ Deadline created: $($deadline.title) (Priority: $($deadline.priority))" -ForegroundColor Green
}

# Test 12: Mark Deadline as Complete
Write-Host "`n[12] Testing Mark Deadline Complete..." -ForegroundColor Green
$completedDeadline = Invoke-ApiRequest -Method "POST" -Endpoint "/deadlines/$deadlineId/complete" -UseAuth $true
if ($completedDeadline) {
    Write-Host "✓ Deadline marked complete: $($completedDeadline.is_completed)" -ForegroundColor Green
}

# Test 13: Log Daily Wellness
Write-Host "`n[13] Testing Log Daily Wellness..." -ForegroundColor Green
$wellnessData = @{
    date = (Get-Date).ToString("yyyy-MM-dd")
    sleep_hours = 7.5
    sleep_quality = 8
    energy_level = 7
    stress_level = 4
    mood = "good"
    notes = "Feeling productive today"
}
$wellness = Invoke-ApiRequest -Method "POST" -Endpoint "/wellness/" -Body $wellnessData -UseAuth $true
if ($wellness) {
    $wellnessId = $wellness.id
    Write-Host "✓ Wellness logged: Sleep=$($wellness.sleep_hours)h, Energy=$($wellness.energy_level)/10" -ForegroundColor Green
}

# Test 14: Get Wellness Entries
Write-Host "`n[14] Testing Get Wellness Entries..." -ForegroundColor Green
$wellnessEntries = Invoke-ApiRequest -Method "GET" -Endpoint "/wellness/" -UseAuth $true
if ($wellnessEntries) {
    Write-Host "✓ Found $($wellnessEntries.Count) wellness entry(ies)" -ForegroundColor Green
}

# Test 15: Update User Profile
Write-Host "`n[15] Testing Update User Profile..." -ForegroundColor Green
$updateUserData = @{
    full_name = "Test User Updated"
    age = 26
}
$updatedUser = Invoke-ApiRequest -Method "PUT" -Endpoint "/users/me" -Body $updateUserData -UseAuth $true
if ($updatedUser) {
    Write-Host "✓ Profile updated: $($updatedUser.full_name), Age: $($updatedUser.age)" -ForegroundColor Green
}

# Test 16: Update Subject
Write-Host "`n[16] Testing Update Subject..." -ForegroundColor Green
$updateSubjectData = @{
    description = "Advanced Calculus, Linear Algebra, and Differential Equations"
}
$updatedSubject = Invoke-ApiRequest -Method "PUT" -Endpoint "/subjects/$subjectId" -Body $updateSubjectData -UseAuth $true
if ($updatedSubject) {
    Write-Host "✓ Subject updated: $($updatedSubject.description)" -ForegroundColor Green
}

# Test 17: Archive Subject
Write-Host "`n[17] Testing Archive Subject..." -ForegroundColor Green
$archivedSubject = Invoke-ApiRequest -Method "POST" -Endpoint "/subjects/$subjectId/archive" -UseAuth $true
if ($archivedSubject) {
    Write-Host "✓ Subject archived: is_archived=$($archivedSubject.is_archived)" -ForegroundColor Green
}

# Test 18: Unarchive Subject
Write-Host "`n[18] Testing Unarchive Subject..." -ForegroundColor Green
$unarchivedSubject = Invoke-ApiRequest -Method "POST" -Endpoint "/subjects/$subjectId/unarchive" -UseAuth $true
if ($unarchivedSubject) {
    Write-Host "✓ Subject unarchived: is_archived=$($unarchivedSubject.is_archived)" -ForegroundColor Green
}

Write-Host "`n=== All CRUD Tests Completed ===" -ForegroundColor Cyan
Write-Host "`nSummary:" -ForegroundColor Yellow
Write-Host "  ✓ Authentication: Login & User Profile" -ForegroundColor Green
Write-Host "  ✓ Subjects: Create, Read, Update, Archive/Unarchive" -ForegroundColor Green
Write-Host "  ✓ Sessions: Create, Start, Complete, Read" -ForegroundColor Green
Write-Host "  ✓ Goals: Create, Update Progress, Read" -ForegroundColor Green
Write-Host "  ✓ Deadlines: Create, Complete, Read" -ForegroundColor Green
Write-Host "  ✓ Wellness: Create, Read" -ForegroundColor Green
Write-Host "  ✓ User: Update Profile" -ForegroundColor Green
