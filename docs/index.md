# AI-Driven Predictive Traffic Flow Optimisation System

<h2>Engineering Team Project | TUS Athlone</h2>

![Java 17](https://img.shields.io/badge/Java-17-blue)
![Python 3.9](https://img.shields.io/badge/Python-3.9-green)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2.3-6DB33F?logo=spring-boot&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Research-success)

![GitHub repo size](https://img.shields.io/github/repo-size/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=blue)
![GitHub top language](https://img.shields.io/github/languages/top/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation)
![Stars](https://img.shields.io/github/stars/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?style=social)

---

### 🔗 Quick Links

#### 🌐 API Gateway: 

- [API Gateway App](https://ai-traffic-control-api.onrender.com/)
- [Swagger UI Docs](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)

#### 🤖 Inference Service:

- [Inference Service App](https://traffic-inference-service.onrender.com)
- [Swagger UI Docs](https://traffic-inference-service.onrender.com/docs)

---

### 👥 Research Team

> - [Joe O'Regan](https://github.com/joeaoregan)
> - [Adam O Neill Mc Knight](https://github.com/AdamQ45)
> - [David Claffey](https://github.com/dclaff)
> - [Edgars Peskaitis](https://github.com/edgar183)

---

## 📈 Performance Targets

> **Project Goal:** Target 15-20% reduction in urban traffic congestion for the Athlone "Orange Loop" using Reinforcement Learning.

> - **Average Travel Time (ATT):** Target -15%
> - **Mean Queue Length (MQL):** Target -20%
> - **Data Integrity:** TLS 1.3 secured telemetry pipeline

---

## 🏗️ System Architecture

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study. 

- **Traffic Monitoring Gateway (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication.
- **RL-Inference Service (Python/FastAPI):** Hosts a trained **PPO (Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic density.
- **Simulation Layer (SUMO):** Integrated high-fidelity environment for testing adaptive signal logic against baseline fixed-time controllers.

This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management in regional Irish hubs.

*For more details see [System Architecture](SYSTEM_ARCHITECTURE.md) page.*

[System Architecture]{#}(SYSTEM_ARCHITECTURE)

---


## 🚗 AI Traffic Control API Setup Guide

This project provides a complete REST API solution for traffic signal control using trained RL models.

### Project Structure

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

### Components

#### 1. Python FastAPI Service (RL Inference Service)

- **Port:** 8000
- **Purpose:** Loads and serves trained PPO models for action prediction
- **Key Endpoints:**
  - `GET /health` - Health check
  - `POST /predict_action` - Action prediction endpoint
  - `GET /model_info` - Model information

#### 2. Java Spring Boot API Gateway

- **Port:** 8080
- **Purpose:** REST API gateway that communicates with the Python service
- **Key Endpoints:**
  - `GET /api/traffic/health` - Health check
  - `GET /api/traffic/action` - Get traffic action (generates dummy observations)
  - `POST /api/traffic/action` - Predict action with custom observations

#### 3. Docker Compose

- Orchestrates both services
- Manages networking and dependencies
- Provides health checks and monitoring

The Java Gateway receives raw vehicle counts, transforms them into an observation vector, and forwards them to the Python service for a decision.

### Setup Instructions

#### Prerequisites
- Docker & Docker Compose
- Or locally:
  - Python 3.9+
  - Java 17+
  - Maven 3.9+

#### Steps to Deploy

##### Option 1: Using Docker Compose (Recommended)

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

##### Option 2: Local Development

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

- Includes Swagger/OpenAPI documentation for all traffic control endpoints.

---

## 📡 API Usage Examples

### 🎯 Get Traffic Action (Auto-generated observations)
```bash
curl -X GET http://localhost:8080/api/traffic/action
```

Response:
```json
{
  "predictedAction": 2,
  "signalState": "GREEN",
  "timestamp": 1684756800000,
  "status": "success"
}
```

### 🔮 Predict Action with Custom Observations
```bash
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -d '{
    "observations": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "metadata": "peak-hour"
  }'
```

Response:
```json
{
  "predictedAction": 1,
  "signalState": "YELLOW",
  "timestamp": 1684756800000,
  "status": "success"
}
```

### 💚 Health Check
```bash
curl http://localhost:8080/api/traffic/health
```

Response:
```json
{
  "status": "healthy",
  "inferenceService": "up",
  "timestamp": 1684756800000
}
```

---

## 🔐 Environment Variables

### Python Service (RL Inference)

| Environment Variable    | Description                        | Default                         |
|-------------------------|------------------------------------|---------------------------------|
| `MODEL_PATH`            | Path to trained model file         | `/app/trained_models/model.zip` |
| `OBSERVATION_SHAPE_DIM` | Observation vector dimension       | `10`                            |
| `NUM_AGENTS`            | Number of agents                   | `1`                             |
| `API_HOST`              | API host address                   | `0.0.0.0`                       |
| `API_PORT`              | API port number                    | `8000`                          |
| `API_RELOAD`            | Enable auto-reload on code changes | `false`                         |

### Java Gateway

| Environment Variable           | Description              | Default                                |
|--------------------------------|--------------------------|----------------------------------------|
| `RL_INFERENCE_SERVICE_URL`     | RL Inference Service URL | `http://localhost:8000/predict_action` |
| `RL_INFERENCE_SERVICE_TIMEOUT` | Request timeout in ms    | `10000`                                |

---


## 🐳 Docker Compose Configuration

The `docker-compose.yml` file includes:

| **RL Inference Service** | **Java Gateway** | **Network** |
|--------------------------|------------------|-------------|
| Python 3.9 slim image | Multi-stage build for optimized image | Port 8080 exposed |
| Volume for trained models | Depends on RL Inference Service |  |
| Health checks enabled | Health checks enabled |  |
| Port 8000 exposed | Port 8080 exposed |  |

----


## 📊 Monitoring and Logging

Both services include:
- Structured logging configuration
- Health check endpoints
- Service-to-service health dependencies
- Docker logging drivers with rotation

Monitor logs:
```bash
docker-compose logs -f rl-inference
docker-compose logs -f java-gateway
```

---


## 🔄 Using Different Models

To use different trained models:

1. **Locate your model:**
   ```
   C:\Users\gemer\Sumo\my-network\Results\sweeps_*\<sweep_name>\seed_*\<variant>\model.zip
   
   Examples:
   - Results\sweeps\pressure\seed_42\A\model.zip
   - Results\sweeps\queue\seed_123\B\model.zip
   - Results\sweeps_2\diff-waiting-time\seed_7\C\model.zip
   ```

2. **Copy to models directory:**
   ```bash
   copy "<source_path>\model.zip" "rl-inference-service\app\trained_models\model.zip"
   ```

3. **Rebuild and restart:**
   ```bash
   docker-compose up --build
   ```

---


## ⚡ Performance Tuning

### For High-Throughput Scenarios
- Adjust Java `RL_INFERENCE_SERVICE_TIMEOUT` if needed
- Consider load balancing multiple Python service instances
- Use connection pooling in Java gateway

### For Lower Latency
- Run services on same machine
- Use local model paths instead of network mounts
- Optimize observation preprocessing in Java gateway

---


## 🐛 Troubleshooting</summary>

| **Service won't start** | **Prediction fails with timeout** | **Model loading fails** |
|-----------|--------|-----------|
| Check Docker logs: `docker-compose logs` | Increase `RL_INFERENCE_SERVICE_TIMEOUT` | Verify model path in environment variables |
| Verify model file exists and is correct format | Check if Python service is running: `docker-compose ps` | Ensure model.zip is a valid stable-baselines3 PPO model |
| Check port availability (8000, 8080) | Verify network connectivity: `docker-compose exec java-gateway ping rl-inference` | Check file permissions |

---


## 🌍 Production Deployment

For production:

1. Use **Docker Compose** with production-grade orchestration (Kubernetes)
2. Add **load balancing** for multiple instances
3. Configure **persistent volumes** for logs
4. Set up **monitoring** and **alerting**
5. Use environment-specific **configuration files**
6. Implement **API rate limiting** and **authentication**
7. Set up **backup strategies** for trained models
