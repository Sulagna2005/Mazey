
import pandas as pd

from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "maze_dataset.csv"

df = pd.read_csv(DATA_PATH)

all_features = [
    "rows",
    "cols",
    "obstacle_density",
    "dead_end_ratio",
    "average_connectivity",
    "junction_ratio"
]

feature_sets = {
    "Full model": all_features,

    "Without obstacle density": [
        feature for feature in all_features
        if feature != "obstacle_density"
    ],

    "Obstacle density only": [
        "obstacle_density"
    ]
}

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

print("\n========== 5-FOLD CROSS-VALIDATION ==========")

for name, features in feature_sets.items():

    X = df[features]
    y = df["difficulty"]

    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    )

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=["accuracy", "f1_macro"]
    )

    accuracy = scores["test_accuracy"]
    macro_f1 = scores["test_f1_macro"]

    print(f"\n{name}")

    print(
        f"Accuracy: {accuracy.mean() * 100:.2f}% "
        f"(+/- {accuracy.std() * 100:.2f}%)"
    )

    print(
        f"Macro F1: {macro_f1.mean() * 100:.2f}% "
        f"(+/- {macro_f1.std() * 100:.2f}%)"
    )

print("\n=============================================")