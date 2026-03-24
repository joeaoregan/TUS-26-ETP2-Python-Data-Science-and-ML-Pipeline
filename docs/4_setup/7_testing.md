# 🧪 Testing

## Test With Included Client
```bash
python test_api.py
```

Tests include:

- Health checks
- Basic functionality
- Custom observation predictions
- Load testing (5 requests)
- Model information retrieval

## Manual Test

```bash
# Test auto-generated action
curl http://localhost:8080/api/traffic/action

# Test custom observations
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -d '{"observations": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}'

# Check API health
curl http://localhost:8080/api/traffic/health

# Check Python model
curl http://localhost:8000/health
```
