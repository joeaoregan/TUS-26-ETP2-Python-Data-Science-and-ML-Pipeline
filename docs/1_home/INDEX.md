# AI-Driven Predictive Traffic Flow Optimisation System

<h2>Engineering Team Project | TUS Athlone</h2>

![Java 17](https://img.shields.io/badge/Java-17-blue)
![Python 3.9](https://img.shields.io/badge/Python-3.9-green)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2.3-6DB33F?logo=spring-boot&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Research-success)

![GitHub repo size](https://img.shields.io/github/repo-size/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=blue)
![GitHub top language](https://img.shields.io/github/languages/top/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation)
![Stars](https://img.shields.io/github/stars/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?style=social)

---

### 🔗 Quick Links

#### 🌐 API Gateway: 

- [API Gateway App](https://ai-traffic-control-api.onrender.com/)
- [Swagger UI Docs](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)

#### 🤖 Inference Service:

- [Inference Service App](https://traffic-inference-service.onrender.com)
- [Swagger UI Docs](https://traffic-inference-service.onrender.com/docs)

---

### 👥 Research Team

> - [Joe O'Regan](https://github.com/joeaoregan)
> - [Adam O Neill Mc Knight](https://github.com/AdamQ45)
> - [David Claffey](https://github.com/dclaff)
> - [Edgars Peskaitis](https://github.com/edgar183)

---

## 📈 Performance Targets

> **Project Goal:** Target 15-20% reduction in urban traffic congestion for the Athlone "Orange Loop" using Reinforcement Learning.

> - **Average Travel Time (ATT):** Target -15%
> - **Mean Queue Length (MQL):** Target -20%
> - **Data Integrity:** TLS 1.3 secured telemetry pipeline

---

## 🏗️ System Architecture

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study. 

- **Traffic Monitoring Gateway (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication.
- **RL-Inference Service (Python/FastAPI):** Hosts a trained **PPO (Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic density.
- **Simulation Layer (SUMO):** Integrated high-fidelity environment for testing adaptive signal logic against baseline fixed-time controllers.

This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management in regional Irish hubs.

*For more details see [System Architecture](../SYSTEM_ARCHITECTURE.md) page.*
