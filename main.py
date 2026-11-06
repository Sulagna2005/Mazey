
import time

from algorithms.astar import astar
from data.maze_generator import generate_solvable_maze
from ml.predict_difficulty import predict_difficulty


def display_maze(grid, path=None):
    """Display the maze in the terminal."""

    path = set(path or [])

    for row_index, row in enumerate(grid):
        line = ""

        for col_index, cell in enumerate(row):
            position = (row_index, col_index)

            if position == (0, 0):
                line += "S "
            elif position == (len(grid) - 1, len(row) - 1):
                line += "G "
            elif position in path:
                line += "* "
            elif cell == 1:
                line += "# "
            else:
                line += ". "

        print(line)


def main():

    print("\n========== MAZEY ==========")
    print("Smart Maze Solver")
    print("===========================\n")

    # 1. Generate a solvable maze
    rows = 15
    cols = 15
    obstacle_probability = 0.25

    print("Generating maze...")

    grid, start, goal = generate_solvable_maze(
        rows=rows,
        cols=cols,
        obstacle_probability=obstacle_probability
    )

    # 2. Calculate actual obstacle density
    total_cells = rows * cols

    wall_count = sum(
        cell == 1
        for row in grid
        for cell in row
    )

    obstacle_density = wall_count / total_cells

    # 3. Predict difficulty using ML
    difficulty = predict_difficulty(
        rows,
        cols,
        obstacle_density
    )

    print(f"\nPredicted Difficulty: {difficulty}")
    print(f"Obstacle Density: {obstacle_density:.2%}")

    # 4. Display original maze
    print("\n========== GENERATED MAZE ==========")
    display_maze(grid)

    # 5. Solve using A*
    print("\nSolving maze using A*...")

    start_time = time.perf_counter()

    path, explored = astar(grid, start, goal)

    execution_time = time.perf_counter() - start_time

    # 6. Display results
    print("\n========== SOLUTION ==========")

    if path:
        print("Status: Solution Found")
        print(f"Path Length: {len(path) - 1}")
        print(f"Nodes Explored: {len(explored)}")
        print(f"Execution Time: {execution_time * 1000:.4f} ms")

        print("\n========== SOLVED MAZE ==========")
        display_maze(grid, path)

    else:
        print("Status: No solution found.")

    print("\n========== MAZEY COMPLETE ==========")


if __name__ == "__main__":
    main()