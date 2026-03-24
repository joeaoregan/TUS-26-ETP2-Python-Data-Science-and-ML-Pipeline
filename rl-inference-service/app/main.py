import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from gymnasium import spaces
from pydantic import BaseModel, ConfigDict
from stable_baselines3 import PPO
from stable_baselines3.common.save_util import load_from_zip_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models
class Observation(BaseModel):
    obs_data: List[float]


class PredictionResponse(BaseModel):
    action: int
    confidence: Optional[float] = None


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_loaded: bool
    model_path: str


# Global model variable
model = None
model_path = None


def register_numpy_compat_aliases():
    """Register NumPy module aliases expected by pickled model metadata."""
    try:
        import numpy._core as numpy_private_core
        import numpy._core.numeric as numpy_private_numeric

        sys.modules.setdefault("numpy._core", numpy_private_core)
        sys.modules.setdefault("numpy._core.numeric", numpy_private_numeric)
        return
    except ModuleNotFoundError:
        pass

    import numpy.core as numpy_core
    import numpy.core.numeric as numpy_core_numeric

    sys.modules.setdefault("numpy._core", numpy_core)
    sys.modules.setdefault("numpy._core.numeric", numpy_core_numeric)


def patch_numpy_bit_generator_ctor():
    """Support models pickled with NumPy versions that serialize BitGenerator classes."""
    import numpy.random._pickle as numpy_random_pickle

    original_ctor = numpy_random_pickle.__bit_generator_ctor
    if getattr(original_ctor, "_ai_traffic_patched", False):
        return

    def compat_ctor(bit_generator_name='MT19937'):
        if isinstance(bit_generator_name, type) and issubclass(bit_generator_name, np.random.BitGenerator):
            return bit_generator_name()
        return original_ctor(bit_generator_name)

    compat_ctor._ai_traffic_patched = True
    numpy_random_pickle.__bit_generator_ctor = compat_ctor


def build_model_custom_objects(observation_dim: int, action_dim: int):
    """Provide explicit objects for model metadata that may not deserialize cross-version."""
    observation_space = spaces.Box(
        low=0.0,
        high=1.0,
        shape=(observation_dim,),
        dtype=np.float32,
    )
    action_space = spaces.Discrete(action_dim)

    def constant_schedule(_progress_remaining):
        return 0.0

    return {
        "observation_space": observation_space,
        "action_space": action_space,
        "lr_schedule": constant_schedule,
        "clip_range": constant_schedule,
    }


def infer_model_dimensions(model_path: str, observation_shape_dim: int, num_agents: int):
    """Infer observation and action dimensions from saved PPO weights when metadata is incompatible."""
    default_observation_dim = observation_shape_dim * max(num_agents, 1)
    default_action_dim = 4

    try:
        _, params, _ = load_from_zip_file(
            model_path,
            custom_objects={
                "observation_space": None,
                "action_space": None,
                "lr_schedule": None,
                "clip_range": None,
            },
        )
    except Exception as exc:
        logger.warning("Falling back to configured dimensions because model introspection failed: %s", exc)
        return default_observation_dim, default_action_dim

    policy_params = params.get("policy", {})
    policy_weight = policy_params.get("mlp_extractor.policy_net.0.weight")
    action_bias = policy_params.get("action_net.bias")

    inferred_observation_dim = int(policy_weight.shape[1]) if policy_weight is not None else default_observation_dim
    inferred_action_dim = int(action_bias.shape[0]) if action_bias is not None else default_action_dim

    return inferred_observation_dim, inferred_action_dim


def load_model():
    """Load the trained PPO model at startup."""
    global model, model_path
    
    # Get model path from environment variable
    model_path = os.getenv('MODEL_PATH', './app/models/my_ppo_model.zip')
    observation_shape_dim = int(os.getenv('OBSERVATION_SHAPE_DIM', '10'))
    num_agents = int(os.getenv('NUM_AGENTS', '1'))
    
    logger.info(f"Attempting to load model from: {model_path}")
    logger.info(f"Observation shape dimension: {observation_shape_dim}")
    logger.info(f"Number of agents: {num_agents}")
    
    try:
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        register_numpy_compat_aliases()
        patch_numpy_bit_generator_ctor()
        inferred_observation_dim, inferred_action_dim = infer_model_dimensions(
            model_path,
            observation_shape_dim,
            num_agents,
        )
        logger.info(
            "Using model dimensions: observation_dim=%s, action_dim=%s",
            inferred_observation_dim,
            inferred_action_dim,
        )
        custom_objects = build_model_custom_objects(
            inferred_observation_dim,
            inferred_action_dim,
        )
        model = PPO.load(model_path, custom_objects=custom_objects)
        logger.info(f"Model loaded successfully from {model_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise RuntimeError(f"Failed to load model at startup: {str(e)}")


# Initialize FastAPI app
app = FastAPI(
    title="RL Inference API",
    description="REST API for traffic signal control using trained RL model",
    version="1.0.0"
)


# mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    try:
        load_model()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_path=model_path or "not set"
    )


@app.post("/predict_action", response_model=PredictionResponse)
async def predict_action(observation: Observation):
    """
    Predict action for given observation.
    
    Args:
        observation: Observation data containing obs_data as a list of floats
        
    Returns:
        PredictionResponse with predicted action
    """
    if model is None:
        logger.error("Model not loaded when predict_action was called")
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Service may not be properly initialized."
        )
    
    try:
        # Convert observation data to numpy array
        obs_array = np.array(observation.obs_data, dtype=np.float32)
        expected_observation_dim = int(model.observation_space.shape[0])

        if obs_array.size != expected_observation_dim:
            raise ValueError(
                f"Expected {expected_observation_dim} observation values but received {obs_array.size}"
            )
        
        logger.info(f"Received observation shape: {obs_array.shape}")
        
        # Reshape if necessary
        if obs_array.ndim == 1:
            obs_array = obs_array.reshape(1, -1)
        
        # Get prediction from model
        action, _states = model.predict(obs_array, deterministic=True)
        
        # Extract the predicted action
        predicted_action = int(action[0]) if isinstance(action, np.ndarray) else int(action)
        
        logger.info(f"Predicted action: {predicted_action}")
        
        return PredictionResponse(
            action=predicted_action,
            confidence=None
        )
    except ValueError as e:
        logger.error(f"Value error during prediction: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid observation data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during prediction: {str(e)}"
        )


@app.get("/model_info")
async def get_model_info():
    """Get information about the loaded model."""
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded"
        )
    
    try:
        return {
            "model_type": "PPO",
            "model_path": model_path,
            "observation_space": str(model.observation_space),
            "action_space": str(model.action_space),
            "action_space_shape": model.action_space.shape if hasattr(model.action_space, 'shape') else "N/A",
            "policy_type": type(model.policy).__name__
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model info: {str(e)}"
        )
    

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI Inference Service</title>
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 min-h-screen flex items-center justify-center p-6">
        <div class="max-w-md w-full bg-slate-800 rounded-3xl shadow-2xl border border-slate-700 p-10 text-center">
            <img src="/static/logo.png" alt="Inference Engine Logo" class="mx-auto mb-8 max-w-[200px] h-auto opacity-90">
            
            <h1 class="text-2xl font-black tracking-tight mb-2">AI Inference Engine</h1>
            <p class="text-indigo-400 font-mono text-xs uppercase tracking-widest mb-8 text-semibold">
                Status: Operational &bull; Region: Frankfurt
            </p>

            <div class="space-y-3">
                <a href="/docs" class="block w-full bg-indigo-600 hover:bg-indigo-500 py-4 rounded-2xl font-bold transition-all shadow-lg shadow-indigo-500/20">
                    View API Documentation
                </a>
                <a href="/health" class="block w-full bg-slate-700 hover:bg-slate-600 py-4 rounded-2xl font-bold transition-all">
                    System Health Check
                </a>
            </div>

            <footer class="mt-10 pt-6 border-t border-slate-700">
                <p class="text-[10px] text-slate-500 uppercase font-medium tracking-tighter">
                    2026 Joe O'Regan • Edgars Peskaitis • David Claffey • Adam O Neill Mc Knight &bull; TUS Engineering Team Project
                </p>
            </footer>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv('API_RELOAD', 'false').lower() == 'true'
    )
