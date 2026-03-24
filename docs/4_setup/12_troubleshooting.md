# 🐛 Troubleshooting

## Services won't start
- Check Docker is installed: `docker --version`
- Verify ports 8000, 8080 are available
- Check logs: `docker-compose logs`

## Model loading fails
- Ensure model file exists: `rl-inference-service/app/trained_models/model.zip`
- Rerun selector: `python select_model.py`
- Check Python logs: `docker-compose logs rl-inference`

## Predictions return errors
- Verify service health: `curl http://localhost:8080/api/traffic/health`
- Check observation dimensions (should be 10 floats)
- View logs: `docker-compose logs`