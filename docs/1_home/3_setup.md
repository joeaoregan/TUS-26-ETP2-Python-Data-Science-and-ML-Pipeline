This project provides a complete REST API solution for traffic signal control using trained RL models.

## Project Structure

```
TUS-26-ETP2-Python-Data-Science-and-ML-Pipeline/
├── java-api-gateway/                       # Java Spring Boot gateway
│   ├── src/
│   │   ├── main/java/com/example/gateway/
│   │   │   ├── GatewayApplication.java     # Spring Boot app
│   │   │   ├── controller/
│   │   │   │   └── TrafficController.java  # REST endpoints
│   │   │   └── service/
│   │   │       └── RlInferenceClient.java  # RL service client
│   │   └── main/resources/
│   │       └── application.properties      # Spring config
│   ├── pom.xml                             # Maven configuration
│   └── Dockerfile                          # Java service Docker image
├── rl-inference-service/                   # Python FastAPI service
│   ├── app/
│   │   ├── main.py                         # FastAPI application
│   │   └── models/                         # Directory for trained models
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies
│   └── .env.example                        # Environment variables template
├── SUMO/                                   # 
│   ├── results/
│   │   ├── Base/
│   ├── Simulations/
│   │   ├── Base/
├── docker-compose.yml                      # Docker Compose orchestration
└── CHANGELOG.md                            # Change log
└── FILE_MAINFEST.md                        # 
└── QUICKSTART.md                           # Quick start guide
└── README.md                               # This file
└── SETUP_COMPLETE.md                       # 
└── SYSTEM_ARCHITECTURE.md                  # 
```

## Components

### 1. Python FastAPI Service (RL Inference Service)

- **Port:** 8000
- **Purpose:** Loads and serves trained PPO models for action prediction
- **Key Endpoints:**
  - `GET /health` - Health check
  - `POST /predict_action` - Action prediction endpoint
  - `GET /model_info` - Model information

### 2. Java Spring Boot API Gateway

- **Port:** 8080
- **Purpose:** REST API gateway that communicates with the Python service
- **Key Endpoints:**
  - `GET /api/traffic/health` - Health check
  - `GET /api/traffic/action` - Get traffic action (generates dummy observations)
  - `POST /api/traffic/action` - Predict action with custom observations

### 3. Docker Compose

- Orchestrates both services
- Manages networking and dependencies
- Provides health checks and monitoring

The Java Gateway receives raw vehicle counts, transforms them into an observation vector, and forwards them to the Python service for a decision.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Or locally:
  - Python 3.9+
  - Java 17+
  - Maven 3.9+

### Steps to Deploy

#### Option 1: Using Docker Compose (Recommended)

1. **Copy your trained model:**
   ```bash
   # Copy trained model to the models directory
   # Example: Copy from C:\Users\gemer\Sumo\my-network\Results\sweeps\<sweep_dir>\<seed>\<variant>\model.zip
   mkdir -p rl-inference-service/app/trained_models
   copy "C:\Users\gemer\Sumo\my-network\Results\sweeps\pressure\seed_42\A\model.zip" "rl-inference-service\app\trained_models\model.zip"
   ```

2. **Set environment variables (optional):**
   ```bash
   # Create .env file for RL Inference Service
   echo MODEL_PATH=/app/trained_models/model.zip > rl-inference-service/.env
   echo OBSERVATION_SHAPE_DIM=10 >> rl-inference-service/.env
   echo NUM_AGENTS=1 >> rl-inference-service/.env
   ```

3. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

4. **Test the API:**
   ```bash
   # Get traffic action (auto-generated observations)
   curl http://localhost:8080/api/traffic/action

   # Predict action with custom observations
   curl -X POST http://localhost:8080/api/traffic/action \
     -H "Content-Type: application/json" \
     -d '{"observations": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}'

   # Check health
   curl http://localhost:8080/api/traffic/health
   ```

#### Option 2: Local Development

**Python Service:**
```bash
cd rl-inference-service

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set MODEL_PATH=path\to\your\model.zip  # Windows
export MODEL_PATH=path/to/your/model.zip  # Linux/Mac

# Run service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Java Gateway:**
```bash
cd java-api-gateway

# Set environment variable
set RL_INFERENCE_SERVICE_URL=http://localhost:8000/predict_action  # Windows
export RL_INFERENCE_SERVICE_URL=http://localhost:8000/predict_action  # Linux/Mac

# Build and run
mvn clean install
mvn spring-boot:run
```

*Includes [Swagger/OpenAPI documentation](../DOCUMENTATION.md) for all traffic control endpoints.*
