# 🚀 Quick Start (5 Minutes)

## Step 1: Select Your Model
```bash
python select_model.py
```
This interactive tool will help you:
- Browse all trained models in `Results/sweeps*`
- Select the best model
- Copy it to the API service

Available models from your sweeps:
- **Locations:** `C:\Users\gemer\Sumo\my-network\Results\sweeps*\`
- **Sweeps:** pressure, queue, diff-waiting-time
- **Seeds:** seed_42, seed_123, seed_7, etc.
- **Variants:** A, B, C

## Step 2: Start Services
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

## Step 3: Test the API
```bash
# Get a prediction with auto-generated observations
curl http://localhost:8080/api/traffic/action

# Or run comprehensive tests
python test_api.py
```