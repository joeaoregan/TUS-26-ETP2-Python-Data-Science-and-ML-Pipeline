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

---

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

---

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
