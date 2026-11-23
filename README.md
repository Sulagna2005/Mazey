# 🧩 Mazey – Smart Maze Solver

**An interactive maze-solving application powered by the A* Search Algorithm and Machine Learning-based difficulty prediction.**

Mazey is a Python-based Smart Maze Solver that generates solvable mazes, predicts their difficulty using a Machine Learning model, and finds optimal paths using the A* Search Algorithm.

It combines Artificial Intelligence, Machine Learning, and interactive visualization through a user-friendly Pygame interface.

---

## ✨ Features

### 1. 🧠 A* Pathfinding Algorithm
- Finds the shortest path from the starting point to the goal.
- Uses Manhattan Distance as its heuristic function.
- Explores neighbouring cells while avoiding obstacles.
- Detects unreachable destinations.
- Supports step-by-step search visualization.

### 2. 🎮 Interactive Pygame Interface
- Interactive graphical interface with a custom pastel-themed design.
- Dynamic maze generation.
- Adjustable maze rows and columns.
- Adjustable obstacle density.
- Animated maze generation and pathfinding.
- Animated mascot that follows the solution path.
- Visual representation of explored cells and the final path.
- Real-time performance statistics.

### 3. 🤖 Machine Learning-Based Difficulty Prediction
- Generates synthetic maze datasets.
- Extracts relevant maze characteristics.
- Trains a Decision Tree classification model.
- Predicts maze difficulty as:
  - Easy
  - Medium
  - Hard
- Predicts difficulty independently of the A* pathfinding algorithm.

### 4. 📊 Performance Evaluation
The project evaluates both the pathfinding algorithm and the Machine Learning model.

**A* Evaluation Metrics**
- Path Length
- Execution Time
- Nodes Explored
- Path Validity
- Path Optimality

**Machine Learning Evaluation Metrics**
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Cross-Validation Accuracy

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pygame | Graphical interface and visualization |
| A* Search | Optimal pathfinding |
| NumPy | Numerical operations |
| Pandas | Dataset processing |
| Scikit-learn | Machine Learning |
| Joblib | Model serialization |
| Matplotlib | Data visualization |
| Git & GitHub | Version control and collaboration |
| PyInstaller | Windows executable packaging |

---

## 📂 Project Structure

```text
Mazey/
│
├── algorithms/
│   ├── __init__.py
│   └── astar.py
│
├── data/
│   ├── maze_generator.py
│   ├── dataset_generator.py
│   ├── maze_dataset.csv
│   └── astar_evaluation_results.csv
│
├── evaluation/
│   └── evaluate_astar.py
│
├── interface/
│   ├── __init__.py
│   ├── app.py
│   ├── components.py
│   ├── maze_renderer.py
│   ├── theme.py
│   └── assets/
│       ├── fonts/
│       ├── mazey.ico
│       ├── mazey_logo.png
│       └── mazey_mascot.png
│
├── ml/
│   ├── train_model.py
│   ├── predict_difficulty.py
│   └── difficulty_model.pkl
│
├── tests/
│   └── test_astar.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or above
- pip package manager
- Git
- Windows, Linux, or macOS for running from source (platform-specific setup may be required)

### 1. Clone the Repository

```bash
git clone https://github.com/Sulagna2005/Mazey.git
```

### 2. Navigate to the Project Directory

```bash
cd Mazey
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Launch the Graphical Application

```bash
python -m interface.app
```

### 7. Run the Command-Line Version

```bash
python main.py
```

---

## 🎮 How to Use Mazey

1. Launch the graphical application.
2. Adjust the number of rows and columns to change the maze dimensions.
3. Adjust obstacle density using the slider.
4. Click **Generate Maze** to create a new solvable maze.
5. View the predicted difficulty level.
6. Click **Solve Maze** to start the A* search animation.
7. Watch the mascot navigate the solution path.
8. View the performance statistics displayed by the application.
9. Use **Reset** or **Clear** to manage the current maze.

---

## 🔍 How It Works

### 1. Maze Generation

Mazey generates random maze grids containing walkable cells and obstacles.

A solvability check ensures that a valid route exists between the starting point and the destination. If repeated random attempts fail, a fallback mechanism carves a guaranteed walkable route.

### 2. A* Search Algorithm

A* is an informed search algorithm that finds an optimal path by evaluating:

**f(n) = g(n) + h(n)**

Where:

- `g(n)` = Actual cost from the starting point to the current node.
- `h(n)` = Estimated cost from the current node to the goal.
- `f(n)` = Estimated total path cost.

Mazey uses the Manhattan Distance heuristic:

**h(n) = |x₁ - x₂| + |y₁ - y₂|**

The algorithm explores promising neighbouring cells until it reaches the destination or determines that no path exists.

### 3. Machine Learning-Based Difficulty Prediction

Mazey uses a Decision Tree classifier to predict the difficulty of generated mazes.

The model uses features including:

- Number of rows and columns
- Obstacle density
- Dead-end ratio
- Average connectivity
- Junction ratio

The model classifies each maze into Easy, Medium, or Hard.

**Important:** Machine Learning is used only for difficulty prediction. It does not replace or modify the A* pathfinding algorithm.

---

## 📊 Model and Algorithm Evaluation

### A* Algorithm Evaluation

The A* implementation was tested on 100 generated solvable mazes.

| Metric | Result |
|---|---:|
| Mazes Tested | 100 |
| Successful Solutions | 100/100 |
| Valid Paths | 100/100 |
| Optimal Paths | 100/100 |
| Average Path Length | 28.52 |
| Average Nodes Explored | 119.54 |
| Average Execution Time | ~0.40 ms |

### Machine Learning Model Evaluation

The Decision Tree classifier was evaluated using an 80:20 training and testing split.

| Metric | Result |
|---|---:|
| Training Samples | 800 |
| Testing Samples | 200 |
| Test Accuracy | 91.00% |
| Macro F1-Score | 91.11% |
| 5-Fold Cross-Validation Accuracy | 94.40% ± 1.24% |

*Note: Execution time and model evaluation results may vary depending on the environment and dataset.*

---

## 🖥️ Windows Application

Mazey is also packaged as a standalone Windows application using PyInstaller.

The packaged application includes the required Python dependencies, assets, fonts, and trained Machine Learning model.

**To run the Windows application:**

1. Download the Windows ZIP package from the repository's GitHub Releases page (when published).
2. Extract the ZIP file.
3. Open the extracted `Mazey` folder.
4. Double-click `Mazey.exe`.

No separate Python installation is required to run the packaged application.

**Important:** Keep the complete extracted `Mazey` folder together. Do not move the executable away from its accompanying `_internal` folder.

---

## 👥 Team Collaboration

Mazey is developed collaboratively using Git and GitHub.

Development responsibilities include:

- **AI and Algorithm Development:** A* implementation, heuristic functions, maze-solving logic, and algorithm evaluation.
- **Machine Learning Development:** Dataset generation, feature extraction, model training, and difficulty prediction.
- **Interface Development:** Pygame interface, maze visualization, animations, and user interactions.
- **Integration:** Combining the pathfinding algorithm, Machine Learning model, and graphical interface.

Development is managed through Git branches and Pull Requests.

---

## 🚀 Project Status

**Core application implemented and Windows build tested.**

Current capabilities include:
- A* maze solving.
- Machine Learning-based difficulty prediction.
- Interactive Pygame interface.
- Animated maze visualization.
- Performance evaluation.
- Standalone Windows application.

---

## 📜 License

This project is developed for academic and educational purposes.