import logging
import os
from pathlib import Path
from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from stable_baselines3 import PPO

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
    confidence: float = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_path: str


# Global model variable
model = None
model_path = None


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
        
        model = PPO.load(model_path)
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
