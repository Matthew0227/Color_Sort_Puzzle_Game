import copy

def check_move_validity(source, dest, tube_colors):
    if source == dest or not tube_colors[source]:
        return False, 0, 0
    top_color = tube_colors[source][-1]
    count = 1
    for i in range(2, len(tube_colors[source])+1):
        if tube_colors[source][-i] == top_color:
            count += 1
        else:
            break
    if len(tube_colors[dest]) >= 4:
        return False, 0, 0
    if tube_colors[dest] and tube_colors[dest][-1] != top_color:
        return False, 0, 0
    move_count = min(count, 4 - len(tube_colors[dest]))
    return True, top_color, move_count

def check_victory(tube_colors):
    for tube in tube_colors:
        if tube and (len(tube) != 4 or len(set(tube)) != 1):
            return False
    return True

def calculate_stars(level_index, time_taken, LEVEL_STAR_TIMES):
    thresholds = LEVEL_STAR_TIMES[level_index]
    time_taken = int(time_taken)
    if time_taken <= thresholds[0]: return 3
    elif time_taken <= thresholds[1]: return 2
    elif time_taken <= thresholds[2]: return 1
    else: return 0

def load_level(level_index, LEVELS):
    return len(LEVELS[level_index]), copy.deepcopy(LEVELS[level_index])
