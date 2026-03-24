
# 📖 API Documentation


## 🔗 Quick Links

- [API Gateway Docs](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)
- [Inference Service Docs](https://traffic-inference-service.onrender.com/docs)

---

## Java API Gateway

The Java API Gateway now includes automatically generated API documentation using **springdoc-openapi**.

Once the gateway is running, Swagger UI is available at:

```
http://localhost:8080/swagger-ui/index.html
```

The API docs for the Java API Gateway have been [deployed to Render](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html):

```
https://ai-traffic-control-api.onrender.com/swagger-ui/index.html
```

Swagger is generated automatically from annotations in the Java controller classes.  
Additional endpoint documentation will be added incrementally.

---

## Python Inference Service

The Python FastAPI service automatically generates interactive API documentation using **Swagger UI**.

Once the inference service is running, Swagger UI is available at:

```
http://localhost:8000/docs
```

The API docs for the Python Inference Service have been [deployed to Render](https://traffic-inference-service.onrender.com/docs):

```
https://traffic-inference-service.onrender.com/docs

```

---

## What Swagger Provides

- Interactive documentation for all REST endpoints
- A complete list of all API endpoints
- Descriptions of each endpoint and its purpose
- Example request and response payloads
- Field‑level documentation for request models
- Live “Try It Out” testing directly from the browser

---

## How It Works

### Java API Gateway

Swagger documentation is generated automatically from annotations in the Java codebase:

- @Operation — endpoint summary and description
- @ApiResponse — documented response codes and examples
- @Schema — request/response model documentation
- @Tag — groups related endpoints in the UI

---

### Python Inference Service

Swagger documentation is generated automatically from annotations and type hints in the FastAPI codebase:

- **`@app.get()` / `@app.post()` decorators** — Define endpoints with automatic route documentation
- **Function docstrings** — Endpoint summaries and detailed descriptions
- **Pydantic model type hints** — Request/response schemas generated automatically (e.g., `Observation`, `PredictionResponse`)
- **Response models** — Define expected HTTP response structures with `response_model=MyModel`
- **Tags** — Organize endpoints into groups (e.g., `tags=["System Health"]`, `tags=["Traffic Inference"]`)
- **HTTP status codes** — Document error responses with `HTTPException` and status codes

### Example

```python
@app.get("/health", response_model=HealthResponse, tags=["System Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_path=model_path or "not set"
    )

@app.post("/predict_action", response_model=PredictionResponse, tags=["Traffic Inference"])
async def predict_action(observation: Observation):
    """
    Predict action for given observation.
    
    Args:
        observation: Observation data containing obs_data as a list of floats
        
    Returns:
        PredictionResponse with predicted action
    """
```

The docstrings, type hints, and response models automatically generate interactive Swagger documentation without any extra annotation overhead.

---

## Where to Add Documentation

All API documentation lives directly in the controller and model classes.   
This keeps the documentation close to the code and ensures Swagger stays up‑to‑date.