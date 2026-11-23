import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "difficulty_model.pkl"


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