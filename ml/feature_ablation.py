
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

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
    "Obstacle density only": ["obstacle_density"]
}

X_train_base, X_test_base, y_train, y_test = train_test_split(
    df[all_features],
    df["difficulty"],
    test_size=0.20,
    random_state=42,
    stratify=df["difficulty"]
)

print("\n========== FEATURE ABLATION TEST ==========")

for name, features in feature_sets.items():

    X_train = X_train_base[features]
    X_test = X_test_base[features]

    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")

    print(f"\n{name}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Macro F1: {macro_f1 * 100:.2f}%")

print("\n============================================")
