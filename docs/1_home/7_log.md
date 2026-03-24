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