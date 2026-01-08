# drawing.py
import pygame
from assets import *
pygame.init()

# ---------------- DRAW FUNCTIONS (DRAW ONLY) ----------------
def draw_background(screen, use_bg, bg_image):
    if use_bg:
        screen.blit(bg_image, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        screen.blit(overlay, (0, 0))
    else:
        screen.fill(BACKGROUND)

def draw_main_menu(screen, menu_buttons, save_data, use_bg, bg_image):
    draw_background(screen, use_bg, bg_image)

    title = title_font.render("Color Sort Puzzle", True, TITLE_COLOR)
    shadow = title_font.render("Color Sort Puzzle", True, SHADOW_COLOR)
    screen.blit(shadow, (104, 124))
    screen.blit(title, (100, 120))

    subtitle = info_font.render(
        "Sort the colors into the correct containers!", True, TEXT_COLOR
    )
    screen.blit(subtitle, (165, 205))

    for button in menu_buttons:
        button.draw(screen)

    progress = f"Level Unlocked: {save_data['level_unlocked']}"
    text = info_font.render(progress, True, TEXT_COLOR)
    screen.blit(text, (100, 620))

def draw_options(screen, back_button, use_bg, bg_image):
    draw_background(screen, use_bg, bg_image)
    back_button.draw(screen)

    title = title_font.render("OPTIONS", True, TITLE_COLOR)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

    options = ["Sound: ON", "Music: ON", "Graphics: Medium"]
    for i, text in enumerate(options):
        label = button_font.render(text, True, TEXT_COLOR)
        screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, 220 + i * 70))

def draw_how_to_play(screen, back_button, use_bg, bg_image):
    draw_background(screen, use_bg, bg_image)
    back_button.draw(screen)

    title = title_font.render("HOW TO PLAY", True, TITLE_COLOR)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

    instructions = [
        "1. Select a container",
        "2. Select another container",
        "3. Only matching colors can stack",
        "4. Sort all colors to win"
    ]

    for i, line in enumerate(instructions):
        text = info_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (100, 200 + i * 50))

def draw_game_placeholder(screen, back_button, use_bg, bg_image):
    draw_background(screen, use_bg, bg_image)
    back_button.draw(screen)

    text = button_font.render("GAMEPLAY COMING SOON", True, TEXT_COLOR)
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))

def draw_playing(screen, back_button, use_bg, bg_image):
    draw_background(screen, use_bg, bg_image)
    back_button.draw(screen)

def draw_stars(screen, x, y, num_stars):
    """Draw star rating (1-3 stars)"""
    star_size = 30
    star_spacing = 60

    for i in range(3):
        star_x = x + i * star_spacing
        star_y = y

        if i < num_stars:
            # Filled star (gold)
            color = (255, 215, 0)  # Gold

        else:
            # Empty star (gray)
            color = (100, 100, 100)  # Gray

        # Draw star outline
        draw_star_shape(screen, color, star_x, star_y, star_size)

def draw_star_shape(surf, color, x, y, size):
    """Draw a star shape"""
    import math
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        if i % 2 == 0:
            r = size
        else:
            r = size * 0.4
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surf, color, points)
    
import pygame

def draw_tubes(screen, tubes_num, tube_cols, color_choices, COLOR_RGB, animation, AnimationState, select_rect, get_tube_rect):
    """
    Draw all tubes and their colors.
    Returns list of tube rects.
    """
    tube_boxes = []

    for i in range(tubes_num):
        # Skip drawing the source tube entirely when animation is active
        if animation['state'] != AnimationState.IDLE and i == animation['source']:
            rect = get_tube_rect(tubes_num, i)
            tube_boxes.append(rect)
            continue

        rect = get_tube_rect(tubes_num, i)
        tube_boxes.append(rect)

        # Draw tube border WITHOUT top line
        border_color = (0, 120, 255)  # Blue
        if select_rect == i and animation['state'] == AnimationState.IDLE:
            border_color = (0, 255, 0)  # Green for selected
        elif i >= tubes_num - 2 and len(tube_cols[i]) == 0:
            border_color = (100, 100, 100)  # Gray for empty

        # Draw left, right, and bottom borders only
        pygame.draw.line(screen, border_color, (rect.x, rect.y), (rect.x, rect.y + rect.height), 5)
        pygame.draw.line(screen, border_color, (rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height), 5)
        pygame.draw.line(screen, border_color, (rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height), 5)

        # Draw colors in tube (from bottom to top)
        for j in range(len(tube_cols[i])):
            color_idx = tube_cols[i][j]
            color_rect = pygame.Rect(rect.x + 2, rect.y + rect.height - 50 - (j * 50), rect.width - 4, 48)
            pygame.draw.rect(screen, COLOR_RGB[color_choices[color_idx]], color_rect, 0, 3)

    return tube_boxes
