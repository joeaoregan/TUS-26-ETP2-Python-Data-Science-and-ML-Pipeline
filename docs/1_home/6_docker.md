The `docker-compose.yml` file includes:

| **RL Inference Service** | **Java Gateway** | **Network** |
|--------------------------|------------------|-------------|
| Python 3.9 slim image | Multi-stage build for optimized image | Port 8080 exposed |
| Volume for trained models | Depends on RL Inference Service |  |
| Health checks enabled | Health checks enabled |  |
| Port 8000 exposed | Port 8080 exposed |  |