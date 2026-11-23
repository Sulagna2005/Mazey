
import pygame
from interface import theme


def draw_maze(
    screen,
    grid,
    start,
    goal,
    explored=None,
    path=None,
    cell_size=30,
    offset_x=0,
    offset_y=0,
    visible_cells=None,
    cell_progress=None
):
    explored = set(explored or [])
    path = set(path or [])

    if visible_cells is not None:
        visible_cells = set(visible_cells)

    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):

            cell = (row, col)

            if visible_cells is not None and cell not in visible_cells:
                continue

            if grid[row][col] == 1:
                color = theme.WALL
            elif cell == start:
                color = theme.START
            elif cell == goal:
                color = theme.GOAL
            elif cell in path:
                color = theme.PATH
            elif cell in explored:
                color = theme.EXPLORED
            else:
                color = theme.EMPTY

            x = offset_x + col * cell_size
            y = offset_y + row * cell_size

            progress = 1.0

            if cell_progress is not None:
                progress = cell_progress.get(cell, 1.0)

            # Normal drawing when no animation is active
            if progress >= 1.0:
                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, cell_size, cell_size)
                )

                pygame.draw.rect(
                    screen,
                    theme.BORDER,
                    (x, y, cell_size, cell_size),
                    1
                )

            else:
                # Smooth pop-in animation
                progress = max(0.0, min(1.0, progress))
                eased = 1 - (1 - progress) ** 3

                animated_size = max(
                    1,
                    int(cell_size * eased)
                )

                animated_x = x + (cell_size - animated_size) // 2
                animated_y = y + (cell_size - animated_size) // 2

                cell_surface = pygame.Surface(
                    (cell_size, cell_size),
                    pygame.SRCALPHA
                )

                alpha = int(255 * eased)

                pygame.draw.rect(
                    cell_surface,
                    (*pygame.Color(color)[:3], alpha),
                    (0, 0, cell_size, cell_size)
                )

                pygame.draw.rect(
                    cell_surface,
                    (*pygame.Color(theme.BORDER)[:3], alpha),
                    (0, 0, cell_size, cell_size),
                    1
                )

                scaled_surface = pygame.transform.smoothscale(
                    cell_surface,
                    (animated_size, animated_size)
                )

                screen.blit(
                    scaled_surface,
                    (animated_x, animated_y)
                )
