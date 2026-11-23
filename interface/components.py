
import pygame
import sys
from pathlib import Path
from interface import theme


# ---------------- RESOURCE PATH ----------------

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


# ---------------- FONT SETTINGS ----------------

FONT_DIR = resource_path("interface/assets/fonts")

HEADING_FONT = pygame.font.Font(
    str(FONT_DIR / "Fredoka-Medium.ttf"),
    22
)

BODY_FONT = pygame.font.Font(
    str(FONT_DIR / "Nunito-Regular.ttf"),
    18
)


# Cache fonts to avoid repeatedly loading them
FONT_CACHE = {
    ("heading", 22): HEADING_FONT,
    ("body", 18): BODY_FONT
}


# ---------------- BUTTON COMPONENT ----------------

class Button:

    def __init__(self, x, y, width, height, text, color):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.base_color = pygame.Color(color)

        self.hover_color = self.base_color.lerp(
            pygame.Color("#FFFFFF"), 0.18
        )

        self.current_color = self.base_color

        self.font = BODY_FONT
        self.hover_progress = 0.0

    def draw(self, screen):

        # Detect mouse hover
        mouse_position = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_position)

        # Smooth hover transition
        target = 1.0 if is_hovered else 0.0

        self.hover_progress += (
            target - self.hover_progress
        ) * 0.18

        self.current_color = self.base_color.lerp(
            self.hover_color,
            self.hover_progress
        )

        # Slight lift when hovered
        lift = round(self.hover_progress * 3)

        button_rect = self.rect.copy()
        button_rect.y -= lift

        # Soft shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3 - lift

        pygame.draw.rect(
            screen,
            pygame.Color("#E8E3DE"),
            shadow_rect,
            border_radius=12
        )

        # Main button
        pygame.draw.rect(
            screen,
            self.current_color,
            button_rect,
            border_radius=12
        )

        # Button text
        label = self.font.render(
            self.text,
            True,
            theme.TEXT_PRIMARY
        )

        text_rect = label.get_rect(
            center=button_rect.center
        )

        screen.blit(label, text_rect)

    def is_clicked(self, position):

        return self.rect.collidepoint(position)


# ---------------- TEXT COMPONENT ----------------

def draw_text(
    screen,
    text,
    x,
    y,
    size=20,
    color=None,
    font_type="body"
):

    if color is None:
        color = theme.TEXT_PRIMARY

    # Reuse cached fonts
    cache_key = (font_type, size)

    if cache_key not in FONT_CACHE:

        if font_type == "heading":
            font_path = FONT_DIR / "Fredoka-Medium.ttf"
        else:
            font_path = FONT_DIR / "Nunito-Regular.ttf"

        FONT_CACHE[cache_key] = pygame.font.Font(
            str(font_path),
            size
        )

    font = FONT_CACHE[cache_key]

    rendered_text = font.render(
        str(text),
        True,
        color
    )

    screen.blit(rendered_text, (x, y))


# ---------------- PANEL COMPONENT ----------------

def draw_panel(screen, x, y, width, height, title):

    panel_rect = pygame.Rect(
        x, y, width, height
    )

    pygame.draw.rect(
        screen,
        theme.PANEL_BACKGROUND,
        panel_rect,
        border_radius=16
    )

    pygame.draw.rect(
        screen,
        theme.BORDER,
        panel_rect,
        width=1,
        border_radius=16
    )

    draw_text(
        screen,
        title,
        x + 20,
        y + 18,
        22,
        font_type="heading"
    )