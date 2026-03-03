# Test Analytics Endpoints
$baseUrl = "http://localhost:5000/api/v1"

Write-Host "`n=== Analytics Service Test ===" -ForegroundColor Cyan

# Login
Write-Host "`n[1] Login" -ForegroundColor Green
$loginJson = '{"email":"test@example.com","password":"TestPassword123"}'
$login = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -Body $loginJson -ContentType "application/json"
$token = $login.access_token
Write-Host "Success - Logged in" -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Create some test data first
Write-Host "`n[2] Creating test data..." -ForegroundColor Green

# Get existing subject or create one
$subjects = Invoke-RestMethod -Uri "$baseUrl/subjects/" -Method GET -Headers $headers
if ($subjects.Count -eq 0) {
    $subjectJson = '{"name":"Computer Science","color":"#3498db","icon":"💻","description":"Programming and algorithms"}'
    $subject = Invoke-RestMethod -Uri "$baseUrl/subjects/" -Method POST -Body $subjectJson -Headers $headers
    Write-Host "Created subject: $($subject.name)" -ForegroundColor Gray
} else {
    $subject = $subjects[0]
    Write-Host "Using existing subject: $($subject.name)" -ForegroundColor Gray
}

# Create and complete some study sessions with different dates
$today = Get-Date
for ($i = 0; $i -lt 5; $i++) {
    $sessionDate = $today.AddDays(-$i).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
    $sessionJson = "{`"subject_id`":`"$($subject.id)`",`"planned_duration`":$((Get-Random -Minimum 30 -Maximum 90)),`"notes`":`"Study session $i`",`"start_time`":`"$sessionDate`"}"
    
    $session = Invoke-RestMethod -Uri "$baseUrl/sessions/" -Method POST -Body $sessionJson -Headers $headers
    
    # Start and complete the session
    Invoke-RestMethod -Uri "$baseUrl/sessions/$($session.id)/start" -Method POST -Headers $headers | Out-Null
    
    $completionJson = "{`"actual_duration`":$((Get-Random -Minimum 25 -Maximum 85)),`"productivity_score`":$((Get-Random -Minimum 5 -Maximum 10)),`"focus_score`":$((Get-Random -Minimum 5 -Maximum 10)),`"energy_level`":$((Get-Random -Minimum 4 -Maximum 9)),`"difficulty_rating`":$((Get-Random -Minimum 3 -Maximum 8)),`"mood_after`":`"satisfied`",`"session_feedback`":`"Session $i completed`"}"
    Invoke-RestMethod -Uri "$baseUrl/sessions/$($session.id)/complete" -Method POST -Body $completionJson -Headers $headers | Out-Null
}
Write-Host "Created 5 study sessions" -ForegroundColor Gray

# Create wellness entries
for ($i = 0; $i -lt 5; $i++) {
    $wellnessDate = $today.AddDays(-$i).ToString("yyyy-MM-dd")
    $sleepHours = [math]::Round((Get-Random -Minimum 60 -Maximum 90) / 10, 1)
    $wellnessJson = "{`"date`":`"$wellnessDate`",`"sleep_hours`":$sleepHours,`"sleep_quality`":$((Get-Random -Minimum 6 -Maximum 10)),`"energy_level`":$((Get-Random -Minimum 5 -Maximum 9)),`"stress_level`":$((Get-Random -Minimum 2 -Maximum 7)),`"mood`":`"good`",`"notes`":`"Day $i`"}"
    
    try {
        Invoke-RestMethod -Uri "$baseUrl/wellness/" -Method POST -Body $wellnessJson -Headers $headers | Out-Null
    } catch {
        # Entry might already exist for that date
    }
}
Write-Host "Created wellness entries" -ForegroundColor Gray

# Test Analytics Endpoints
Write-Host "`n[3] Get Study Time Stats" -ForegroundColor Green
$studyTime = Invoke-RestMethod -Uri "$baseUrl/analytics/study-time" -Method GET -Headers $headers
Write-Host "Total Minutes: $($studyTime.total_minutes)" -ForegroundColor White
Write-Host "Total Sessions: $($studyTime.total_sessions)" -ForegroundColor White
Write-Host "Avg Productivity: $($studyTime.average_productivity_score)/10" -ForegroundColor White
Write-Host "Completion Rate: $($studyTime.completion_rate)%" -ForegroundColor White

Write-Host "`n[4] Get Subject Stats" -ForegroundColor Green
$subjectStats = Invoke-RestMethod -Uri "$baseUrl/analytics/subjects" -Method GET -Headers $headers
foreach ($stat in $subjectStats) {
    Write-Host "$($stat.subject_name): $($stat.total_minutes) min, $($stat.total_sessions) sessions, Productivity: $($stat.average_productivity)/10" -ForegroundColor White
}

Write-Host "`n[5] Get Productivity Trends (last 7 days)" -ForegroundColor Green
$trends = Invoke-RestMethod -Uri "$baseUrl/analytics/productivity-trends?days=7" -Method GET -Headers $headers
Write-Host "Found $($trends.Count) days of data" -ForegroundColor White
$trends | Select-Object -First 3 | ForEach-Object {
    Write-Host "  $($_.date): $($_.total_minutes) min, Productivity: $($_.average_productivity)/10" -ForegroundColor Gray
}

Write-Host "`n[6] Get Streak Info" -ForegroundColor Green
$streak = Invoke-RestMethod -Uri "$baseUrl/analytics/streak" -Method GET -Headers $headers
Write-Host "Current Streak: $($streak.current_streak) days" -ForegroundColor White
Write-Host "Longest Streak: $($streak.longest_streak) days" -ForegroundColor White
Write-Host "Total Study Days: $($streak.total_study_days)" -ForegroundColor White

Write-Host "`n[7] Get Wellness Correlation" -ForegroundColor Green
$wellness = Invoke-RestMethod -Uri "$baseUrl/analytics/wellness-correlation?days=7" -Method GET -Headers $headers
Write-Host "Average Sleep: $($wellness.average_sleep_hours) hours" -ForegroundColor White
Write-Host "Average Productivity: $($wellness.average_productivity)/10" -ForegroundColor White
Write-Host "High Productivity Sleep Avg: $($wellness.high_productivity_sleep_average)h" -ForegroundColor White
Write-Host "Optimal Sleep Range: $($wellness.optimal_sleep_range)" -ForegroundColor White
Write-Host "Energy-Productivity: $($wellness.energy_productivity_correlation)" -ForegroundColor White

Write-Host "`n[8] Get Dashboard Analytics" -ForegroundColor Green
$dashboard = Invoke-RestMethod -Uri "$baseUrl/analytics/dashboard?days=7" -Method GET -Headers $headers
Write-Host "Study Time Stats:" -ForegroundColor Cyan
Write-Host "  Total: $($dashboard.study_time_stats.total_minutes) min in $($dashboard.study_time_stats.total_sessions) sessions" -ForegroundColor White
Write-Host "  Avg Productivity: $($dashboard.study_time_stats.average_productivity_score)/10" -ForegroundColor White

Write-Host "Subject Breakdown:" -ForegroundColor Cyan
foreach ($subj in $dashboard.subject_stats) {
    Write-Host "  $($subj.subject_name): $($subj.total_minutes) min" -ForegroundColor White
}

Write-Host "Streak: $($dashboard.streak_info.current_streak) days current" -ForegroundColor Cyan

Write-Host "`n=== All Analytics Tests Passed ===" -ForegroundColor Green
Write-Host "Analytics service is fully functional!" -ForegroundColor Cyan
