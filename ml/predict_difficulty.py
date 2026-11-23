
import joblib
import pandas as pd
import sys
from pathlib import Path


# ---------------- RESOURCE PATH ----------------

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


# ---------------- MODEL SETTINGS ----------------

MODEL_PATH = resource_path("ml/difficulty_model.pkl")


# ---------------- DIFFICULTY PREDICTION ----------------

def predict_difficulty(
    rows,
    cols,
    obstacle_density,
    dead_end_ratio,
    average_connectivity,
    junction_ratio
):

    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    features = saved_data["features"]

    maze_data = pd.DataFrame(
        [[
            rows,
            cols,
            obstacle_density,
            dead_end_ratio,
            average_connectivity,
            junction_ratio
        ]],
        columns=features
    )

    prediction = model.predict(maze_data)

    return prediction[0]
