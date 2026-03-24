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
