# 🔐 Environment Variables

## Python Service

```
MODEL_PATH=./app/trained_models/model.zip    # Model location
OBSERVATION_SHAPE_DIM=10                      # Input dimension
NUM_AGENTS=1                                  # Number of agents
API_HOST=0.0.0.0                             # Bind address
API_PORT=8000                                # Service port
```

## Java Gateway

```
RL_INFERENCE_SERVICE_URL=http://localhost:8000/predict_action
RL_INFERENCE_SERVICE_TIMEOUT=10000  # milliseconds
```
