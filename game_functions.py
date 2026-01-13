import copy
import random
import pygame
import sys
import math
import levels
import star_tracker

# Initialize pygame
pygame.init()

# Initialize game variables
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Color Sort PyGame')
font = pygame.font.SysFont('arial', 36, bold=True)
small_font = pygame.font.SysFont('arial', 24, bold=True)
fps = 60
timer = pygame.time.Clock()
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']

# Color definitions for pygame
COLOR_RGB = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'light blue': (173, 216, 230),
    'dark blue': (0, 0, 139),
    'dark green': (0, 100, 0),
    'pink': (255, 192, 203),
    'purple': (128, 0, 128),
    'dark gray': (169, 169, 169),
    'brown': (165, 42, 42),
    'light green': (144, 238, 144),
    'yellow': (255, 255, 0),
    'white': (255, 255, 255)
}

# Animation states
class AnimationState:
    IDLE = 0
    MOVE = 1
    POUR = 2
    RETURN = 3

# Game variables (will be initialized per game)
tube_colors = []
initial_colors = []
tubes = 0
new_game = True
tutorial_game = True
selected = False
tube_rects = []
select_rect = 100
win = False
game_time = 0
stars = 0
current_star_times = [60, 120, 180]

# Animation variables
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

# Initialize star tracker
star_tracker_instance = star_tracker.StarTracker()

def draw_stars(x, y, num_stars):
    star_size = 30
    star_spacing = 60

    for i in range(3):
        star_x = x + i * star_spacing
        star_y = y

        if i < num_stars:
            color = (255, 215, 0)
        else:
            color = (100, 100, 100)

        draw_star_shape(screen, color, star_x, star_y, star_size)

def draw_star_shape(surf, color, x, y, size):
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

def calculate_stars(time_taken, star_times):
    if time_taken < star_times[0]:
        return 3
    elif time_taken < star_times[1]:
        return 2
    elif time_taken < star_times[2]:
        return 1
    else:
        return 0

def generate_start(level_num=None):
    if level_num is not None and 1 <= level_num <= levels.get_total_levels():
        level_data = levels.get_level(level_num)
        if level_data:
            tubes = level_data["tubes"]
            tube_colors = [tube.copy() for tube in level_data["layout"]]
            return tubes, tube_colors
    
    tubes_number = random.randint(10, 14)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    return tubes_number, tubes_colors

def tut_generate_start(level_num=None):
    if level_num is not None and 1 <= level_num <= levels.get_tut_total_levels():
        level_data = levels.get_tut_level(level_num)
        if level_data:
            tubes = level_data["tubes"]
            tube_colors = [tube.copy() for tube in level_data["layout"]]
            return tubes, tube_colors
    
    tubes_number = random.randint(10, 14)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    return tubes_number, tubes_colors

def get_tube_rect(tubes_num, index):
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True

    spacing = WIDTH / tubes_per_row
    start_x = 50

    if offset:
        if index < tubes_per_row:
            x = start_x + spacing * index
            y = 100
            return pygame.Rect(x, y, 65, 200)
        else:
            x = start_x + spacing * (index - tubes_per_row) + spacing * 0.5
            y = 350
            return pygame.Rect(x, y, 65, 200)
    else:
        if index < tubes_per_row:
            x = start_x + spacing * index
            y = 100
            return pygame.Rect(x, y, 65, 200)
        else:
            x = start_x + spacing * (index - tubes_per_row)
            y = 350
            return pygame.Rect(x, y, 65, 200)
        
def get_centered_tube_rect(tubes_num, index):
    """Smart tube positioning that works for both game and tutorial"""
    # For tutorial (small number of tubes), use centered layout
    # For regular game (many tubes), use the original layout
    if tubes_num <= 6:  # Tutorial typically has fewer tubes
        tube_width = 65
        tube_spacing = 80
        total_width = tubes_num * tube_width + (tubes_num - 1) * tube_spacing
        start_x = (WIDTH - total_width) // 2
        
        x = start_x + index * (tube_width + tube_spacing)
        y = 250  # Centered vertically
        
        return pygame.Rect(x, y, tube_width, 200)
    else:
        # Use original layout for regular game
        if tubes_num % 2 == 0:
            tubes_per_row = tubes_num // 2
            offset = False
        else:
            tubes_per_row = tubes_num // 2 + 1
            offset = True

        spacing = WIDTH / tubes_per_row
        start_x = 50

        if offset:
            if index < tubes_per_row:
                x = start_x + spacing * index
                y = 100
                return pygame.Rect(x, y, 65, 200)
            else:
                x = start_x + spacing * (index - tubes_per_row) + spacing * 0.5
                y = 350
                return pygame.Rect(x, y, 65, 200)
        else:
            if index < tubes_per_row:
                x = start_x + spacing * index
                y = 100
                return pygame.Rect(x, y, 65, 200)
            else:
                x = start_x + spacing * (index - tubes_per_row)
                y = 350
                return pygame.Rect(x, y, 65, 200)

def draw_tubes(tubes_num, tube_cols):
    """Improved draw tubes that handles both game and tutorial layouts"""
    tube_boxes = []

    for i in range(tubes_num):
        if animation['state'] != AnimationState.IDLE and i == animation['source']:
            rect = get_centered_tube_rect(tubes_num, i)
            tube_boxes.append(rect)
            continue

        rect = get_centered_tube_rect(tubes_num, i)
        tube_boxes.append(rect)

        border_color = (0, 120, 255)
        if select_rect == i and animation['state'] == AnimationState.IDLE:
            border_color = (0, 255, 0)
        elif i >= tubes_num - 2 and len(tube_cols[i]) == 0:
            border_color = (100, 100, 100)

        pygame.draw.line(screen, border_color, (rect.x, rect.y), (rect.x, rect.y + rect.height), 5)
        pygame.draw.line(screen, border_color, (rect.x + rect.width, rect.y), 
                        (rect.x + rect.width, rect.y + rect.height), 5)
        pygame.draw.line(screen, border_color, (rect.x, rect.y + rect.height), 
                        (rect.x + rect.width, rect.y + rect.height), 5)

        for j in range(len(tube_cols[i])):
            color_idx = tube_cols[i][j]
            color_rect = pygame.Rect(rect.x + 2, rect.y + 150 - (j * 50), 61, 48)
            pygame.draw.rect(screen, COLOR_RGB[color_choices[color_idx]], color_rect, 0, 3)

    return tube_boxes

def draw_moving_tube():
    """Improved moving tube animation that works with both layouts"""
    if animation['state'] == AnimationState.IDLE:
        return

    tube_width = 65
    tube_height = 200

    source_rect = get_centered_tube_rect(tubes, animation['source'])
    dest_rect = get_centered_tube_rect(tubes, animation['dest'])

    progress = animation['progress']

    if animation['state'] == AnimationState.MOVE:
        # Move to position above destination tube
        target_x = dest_rect.x
        target_y = dest_rect.y - 100

        x = source_rect.x + (target_x - source_rect.x) * progress
        y = source_rect.y + (target_y - source_rect.y) * progress
        angle = 0
    elif animation['state'] == AnimationState.POUR:
        # Stay above destination and pour
        target_x = dest_rect.x
        target_y = dest_rect.y - 100

        x = target_x
        y = target_y
        angle = 90 * progress
    elif animation['state'] == AnimationState.RETURN:
        # Return to original position
        target_x = dest_rect.x
        target_y = dest_rect.y - 100

        x = target_x + (source_rect.x - target_x) * progress
        y = target_y + (source_rect.y - target_y) * progress
        angle = 90 * (1 - progress)

    animation['current_x'] = x
    animation['current_y'] = y
    animation['angle'] = angle

    padding = 20
    tube_surface = pygame.Surface((tube_width + padding * 2, tube_height + padding * 2), pygame.SRCALPHA)

    border_color = (0, 220, 0)
    pygame.draw.line(tube_surface, border_color, (padding, padding), (padding, padding + tube_height), 5)
    pygame.draw.line(tube_surface, border_color, (padding + tube_width, padding), 
                    (padding + tube_width, padding + tube_height), 5)
    pygame.draw.line(tube_surface, border_color, (padding, padding + tube_height), 
                    (padding + tube_width, padding + tube_height), 5)

    colors_to_draw = []
    if animation['state'] == AnimationState.MOVE:
        colors_to_draw = animation['all_colors'].copy()
    elif animation['state'] == AnimationState.POUR:
        pour_progress = min(1.0, progress * 3)
        colors_poured = int(len(animation['colors_to_pour']) * pour_progress)
        colors_to_draw = animation['remaining_colors'] + animation['colors_to_pour'][colors_poured:]
    elif animation['state'] == AnimationState.RETURN:
        colors_to_draw = animation['remaining_colors'].copy()

    for j, color_idx in enumerate(colors_to_draw):
        color_height = 48
        color_y = padding + tube_height - 52 - (j * 50)
        color_rect = pygame.Rect(padding + 2, color_y, tube_width - 4, color_height)
        pygame.draw.rect(tube_surface, COLOR_RGB[color_choices[color_idx]], color_rect, 0, 3)

    if angle != 0:
        rotated_surface = pygame.transform.rotate(tube_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=(x + tube_width//2 + padding, y + tube_height//2 + padding))
        screen.blit(rotated_surface, rotated_rect)
    else:
        screen.blit(tube_surface, (x - padding, y - padding))

def update_animation():
    if animation['state'] == AnimationState.IDLE:
        return False

    speeds = {
        AnimationState.MOVE: 0.2,
        AnimationState.POUR: 0.4,
        AnimationState.RETURN: 0.2
    }

    animation['progress'] += 1.0 / (fps * speeds[animation['state']])

    if animation['progress'] >= 1.0:
        if animation['state'] == AnimationState.MOVE:
            animation['state'] = AnimationState.POUR
            animation['progress'] = 0.0
        elif animation['state'] == AnimationState.POUR:
            for _ in range(animation['count']):
                if len(tube_colors[animation['source']]) > 0:
                    color = tube_colors[animation['source']].pop()
                    tube_colors[animation['dest']].append(color)

            animation['state'] = AnimationState.RETURN
            animation['progress'] = 0.0
        elif animation['state'] == AnimationState.RETURN:
            animation['state'] = AnimationState.IDLE
            animation['progress'] = 0.0
            return True

    return False

def check_move_validity(source, dest):
    if source == dest:
        return False, 0, 0

    if len(tube_colors[source]) == 0:
        return False, 0, 0

    top_color = tube_colors[source][-1]
    count = 1
    for i in range(2, len(tube_colors[source]) + 1):
        if tube_colors[source][-i] == top_color:
            count += 1
        else:
            break

    if len(tube_colors[dest]) >= 4:
        return False, 0, 0

    if len(tube_colors[dest]) > 0:
        if tube_colors[dest][-1] != top_color:
            return False, 0, 0

    available_space = 4 - len(tube_colors[dest])
    move_count = min(count, available_space)

    return True, top_color, move_count

def start_animation(source, dest):
    is_valid, color, count = check_move_validity(source, dest)

    if not is_valid:
        return

    animation['state'] = AnimationState.MOVE
    animation['source'] = source
    animation['dest'] = dest
    animation['color'] = color
    animation['count'] = count
    animation['progress'] = 0.0

    animation['all_colors'] = tube_colors[source].copy()

    animation['colors_to_pour'] = []
    for i in range(min(count, len(tube_colors[source]))):
        animation['colors_to_pour'].append(tube_colors[source][-1 - i])
    animation['colors_to_pour'].reverse()

    animation['remaining_colors'] = []
    if len(tube_colors[source]) > count:
        animation['remaining_colors'] = tube_colors[source][:-count].copy()

def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won

# Main game function (called from main.py)
def run_game(level_num):
    global tube_colors, initial_colors, tubes, new_game, selected, tube_rects, select_rect, win, game_time, stars, current_star_times, animation
    
    try:
        tracker = star_tracker_instance  # Use existing global
    except:
        tracker = star_tracker.StarTracker()

    # Reset game state
    current_level = level_num
    new_game = True
    selected = False
    select_rect = 100
    win = False
    game_time = 0
    stars = 0
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
    best_stars, best_time = star_tracker_instance.get_best_stars(current_level)

    run = True
    while run:
        screen.fill((20, 20, 40))

        if animation['state'] != AnimationState.IDLE:
            update_animation()

        if new_game:
            tubes, tube_colors = generate_start(current_level)
            initial_colors = copy.deepcopy(tube_colors)
            game_time = 0
            stars = 0
            current_star_times = levels.get_level_star_times(current_level)
            new_game = False
            animation['state'] = AnimationState.IDLE
            win = False
        else:
            tube_rects = draw_tubes(tubes, tube_colors)

        draw_moving_tube()

        if not win:
            game_time += 1 / fps

        win = check_victory(tube_colors)
        if win and stars == 0:
            stars = calculate_stars(game_time, current_star_times)
            star_tracker_instance.push_star_achievement(current_level, stars, game_time)
        
        best_stars, best_time = star_tracker_instance.get_best_stars(current_level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return stars

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    tube_colors = copy.deepcopy(initial_colors)
                    stars = 0
                    win = False
                    animation['state'] = AnimationState.IDLE
                    selected = False
                    select_rect = 100
                elif event.key == pygame.K_RETURN:
                    new_game = True
                    selected = False
                    select_rect = 100
                elif event.key == pygame.K_ESCAPE:
                    # Return to menu
                    return stars
                elif event.key == pygame.K_s:
                    star_tracker_instance.display_stats()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if animation['state'] != AnimationState.IDLE:
                    continue

                if not selected:
                    for item in range(len(tube_rects)):
                        if tube_rects[item].collidepoint(event.pos):
                            selected = True
                            select_rect = item
                else:
                    for item in range(len(tube_rects)):
                        if tube_rects[item].collidepoint(event.pos):
                            start_animation(select_rect, item)
                            selected = False
                            select_rect = 100
        
        if win:
            victory_text = font.render('You Won! Press ESC to return to menu!', True, 'white')
            star_text = font.render(f'Stars earned: {stars}', True, 'yellow')
            
            box_width = max(victory_text.get_width(), star_text.get_width()) + 80
            box_height = 120
            box_x = WIDTH//2 - box_width//2
            box_y = HEIGHT//2 - box_height//2 - 20
            
            pygame.draw.rect(screen, (30, 30, 70), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (0, 200, 255), (box_x, box_y, box_width, box_height), 4)
            
            screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, box_y + 30))
            screen.blit(star_text, (WIDTH//2 - star_text.get_width()//2, box_y + 80))

        timer_text = font.render(f'Time: {game_time:.2f}s', True, 'yellow')
        screen.blit(timer_text, (WIDTH - 300, 20))

        if win:
            current_stars = stars
        else:
            current_stars = calculate_stars(game_time, current_star_times)
        draw_stars(50, 60, current_stars)

        level_text = font.render(f'Level {current_level}', True, 'white')
        screen.blit(level_text, (50, HEIGHT - 50))

        if best_time > 0:
            best_time_text = small_font.render(f'Best: {best_time:.2f}s', True, (144, 238, 144))
            screen.blit(best_time_text, (WIDTH - 250, HEIGHT - 50))
        else:
            no_best_text = small_font.render(f'Best: --', True, (150, 150, 150))
            screen.blit(no_best_text, (WIDTH - 250, HEIGHT - 50))

        restart_text = font.render('Stuck? Press "space" to restart!', True, 'white')
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 20))

        pygame.display.flip()
        timer.tick(fps)

def run_how_to_play_screen():
    global tube_colors, initial_colors, tubes, tutorial_game, selected, tube_rects, select_rect, win, animation
    
    tutorial_level = 1
    tutorial_game = True
    selected = False
    select_rect = 100
    win = False
    tutorial_complete = False
    instruction_state = "select_first"  # Track tutorial instruction state

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

    # Initialize the tutorial game
    tubes, tube_colors = tut_generate_start(tutorial_level)
    initial_colors = copy.deepcopy(tube_colors)

    run = True
    while run:
        screen.fill((20, 20, 40))

        if animation['state'] != AnimationState.IDLE:
            update_animation()

        # Use the improved draw functions (they automatically center for tutorial)
        tube_rects = draw_tubes(tubes, tube_colors)
        draw_moving_tube()

        win = check_victory(tube_colors)

        if win and not tutorial_complete:
            pygame.time.delay(500)  # Small delay to show completed state
            if tutorial_level < 3:
                tutorial_level += 1
                tubes, tube_colors = tut_generate_start(tutorial_level)
                initial_colors = copy.deepcopy(tube_colors)
                animation['state'] = AnimationState.IDLE
                win = False
                selected = False
                select_rect = 100
                instruction_state = "select_first"  # Reset for next level
            else:
                tutorial_complete = True  # Player has completed all tutorial levels

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return "quit"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    tube_colors = copy.deepcopy(initial_colors)
                    win = False
                    animation['state'] = AnimationState.IDLE
                    selected = False
                    select_rect = 100
                    instruction_state = "select_first"  # Reset tutorial instructions
                elif event.key == pygame.K_ESCAPE:
                    return "main_menu"
                elif event.key == pygame.K_s:
                    star_tracker_instance.display_stats()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if animation['state'] != AnimationState.IDLE:
                    continue

                if not selected:
                    for item in range(len(tube_rects)):
                        if tube_rects[item].collidepoint(event.pos):
                            selected = True
                            select_rect = item
                            if instruction_state == "select_first":
                                instruction_state = "select_second"  # Update instruction state
                else:
                    for item in range(len(tube_rects)):
                        if tube_rects[item].collidepoint(event.pos):
                            start_animation(select_rect, item)
                            selected = False
                            select_rect = 100
                            if instruction_state == "select_second":
                                instruction_state = "completed_move"  # Player completed a move

        # ESC instruction at the top
        esc_text = small_font.render('Press ESC to return to menu', True, (200, 200, 200))
        screen.blit(esc_text, (WIDTH - esc_text.get_width() - 20, 20))

        # Display tutorial instructions based on level and state
        if tutorial_level == 1 and not win:
            if instruction_state == "select_first":
                instruction_text = font.render('Press the container to select it', True, (0, 255, 255))
                screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 100))
            elif instruction_state == "select_second":
                instruction_text = font.render('Tap another container to pour', True, (0, 255, 255))
                screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 100))
        
        elif tutorial_level == 2 and not win:
            instruction_text = font.render('Only SAME COLOR can be poured on top of each other', True, (0, 255, 255))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 100))
        
        elif tutorial_level == 3 and not win:
            instruction_text = font.render('Fill containers with 4 same colors to win!', True, (0, 255, 255))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 100))

        # Display completion message
        if tutorial_complete:
            complete_text = font.render('Tutorial Completed! Press ESC to return to menu!', True, 'white')
            box_width = complete_text.get_width() + 80
            box_height = 120
            box_x = WIDTH//2 - box_width//2
            box_y = HEIGHT//2 - box_height//2 - 20
            pygame.draw.rect(screen, (30, 30, 70), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (0, 200, 255), (box_x, box_y, box_width, box_height), 4)
            screen.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, box_y + 30))
        elif win:
            victory_text = font.render('You Won! Proceeding to next tutorial...', True, 'white')
            box_width = victory_text.get_width() + 80
            box_height = 120
            box_x = WIDTH//2 - box_width//2
            box_y = HEIGHT//2 - box_height//2 - 20
            pygame.draw.rect(screen, (30, 30, 70), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (0, 200, 255), (box_x, box_y, box_width, box_height), 4)
            screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, box_y + 30))

        # Restart instruction at bottom
        restart_text = small_font.render('Press SPACE to restart', True, (200, 200, 200))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT - 40))

        pygame.display.flip()
        timer.tick(fps)
    return "main_menu"