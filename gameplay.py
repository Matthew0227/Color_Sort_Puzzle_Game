import copy
import random
import math


# Game variables
tube_colors = []
initial_colors = []
tubes = 0  # Will be set by generate_start
new_game = True

def gameplay_update(events, dt):
    global tube_colors, tubes, new_game

    # Example: generate new game if needed
    if new_game:
        tubes, tube_colors = generate_start()
        new_game = False
        # Return any other info main.py might need
        return
    
def reset_game():
    global tube_colors, initial_colors, tubes, new_game
    tubes, tube_colors = generate_start()
    initial_colors = copy.deepcopy(tube_colors)
    new_game = False

def calculate_stars(time_taken):
    """Calculate stars based on time taken - LIVE UPDATE"""
    if time_taken < 20:
        return 3  # 3 gold stars for under 20 seconds
    elif time_taken < 40:
        return 2  # 2 gold stars for under 40 seconds
    elif time_taken < 60:
        return 1  # 1 gold star for under 60 seconds
    else:
        return 0  # 0 gold stars (all silver) for 60+ seconds

# select a number of tubes and pick random colors upon new game setup
def generate_start():
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

def check_move_validity(source, dest, tube_colors):
    """Check if a move from source to dest is valid"""
    if source == dest:
        return False, 0, 0

    if len(tube_colors[source]) == 0:
        return False, 0, 0

    # Get top color and count of consecutive same colors
    top_color = tube_colors[source][-1]
    count = 1
    for i in range(2, len(tube_colors[source]) + 1):
        if tube_colors[source][-i] == top_color:
            count += 1
        else:
            break

    # Check destination
    if len(tube_colors[dest]) >= 4:
        return False, 0, 0

    if len(tube_colors[dest]) > 0:
        if tube_colors[dest][-1] != top_color:
            return False, 0, 0

    # Calculate how many can be poured
    available_space = 4 - len(tube_colors[dest])
    move_count = min(count, available_space)

    return True, top_color, move_count

# STACK-BASED MOVE LOGIC (LIFO) - Original function kept for reference
def calc_move(colors, selected_rect, destination):
    # cannot move to same stack
    if selected_rect == destination:
        return colors

    source_stack = colors[selected_rect]
    dest_stack = colors[destination]

    # empty source stack
    if not source_stack:
        return colors

    # destination stack is full (capacity = 4)
    if len(dest_stack) == 4:
        return colors

    # peek top of source stack
    color_to_move = source_stack[-1]

    # count chain of same color on top (stack behavior)
    chain_length = 1
    for i in range(len(source_stack) - 2, -1, -1):
        if source_stack[i] == color_to_move:
            chain_length += 1
        else:
            break

    # destination must be empty or same color on top
    if dest_stack and dest_stack[-1] != color_to_move:
        return colors

    # available space in destination stack
    space = 4 - len(dest_stack)
    moves = min(chain_length, space)

    # pop from source and push to destination
    for _ in range(moves):
        dest_stack.append(source_stack.pop())

    return colors


# check if every tube with colors is 4 long and all the same color
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