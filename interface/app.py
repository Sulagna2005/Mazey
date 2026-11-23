
import pygame
import time
import math
import sys
import ctypes
from pathlib import Path

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "Mazey.SmartMazeSolver"
    )
except Exception:
    pass

pygame.init()


# ---------------- RESOURCE PATH ----------------

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


# ---------------- IMPORTS ----------------

from interface import theme
from interface.components import Button, draw_text, draw_panel
from interface.maze_renderer import draw_maze

from data.maze_generator import generate_solvable_maze
from data.dataset_generator import extract_maze_features
from ml.predict_difficulty import predict_difficulty
from algorithms.astar import astar_steps


# ---------------- WINDOW SETTINGS ----------------

WIDTH = 1440
HEIGHT = 900
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mazey - Smart Maze Solver")


# ---------------- ASSETS ----------------

ASSETS_DIR = resource_path("interface/assets")

LOGO_PATH = ASSETS_DIR / "mazey_logo.png"
MASCOT_PATH = ASSETS_DIR / "mazey_mascot.png"

# Set Mazey mascot as the application window icon
app_icon = pygame.image.load(
    str(MASCOT_PATH)
).convert_alpha()

pygame.display.set_icon(app_icon)

logo_original = pygame.image.load(
    str(LOGO_PATH)
).convert_alpha()

mascot_original = pygame.image.load(
    str(MASCOT_PATH)
).convert_alpha()

logo_rect = logo_original.get_rect().fit(
    pygame.Rect(0, 0, 180, 90)
)

logo_image = pygame.transform.smoothscale(
    logo_original,
    logo_rect.size
)

clock = pygame.time.Clock()


# ---------------- APPLICATION STATE ----------------

rows = 15
cols = 15
obstacle_probability = 0.25

grid = None
start = None
goal = None

path = []
explored = []

difficulty = "Not predicted"
path_length = 0
nodes_explored = 0
execution_time = 0.0
solution_status = "Not solved"


# ---------------- ANIMATION STATE ----------------

search_iterator = None
animation_mode = "idle"

path_animation_index = 0
search_compute_time = 0.0

agent_animation_index = 0
agent_animation_timer = 0

agent_segment_start_time = None
agent_move_duration = 8 / FPS

celebration_start_time = None

visible_cells = None
generation_cells = []
generation_index = 0
generation_progress = {}


# ---------------- BUTTONS ----------------

buttons = {
    "row_minus": Button(50, 225, 45, 35, "-", theme.LAVENDER),
    "row_plus": Button(195, 225, 45, 35, "+", theme.LAVENDER),

    "col_minus": Button(50, 300, 45, 35, "-", theme.LAVENDER),
    "col_plus": Button(195, 300, 45, 35, "+", theme.LAVENDER),

    "generate": Button(50, 440, 190, 45, "Generate Maze", theme.MINT),
    "solve": Button(50, 500, 190, 45, "Solve Maze", theme.PASTEL_BLUE),
    "reset": Button(50, 560, 190, 45, "Reset", theme.PEACH),
    "clear": Button(50, 620, 190, 45, "Clear", theme.LAVENDER),
}


# ---------------- MAZE FUNCTIONS ----------------

def generate_new_maze():

    global grid, start, goal
    global path, explored, difficulty
    global path_length, nodes_explored
    global execution_time, solution_status
    global search_iterator, animation_mode
    global path_animation_index, search_compute_time
    global agent_animation_index, agent_animation_timer
    global agent_segment_start_time
    global celebration_start_time
    global visible_cells, generation_cells, generation_index
    global generation_progress

    grid, start, goal = generate_solvable_maze(
        rows=rows,
        cols=cols,
        obstacle_probability=obstacle_probability
    )

    features = extract_maze_features(grid)

    total_cells = rows * cols

    wall_count = sum(
        cell == 1
        for row in grid
        for cell in row
    )

    density = wall_count / total_cells

    difficulty = predict_difficulty(
        rows,
        cols,
        density,
        features["dead_end_ratio"],
        features["average_connectivity"],
        features["junction_ratio"]
    )

    path = []
    explored = []

    path_length = 0
    nodes_explored = 0
    execution_time = 0.0

    search_iterator = None

    path_animation_index = 0
    search_compute_time = 0.0

    agent_animation_index = 0
    agent_animation_timer = 0
    agent_segment_start_time = None

    celebration_start_time = None

    visible_cells = set()

    generation_cells = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
    ]

    generation_index = 0
    generation_progress = {}

    animation_mode = "generating"
    solution_status = "Generating maze..."


def update_maze_preview():

    global grid, start, goal
    global path, explored, difficulty
    global path_length, nodes_explored
    global execution_time, solution_status
    global search_iterator, animation_mode
    global visible_cells, generation_cells, generation_index
    global generation_progress
    global path_animation_index, search_compute_time
    global agent_animation_index, agent_animation_timer
    global agent_segment_start_time, celebration_start_time

    if grid is None:
        return

    # Generate a fresh preview with the selected dimensions.
    grid, start, goal = generate_solvable_maze(
        rows=rows,
        cols=cols,
        obstacle_probability=obstacle_probability
    )

    # Reset previous solution data.
    path = []
    explored = []

    difficulty = "Not predicted"
    path_length = 0
    nodes_explored = 0
    execution_time = 0.0

    # Reset search and animations.
    search_iterator = None
    animation_mode = "idle"

    path_animation_index = 0
    search_compute_time = 0.0

    agent_animation_index = 0
    agent_animation_timer = 0

    agent_segment_start_time = None
    celebration_start_time = None

    visible_cells = None
    generation_cells = []
    generation_index = 0
    generation_progress = {}

    solution_status = "Ready to generate"


def solve_maze():

    global path, explored
    global path_length, nodes_explored
    global execution_time, solution_status
    global search_iterator, animation_mode
    global path_animation_index, search_compute_time
    global agent_animation_index, agent_animation_timer
    global agent_segment_start_time
    global celebration_start_time

    if grid is None:
        return

    if animation_mode == "generating":
        return

    path = []
    explored = []

    path_length = 0
    nodes_explored = 0
    execution_time = 0.0

    path_animation_index = 0
    search_compute_time = 0.0

    agent_animation_index = 0
    agent_animation_timer = 0
    agent_segment_start_time = None

    celebration_start_time = None

    search_iterator = astar_steps(grid, start, goal)

    animation_mode = "exploring"
    solution_status = "Searching..."


def reset_maze():

    global path, explored
    global path_length, nodes_explored
    global execution_time, solution_status
    global search_iterator, animation_mode
    global path_animation_index, search_compute_time
    global agent_animation_index, agent_animation_timer
    global agent_segment_start_time
    global celebration_start_time
    global visible_cells, generation_cells, generation_index
    global generation_progress

    path = []
    explored = []

    path_length = 0
    nodes_explored = 0
    execution_time = 0.0

    solution_status = "Ready to solve"

    search_iterator = None
    animation_mode = "idle"

    path_animation_index = 0
    search_compute_time = 0.0

    agent_animation_index = 0
    agent_animation_timer = 0
    agent_segment_start_time = None

    celebration_start_time = None

    visible_cells = None
    generation_cells = []
    generation_index = 0
    generation_progress = {}


def clear_maze():

    global grid, start, goal
    global difficulty

    reset_maze()

    grid = None
    start = None
    goal = None

    difficulty = "Not predicted"


# ---------------- SLIDER ----------------

def draw_slider():

    slider_x = 50
    slider_y = 390
    slider_width = 190

    pygame.draw.line(
        screen,
        theme.BORDER,
        (slider_x, slider_y),
        (slider_x + slider_width, slider_y),
        6
    )

    position = (
        slider_x
        + (obstacle_probability - 0.10) / 0.40 * slider_width
    )

    pygame.draw.circle(
        screen,
        theme.LAVENDER,
        (int(position), slider_y),
        10
    )

    legend_items = [
        ("Start", theme.START),
        ("Goal", theme.GOAL),
        ("Wall", theme.WALL),
        ("Empty", theme.EMPTY),
        ("Explored", theme.EXPLORED),
        ("Path", theme.PATH),
    ]

    legend_x = 350
    legend_y = 800
    legend_gap = 125

    for label, color in legend_items:

        pygame.draw.rect(
            screen,
            color,
            (legend_x, legend_y, 15, 15),
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            theme.BORDER,
            (legend_x, legend_y, 15, 15),
            width=1,
            border_radius=3
        )

        draw_text(
            screen,
            label,
            legend_x + 22,
            legend_y - 2,
            14,
            theme.TEXT_SECONDARY
        )

        legend_x += legend_gap


def update_slider(mouse_x):

    global obstacle_probability

    slider_x = 50
    slider_width = 190

    value = (mouse_x - slider_x) / slider_width

    value = max(0, min(1, value))

    obstacle_probability = round(
        0.10 + value * 0.40,
        2
    )


# ---------------- GOAL CELEBRATION ----------------

def draw_celebration(goal_x, goal_y, cell_size):

    if celebration_start_time is None:
        return

    elapsed = time.perf_counter() - celebration_start_time

    if elapsed >= 2.5:
        return

    sparkle_colors = [
        theme.LAVENDER,
        theme.PEACH,
        theme.MINT,
        theme.PASTEL_BLUE
    ]

    for i in range(8):

        angle = (
            i * math.tau / 8
            + elapsed * 1.5
        )

        distance = cell_size * (
            1.1 + 0.2 * math.sin(elapsed * 5 + i)
        )

        sparkle_x = int(
            goal_x + math.cos(angle) * distance
        )

        sparkle_y = int(
            goal_y + math.sin(angle) * distance
        )

        radius = 3 + int(
            2 * abs(math.sin(elapsed * 6 + i))
        )

        color = sparkle_colors[i % len(sparkle_colors)]

        pygame.draw.circle(
            screen,
            color,
            (sparkle_x, sparkle_y),
            radius
        )

        pygame.draw.line(
            screen,
            color,
            (sparkle_x - radius - 2, sparkle_y),
            (sparkle_x + radius + 2, sparkle_y),
            2
        )

        pygame.draw.line(
            screen,
            color,
            (sparkle_x, sparkle_y - radius - 2),
            (sparkle_x, sparkle_y + radius + 2),
            2
        )


# ---------------- DRAW INTERFACE ----------------

def draw_interface():

    screen.fill(theme.BACKGROUND)

    logo_position = logo_image.get_rect(
        topleft=(30, 15)
    )

    screen.blit(logo_image, logo_position)

    draw_text(
        screen,
        "Smart Maze Solver using A* Search and Machine Learning",
        60,
        70,
        20,
        theme.TEXT_SECONDARY
    )

    draw_panel(screen, 30, 120, 250, 730, "Controls")
    draw_panel(screen, 300, 120, 820, 730, "Maze Visualization")
    draw_panel(screen, 1140, 120, 270, 730, "Statistics")

    draw_text(screen, "Rows", 50, 195, 17)

    draw_text(
        screen,
        str(rows),
        125,
        230,
        20
    )

    draw_text(screen, "Columns", 50, 270, 17)

    draw_text(
        screen,
        str(cols),
        125,
        305,
        20
    )

    for button in buttons.values():
        button.draw(screen)

    draw_slider()

    if grid is not None:

        visible_explored = explored
        visible_path = path[:path_animation_index]

        cell_size = max(
            12,
            min(34, int(min(760 / cols, 580 / rows)))
        )

        maze_width = cols * cell_size
        maze_height = rows * cell_size

        offset_x = 300 + (820 - maze_width) // 2
        offset_y = 190 + (580 - maze_height) // 2

        draw_maze(
            screen,
            grid,
            start,
            goal,
            explored=visible_explored,
            path=visible_path,
            cell_size=cell_size,
            offset_x=offset_x,
            offset_y=offset_y,
            visible_cells=(
                visible_cells
                if animation_mode == "generating"
                else None
            ),
            cell_progress=(
                generation_progress
                if animation_mode == "generating"
                else None
            )
        )

        if path and (
            animation_mode == "path"
            or solution_status == "Agent reached goal!"
        ):

            current_index = min(
                agent_animation_index,
                len(path) - 1
            )

            current_row, current_col = path[current_index]

            next_row, next_col = path[
                min(current_index + 1, len(path) - 1)
            ]

            progress = 0.0

            if (
                animation_mode == "path"
                and agent_segment_start_time is not None
                and current_index < len(path) - 1
            ):

                elapsed = (
                    time.perf_counter()
                    - agent_segment_start_time
                )

                progress = max(
                    0.0,
                    min(1.0, elapsed / agent_move_duration)
                )

            agent_row = (
                current_row
                + (next_row - current_row) * progress
            )

            agent_col = (
                current_col
                + (next_col - current_col) * progress
            )

            mascot_size = max(
                1,
                int(cell_size * 0.85)
            )

            movement_pulse = math.sin(progress * math.pi)

            scale_x = 1.0 + 0.08 * movement_pulse
            scale_y = 1.0 - 0.08 * movement_pulse

            mascot_width = max(
                1,
                int(mascot_size * scale_x)
            )

            mascot_height = max(
                1,
                int(mascot_size * scale_y)
            )

            mascot_image = pygame.transform.smoothscale(
                mascot_original,
                (mascot_width, mascot_height)
            )

            dx = next_col - current_col
            dy = next_row - current_row

            tilt_angle = (
                -dx * 7 * movement_pulse
                + dy * 5 * movement_pulse
            )

            if abs(tilt_angle) > 0.1:

                mascot_image = pygame.transform.rotate(
                    mascot_image,
                    tilt_angle
                )

            agent_x = (
                offset_x
                + (agent_col + 0.5) * cell_size
            )

            agent_y = (
                offset_y
                + (agent_row + 0.5) * cell_size
            )

            if celebration_start_time is not None:

                celebration_elapsed = (
                    time.perf_counter()
                    - celebration_start_time
                )

                if celebration_elapsed < 2.5:

                    jump_height = (
                        abs(
                            math.sin(
                                celebration_elapsed * math.tau * 1.5
                            )
                        )
                        * cell_size
                        * 0.4
                    )

                    agent_y -= jump_height

            mascot_rect = mascot_image.get_rect(
                center=(
                    round(agent_x),
                    round(agent_y)
                )
            )

            screen.blit(
                mascot_image,
                mascot_rect
            )

        if celebration_start_time is not None:

            goal_x = (
                offset_x
                + goal[1] * cell_size
                + cell_size // 2
            )

            goal_y = (
                offset_y
                + goal[0] * cell_size
                + cell_size // 2
            )

            draw_celebration(
                goal_x,
                goal_y,
                cell_size
            )

    else:

        draw_text(
            screen,
            "Click Generate Maze to begin",
            580,
            450,
            22,
            theme.TEXT_SECONDARY
        )

    stats = [
        ("Difficulty", difficulty),
        ("Path Length", str(path_length)),
        ("Nodes Explored", str(nodes_explored)),
        ("Execution Time", f"{execution_time:.3f} ms"),
        ("Solution Status", solution_status),
    ]

    y = 195

    for label, value in stats:

        draw_text(
            screen,
            label,
            1160,
            y,
            16,
            theme.TEXT_SECONDARY
        )

        draw_text(
            screen,
            value,
            1160,
            y + 28,
            19
        )

        y += 115

    pygame.display.flip()


# ---------------- EVENT LOOP ----------------

generate_new_maze()

running = True
slider_dragging = False

while running:

    clock.tick(FPS)

    # ---------------- MAZE GENERATION ANIMATION ----------------

    if animation_mode == "generating":

        for _ in range(2):

            if generation_index < len(generation_cells):

                cell = generation_cells[generation_index]

                visible_cells.add(cell)
                generation_progress[cell] = 0.0

                generation_index += 1

        for cell in generation_progress:

            generation_progress[cell] = min(
                1.0,
                generation_progress[cell] + 0.22
            )

        all_cells_revealed = (
            generation_index >= len(generation_cells)
        )

        all_cells_animated = (
            all(
                progress >= 1.0
                for progress in generation_progress.values()
            )
        )

        if all_cells_revealed and all_cells_animated:

            animation_mode = "idle"
            solution_status = "Ready to solve"

            visible_cells = None
            generation_progress = {}

    # ---------------- LIVE A* ANIMATION ----------------

    elif animation_mode == "exploring" and search_iterator:

        step_start = time.perf_counter()

        try:

            event_type, data = next(search_iterator)

            search_compute_time += (
                time.perf_counter() - step_start
            ) * 1000

            execution_time = search_compute_time

            if event_type == "explore":

                explored.append(data)
                nodes_explored = len(explored)

            elif event_type == "complete":

                path = data
                path_length = len(path) - 1

                path_animation_index = 1

                agent_animation_index = 0
                agent_animation_timer = 0

                agent_segment_start_time = time.perf_counter()

                celebration_start_time = None

                animation_mode = "path"

                solution_status = "Agent moving..."

            elif event_type == "failed":

                solution_status = "No solution found"
                animation_mode = "idle"
                search_iterator = None

        except StopIteration:

            animation_mode = "idle"
            search_iterator = None

    # ---------------- SMOOTH PATH + MASCOT ANIMATION ----------------

    elif animation_mode == "path" and path:

        now = time.perf_counter()

        if agent_segment_start_time is None:
            agent_segment_start_time = now

        while (
            agent_animation_index < len(path) - 1
            and now - agent_segment_start_time >= agent_move_duration
        ):

            agent_animation_index += 1

            agent_segment_start_time += agent_move_duration

            path_animation_index = agent_animation_index + 1

        if agent_animation_index >= len(path) - 1:

            path_animation_index = len(path)

            animation_mode = "idle"

            solution_status = "Agent reached goal!"

            celebration_start_time = time.perf_counter()

            agent_segment_start_time = None

            search_iterator = None

    # ---------------- EVENT HANDLING ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            if (
                370 <= mouse_pos[1] <= 410
                and 50 <= mouse_pos[0] <= 240
            ):

                slider_dragging = True
                update_slider(mouse_pos[0])

            elif buttons["row_minus"].is_clicked(mouse_pos):

                rows = max(2, rows - 1)
                update_maze_preview()

            elif buttons["row_plus"].is_clicked(mouse_pos):

                rows = min(20, rows + 1)
                update_maze_preview()

            elif buttons["col_minus"].is_clicked(mouse_pos):

                cols = max(2, cols - 1)
                update_maze_preview()

            elif buttons["col_plus"].is_clicked(mouse_pos):

                cols = min(20, cols + 1)
                update_maze_preview()

            elif buttons["generate"].is_clicked(mouse_pos):

                generate_new_maze()

            elif buttons["solve"].is_clicked(mouse_pos):

                solve_maze()

            elif buttons["reset"].is_clicked(mouse_pos):

                reset_maze()

            elif buttons["clear"].is_clicked(mouse_pos):

                clear_maze()

        elif event.type == pygame.MOUSEBUTTONUP:

            slider_dragging = False

        elif event.type == pygame.MOUSEMOTION and slider_dragging:

            update_slider(event.pos[0])

    draw_interface()


pygame.quit()