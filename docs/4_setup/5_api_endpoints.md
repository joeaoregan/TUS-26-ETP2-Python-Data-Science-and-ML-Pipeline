# 📡 API Endpoints

## Python Service (Port 8000)

```
GET  /health              - Service health status
POST /predict_action      - Predict traffic action
GET  /model_info          - Get model details
GET  /docs                - Swagger UI documentation
```

## Java Gateway (Port 8080)

```
GET  /api/traffic/health  - Service health status
GET  /api/traffic/action  - Get traffic action (auto-generated obs)
POST /api/traffic/action  - Predict with custom observations
```