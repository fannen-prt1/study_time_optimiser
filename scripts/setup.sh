#!/bin/bash

# Study Time Optimizer - Setup Script (Linux/macOS)
# Run this script to set up the project for the first time

set -e  # Exit on error

echo "============================================"
echo "  Study Time Optimizer - Initial Setup"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python is installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3.11+ is required but not found!${NC}"
    echo -e "${RED}  Please install Python from https://www.python.org/${NC}"
    exit 1
fi

# Check if Node.js is installed
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js is installed: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js 18+ is required but not found!${NC}"
    echo -e "${RED}  Please install Node.js from https://nodejs.org/${NC}"
    exit 1
fi

# Create .env files from examples
echo ""
echo -e "${YELLOW}Creating environment files...${NC}"

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠ backend/.env already exists, skipping${NC}"
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created root .env${NC}"
else
    echo -e "${YELLOW}⚠ .env already exists, skipping${NC}"
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Created frontend/.env${NC}"
else
    echo -e "${YELLOW}⚠ frontend/.env already exists, skipping${NC}"
fi

# Setup Backend
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Setting up Backend${NC}"
echo -e "${CYAN}============================================${NC}"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Run database migrations
echo -e "${YELLOW}Setting up database...${NC}"
alembic upgrade head
echo -e "${GREEN}✓ Database migrations complete${NC}"

# Deactivate virtual environment
deactivate

cd ..

# Setup Frontend
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Setting up Frontend${NC}"
echo -e "${CYAN}============================================${NC}"

cd frontend

echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

cd ..

# Setup ML Engine
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Setting up ML Engine${NC}"
echo -e "${CYAN}============================================${NC}"

cd ml-engine

echo -e "${YELLOW}Installing ML dependencies...${NC}"
pip3 install -r requirements.txt
echo -e "${GREEN}✓ ML dependencies installed${NC}"

cd ..

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

# Final message
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Setup Complete! 🎉${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo -e "${NC}  1. Review and update .env files with your configuration${NC}"
echo -e "${NC}  2. Start the backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload${NC}"
echo -e "${NC}  3. Start the frontend: cd frontend && npm run dev${NC}"
echo ""
echo -e "${CYAN}Or use Docker:${NC}"
echo -e "${NC}  docker-compose up --build${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
