# Initialize Database Script
# Run this after backend dependencies are installed

Write-Host "🚀 Initializing Database..." -ForegroundColor Cyan

# Make sure we're in the backend directory
Set-Location $PSScriptRoot\..\backend

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "✅ Created logs directory" -ForegroundColor Green
}

# Run Alembic migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialized successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now you can start the backend with:" -ForegroundColor Cyan
    Write-Host "  uvicorn app.main:app --reload --port 5000" -ForegroundColor White
} else {
    Write-Host "❌ Database initialization failed!" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
}
