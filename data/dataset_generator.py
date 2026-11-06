
import csv
import random
from pathlib import Path

from algorithms.astar import astar
from data.maze_generator import generate_solvable_maze


def calculate_difficulty(
    obstacle_density,
    path_stretch,
    exploration_ratio
):
    """Classify maze difficulty using a scoring rule."""

    score = (
        0.40 * obstacle_density
        + 0.35 * min(path_stretch / 3, 1)
        + 0.25 * exploration_ratio
    )

    if score < 0.332:
        return "Easy"
    elif score < 0.354:
        return "Medium"
    else:
        return "Hard"


def generate_dataset(number_of_mazes=1000):
    random.seed(42)

    dataset = []

    for index in range(number_of_mazes):

        rows = random.randint(10, 20)
        cols = random.randint(10, 20)

        obstacle_probability = random.uniform(0.10, 0.35)

        try:
            grid, start, goal = generate_solvable_maze(
                rows=rows,
                cols=cols,
                obstacle_probability=obstacle_probability
            )
        except RuntimeError:
            continue

        path, explored = astar(grid, start, goal)

        if not path:
            continue

        total_cells = rows * cols

        wall_count = sum(
            cell == 1
            for row in grid
            for cell in row
        )

        obstacle_density = wall_count / total_cells

        path_length = len(path) - 1

        manhattan_distance = (
            abs(goal[0] - start[0])
            + abs(goal[1] - start[1])
        )

        path_stretch = (
            path_length / manhattan_distance
            if manhattan_distance > 0
            else 1
        )

        explored_nodes = len(explored)
        exploration_ratio = explored_nodes / total_cells

        difficulty = calculate_difficulty(
            obstacle_density,
            path_stretch,
            exploration_ratio
        )

        dataset.append({
            "rows": rows,
            "cols": cols,
            "obstacle_density": round(obstacle_density, 4),
            "path_length": path_length,
            "path_stretch": round(path_stretch, 4),
            "explored_nodes": explored_nodes,
            "difficulty": difficulty
        })

        if (index + 1) % 100 == 0:
            print(f"Processed {index + 1}/{number_of_mazes} mazes")

    if not dataset:
        raise RuntimeError("No valid mazes were generated.")

    output_path = Path(__file__).parent / "maze_dataset.csv"

    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=dataset[0].keys()
        )

        writer.writeheader()
        writer.writerows(dataset)

    print("\nDataset generation completed!")
    print(f"Total valid mazes: {len(dataset)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    generate_dataset(1000)