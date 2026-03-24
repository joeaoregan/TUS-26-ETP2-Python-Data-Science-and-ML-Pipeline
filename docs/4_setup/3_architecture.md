# 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Client/External System                │
└──────────────────────────┬──────────────────────────────────┘
                         │ 
                         └─→ HTTP on port 8080
                              │
                ┌─────────────▼────────────────────────┐
                │  Java Spring Boot Gateway         │  Port 8080
                │  - REST API endpoints             │
                │  - Observation handling           │
                │  - Error management               │
                └───────────────┬──────────────────────┘
                               │
                               └─→ HTTP on port 8000
                                 │
                ┌─────────────────▼────────────────────┐
                │  Python FastAPI Service           │  Port 8000
                │  - Model loading & management     │
                │  - Action prediction              │
                │  - Health monitoring              │
                └──────────────┬───────────────────────┘
                              │
                ┌──────────────▼───────────────────────┐
                │  Trained RL Model (PPO)           │
                │  From: Results/sweeps_*/model.zip │
                └──────────────────────────────────────┘
```
