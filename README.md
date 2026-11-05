# 🧩 Mazey – Smart Maze Solver

**An intelligent maze-solving application powered by the A* Search Algorithm and Machine Learning.**

Mazey is a Python-based maze-solving system designed to find the shortest path between a starting point and a destination while navigating through obstacles. It combines the A* Search Algorithm with a Machine Learning-based difficulty prediction system to provide an interactive and intelligent maze-solving experience.

---

## 🎯 Project Objectives

- Implement the A* Search Algorithm to find optimal paths through mazes.
- Use Manhattan Distance as the heuristic function.
- Visualize maze exploration and shortest-path discovery.
- Predict maze difficulty using a Machine Learning model.
- Evaluate algorithm performance using standard evaluation metrics.

## ✨ Key Features

### 1. A* Pathfinding
- Intelligent shortest-path search.
- Manhattan Distance heuristic.
- Obstacle detection and avoidance.
- Exploration of neighbouring cells.
- Detection of unreachable destinations.

### 2. Interactive Maze Visualization
- Graphical maze representation using Pygame.
- Visual distinction between obstacles, explored cells and final paths.
- Start and destination markers.
- Interactive maze controls.

### 3. Machine Learning-Based Difficulty Prediction
- Generate maze datasets.
- Extract relevant maze features.
- Train a Decision Tree classification model.
- Classify mazes into Easy, Medium and Hard categories.

### 4. Performance Evaluation
- Path Length
- Execution Time
- Nodes Explored
- Path Validity
- Model Accuracy
- Precision
- Recall
- F1-Score

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pygame | Graphical visualization |
| A* Search | Shortest-path algorithm |
| NumPy | Numerical operations |
| Pandas | Dataset processing |
| Scikit-learn | Machine Learning |
| Matplotlib | Data visualization |
| Git & GitHub | Version control and collaboration |

---

## 📂 Project Structure

```text
Mazey/
│
├── algorithms/
│   ├── __init__.py
│   └── astar.py
│
├── ml/
│   ├── dataset_generator.py
│   ├── train_model.py
│   └── predictor.py
│
├── interface/
│   ├── __init__.py
│   ├── grid.py
│   └── buttons.py
│
├── data/
│
├── tests/
│   └── test_astar.py
│
├── main.py
├── config.py
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
- Visual Studio Code (recommended)

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

**Windows:**

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python main.py
```

*Note: Application execution instructions will be updated as development progresses.*

---

## 🧠 How It Works

### A* Search Algorithm

Mazey uses the A* Search Algorithm to find the shortest path through a maze.

It calculates the estimated total cost using:

**f(n) = g(n) + h(n)**

Where:

- `g(n)` = Actual cost from the starting point to the current node.
- `h(n)` = Estimated cost from the current node to the destination.
- `f(n)` = Estimated total path cost.

The Manhattan Distance heuristic is used:

**h(n) = |x₁ - x₂| + |y₁ - y₂|**

### Machine Learning Model

A separate Decision Tree classifier analyses maze characteristics, such as grid size and obstacle density, to predict maze difficulty.

The ML component operates independently and does not modify the A* pathfinding algorithm.

---

## 📊 Evaluation Methodology

The project will be evaluated through the following parameters:

**A* Algorithm Evaluation**
- Path length
- Execution time
- Number of explored nodes
- Path validity and optimality

**Machine Learning Evaluation**
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

---

## 👥 Team Collaboration

Mazey is developed collaboratively using GitHub.

- **AI & Algorithm Development:** A* implementation, heuristic functions, ML model training and evaluation.
- **Interface Development:** Pygame interface, grid visualization and user interactions.
- **Integration:** Combining the algorithm, ML model and graphical interface.

Development is managed through separate Git branches and Pull Requests.

---

## 🚀 Project Status

**Currently Under Development**

Features, evaluation results, screenshots and documentation will be updated as development progresses.

---

## 📜 License

This project is developed for academic and educational purposes.