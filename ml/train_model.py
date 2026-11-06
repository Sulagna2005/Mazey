
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "maze_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "difficulty_model.pkl"


def train_model():

    # 1. Load dataset
    print("Loading maze dataset...")

    df = pd.read_csv(DATA_PATH)

    # 2. Data preprocessing
    features = [
        "rows",
        "cols",
        "obstacle_density"
    ]

    target = "difficulty"

    df = df.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    print(f"Dataset records: {len(df)}")
    print("\nClass distribution:")
    print(y.value_counts())

    # 3. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(f"\nTraining records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")

    # 4. Initialize Decision Tree
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    )

    # 5. Train model
    print("\nTraining Decision Tree model...")

    model.fit(X_train, y_train)

    # 6. Make predictions
    predictions = model.predict(X_test)

    # 7. Evaluation
    accuracy = accuracy_score(y_test, predictions)

    print("\n========== MODEL EVALUATION ==========")

    print(f"\nAccuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=model.classes_,
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions,
            labels=model.classes_
        )
    )

    # 8. Feature importance
    print("\nFeature Importance:")

    for name, importance in zip(
        features,
        model.feature_importances_
    ):
        print(f"{name}: {importance:.4f}")

    # 9. Save trained model
    joblib.dump(
        {
            "model": model,
            "features": features
        },
        MODEL_PATH
    )

    print(f"\nModel saved successfully: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()