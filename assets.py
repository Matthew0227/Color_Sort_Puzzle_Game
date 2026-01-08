import pygame

pygame.init()

# Colors
BACKGROUND = (25, 25, 40)
TITLE_COLOR = (70, 200, 255)
BUTTON_COLOR = (50, 120, 180)
BUTTON_HOVER = (80, 160, 220)
BUTTON_TEXT = (240, 240, 240)
TEXT_COLOR = (220, 220, 220)
SHADOW_COLOR = (10, 10, 20)

# Fonts
title_font = pygame.font.SysFont("arial", 76, bold=True)
button_font = pygame.font.SysFont("arial", 36)
info_font = pygame.font.SysFont("arial", 24)

#Gameplay Assets
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']

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

LEVELS = [
    [[0, 0, 0],[0]],
    [[0, 1, 0, 2],[1, 2, 1, 0],[2, 0, 2, 1],[],[]],
    [[0, 1, 2, 3],[0, 1, 2, 3],[0, 1, 2, 3],[0, 1, 2, 3],[],[]],
    [[0, 0, 1, 1],[2, 2, 3, 3],[0, 1, 2, 3],[0, 1, 2, 3],[],[]],
    [[0, 1, 0, 2],[1, 2, 3, 3],[0, 1, 2, 3],[0, 1, 2, 3],[],[]],
    [[0, 1, 2, 0],[1, 2, 3, 3],[4, 4, 0, 2],[1, 3, 4, 1],[],[],[]],
    [[0, 1, 2, 0],[1, 2, 3, 3],[4, 0, 1, 2],[3, 4, 4, 0],[],[],[]],
    [[0, 1, 2, 3],[3, 2, 1, 0],[4, 5, 4, 5],[0, 1, 2, 3],[],[],[],[]],
    [[0, 1, 2, 3],[3, 2, 1, 0],[4, 5, 0, 1],[2, 3, 4, 5],[],[],[],[]],
    [[0, 1, 2, 3],[3, 2, 1, 0],[4, 5, 0, 1],[2, 3, 4, 5],[],[],[],[]]
]

LEVEL_STAR_TIMES = [
    [20, 40, 60],
    [25, 50, 75],
    [30, 60, 90],
    [35, 70, 105],
    [40, 80, 120],
    [45, 90, 135],
    [50, 100, 150],
    [55, 110, 165],
    [60, 120, 180],
    [70, 140, 210]
]