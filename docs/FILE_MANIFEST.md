# AI Traffic Control API - File Manifest

## Project Root
📁 `c:\Users\gemer\Sumo\my-network\ai-traffic-api\`

### Root Level Files
- 📄 `docker-compose.yml` - Multi-service Docker orchestration
- 📄 `README.md` - Comprehensive documentation (5500+ lines)
- 📄 `QUICKSTART.md` - 5-minute setup guide
- 📄 `SETUP_COMPLETE.md` - This setup summary
- 📄 `.gitignore` - Git ignore configuration
- 🐍 `select_model.py` - Interactive model selector utility
- 🐍 `test_api.py` - API test client with load testing
- 🪟 `start.bat` - Windows startup script
- 🐧 `start.sh` - Linux/Mac startup script

## Python FastAPI Service
📁 `rl-inference-service/`

### Core Application
- 🐍 `app/main.py` - FastAPI application
  - Loads trained PPO models
  - `/predict_action` endpoint
  - `/health` and `/model_info` endpoints
  - Error handling and logging

### Configuration
- 📄 `requirements.txt` - Python dependencies
  - fastapi==0.110.0
  - uvicorn==0.28.0
  - stable-baselines3==2.2.1
  - torch==2.2.1
  - numpy==1.26.4
  - pydantic==2.6.4
  - python-dotenv==1.0.1
  - shimmy==0.2.1
  - jinja2==3.1.3
  - aiofiles==24.1.0

### Deployment
- 📄 `Dockerfile` - Python 3.9-slim container
  - Builds dependencies
  - Exposes port 8000
  - Runs with uvicorn

### Configuration Templates
- 📄 `.env.example` - Environment variable template

### Data Directory
- 📁 `app/models/` - Directory for trained models
  - (Models copied here by select_model.py)
  - `model.zip` - Trained PPO model

## Java Spring Boot Gateway
📁 `java-api-gateway/`

### Project Configuration
- 📄 `pom.xml` - Maven configuration
  - Spring Boot 3.2.3
  - Java 17
  - Dependencies: spring-boot-starter-web, spring-boot-starter-webflux, lombok

### Application Entry Point
- ☕ `src/main/java/com/example/gateway/GatewayApplication.java`
  - Spring Boot application class
  - RestTemplate and WebClient beans

### REST Controller
- ☕ `src/main/java/com/example/gateway/controller/TrafficController.java`
  - GET `/api/traffic/health` - Health check
  - GET `/api/traffic/action` - Action with auto-generated observations
  - POST `/api/traffic/action` - Action with custom observations
  - Helper methods for observation generation and action mapping

### Service Client
- ☕ `src/main/java/com/example/gateway/service/RlInferenceClient.java`
  - HTTP client for Python FastAPI service
  - `predictAction()` method
  - Health check functionality
  - Error handling with RlInferenceException
  - Inner classes: PredictionResponse, HealthResponse

### Configuration
- 📄 `src/main/resources/application.properties`
  - Server configuration
  - RL service URL and timeout
  - Logging levels

### Deployment
- 📄 `Dockerfile` - Multi-stage Java container
  - Maven builder stage
  - Eclipse Temurin 17 JRE runtime
  - Exposes port 8080

## File Statistics

### Total Files Created: 21
- Root level: 9 files
- Python service: 5 files
- Java service: 7 files

### Code Files
- Python: 2 main files (main.py, select_model.py, test_api.py)
- Java: 3 files (Application, Controller, Service)

### Configuration Files
- Docker: 2 files (Dockerfile x2, docker-compose.yml)
- Build: 1 file (pom.xml, requirements.txt)
- Properties: 2 files (application.properties, .env.example)

### Documentation Files
- **5 markdown documentation files** covering setup, architecture, API usage, and troubleshooting
- **mkdocs.yml** configuration file for site structure and theme settings
- **MkDocs site** with full project documentation (https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/)
- **Interactive API docs** via Swagger UI for both Java Gateway and Python Inference Service
- **README.md** with quick links and project overview

### Scripts
- 3 scripts (start.bat, start.sh, select_model.py, test_api.py)

## File Sizes (Approximate)

| Component      | Files   | Total Size |
|----------------|--------:|-----------:|
| Documentation  | 4       | ~25 KB     |
| Python Service | 3       | ~12 KB     |
| Java Service   | 3       | ~18 KB     |
| Configuration  | 6       | ~5 KB      |
| Scripts        | 4       | ~15 KB     |
| **Total**      | **20+** | **~75 KB** |

## Integration with Existing Project

### Location in Project
```
my-network/
├── ai-traffic-api/                 ← NEW API files here
├── Results/
│   ├── sweeps/                     ← Existing trained models
│   ├── sweeps_2/ through sweeps_9/
│   └── (other directories)
├── train_ppo_agent.py              ← Can call API
└── ... (other files)
```

### Data Flow Integration
```
train_ppo_agent.py
    ↓
Can now use:
    ↓
ai-traffic-api/
├── select_model.py          (Choose best model)
└── test_api.py              (Verify predictions)
    ↓
Docker services running:
├── Python FastAPI Service   (Model inference)
└── Java API Gateway         (REST interface)
    ↓
External system or SUMO can call:
    http://localhost:8080/api/traffic/action
```

## Environment Setup

### Prerequisites Installed
- Docker & Docker Compose (for containerized deployment)
- Python 3.9+ (for running select_model.py and test_api.py)
- Java 17+ (optional, for local Java development)
- Maven (optional, for building Java locally)

### Directories Created
```
ai-traffic-api/
├── rl-inference-service/
│   ├── app/
│   │   └── models/         (will contain model.zip)
│   └── (config files)
└── java-api-gateway/
    ├── src/main/
    │   ├── java/...
    │   └── resources/
    └── (config files)
```

### Volumes/Mounts (Docker)
- Python models: `./rl-inference-service/app/trained_models:/app/trained_models`
- Java application: Built into container image

## How to Use Each Component

### select_model.py
```bash
python select_model.py
# Shows all available models from Results/sweeps*
# Allows interactive selection
# Copies chosen model to rl-inference-service/app/trained_models/
```

### test_api.py
```bash
python test_api.py
# Requires services to be running (via docker-compose up)
# Tests all API endpoints
# Includes load testing capability
```

### start.bat / start.sh
```bash
start.bat  # Windows
./start.sh # Linux/Mac
# Builds and starts Docker services
# Displays service URLs
```

### docker-compose.yml
```yaml
# Services defined:
# - rl-inference (Python, port 8000)
# - java-gateway (Java, port 8080)
# Networking: traffic-network bridge
# Health checks: Enabled
```

## Quick Reference

### Starting Fresh
1. `python select_model.py` - Select and copy model
2. `start.bat` (Windows) or `./start.sh` (Linux) - Start services
3. `python test_api.py` - Run tests
4. `curl http://localhost:8080/api/traffic/action` - Make predictions

### Stopping Services
```bash
docker-compose down
```

### Viewing Logs
```bash
docker-compose logs rl-inference    # Python service
docker-compose logs java-gateway    # Java service
docker-compose logs -f              # All services, follow mode
```

### Restarting with New Model
```bash
docker-compose down
python select_model.py              # Choose new model
docker-compose up --build
```

## Notes

- All services use Docker for consistent deployment
- Python service uses FastAPI with automatic Swagger UI at `/docs`
- Java service uses Spring Boot 3.2.3 for modern framework features
- Services communicate via HTTP internally
- Health checks ensure services are ready before dependent services start
- Comprehensive error handling and logging in both services
- Configurable via environment variables for flexibility

## Success Indicators

✅ If setup is complete:
- `ai-traffic-api/` directory exists with all files
- Can run `python select_model.py` successfully
- Can run `start.bat`/`start.sh` without errors
- API responds at `http://localhost:8080/api/traffic/action`
- Services show "healthy" in `docker-compose ps`

---

**Generated:** March 2026
**Last Updated:** 24/03/2026
**Status:** Setup Complete ✓
