#!/usr/bin/env python3
"""
Model Selector Utility
Helps identify and copy the best trained model to the RL Inference Service
"""

import os
import shutil
import json
from pathlib import Path
from typing import List, Tuple

RESULTS_BASE = Path(__file__).parent.parent / "Results"


def find_all_models() -> List[Tuple[str, Path]]:
    """Find all available trained models in the results directory."""
    models = []
    
    # Look for sweeps directories
    for sweep_dir in sorted(RESULTS_BASE.glob("sweeps*")):
        if not sweep_dir.is_dir():
            continue
            
        # Search for model.zip files
        for model_file in sweep_dir.rglob("model.zip"):
            # Create a friendly name from the path
            relative_path = model_file.relative_to(RESULTS_BASE)
            friendly_name = str(relative_path).replace("\\", "/")
            models.append((friendly_name, model_file))
    
    return models


def get_sweep_info(model_path: Path) -> dict:
    """Extract information about the sweep from model path."""
    parts = model_path.parts
    
    info = {
        "path": str(model_path),
        "sweep": None,
        "metric": None,
        "seed": None,
        "variant": None
    }
    
    # Parse path structure: Results/sweeps_X/metric_name/seed_Y/variant/model.zip
    if len(parts) >= 5:
        info["sweep"] = parts[1]  # sweeps, sweeps_2, etc.
        info["metric"] = parts[2]  # pressure, queue, etc.
        info["seed"] = parts[3]     # seed_42, etc.
        info["variant"] = parts[4]  # A, B, C, etc.
    
    return info


def display_models(models: List[Tuple[str, Path]]) -> None:
    """Display available models."""
    if not models:
        print("No trained models found in the Results directory.")
        return
    
    print(f"\nFound {len(models)} trained models:\n")
    print(f"{'#':<3} {'Path':<60} {'Metric':<12} {'Seed':<10}")
    print("-" * 85)
    
    for idx, (friendly_name, model_path) in enumerate(models, 1):
        info = get_sweep_info(model_path)
        print(f"{idx:<3} {friendly_name:<60} {info['metric']:<12} {info['seed']:<10}")


def select_model(models: List[Tuple[str, Path]]) -> Tuple[int, Path]:
    """Let user select a model."""
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(models)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None, None
            
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(models):
                return choice_idx, models[choice_idx][1]
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(models)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")


def copy_model(source_path: Path, destination_dir: Path) -> bool:
    """Copy model file to destination directory."""
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        dest_file = destination_dir / "model.zip"
        
        print(f"\nCopying model from: {source_path}")
        print(f"Copying model to:   {dest_file}")
        
        shutil.copy2(source_path, dest_file)
        
        print(f"✓ Model copied successfully!")
        return True
    except Exception as e:
        print(f"✗ Error copying model: {e}")
        return False


def main():
    """Main function."""
    print("=" * 85)
    print("AI Traffic Control API - Model Selector")
    print("=" * 85)
    
    # Find all available models
    models = find_all_models()
    
    if not models:
        print("\nNo trained models found in the Results directory.")
        print(f"Expected location: {RESULTS_BASE}")
        return
    
    # Display models
    display_models(models)
    
    # Let user select a model
    idx, selected_model = select_model(models)
    
    if selected_model is None:
        print("Cancelled.")
        return
    
    # Confirm selection
    info = get_sweep_info(selected_model)
    print(f"\nSelected model:")
    print(f"  Sweep:   {info['sweep']}")
    print(f"  Metric:  {info['metric']}")
    print(f"  Seed:    {info['seed']}")
    print(f"  Variant: {info['variant']}")
    print(f"  Path:    {selected_model}")
    
    confirm = input("\nCopy this model to the API service? (y/n): ").strip().lower()
    
    if confirm == 'y':
        api_models_dir = Path(__file__).parent / "rl-inference-service" / "app" / "trained_models"
        
        if copy_model(selected_model, api_models_dir):
            print(f"\nModel is ready! You can now start the API services.")
            print(f"Location: {api_models_dir / 'model.zip'}")


if __name__ == "__main__":
    main()
