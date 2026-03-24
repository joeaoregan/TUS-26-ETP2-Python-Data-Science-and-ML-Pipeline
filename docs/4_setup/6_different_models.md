# 💾 Using Different Models

## Option 1: Interactive Selector
```bash
python select_model.py
```

## Option 2: Manual Copy
```bash
# Copy your chosen model
copy "C:\Users\gemer\Sumo\my-network\Results\sweeps\pressure\seed_42\A\model.zip" \
     "rl-inference-service\app\trained_models\model.zip"

# Rebuild and start
docker-compose up --build
```

## Available Models
```
Results/
├── sweeps/
│   └── pressure/
│       ├── seed_42/  → A, B, C models
│       ├── seed_123/ → A, B, C models
│       └── seed_7/   → A, B, C models
├── sweeps_2/ through sweeps_9/
│   └── (similar structure)
└── (other directories: queue, diff-waiting-time, etc.)
```