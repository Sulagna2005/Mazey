
import csv
import random
import time

from collections import deque
from pathlib import Path

from algorithms.astar import astar
from data.maze_generator import generate_solvable_maze


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "astar_evaluation_results.csv"


def bfs_shortest_path_length(grid, start, goal):
    """Find shortest path length independently using BFS."""

    queue = deque([(start, 0)])
    visited = {start}

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:
        (row, col), distance = queue.popleft()

        if (row, col) == goal:
            return distance

        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < len(grid)
                and 0 <= nc < len(grid[0])
                and grid[nr][nc] == 0
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append(((nr, nc), distance + 1))

    return None


def validate_path(grid, path, start, goal):
    """Check whether the returned path is valid."""

    if not path:
        return False

    if path[0] != start or path[-1] != goal:
        return False

    for index, position in enumerate(path):

        row, col = position

        if not (
            0 <= row < len(grid)
            and 0 <= col < len(grid[0])
        ):
            return False

        if grid[row][col] == 1:
            return False

        if index > 0:
            previous = path[index - 1]

            distance = (
                abs(row - previous[0])
                + abs(col - previous[1])
            )

            if distance != 1:
                return False

    return True


def evaluate_astar(number_of_mazes=100):

    random.seed(42)

    results = []

    print("\n========== ASTAR EVALUATION ==========")

    for index in range(number_of_mazes):

        rows = random.randint(10, 20)
        cols = random.randint(10, 20)

        obstacle_probability = random.uniform(0.10, 0.35)

        grid, start, goal = generate_solvable_maze(
            rows,
            cols,
            obstacle_probability
        )

        # Run A* and measure execution time
        start_time = time.perf_counter()

        path, explored = astar(grid, start, goal)

        execution_time = (
            time.perf_counter() - start_time
        ) * 1000

        # Calculate independent BFS result
        bfs_length = bfs_shortest_path_length(
            grid,
            start,
            goal
        )

        path_length = len(path) - 1 if path else None

        valid = validate_path(
            grid,
            path,
            start,
            goal
        )

        optimal = (
            valid
            and bfs_length is not None
            and path_length == bfs_length
        )

        results.append({
            "maze_number": index + 1,
            "rows": rows,
            "cols": cols,
            "obstacle_probability": round(
                obstacle_probability, 4
            ),
            "path_length": path_length,
            "explored_nodes": len(explored),
            "execution_time_ms": round(execution_time, 6),
            "path_valid": valid,
            "optimal": optimal
        })

        if (index + 1) % 10 == 0:
            print(
                f"Evaluated {index + 1}/{number_of_mazes} mazes"
            )

    # Calculate summary metrics
    successful = [
        result for result in results
        if result["path_valid"]
    ]

    optimal_count = sum(
        result["optimal"] for result in results
    )

    average_time = sum(
        result["execution_time_ms"] for result in results
    ) / number_of_mazes

    average_explored = sum(
        result["explored_nodes"] for result in results
    ) / number_of_mazes

    average_path_length = (
        sum(result["path_length"] for result in successful)
        / len(successful)
        if successful else 0
    )

    # Save individual results
    with open(OUTPUT_PATH, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    # Display final report
    print("\n========== FINAL EVALUATION ==========")

    print(f"Total mazes tested: {number_of_mazes}")

    print(
        f"Successful solutions: "
        f"{len(successful)}/{number_of_mazes}"
    )

    print(
        f"Valid paths: "
        f"{sum(r['path_valid'] for r in results)}/{number_of_mazes}"
    )

    print(
        f"Optimal paths: "
        f"{optimal_count}/{number_of_mazes}"
    )

    print(
        f"Average path length: "
        f"{average_path_length:.2f}"
    )

    print(
        f"Average explored nodes: "
        f"{average_explored:.2f}"
    )

    print(
        f"Average execution time: "
        f"{average_time:.6f} ms"
    )

    print(f"\nDetailed results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    evaluate_astar(100)