tutorial_levels = [
    {
        "tubes": 2,  # Level 1
        "colors": 1,
        "layout": [
            [0, 0, 0],
            [0]
        ]
    },
    {
        "tubes": 3,  # Level 2
        "colors": 2,
        "layout": [
            [1, 1],
            [0, 0, 0],
            [1, 1, 0]
        ]
    },
    {
        "tubes": 5,  # Level 2
        "colors": 3,
        "layout": [
            [2, 2, 2, 1],
            [0, 0, 1, 1],
            [0, 0, 1],
            [2],
            []
        ]
    }
]

levels = [
    {
        "tubes": 4,  # Level 1
        "colors": 2,
        "star_times": [20, 40, 60],  # 3 stars: <20s, 2 stars: <40s, 1 star: <60s
        "layout": [
            [0, 1, 1, 0],  # Tube 1
            [0, 1, 0, 1],  # Tube 2
            [],             # Empty
            []              # Empty
        ]
    },
    
    {
        "tubes": 5,
        "colors": 3,
        "star_times": [30, 60, 90],  # Level 2 thresholds
        "layout": [
            [0, 1, 2, 1],  # Level 2
            [1, 0, 1, 2],
            [2, 0, 0, 2],
            [],
            []
        ]
    },

    {
        "tubes": 7,
        "colors": 5,
        "star_times": [40, 80, 120],  # Level 3 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 3
            [0, 1, 4, 3],
            [0, 2, 4, 1],
            [4, 3, 2, 1],
            [4, 3, 0, 2],
            [],
            []
        ]
    },
    
    {
        "tubes": 7,
        "colors": 5,
        "star_times": [50, 100, 150],  # Level 4 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 4
            [4, 0, 1, 2],
            [3, 4, 0, 1],
            [2, 3, 4, 0],
            [1, 2, 3, 4],
            [],
            []
        ]
    },
    
    {
        "tubes": 8,
        "colors": 6,
        "star_times": [60, 120, 180],  # Level 5 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 5
            [0, 1, 4, 5],
            [0, 2, 4, 5],
            [3, 1, 2, 5],
            [4, 3, 5, 2],
            [4, 3, 1, 0],
            [],
            []
        ]
    },
    
    {
        "tubes": 8,
        "colors": 6,
        "star_times": [70, 140, 210],  # Level 6 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 6
            [4, 5, 0, 1],
            [2, 3, 4, 5],
            [5, 4, 3, 2],
            [1, 0, 5, 4],
            [3, 2, 1, 0],
            [],
            []
        ]
    },
    
    {
        "tubes": 9,
        "colors": 7,
        "star_times": [80, 160, 240],  # Level 7 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 7
            [0, 1, 4, 5],
            [0, 2, 4, 6],
            [3, 1, 2, 6],
            [4, 3, 5, 6],
            [4, 3, 1, 0],
            [5, 2, 6, 5],
            [],
            []
        ]
    },
    
    {
        "tubes": 9,
        "colors": 7,
        "star_times": [90, 180, 270],  # Level 8 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 8
            [4, 5, 6, 0],
            [1, 2, 3, 4],
            [5, 6, 0, 1],
            [2, 3, 4, 5],
            [6, 0, 1, 2],
            [3, 4, 5, 6],
            [],
            []
        ]
    },
    
    {
        "name": "Level 9 - Master Challenge",
        "difficulty": 4,
        "tubes": 10,
        "colors": 8,
        "star_times": [100, 200, 300],  # Level 9 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 9
            [0, 1, 4, 5],
            [0, 2, 4, 6],
            [3, 1, 2, 6],
            [4, 3, 5, 7],
            [4, 3, 1, 0],
            [5, 2, 6, 7],
            [7, 6, 5, 7],
            [],
            []
        ]
    },
    
    {
        "tubes": 10,
        "colors": 8,
        "star_times": [120, 240, 360],  # Level 10 thresholds
        "layout": [
            [0, 1, 2, 3],  # Level 10
            [4, 5, 6, 7],
            [7, 6, 5, 4],
            [3, 2, 1, 0],
            [0, 2, 4, 6],
            [1, 3, 5, 7],
            [2, 4, 6, 0],
            [3, 5, 7, 1],
            [],
            []
        ]
    }
]

# Color index to name mapping (matches your color_choices list)
COLOR_NAMES = [
    'red',           # 0
    'orange',        # 1
    'light blue',    # 2
    'dark blue',     # 3
    'dark green',    # 4
    'pink',          # 5
    'purple',        # 6
    'dark gray',     # 7
    'brown',         # 8
    'light green',   # 9
    'yellow',        # 10
    'white'          # 11
]

def get_level(level_num):
    """Get level data by number (1-10)"""
    if 1 <= level_num <= len(levels):
        return levels[level_num - 1]
    else:
        return None

def get_tut_level(level_num):
    """Get level data by number (1-10)"""
    if 1 <= level_num <= len(tutorial_levels):
        return tutorial_levels[level_num - 1]
    else:
        return None

def get_total_levels():
    """Get total number of levels"""
    return len(levels)

def get_tut_total_levels():
    return len(tutorial_levels)

def get_level_layout(level_num):
    """Get just the tube layout for a level"""
    level = get_level(level_num)
    if level:
        return level["layout"]
    return None

def get_level_star_times(level_num):
    """Get star time thresholds for a level"""
    level = get_level(level_num)
    if level and "star_times" in level:
        return level["star_times"]
    return [60, 120, 180]  # Default if not specified

def print_level_info(level_num):
    """Print level information (for debugging)"""
    level = get_level(level_num)
    if level:
        print(f"Level {level_num}: {level.get('name', 'Unnamed Level')}")
        print(f"Difficulty: {level.get('difficulty', 'N/A')}/5")
        print(f"Tubes: {level['tubes']} (Colors: {level['colors']})")
        if "star_times" in level:
            print(f"Star Times: {level['star_times'][0]}s for 3 stars, {level['star_times'][1]}s for 2 stars, {level['star_times'][2]}s for 1 star")
        print("Layout:")
        for i, tube in enumerate(level['layout']):
            color_names = [COLOR_NAMES[idx] for idx in tube]
            print(f"  Tube {i+1}: {color_names}")