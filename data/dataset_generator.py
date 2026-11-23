
import csv
import random
from pathlib import Path

from algorithms.astar import astar
from data.maze_generator import generate_solvable_maze


def extract_maze_features(grid):
    """Extract structural features available before solving."""

    rows = len(grid)
    cols = len(grid[0])

    walkable_cells = 0
    dead_ends = 0
    junctions = 0
    total_connectivity = 0

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for r in range(rows):
        for c in range(cols):

            if grid[r][c] == 1:
                continue

            walkable_cells += 1
            neighbors = 0

            for dr, dc in directions:
                nr = r + dr
                nc = c + dc

                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == 0
                ):
                    neighbors += 1

            total_connectivity += neighbors

            if neighbors == 1:
                dead_ends += 1

            if neighbors >= 3:
                junctions += 1

    if walkable_cells == 0:
        return {
            "dead_end_ratio": 0,
            "average_connectivity": 0,
            "junction_ratio": 0
        }

    return {
        "dead_end_ratio": dead_ends / walkable_cells,
        "average_connectivity": total_connectivity / walkable_cells,
        "junction_ratio": junctions / walkable_cells
    }

def calculate_difficulty(
    obstacle_density,
    dead_end_ratio,
    average_connectivity,
    junction_ratio
):
    """Classify maze difficulty using pre-solve features."""

    score = (
        0.35 * obstacle_density
        + 0.30 * dead_end_ratio
        + 0.20 * (1 - average_connectivity / 4)
        + 0.15 * (1 - junction_ratio)
    )

    if score < 0.1564:
        return "Easy"
    elif score < 0.2335:
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
        maze_features = extract_maze_features(grid)

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
            maze_features["dead_end_ratio"],
            maze_features["average_connectivity"],
            maze_features["junction_ratio"]
        )

        dataset.append({
            "rows": rows,
            "cols": cols,
            "obstacle_density": round(obstacle_density, 4),

            "dead_end_ratio": round(
                maze_features["dead_end_ratio"], 4
            ),
            "average_connectivity": round(
                maze_features["average_connectivity"], 4
            ),
            "junction_ratio": round(
                maze_features["junction_ratio"], 4
            ),

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