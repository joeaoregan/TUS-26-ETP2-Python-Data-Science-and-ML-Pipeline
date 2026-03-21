# Changelog
All notable changes to the AI-Driven Predictive Traffic Flow Optimisation System will be documented in this file.

## [1.0.0] - 2026-03-21
### Added
- **Microservices Architecture:** Integrated Java Spring Boot API Gateway and Python RL-Inference service.
- **ML Pipeline:** Support for PPO (Proximal Policy Optimization) model inference.
- [cite_start]**Simulation Environment:** Integrated SUMO (Simulation of Urban MObility) configurations for the Athlone "Orange Loop"[cite: 101, 161, 424].

### Changed
- [cite_start]**Monorepo Consolidation:** Merged standalone API branch into the main branch to establish a cohesive pipeline[cite: 64, 455].
- **Dependency Management:** Updated Python requirements to include FastAPI, Pydantic v2, and Stable-Baselines3.

### Security
- [cite_start]**Data Integrity:** Initial implementation of TLS 1.3 for telemetry ingestion[cite: 424].
- [cite_start]**Authentication:** Added digital signature placeholders in `OpenApiConfig.java` to prevent data injection attacks[cite: 43, 63, 500].