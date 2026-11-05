
from algorithms.astar import astar

grid = [
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path, explored = astar(grid, start, goal)

print("Path:", path)
print("Path Length:", len(path) - 1 if path else 0)
print("Nodes Explored:", len(explored))

assert path, "No path found!"
assert path[0] == start
assert path[-1] == goal

for r, c in path:
    assert grid[r][c] == 0

for a, b in zip(path, path[1:]):
    assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

print("\nAll tests passed!")
