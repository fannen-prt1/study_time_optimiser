# Study Time Optimizer - Setup Script (Windows PowerShell)
# Run this script to set up the project for the first time

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Study Time Optimizer - Initial Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python 3.11+ is required but not found!" -ForegroundColor Red
    Write-Host "  Please install Python from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js is installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js 18+ is required but not found!" -ForegroundColor Red
    Write-Host "  Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Create .env files from examples
Write-Host ""
Write-Host "Creating environment files..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" -Destination ".env"
    Write-Host "✓ Created root .env" -ForegroundColor Green
} else {
    Write-Host "⚠ .env already exists, skipping" -ForegroundColor Yellow
}

if (-not (Test-Path "frontend\.env")) {
    Copy-Item "frontend\.env.example" -Destination "frontend\.env"
    Write-Host "✓ Created frontend\.env" -ForegroundColor Green
} else {
    Write-Host "⚠ frontend\.env already exists, skipping" -ForegroundColor Yellow
}

# Setup Backend
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Setting up Backend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

# Run database migrations
Write-Host "Setting up database..." -ForegroundColor Yellow
alembic upgrade head
Write-Host "✓ Database migrations complete" -ForegroundColor Green

# Deactivate virtual environment
deactivate

Set-Location ..

# Setup Frontend
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Setting up Frontend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

Set-Location ..

# Setup ML Engine
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Setting up ML Engine" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Set-Location ml-engine

Write-Host "Installing ML dependencies..." -ForegroundColor Yellow
..\backend\venv\Scripts\pip.exe install -r requirements.txt
Write-Host "✓ ML dependencies installed" -ForegroundColor Green

Set-Location ..

# Final message
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Setup Complete! 🎉" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review and update .env files with your configuration" -ForegroundColor White
Write-Host "  2. Start the backend: cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload --port 5000" -ForegroundColor White
Write-Host "  3. Start the frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Or use Docker:" -ForegroundColor Cyan
Write-Host "  docker-compose up --build" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
