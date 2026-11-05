
import heapq
from itertools import count


def heuristic(a, b):
    """Calculate Manhattan Distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(position, grid):
    """Get valid neighboring cells."""
    row, col = position
    rows, cols = len(grid), len(grid[0])

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for dr, dc in directions:
        nr, nc = row + dr, col + dc

        if (0 <= nr < rows and
            0 <= nc < cols and
            grid[nr][nc] == 0):
            neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(came_from, current):
    """Reconstruct the path from start to goal."""
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    return path[::-1]


def astar(grid, start, goal):
    """
    A* Search Algorithm.

    0 = Walkable
    1 = Obstacle

    Returns:
        path: Shortest path
        explored: Nodes visited
    """

    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty.")

    rows, cols = len(grid), len(grid[0])

    if any(len(row) != cols for row in grid):
        raise ValueError("Grid must be rectangular.")

    if any(cell not in (0, 1) for row in grid for cell in row):
        raise ValueError("Grid must contain only 0 and 1.")

    for point in (start, goal):
        if (
            not isinstance(point, tuple)
            or len(point) != 2
            or any(type(x) is not int for x in point)
            or not (0 <= point[0] < rows and 0 <= point[1] < cols)
        ):
            raise ValueError("Invalid start or goal coordinates.")

    if grid[start[0]][start[1]] == 1:
        raise ValueError("Start cannot be an obstacle.")

    if grid[goal[0]][goal[1]] == 1:
        raise ValueError("Goal cannot be an obstacle.")

    open_list = []
    counter = count()

    heapq.heappush(
        open_list,
        (heuristic(start, goal), next(counter), 0, start)
    )

    came_from = {}
    g_score = {start: 0}
    closed_set = set()
    explored = []

    while open_list:
        _, _, current_g, current = heapq.heappop(open_list)

        if current in closed_set:
            continue

        if current_g != g_score[current]:
            continue

        closed_set.add(current)
        explored.append(current)

        if current == goal:
            return reconstruct_path(came_from, current), explored

        for neighbor in get_neighbors(current, grid):

            if neighbor in closed_set:
                continue

            tentative_g = current_g + 1

            if tentative_g < g_score.get(neighbor, float("inf")):

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(
                    open_list,
                    (f_score, next(counter), tentative_g, neighbor)
                )

    return [], explored
