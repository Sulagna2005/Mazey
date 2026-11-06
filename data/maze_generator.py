
import random


def generate_maze(rows=15, cols=15, obstacle_probability=0.25):
    """
    Generate a random maze.

    0 = walkable cell
    1 = wall
    """

    if rows < 2 or cols < 2:
        raise ValueError("Maze dimensions must be at least 2x2.")

    if not 0 <= obstacle_probability < 1:
        raise ValueError("Obstacle probability must be between 0 and 1.")

    grid = []

    for row in range(rows):
        current_row = []

        for col in range(cols):
            if random.random() < obstacle_probability:
                current_row.append(1)
            else:
                current_row.append(0)

        grid.append(current_row)

    # Keep start and goal positions clear.
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    return grid, start, goal


def generate_solvable_maze(
    rows=15,
    cols=15,
    obstacle_probability=0.25,
    max_attempts=100
):
    """
    Generate a maze with a valid path from start to goal.
    """

    from algorithms.astar import astar

    for _ in range(max_attempts):
        grid, start, goal = generate_maze(
            rows,
            cols,
            obstacle_probability
        )

        path, explored = astar(grid, start, goal)

        if path:
            return grid, start, goal

    raise RuntimeError(
        "Could not generate a solvable maze. "
        "Try reducing obstacle probability."
    )

import random


def generate_maze(rows=15, cols=15, obstacle_probability=0.25):
    """
    Generate a random maze.

    0 = walkable cell
    1 = wall
    """

    if rows < 2 or cols < 2:
        raise ValueError("Maze dimensions must be at least 2x2.")

    if not 0 <= obstacle_probability < 1:
        raise ValueError("Obstacle probability must be between 0 and 1.")

    grid = []

    for row in range(rows):
        current_row = []

        for col in range(cols):
            if random.random() < obstacle_probability:
                current_row.append(1)
            else:
                current_row.append(0)

        grid.append(current_row)

    # Keep start and goal positions clear.
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    return grid, start, goal


def generate_solvable_maze(
    rows=15,
    cols=15,
    obstacle_probability=0.25,
    max_attempts=100
):
    """
    Generate a maze with a valid path from start to goal.
    """

    from algorithms.astar import astar

    for _ in range(max_attempts):
        grid, start, goal = generate_maze(
            rows,
            cols,
            obstacle_probability
        )

        path, explored = astar(grid, start, goal)

        if path:
            return grid, start, goal

    raise RuntimeError(
        "Could not generate a solvable maze. "
        "Try reducing obstacle probability."
    )
