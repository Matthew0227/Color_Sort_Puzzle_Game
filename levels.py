tutorial_levels = [
    {
        "tubes": 2,  
        "colors": 1,
        "layout": [
            [0, 0, 0],
            [0]
        ]
    },
    {
        "tubes": 3,  
        "colors": 2,
        "layout": [
            [1, 1],
            [0, 0, 0],
            [1, 1, 0]
        ]
    },
    {
        "tubes": 5,  
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
        "tubes": 4,  
        "colors": 2,
        "star_times": [20, 40, 60],  
        "layout": [
            [0, 1, 1, 0],  
            [0, 1, 0, 1],  
            [],             
            []              
        ]
    },
    
    {
        "tubes": 5,
        "colors": 3,
        "star_times": [30, 60, 90],  
        "layout": [
            [0, 1, 2, 1],  
            [1, 0, 1, 2],
            [2, 0, 0, 2],
            [],
            []
        ]
    },

    {
        "tubes": 7,
        "colors": 5,
        "star_times": [40, 80, 120],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [50, 100, 150],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [60, 120, 180],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [70, 140, 210],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [80, 160, 240],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [90, 180, 270],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [100, 200, 300],  
        "layout": [
            [0, 1, 2, 3],  
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
        "star_times": [120, 240, 360],  
        "layout": [
            [0, 1, 2, 3],  
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


COLOR_NAMES = [
    'red',           
    'orange',        
    'light blue',    
    'dark blue',     
    'dark green',    
    'pink',          
    'purple',        
    'dark gray',     
    'brown',         
    'light green',   
    'yellow',        
    'white'          
]

def get_level(level_num):
    if 1 <= level_num <= len(levels):
        return levels[level_num - 1]
    else:
        return None

def get_tut_level(level_num):
    if 1 <= level_num <= len(tutorial_levels):
        return tutorial_levels[level_num - 1]
    else:
        return None

def get_total_levels():
    return len(levels)

def get_tut_total_levels():
    return len(tutorial_levels)

def get_level_layout(level_num):
    level = get_level(level_num)
    if level:
        return level["layout"]
    return None

def get_level_star_times(level_num):
    level = get_level(level_num)
    if level and "star_times" in level:
        return level["star_times"]
    return [60, 120, 180]  

def print_level_info(level_num):
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