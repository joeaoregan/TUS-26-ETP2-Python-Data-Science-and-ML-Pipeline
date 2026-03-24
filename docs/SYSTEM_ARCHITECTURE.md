# System Architecture - AI Traffic Control API

## Overview

The AI Traffic Control API is a distributed, microservices-based system designed to provide real-time traffic signal control recommendations using trained Reinforcement Learning (RL) models.

---

## 1. High-Level System Architecture

```mermaid
graph TB
    Client["🚗 Client Applications<br/>(SUMO Simulation<br/>External Systems<br/>Mobile Apps)"]
    
    subgraph Docker["🐳 Docker Container Network"]
        subgraph JavaService["Java API Gateway<br/>Spring Boot 3.2<br/>Port 8080"]
            Controller["TrafficController<br/>REST Endpoints"]
            ServiceClient["RlInferenceClient<br/>HTTP Client"]
        end
        
        subgraph PythonService["Python FastAPI Service<br/>Port 8000"]
            API["FastAPI App<br/>uvicorn"]
            ModelLoader["Model Loader<br/>PPO Model"]
            Predictor["Predictor<br/>stable-baselines3"]
        end
    end
    
    ModelStorage["📦 Trained Models<br/>Results/sweeps/*<br/>model.zip"]
    
    Client -->|HTTP:8080| Controller
    Controller -->|HTTP:8000| ServiceClient
    ServiceClient -->|HTTP Request| API
    API --> ModelLoader
    ModelLoader -->|Load| ModelStorage
    ModelLoader --> Predictor
    Predictor -->|Prediction| API
    API -->|JSON Response| ServiceClient
    ServiceClient -->|Response| Controller
    Controller -->|JSON Response| Client
    
    style Docker fill:#e1f5ff
    style JavaService fill:#fff3e0
    style PythonService fill:#f3e5f5
    style ModelStorage fill:#e8f5e9
```

---

## 2. Request-Response Flow Diagram

### **GET /api/traffic/action** (Auto-generated observations)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant PS as Python Service<br/>Port 8000
    participant Model as RL Model<br/>PPO
    
    Client->>JG: GET /api/traffic/action
    
    Note over JG: Generate dummy<br/>observations (10 values)
    JG->>JG: Create random observation<br/>values [0-1]
    
    JG->>PS: POST /predict_action<br/>{"obs_data": [0.1, 0.2, ...]}
    
    Note over PS: Load model & predict
    PS->>Model: Call model.predict()
    Model-->>PS: Return action (0-3)
    
    Note over PS: Format response
    PS-->>JG: {"action": 2}
    
    Note over JG: Map action to signal
    JG->>JG: 2 → "GREEN"
    
    JG-->>Client: {<br/>"predictedAction": 2,<br/>"signalState": "GREEN",<br/>"timestamp": ...,<br/>"status": "success"<br/>}
```

### **POST /api/traffic/action** (Custom observations)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant Val as Validator
    participant PS as Python Service<br/>Port 8000
    participant Model as RL Model<br/>PPO
    
    Client->>JG: POST /api/traffic/action<br/>{"observations": [0.1, 0.2, ...]}
    
    JG->>Val: Validate observations
    alt Validation Success
        Val-->>JG: ✓ Valid
    else Validation Failed
        Val-->>JG: ✗ Error: Empty/Null
        JG-->>Client: 400 Bad Request
    end
    
    JG->>PS: POST /predict_action<br/>{"obs_data": [0.1, 0.2, ...]}
    
    Note over PS: Process with model
    PS->>Model: Call model.predict()
    Model-->>PS: Return action
    
    PS-->>JG: {"action": 1}
    
    JG-->>Client: {<br/>"predictedAction": 1,<br/>"signalState": "YELLOW",<br/>"timestamp": ...,<br/>"status": "success"<br/>}
```

### **GET /api/traffic/health** (Health Check)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant HealthCheck as Health Checker
    participant PS as Python Service<br/>Port 8000
    
    Client->>JG: GET /api/traffic/health
    
    JG->>HealthCheck: Check all services
    
    HealthCheck->>PS: GET /health
    
    alt Python Service "Up"
        PS-->>HealthCheck: {"status": "healthy"}
        HealthCheck-->>JG: ✓ All healthy
    else Python Service "Down"
        PS--xHealthCheck: Connection refused
        HealthCheck-->>JG: ⚠️ Degraded
    end
    
    JG-->>Client: {<br/>"status": "healthy",<br/>"inferenceService": "up",<br/>"timestamp": ...<br/>}
```

---


## 3. System Component Architecture

```mermaid
graph LR
    subgraph External["External Systems"]
        SUMO["SUMO Simulation"]
        ExtApp["External Applications"]
        Mobile["Mobile/Web Clients"]
    end
    
    subgraph Gateway["API Gateway Layer"]
        REST["REST Controller"]
        ErrorHandler["Error Handler"]
        Logger["Request Logger"]
    end
    
    subgraph ServiceLayer["Service Layer"]
        Client["RL Inference Client"]
        HTTPClient["HTTP Client"]
    end
    
    subgraph InferenceService["Inference Service"]
        FastAPI["FastAPI Application"]
        ModelMgmt["Model Manager"]
        PredictionEngine["Prediction Engine"]
    end
    
    subgraph MLLayer["Machine Learning Layer"]
        PPOModel["PPO Model<br/>stable-baselines3"]
        NeuralNet["Neural Network<br/>Policy & Value"]
    end
    
    subgraph Storage["Storage & Persistence"]
        ModelFiles["Model Files<br/>model.zip"]
        Logs["Application Logs"]
    end
    
    External -->|HTTP Request| Gateway
    Gateway -->|Validate/Log| REST
    Gateway -->|Handle Errors| ErrorHandler
    REST -->|Call Service| Client
    Client -->|Make HTTP Call| HTTPClient
    HTTPClient -->|POST| FastAPI
    FastAPI -->|Manage| ModelMgmt
    FastAPI -->|Execute| PredictionEngine
    PredictionEngine -->|Query| PPOModel
    PPOModel -->|Forward Pass| NeuralNet
    ModelMgmt -->|Load/Store| ModelFiles
    Logger -->|Persist| Logs
    
    style External fill:#e3f2fd
    style Gateway fill:#fff3e0
    style ServiceLayer fill:#f3e5f5
    style InferenceService fill:#e8f5e9
    style MLLayer fill:#fce4ec
    style Storage fill:#eceff1
```

---


## 4. Data Flow Through System

```mermaid
graph TD
    Start["User/SUMO<br/>Request Arrives"]
    
    Start -->|HTTP Request| ParseReq["Parse Request<br/>Method: GET/POST<br/>Endpoint: /api/traffic/action"]
    
    ParseReq -->|GET /action| AutoGen["Generate Dummy<br/>Observations<br/>10 random floats"]
    ParseReq -->|POST /action| ValidateObs["Validate<br/>Custom Observations<br/>Must be 10 floats"]
    
    ValidateObs -->|Invalid| ReturnError400["Return 400<br/>Bad Request"]
    ValidateObs -->|Valid| FwdPython["Forward to<br/>Python Service"]
    
    AutoGen --> CreatePayload["Create Payload<br/>{obs_data: [...]}"]
    CreatePayload --> FwdPython
    
    FwdPython -->|HTTP POST| PythonReceive["Python Service<br/>Receives Request"]
    
    PythonReceive -->|Check Model| ModelLoaded{"Model<br/>Loaded?"}
    
    ModelLoaded -->|No| LoadModel["Load PPO Model<br/>from model.zip"]
    ModelLoaded -->|Yes| UseModel["Use Existing Model"]
    
    LoadModel --> Predict
    UseModel --> Predict["Call Model<br/>model.predict"]
    
    Predict -->|Process| Forward["Forward Pass<br/>Through Neural Network"]
    Forward --> Output["Get Output<br/>Action: 0-3"]
    
    Output -->|Return| ResponsePython["Python Response<br/>{action: n}"]
    
    ResponsePython -->|HTTP Response| JavaGateway["Java Gateway<br/>Receives Response"]
    
    JavaGateway -->|Map Action| MapSignal["Map Action to Signal<br/>0→RED, 1→YELLOW<br/>2→GREEN, 3→GREEN_EXTENDED"]
    
    MapSignal --> BuildResp["Build JSON Response<br/>{predictedAction, signalState,<br/>timestamp, status}"]
    
    BuildResp --> ReturnSuccess["Return 200<br/>Success Response"]
    
    ReturnSuccess --> Client["Response to Client"]
    ReturnError400 --> Client
    
    style Start fill:#e3f2fd
    style AutoGen fill:#fff3e0
    style ValidateObs fill:#fff3e0
    style FwdPython fill:#f3e5f5
    style Forward fill:#fce4ec
    style Output fill:#fce4ec
    style MapSignal fill:#fff3e0
    style Client fill:#e8f5e9
```

---


## 5. Deployment Architecture

```mermaid
graph TB
    Host["Host Machine<br/>Windows/Linux/Mac"]
    
    subgraph DockerEng["Docker Engine"]
        Network["traffic-network<br/>Bridge Network"]
        
        subgraph Container1["Java Gateway Container"]
            JG["Spring Boot App"]
            Config1["Port: 8080<br/>Memory: 512MB<br/>CPU: 1 core"]
        end
        
        subgraph Container2["Python Service Container"]
            PS["FastAPI App<br/>uvicorn"]
            Config2["Port: 8000<br/>Memory: 1GB<br/>CPU: 2 cores"]
        end
        
        subgraph Volume["Persistent Volume"]
            Models["trained_models/<br/>model.zip"]
        end
    end
    
    Host -->|Docker Compose| DockerEng
    Network -->|Connect| Container1
    Network -->|Connect| Container2
    Container1 -->|Mount| Volume
    Container2 -->|Mount| Volume
    
    Container1 -->|Depends On| Container2
    
    style Host fill:#eceff1
    style DockerEng fill:#e1f5ff
    style Container1 fill:#fff3e0
    style Container2 fill:#f3e5f5
    style Volume fill:#e8f5e9
```

---


## 6. Detailed Internal Flow - Action Prediction

```mermaid
graph LR
    subgraph Input["Input Stage"]
        Obs["Observation Vector<br/>10 float values"]
    end
    
    subgraph Processing["Processing Stage"]
        Normalize["Normalize<br/>Convert to numpy array<br/>dtype: float32"]
        ModelInfer["Model Inference<br/>PPO.predict()"]
        Extract["Extract Action<br/>Convert to integer<br/>0, 1, 2, or 3"]
    end
    
    subgraph Mapping["Mapping Stage"]
        Switch{"Action<br/>Value?"}
        A0["0"]
        A1["1"]
        A2["2"]
        A3["3"]
        Default["Other"]
    end
    
    subgraph Output["Output Stage"]
        Red["RED<br/>Stop traffic"]
        Yellow["YELLOW<br/>Caution"]
        Green["GREEN<br/>Allow flow"]
        Extended["GREEN_EXTENDED<br/>Extended green"]
        Unknown["UNKNOWN<br/>Error state"]
    end
    
    Obs --> Normalize
    Normalize --> ModelInfer
    ModelInfer --> Extract
    Extract --> Switch
    Switch -->|0| A0
    Switch -->|1| A1
    Switch -->|2| A2
    Switch -->|3| A3
    Switch -->|Other| Default
    A0 --> Red
    A1 --> Yellow
    A2 --> Green
    A3 --> Extended
    Default --> Unknown
    
    style Obs fill:#e3f2fd
    style Normalize fill:#fff3e0
    style ModelInfer fill:#fce4ec
    style Extract fill:#f3e5f5
    style Red fill:#ffebee
    style Yellow fill:#fff8e1
    style Green fill:#e8f5e9
    style Extended fill:#c8e6c9
    style Unknown fill:#f5f5f5
```

---


## 7. Error Handling Flow

```mermaid
graph TD
    Request["Request<br/>Arrives"]
    
    Request -->|Parse & Validate| Validation{Input<br/>Valid?}
    
    Validation -->|No| BadReq["400<br/>Bad Request<br/>Invalid observations"]
    
    Validation -->|Yes| CanConnect{Python Service<br/>Reachable?}
    
    CanConnect -->|No| Unavail["503<br/>Service Unavailable<br/>Inference service down"]
    
    CanConnect -->|Yes| Predict{Prediction<br/>Success?}
    
    Predict -->|ValueError| BadVal["400<br/>Invalid observation data"]
    
    Predict -->|Network Error| NetErr["503<br/>Service Unavailable<br/>Connection failed"]
    
    Predict -->|Other Exception| ServerErr["500<br/>Internal Server Error<br/>Unexpected error"]
    
    Predict -->|Success| Success["200<br/>OK<br/>Return prediction"]
    
    BadReq --> Response["Send Error Response<br/>with status, message,<br/>timestamp"]
    Unavail --> Response
    BadVal --> Response
    NetErr --> Response
    ServerErr --> Response
    Success --> Response
    Response --> Client["Client<br/>Receives Response"]
    
    style BadReq fill:#ffebee
    style Unavail fill:#fff3e0
    style BadVal fill:#ffebee
    style NetErr fill:#fff3e0
    style ServerErr fill:#ffcdd2
    style Success fill:#e8f5e9
    style Client fill:#eceff1
```

---


## 8. Inter-Service Communication Protocol

```mermaid
graph LR
    subgraph JavaGW["Java Gateway<br/>HTTP Client"]
        Create["Create Request<br/>{obs_data: [...]}"]
        Send["Send POST Request<br/>to http://python:8000"]
        Timeout["Set Timeout<br/>10 seconds"]
        Handle["Handle Response"]
    end
    
    subgraph Network["Network Connection<br/>Docker Bridge"]
        HTTP["HTTP/1.1<br/>Content-Type: application/json"]
    end
    
    subgraph PythonSVC["Python Service<br/>FastAPI"]
        Receive["Receive Request"]
        ValidateInput["Validate Input<br/>Check obs_data"]
        Predict["Call Model"]
        Format["Format Response<br/>{action: n}"]
        ReturnResp["Return JSON<br/>HTTP 200"]
    end
    
    Create --> HTTP
    Send --> HTTP
    Timeout --> HTTP
    HTTP --> Receive
    Receive --> ValidateInput
    ValidateInput --> Predict
    Predict --> Format
    Format --> HTTP
    HTTP --> Handle
    
    style Create fill:#fff3e0
    style HTTP fill:#b3e5fc
    style Receive fill:#f3e5f5
    style Predict fill:#fce4ec
    style Handle fill:#fff3e0
```

---


## 9. Model Loading & Caching Strategy

```mermaid
graph TD
    Start["Python Service<br/>Starts"]
    
    Start -->|startup event| Check{Model in<br/>Memory?}
    
    Check -->|Yes| Use["Use Cached Model"]
    
    Check -->|No| LoadFile["Read Model File<br/>model.zip from disk"]
    
    LoadFile -->|File exists?| Found{File<br/>Found?}
    
    Found -->|No| Error["Log Error<br/>Raise RuntimeError<br/>Startup Fails"]
    
    Found -->|Yes| Parse["Parse ZIP<br/>Extract model data"]
    
    Parse -->|Load via| StableBase["stable-baselines3<br/>PPO.load()"]
    
    StableBase -->|Success| Cache["Cache in Memory<br/>Global variable"]
    
    Cache -->|Ready| Ready["Model Ready<br/>for Predictions"]
    
    Use --> Ready
    
    Ready -->|Request arrives| Predict["Call model.predict()"]
    
    Predict -->|Return| Action["Action value<br/>0, 1, 2, or 3"]
    
    style Start fill:#e3f2fd
    style Check fill:#fff3e0
    style LoadFile fill:#fff3e0
    style Cache fill:#e8f5e9
    style Ready fill:#a5d6a7
    style Predict fill:#fce4ec
    style Action fill:#c8e6c9
```

---


## 10. Complete End-to-End Workflow

```mermaid
graph TB
    Client["🚗 SUMO Simulation/<br/>External Client"]
    
    Step1["1️⃣ Read Traffic Metrics<br/>Queue lengths, waiting times,<br/>vehicle speeds, congestion"]
    
    Step2["2️⃣ Normalize Observations<br/>Convert to 10 feature values<br/>Scale to 0-1 range"]
    
    Step3["3️⃣ Send HTTP Request<br/>POST /api/traffic/action<br/>JSON body: observations"]
    
    Step4["4️⃣ Java Gateway Receives<br/>Validates input<br/>Creates service client"]
    
    Step5["5️⃣ Forward to Python Service<br/>HTTP POST to port 8000<br/>POST /predict_action"]
    
    Step6["6️⃣ Python Service Processes<br/>Loads PPO model if needed<br/>Converts observation to numpy"]
    
    Step7["7️⃣ Model Prediction<br/>Forward pass through neural network<br/>Returns action: 0, 1, 2, or 3"]
    
    Step8["8️⃣ Java Gateway Maps<br/>0→RED, 1→YELLOW<br/>2→GREEN, 3→GREEN_EXTENDED"]
    
    Step9["9️⃣ Format Response<br/>Add timestamp, status<br/>Convert to JSON"]
    
    Step10["🔟 Send Back to Client<br/>HTTP 200 OK<br/>Include signal state"]
    
    Step11["1️⃣1️⃣ Update Traffic Light<br/>Set signal to recommended state<br/>Simulate for next timestep"]
    
    Client --> Step1
    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
    Step5 --> Step6
    Step6 --> Step7
    Step7 --> Step8
    Step8 --> Step9
    Step9 --> Step10
    Step10 --> Step11
    Step11 -->|Next cycle| Step1
    
    style Client fill:#e3f2fd
    style Step1 fill:#fff3e0
    style Step2 fill:#fff3e0
    style Step3 fill:#e1f5fe
    style Step4 fill:#fff3e0
    style Step5 fill:#e1f5fe
    style Step6 fill:#f3e5f5
    style Step7 fill:#fce4ec
    style Step8 fill:#fff3e0
    style Step9 fill:#fff3e0
    style Step10 fill:#e1f5fe
    style Step11 fill:#e8f5e9
```

---

## 11. Architecture Decision Rationale

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Java Gateway** | Spring Boot | Enterprise-grade framework, excellent REST support, easy testing |
| **Python Service** | FastAPI | High performance, automatic API documentation, great async support |
| **ML Library** | stable-baselines3 | Industry standard for PPO, well-tested, robust |
| **Containerization** | Docker | Consistent deployment, easy scaling, isolated environments |
| **Communication** | REST/JSON | Universal, stateless, easy to monitor, language-agnostic |
| **Data Format** | JSON | Human-readable, widely supported, easy serialization |

---

## 12. Performance Characteristics

### **Latency Breakdown** (typical)

```
Total Request Time: ~100-200ms

┌─────────────────────────────────────────────────────┐
│ Total: ~150ms                                       │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐             │
│ │ Java Gateway: ~20ms                 │             │
│ │ - Parse request: 2ms                │             │
│ │ - Validate data: 3ms                │             │
│ │ - HTTP call: 10ms                   │             │
│ │ - Response building: 5ms            │             │
│ └─────────────────────────────────────┘             │
│ ┌─────────────────────────────────────┐             │
│ │ Network: ~10-30ms                   │             │
│ │ - Request transmission: 5ms         │             │
│ │ - Response transmission: 5ms        │             │
│ │ - Latency: 0-20ms                   │             │
│ └─────────────────────────────────────┘             │
│ ┌─────────────────────────────────────┐             │
│ │ Python Service: ~80-120ms           │             │
│ │ - Request parsing: 5ms              │             │
│ │ - Model prediction: 70-100ms        │             │
│ │ - Response formatting: 5ms          │             │
│ └─────────────────────────────────────┘             │
└─────────────────────────────────────────────────────┘
```

### **Throughput** (requests per second)

- **Single instance:** 10-50 RPS (requests per second)
- **With horizontal scaling:** Linear increase with load balancing
- **Bottleneck:** Python model inference (70-100ms per prediction)

### **Resource Usage**

| Service | CPU | Memory | Disk |
|---------|-----|--------|------|
| Java Gateway | 0.1-0.2 cores | 512 MB | 100 MB |
| Python Service | 0.5-1.0 cores | 1-2 GB | 200 MB + model size |
| Model Storage | N/A | N/A | 50-500 MB per model |

---


## 13. Scalability Considerations

### **Horizontal Scaling**

```mermaid
graph TB
    LB["Load Balancer<br/>nginx/haproxy"]
    
    subgraph Gateway["Java Gateway Fleet"]
        JG1["Instance 1"]
        JG2["Instance 2"]
        JG3["Instance N"]
    end
    
    subgraph Python["Python Service Fleet"]
        PS1["Instance 1"]
        PS2["Instance 2"]
        PS3["Instance N"]
    end
    
    Cache["Model Cache<br/>Shared Volume"]
    
    LB -->|Round Robin| JG1
    LB -->|Round Robin| JG2
    LB -->|Round Robin| JG3
    
    JG1 -->|Load Balanced| PS1
    JG2 -->|Load Balanced| PS2
    JG3 -->|Load Balanced| PS3
    
    PS1 -->|Read| Cache
    PS2 -->|Read| Cache
    PS3 -->|Read| Cache
    
    style LB fill:#ffeb3b
    style Cache fill:#e8f5e9
```

### **Vertical Scaling**

- Increase container memory (Python: 1GB → 4GB)
- Increase CPU allocation (Java: 1 core → 4 cores)
- Use GPU acceleration for Python service (CUDA-enabled Docker)

---

## 14. Security Architecture

```mermaid
graph TB
    Client["External Client"]
    Firewall["Firewall<br/>Allow 8080"]
    
    subgraph DMZ["DMZ"]
        Gateway["Java Gateway<br/>8080 exposed"]
    end
    
    subgraph Private["Private Network"]
        Python["Python Service<br/>8000 internal only"]
        Storage["Model Storage<br/>Internal access only"]
    end
    
    Client -->|Port 8080| Firewall
    Firewall -->|Allow| Gateway
    Gateway -->|Internal network| Python
    Python -->|Read only| Storage
    
    style Firewall fill:#ffebee
    style Gateway fill:#fff3e0
    style Python fill:#f3e5f5
    style Storage fill:#e8f5e9
```

---

## 15. Monitoring & Observability Points

```mermaid
graph LR
    subgraph Metrics["Metrics"]
        RPS["Requests/sec"]
        Latency["Latency (ms)"]
        ErrorRate["Error Rate (%)"]
        Memory["Memory Usage"]
        CPU["CPU Usage"]
    end
    
    subgraph Logs["Logs"]
        RequestLog["Request Logs"]
        ErrorLog["Error Logs"]
        ModelLog["Model Logs"]
        ServiceLog["Service Logs"]
    end
    
    subgraph Health["Health Checks"]
        JavaHealth["Java Gateway<br>/api/traffic/health"]
        PythonHealth["Python Service<br>/health"]
        ModelHealth["Model Status"]
    end
    
    subgraph Alerting["Alerts"]
        HighLatency["High Latency"]
        ServiceDown["Service Down"]
        ErrorSpike["Error Spike"]
        ResourceLow["Low Resources"]
    end
    
    Metrics --> Alerting
    Logs --> Alerting
    Health --> Alerting
    
    style Metrics fill:#fff3e0
    style Logs fill:#f3e5f5
    style Health fill:#e8f5e9
    style Alerting fill:#ffebee
```

---

## 16. Deployment Patterns

### **Development**
```
Local Machine
├── Java Gateway: localhost:8080
└── Python Service: localhost:8000
```

### **Testing**
```
Docker Compose (Single Host)
├── Java Gateway Container: 8080
└── Python Service Container: 8000
```

### **Production (Cloud)**
```
Kubernetes Cluster
├── Service Mesh (Istio)
├── Load Balancer
├── Java Gateway Pods (3+)
├── Python Service Pods (2+)
├── Model Persistent Volume
└── Monitoring Stack
```

---
