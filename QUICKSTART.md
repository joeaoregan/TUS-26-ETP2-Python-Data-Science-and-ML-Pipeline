# Quick Start Guide - AI Traffic Control API

## 5-Minute Setup

### 1. Select Your Trained Model
```bash
python select_model.py
```
This will show you all available trained models and help you copy one to the API.

**Available sweeps:** pressure, queue, diff-waiting-time  
**Locations:** `C:\Users\gemer\Sumo\my-network\Results\sweeps*\`

### 2. Start the Services
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

### 3. Test the API
```bash
# Get a traffic action
curl http://localhost:8080/api/traffic/action

# Or run the comprehensive test
python test_api.py
```

## API Endpoints

### Python FastAPI Service (Port 8000)
- `GET /health` - Health check
- `POST /predict_action` - Action prediction
- `GET /model_info` - Model information
- `GET /docs` - Interactive API documentation (Swagger UI)

### Java API Gateway (Port 8080)
- `GET /api/traffic/health` - Health check
- `GET /api/traffic/action` - Get traffic action (auto-generated observations)
- `POST /api/traffic/action` - Predict action with custom observations

## Example Requests

### Get Traffic Action
```bash
curl http://localhost:8080/api/traffic/action
```

**Response:**
```json
{
  "predictedAction": 2,
  "signalState": "GREEN",
  "timestamp": 1710521600000,
  "status": "success"
}
```

### Custom Observations
```bash
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -d '{
    "observations": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  }'
```

### Health Check
```bash
curl http://localhost:8080/api/traffic/health
```

## Architecture

```
Flow: HTTP Request → Java Gateway (8080) → Python FastAPI (8000) → RL Model
```

**Components:**
1. **Java Spring Boot Gateway** - REST API entry point
2. **Python FastAPI Service** - RL model inference
3. **Trained PPO Model** - Action prediction

## Docker Commands

```bash
# Start services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Check service status
docker-compose ps
```

## Troubleshooting

### Services won't start
1. Ensure Docker is installed: `docker --version`
2. Check if ports 8000 and 8080 are available
3. Check logs: `docker-compose logs`

### Model loading fails
1. Verify model file exists: `rl-inference-service/app/trained_models/model.zip`
2. Rerun model selector: `python select_model.py`
3. Rebuild: `docker-compose up --build`

### API returns errors
1. Check Python service logs: `docker-compose logs rl-inference`
2. Verify model is loaded: `curl http://localhost:8000/model_info`
3. Test health: `curl http://localhost:8080/api/traffic/health`

## Next Steps

1. **Integrate with SUMO:** Modify SUMO simulation to call the API
2. **Custom Observations:** Replace dummy observations with real traffic data
3. **Production Deployment:** Use Kubernetes or cloud platforms
4. **Monitoring:** Add logging and metrics collection

## Files Overview

| File | Purpose |
|------|---------|
| `select_model.py` | Interactive model selector |
| `test_api.py` | API test client |
| `start.bat/.sh` | Quick startup script |
| `docker-compose.yml` | Service orchestration |
| `rl-inference-service/` | Python FastAPI service |
| `java-api-gateway/` | Java Spring Boot gateway |
| `README.md` | Full documentation |

## Documentation

For detailed documentation, see [README.md](README.md)
