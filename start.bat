@echo off
REM Startup script for AI Traffic Control API

echo ========================================
echo AI Traffic Control API - Startup Script
echo ========================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not available
    echo Please ensure Docker Desktop is properly installed
    exit /b 1
)

echo Docker found: 
docker --version
echo Docker Compose version:
docker-compose --version
echo.

REM Check if model file exists
if not exist "rl-inference-service\app\trained_models\model.zip" (
    echo Warning: Model file not found at rl-inference-service\app\trained_models\model.zip
    echo Please copy your trained model before starting the services.
    echo.
    echo Available models in sweeps:
    dir "..\Results\sweeps*" /b /d 2>nul || echo (Models not found)
    echo.
)

REM Build and start services
echo Starting AI Traffic Control API services...
echo.
docker-compose up --build

echo.
echo ========================================
echo AI Traffic Control API Started
echo ========================================
echo.
echo Python FastAPI Service (RL Inference):
echo   URL: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo.
echo Java API Gateway:
echo   URL: http://localhost:8080
echo   Traffic API: http://localhost:8080/api/traffic
echo.
echo To test the API:
echo   curl http://localhost:8080/api/traffic/action
echo.
echo Press Ctrl+C to stop services
