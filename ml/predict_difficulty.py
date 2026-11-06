import joblib
import pandas as pd

from pathlib import Path


MODEL_PATH = Path(__file__).parent / "difficulty_model.pkl"


def predict_difficulty(rows, cols, obstacle_density):

    # Load trained model
    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    features = saved_data["features"]

    # Prepare input
    maze_data = pd.DataFrame(
        [[rows, cols, obstacle_density]],
        columns=features
    )

    # Predict difficulty
    prediction = model.predict(maze_data)

    return prediction[0]


if __name__ == "__main__":

    test_cases = [
        (10, 10, 0.10),
        (15, 15, 0.25),
        (20, 20, 0.35),
        (12, 18, 0.20),
        (18, 12, 0.30)
    ]

    for rows, cols, density in test_cases:

        result = predict_difficulty(
            rows,
            cols,
            density
        )

        print(
            f"Maze: {rows}x{cols} | "
            f"Obstacle Density: {density} | "
            f"Predicted Difficulty: {result}"
        )