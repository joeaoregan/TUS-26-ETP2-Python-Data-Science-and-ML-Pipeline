# 🛠 Development vs Production

## Development (Local)

```bash
# Run services individually
cd rl-inference-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# In another terminal:
cd java-api-gateway
mvn spring-boot:run
```

## Production (Docker)

```bash
docker-compose up --build -d
docker-compose logs -f
docker-compose ps
```