#!/bin/bash

# Startup script for AI Traffic Control API

echo "========================================"
echo "AI Traffic Control API - Startup Script"
echo "========================================"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not available"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "Docker version:"
docker --version
echo "Docker Compose version:"
docker-compose --version
echo ""

# Check if model file exists
if [ ! -f "rl-inference-service/app/trained_models/model.zip" ]; then
    echo "Warning: Model file not found at rl-inference-service/app/trained_models/model.zip"
    echo "Please copy your trained model before starting the services."
    echo ""
    echo "Available models in sweeps:"
    find ../Results/sweeps* -name "model.zip" 2>/dev/null | head -5
    echo ""
fi

# Build and start services
echo "Starting AI Traffic Control API services..."
echo ""
docker-compose up --build

echo ""
echo "========================================"
echo "AI Traffic Control API Started"
echo "========================================"
echo ""
echo "Python FastAPI Service (RL Inference):"
echo "  URL: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo ""
echo "Java API Gateway:"
echo "  URL: http://localhost:8080"
echo "  Traffic API: http://localhost:8080/api/traffic"
echo ""
echo "To test the API:"
echo "  curl http://localhost:8080/api/traffic/action"
echo ""
echo "Press Ctrl+C to stop services"
