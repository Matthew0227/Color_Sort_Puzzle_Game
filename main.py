from save_manager import load_save, save_game
import drawing
from ui import Button
import pygame
import sys
import copy
import timer
from gameplay import check_move_validity, generate_start, check_victory, calculate_stars
from assets import (
    color_choices,
    COLOR_RGB
)

save_data = load_save()
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ColorSortingGame")
fps = 60
timer = pygame.time.Clock()

# Colors
BACKGROUND = (25, 25, 40)

background_image = None
use_background_image = False

try:
    background_image = pygame.image.load("assets/background.jpg").convert()
    background_image = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    use_background_image = True

except pygame.error:
    pass

# ---------------- BUTTON INSTANCES ----------------
menu_buttons = [
    Button(190, 250, 300, 60, "Start Game", "play"),
    Button(190, 330, 300, 60, "Settings", "options"),
    Button(190, 410, 300, 60, "How to Play", "how_to_play"),
    Button(190, 490, 300, 60, "Quit", "quit")
]

back_button = Button(50, 40, 120, 50, "← Back", "back")

# ---------------- GAME STATE ----------------
game_state = {
    "screen": "main_menu",
    "running": True
}
# ---------------- GAME VARIABLES ----------------
tube_colors = []
initial_colors = []
tubes = 0
new_game = True
selected = False
select_rect = 100
win = False
game_time = 0
stars = 0

# ---------------- GAME ANIMATION ----------------
class AnimationState:
    IDLE = 0
    MOVE = 1
    POUR = 2
    RETURN = 3

animation = {
    'state': AnimationState.IDLE,
    'source': -1,
    'dest': -1,
    'color': -1,
    'count': 0,
    'progress': 0.0,
    'all_colors': [],
    'colors_to_pour': [],
    'remaining_colors': [],
    'current_x': 0,
    'current_y': 0,
    'angle': 0
}
def update_animation(tube_colors, fps):
    if animation['state'] == AnimationState.IDLE:
        return False

    speeds = {AnimationState.MOVE:0.2, AnimationState.POUR:0.4, AnimationState.RETURN:0.2}
    animation['progress'] += 1.0 / (fps * speeds[animation['state']])

    if animation['progress'] >= 1.0:
        if animation['state'] == AnimationState.MOVE:
            animation['state'] = AnimationState.POUR
            animation['progress'] = 0.0
        elif animation['state'] == AnimationState.POUR:
            for _ in range(animation['count']):
                if tube_colors[animation['source']]:
                    tube_colors[animation['dest']].append(tube_colors[animation['source']].pop())
            animation['state'] = AnimationState.RETURN
            animation['progress'] = 0.0
        elif animation['state'] == AnimationState.RETURN:
            animation['state'] = AnimationState.IDLE
            animation['progress'] = 0.0
            return True
    return False

def start_animation(source, dest, tube_colors, check_move_validity):
    is_valid, color, count = check_move_validity(source, dest, tube_colors)
    if not is_valid:
        return
    animation['state'] = AnimationState.MOVE
    animation['source'] = source
    animation['dest'] = dest
    animation['color'] = color
    animation['count'] = count
    animation['progress'] = 0.0
    animation['all_colors'] = tube_colors[source].copy()
    animation['colors_to_pour'] = tube_colors[source][-count:][::-1]
    animation['remaining_colors'] = tube_colors[source][:-count].copy()

def draw_moving_tube():
    """Draw the moving tube with animation"""
    if animation['state'] == AnimationState.IDLE:
        return

    tube_width = 65
    tube_height = 200

    # Get positions
    source_rect = get_tube_rect(tubes, animation['source'])
    dest_rect = get_tube_rect(tubes, animation['dest'])

    # Calculate position based on animation state
    progress = animation['progress']

    if animation['state'] == AnimationState.MOVE:
        # Move to position higher above destination, to the right
        target_x = dest_rect.x + tube_width + 25
        target_y = dest_rect.y - 150  # Increased from -100 to -150 for higher position

        x = source_rect.x + (target_x - source_rect.x) * progress
        y = source_rect.y + (target_y - source_rect.y) * progress
        angle = 0
    elif animation['state'] == AnimationState.POUR:
        # Position for pouring - higher to avoid clipping
        target_x = dest_rect.x + tube_width + 25
        target_y = dest_rect.y - 150  # Increased from -100 to -150 for higher position

        x = target_x
        y = target_y
        # Gradually tilt to horizontal (90 degrees) as pouring progresses
        angle = 90 * progress
    elif animation['state'] == AnimationState.RETURN:
        # Move back to original position
        target_x = dest_rect.x + tube_width + 25
        target_y = dest_rect.y - 150  # Increased from -100 to -150 for higher position

        x = target_x + (source_rect.x - target_x) * progress
        y = target_y + (source_rect.y - target_y) * progress
        # Gradually tilt back to vertical as returning progresses
        angle = 90 * (1 - progress)

    # Store current position
    animation['current_x'] = x
    animation['current_y'] = y
    animation['angle'] = angle

    # Draw the moving tube - FIX: Create a larger surface to prevent scaling during rotation
    # Create surface with extra padding to maintain size during rotation
    padding = 20
    tube_surface = pygame.Surface((tube_width + padding * 2, tube_height + padding * 2), pygame.SRCALPHA)

    # Draw tube border WITHOUT top line
    border_color = (0, 220, 0)
    # Draw left border (offset by padding)
    pygame.draw.line(tube_surface, border_color, (padding, padding), (padding, padding + tube_height), 5)
    # Draw right border
    pygame.draw.line(tube_surface, border_color, (padding + tube_width, padding), (padding + tube_width, padding + tube_height), 5)
    # Draw bottom border
    pygame.draw.line(tube_surface, border_color, (padding, padding + tube_height), (padding + tube_width, padding + tube_height), 5)

    # Determine which colors to draw (static - colors stay in same positions)
    colors_to_draw = []
    if animation['state'] == AnimationState.MOVE:
        colors_to_draw = animation['all_colors'].copy()
    elif animation['state'] == AnimationState.POUR:
        pour_progress = min(1.0, progress * 3)
        colors_poured = int(len(animation['colors_to_pour']) * pour_progress)
        colors_to_draw = animation['remaining_colors'] + animation['colors_to_pour'][colors_poured:]
    elif animation['state'] == AnimationState.RETURN:
        colors_to_draw = animation['remaining_colors'].copy()

    # Draw colors inside the moving tube - ALWAYS STACK FROM BOTTOM (static positions)
    for j, color_idx in enumerate(colors_to_draw):
        color_height = 48
        # Always stack from bottom regardless of tilt angle
        color_y = padding + tube_height - 52 - (j * 50)
        color_rect = pygame.Rect(padding + 2, color_y, tube_width - 4, color_height)
        pygame.draw.rect(tube_surface, COLOR_RGB[color_choices[color_idx]], color_rect, 0, 3)

    # Rotate and draw
    if angle != 0:
        rotated_surface = pygame.transform.rotate(tube_surface, angle)
        # Center the rotated surface at the same point
        rotated_rect = rotated_surface.get_rect(center=(x + tube_width//2 + padding, y + tube_height//2 + padding))
        screen.blit(rotated_surface, rotated_rect)
    else:
        # Draw without rotation (adjust for padding)
        screen.blit(tube_surface, (x - padding, y - padding))

def get_tube_rect(tubes_num, index):
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True

    spacing = SCREEN_WIDTH / tubes_per_row
    start_x = 50  # Added margin

    if offset:
        if index < tubes_per_row:
            # Top row
            x = start_x + spacing * index
            y = 100  # Increased from 50
            return pygame.Rect(x, y, 65, 200)
        else:
            # Bottom row
            x = start_x + spacing * (index - tubes_per_row) + spacing * 0.5
            y = 350  # Increased from 300
            return pygame.Rect(x, y, 65, 200)
    else:
        if index < tubes_per_row:
            # Top row
            x = start_x + spacing * index
            y = 100
            return pygame.Rect(x, y, 65, 200)
        else:
            # Bottom row
            x = start_x + spacing * (index - tubes_per_row)
            y = 350
            return pygame.Rect(x, y, 65, 200)

def get_all_tube_rects(tubes):
    return [get_tube_rect(tubes, i) for i in range(tubes)]

# draw all tubes and colors on screen, as well as indicating what tube was selected

# ---------------- MAIN LOOP ----------------
while game_state["running"]:
    mouse_pos = pygame.mouse.get_pos()

    # -------- INPUT PHASE --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state["running"] = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state["screen"] == "main_menu":
                game_state["running"] = False
            else:
                game_state["screen"] = "main_menu"

        if game_state["screen"] == "main_menu":
            for btn in menu_buttons:
                action = btn.click(event)
                if action == "play":
                    game_state["screen"] = "playing"
                    tubes, tube_colors = generate_start()
                    initial_colors = copy.deepcopy(tube_colors)
                    game_time = 0
                    stars = 0
                    selected = False
                    select_rect = 100
                    win = False
                    animation['state'] = AnimationState.IDLE

                elif action == "options":
                    game_state["screen"] = "options"
                elif action == "how_to_play":
                    game_state["screen"] = "how_to_play"
                elif action == "quit":
                    game_state["running"] = False

        elif game_state["screen"] in ["options", "how_to_play"]:
            action = back_button.click(event)
            if action == "back":
                game_state["screen"] = "main_menu"

        elif game_state["screen"] == "playing":
                # ---- BACK BUTTON ----
            action = back_button.click(event)
            if action == "back":
                game_state["screen"] = "main_menu"
                selected = False
                animation['state'] = AnimationState.IDLE
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle tube selection
                if not selected:
                    for idx, rect in enumerate(get_all_tube_rects(tubes)):
                        if rect.collidepoint(event.pos):
                            selected = True
                            select_rect = idx
                else:
                    for idx, rect in enumerate(get_all_tube_rects(tubes)):
                        if rect.collidepoint(event.pos):
                            # Start animation move
                            start_animation(select_rect, idx, tube_colors, check_move_validity)
                            selected = False
                            select_rect = 100

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset level
                    tube_colors = copy.deepcopy(initial_colors)
                    game_time = 0
                    stars = 0
                    animation['state'] = AnimationState.IDLE
                    selected = False
                    select_rect = 100
                elif event.key == pygame.K_RETURN:
                    # New level
                    tubes, tube_colors = generate_start()
                    initial_colors = copy.deepcopy(tube_colors)
                    game_time = 0
                    stars = 0
                    selected = False
                    select_rect = 100
                    animation['state'] = AnimationState.IDLE
                    win = False

    # -------- UPDATE PHASE --------
    if game_state["screen"] == "main_menu":
        for btn in menu_buttons:
            btn.update(mouse_pos)
    elif game_state["screen"] in ["options", "how_to_play"]:
        back_button.update(mouse_pos)
    elif game_state["screen"] == "playing":
        back_button.update(mouse_pos)
        # Update animation
        update_animation(tube_colors, fps)
        # Update timer
        game_time += 1 / fps
        # Check victory
        win = check_victory(tube_colors)
        if win and stars == 0:
            stars = calculate_stars(game_time)

    # -------- DRAW PHASE --------
    screen.fill(BACKGROUND)
    if use_background_image:
        screen.blit(background_image, (0,0))

    if game_state["screen"] == "main_menu":
        drawing.draw_main_menu(screen, menu_buttons, save_data, use_background_image, background_image)
    elif game_state["screen"] == "options":
        drawing.draw_options(screen, back_button, use_background_image, background_image)
    elif game_state["screen"] == "how_to_play":
        drawing.draw_how_to_play(screen, back_button, use_background_image, background_image)
    elif game_state["screen"] == "playing":
        drawing.draw_playing(screen, back_button, use_background_image, background_image)
        # Draw tubes & moving tube
        for rect in get_all_tube_rects(tubes):
            drawing.draw_tubes(
                screen,
                tubes,
                tube_colors,
                color_choices,
                COLOR_RGB,
                animation,
                AnimationState,
                select_rect,
                get_tube_rect
            )
        draw_moving_tube()

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
sys.exit()