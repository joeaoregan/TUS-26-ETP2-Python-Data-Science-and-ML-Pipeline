To use different trained models:

1. **Locate your model:**

   ```
   C:\Users\gemer\Sumo\my-network\Results\sweeps_*\<sweep_name>\seed_*\<variant>\model.zip
   
   Examples:
   - Results\sweeps\pressure\seed_42\A\model.zip
   - Results\sweeps\queue\seed_123\B\model.zip
   - Results\sweeps_2\diff-waiting-time\seed_7\C\model.zip
   ```

2. **Copy to models directory:**

   ```bash
   copy "<source_path>\model.zip" "rl-inference-service\app\trained_models\model.zip"
   ```

3. **Rebuild and restart:**

   ```bash
   docker-compose up --build
   ```