# test_visualization.py
import pytest
import numpy as np
from src.visualization import visualize_system

def test_visualize_system():
    positions = {
        "Earth": [np.array([1.5e11, 0]), np.array([1.5e11, 1e7])],
        "Sun": [np.array([0, 0]), np.array([0, 0])]
    }
    try:
        visualize_system(positions)
    except Exception as e:
        pytest.fail(f"Visualization failed with exception: {e}")
