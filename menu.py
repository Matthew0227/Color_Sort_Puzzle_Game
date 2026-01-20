import pygame
import sys
import os
import star_tracker

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle")

BACKGROUND = (25, 25, 40)
TITLE_COLOR = (70, 200, 255)
BUTTON_COLOR = (50, 120, 180)
BUTTON_HOVER = (80, 160, 220)
BUTTON_TEXT = (240, 240, 240)
TEXT_COLOR = (220, 220, 220)
SHADOW_COLOR = (10, 10, 20)
SLIDER_COLOR = (100, 100, 140)
SLIDER_HANDLE = (70, 200, 255)
LEVEL_COLOR = (60, 140, 200)
LEVEL_HOVER = (90, 180, 240)
STAR_EMPTY = (100, 100, 120)
STAR_FILLED = (255, 215, 0) 
LEVEL_TITLE_COLOR = (255, 255, 255)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = resource_path("assets")

background_image_main = None
background_image_level_select = None
use_background_image_main = False
use_background_image_level_select = False

possible_paths_main = [
    os.path.join(ASSETS_DIR, "background.jpg"),
    os.path.join(ASSETS_DIR, "menu_background.jpg"),
    os.path.join(ASSETS_DIR, "background.png"),
    "background.jpg",
    os.path.join("assets", "background.jpg")
]

for path in possible_paths_main:
    try:
        background_image_main = pygame.image.load(path).convert()
        background_image_main = pygame.transform.scale(background_image_main, (SCREEN_WIDTH, SCREEN_HEIGHT))
        use_background_image_main = True
        break
    except (pygame.error, FileNotFoundError):
        continue

possible_paths_level = [
    os.path.join(ASSETS_DIR, "background_level_select.jpg"),
    os.path.join(ASSETS_DIR, "level_select_background.jpg"),
    os.path.join(ASSETS_DIR, "background_level.png"),
    "background_level_select.jpg",
    os.path.join("assets", "background_level_select.jpg")
]

for path in possible_paths_level:
    try:
        background_image_level_select = pygame.image.load(path).convert()
        background_image_level_select = pygame.transform.scale(background_image_level_select, (SCREEN_WIDTH, SCREEN_HEIGHT))
        use_background_image_level_select = True
        break
    except (pygame.error, FileNotFoundError):
        continue

if not use_background_image_level_select and use_background_image_main:
    background_image_level_select = background_image_main
    use_background_image_level_select = True

music_volume = 0.5

tracker = star_tracker.StarTracker()

try:
    music_path = os.path.join(ASSETS_DIR, "menu_music.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_volume)
except:
    try:
        music_path = os.path.join(ASSETS_DIR, "music.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(music_volume)
    except:
        pass

title_font = pygame.font.SysFont("arial", 76, bold=True)
button_font = pygame.font.SysFont("arial", 36)
info_font = pygame.font.SysFont("arial", 24)
slider_font = pygame.font.SysFont("arial", 28)
level_font = pygame.font.SysFont("arial", 32, bold=True)

class Button:
    def __init__(self, x, y, width, height, text, action=None, data=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.data = data
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, SHADOW_COLOR, self.rect, 4, border_radius=12)
        text_surf = button_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                return self.action, self.data
        return None, None

class LevelButton:
    def __init__(self, x, y, size, level_num, stars=0, is_locked=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.level_num = level_num
        self.stars = stars
        self.hovered = False
        self.is_locked = is_locked
        
    def draw(self, surface):     
        if self.is_locked:
            color = (40, 40, 60)  
        else:
            color = LEVEL_HOVER if self.hovered else LEVEL_COLOR
        
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, SHADOW_COLOR, self.rect, 4, border_radius=15)
        run_level_select_screen

        level_text = level_font.render(str(self.level_num), True, BUTTON_TEXT)
        text_rect = level_text.get_rect(center=(self.rect.centerx, self.rect.centery - 15))
        surface.blit(level_text, text_rect)
        
        star_size = 20
        spacing = 10
        total_width = 3 * star_size + 2 * spacing
        start_x = self.rect.centerx - total_width // 2
        
        for i in range(3):
            star_x = start_x + i * (star_size + spacing)
            star_y = self.rect.centery + 15
            
            if i < self.stars:
                star_points = [
                    (star_x + star_size//2, star_y),
                    (star_x + star_size, star_y + star_size//3),
                    (star_x + star_size*3//4, star_y + star_size),
                    (star_x + star_size//4, star_y + star_size),
                    (star_x, star_y + star_size//3)
                ]
                pygame.draw.polygon(surface, STAR_FILLED, star_points)
                pygame.draw.polygon(surface, (200, 160, 0), star_points, 2)
            else:
                star_points = [
                    (star_x + star_size//2, star_y),
                    (star_x + star_size, star_y + star_size//3),
                    (star_x + star_size*3//4, star_y + star_size),
                    (star_x + star_size//4, star_y + star_size),
                    (star_x, star_y + star_size//3)
                ]
                pygame.draw.polygon(surface, STAR_EMPTY, star_points, 2)
                
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos) and not self.is_locked
        return self.hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and not self.is_locked:
                return "play_level", self.level_num
        return None, None

class Slider:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y - 5, 20, height + 10)
        self.handle_rect.centerx = x + int(width * music_volume)
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, SLIDER_COLOR, self.rect, border_radius=5)
        pygame.draw.rect(surface, SLIDER_HANDLE, self.handle_rect, border_radius=6)
        pygame.draw.rect(surface, SHADOW_COLOR, self.handle_rect, 2, border_radius=6)
        volume_text = slider_font.render(f"Music Volume: {int(music_volume * 100)}%", True, TEXT_COLOR)
        surface.blit(volume_text, (self.rect.x, self.rect.y - 40))

    def handle_event(self, event):
        global music_volume
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_rect.centerx = max(self.rect.left, 
                                             min(event.pos[0], self.rect.right))
                music_volume = (self.handle_rect.centerx - self.rect.left) / self.rect.width
                music_volume = max(0.0, min(1.0, music_volume))
                pygame.mixer.music.set_volume(music_volume)

level_stars = [0] * 10
level_buttons = []

def load_level_stars():
    global level_stars
    level_stars = [0] * 10
    for level in range(1, 11):
        best_stars, _ = tracker.get_best_stars(level)
        level_stars[level - 1] = best_stars

load_level_stars()

def create_level_buttons():
    global level_buttons
    level_buttons = []
    level_size = 100
    level_spacing = 20
    start_x = (SCREEN_WIDTH - (5 * level_size + 4 * level_spacing)) // 2
    start_y = 250
    
    unlocked_levels = tracker.get_unlocked_levels()
    
    for i in range(10):
        row = i // 5
        col = i % 5
        x = start_x + col * (level_size + level_spacing)
        y = start_y + row * (level_size + level_spacing)
        level_num = i + 1
        is_locked = level_num not in unlocked_levels
        level_buttons.append(LevelButton(x, y, level_size, level_num, level_stars[i], is_locked=is_locked))

create_level_buttons()

def draw_background(screen_type="main_menu"):
    if screen_type == "level_select":
        if use_background_image_level_select:
            screen.blit(background_image_level_select, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 20))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BACKGROUND)
    else:
        if use_background_image_main:
            screen.blit(background_image_main, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 20))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BACKGROUND)

def update_level_stars(level_num, stars_earned):
    if 1 <= level_num <= 10:
        if stars_earned > level_stars[level_num - 1]:
            level_stars[level_num - 1] = stars_earned
            
            tracker.push_star_achievement(level_num, stars_earned, 0)
            
            tracker.unlock_next_level(level_num)
            create_level_buttons()  
            return True
    return False

def run_menu_screen():
    buttons = [
        Button(190, 250, 300, 60, "Start Game", "level_select"),
        Button(190, 330, 300, 60, "Settings", "options"),
        Button(190, 410, 300, 60, "How to Play", "how_to_play"),
        Button(190, 490, 300, 60, "Quit", "quit")
    ]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            
            for button in buttons:
                button.check_hover(mouse_pos)
                action, data = button.handle_event(event)
                if action:
                    return action
        
        draw_background("main_menu")
        
        title_text = title_font.render("Color Sort Puzzle", True, TITLE_COLOR)
        title_shadow = title_font.render("Color Sort Puzzle", True, SHADOW_COLOR)
        title_x = 100
        title_y = 120
        screen.blit(title_shadow, (title_x + 4, title_y + 4))
        screen.blit(title_text, (title_x, title_y))
        
        subtitle = info_font.render("Sort the colors into the correct containers!", True, TEXT_COLOR)
        screen.blit(subtitle, (title_x + 65, title_y + 85))
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def run_level_select_screen():
    global level_buttons
    tracker.load_data()
    create_level_buttons()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", 0
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back", 0
            
            back_button = Button(50, 40, 120, 50, "← Back", "back")
            back_button.check_hover(mouse_pos)
            action, data = back_button.handle_event(event)
            if action == "back":
                return "back", 0
            
            for level_button in level_buttons:
                level_button.check_hover(mouse_pos)
                action, level_num = level_button.handle_event(event)
                if action == "play_level":
                    return "play_level", level_num
        
        draw_background("level_select")
        
        back_button = Button(50, 40, 120, 50, "← Back", "back")
        back_button.draw(screen)
        
        title = title_font.render("SELECT LEVEL", True, LEVEL_TITLE_COLOR)
        title_shadow = title_font.render("SELECT LEVEL", True, SHADOW_COLOR)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        title_y = 150
        screen.blit(title_shadow, (title_x + 3, title_y + 3))
        screen.blit(title, (title_x, title_y))
        
        for level_button in level_buttons:
            level_button.draw(screen)
                
        next_locked = tracker.get_next_locked_level()
        if next_locked:
            
            card_width, card_height = 500, 80
            
            max_bottom = 0
            for btn in level_buttons:
                if btn.rect.bottom > max_bottom:
                    max_bottom = btn.rect.bottom
            
            card_y = max_bottom + 20  
            card_x = SCREEN_WIDTH // 2 - card_width // 2
                        
            if card_y + card_height > SCREEN_HEIGHT - 50:
                card_y = SCREEN_HEIGHT - 50 - card_height
                       
            shadow_offset = 3
            pygame.draw.rect(screen, (25, 20, 15), 
                            (card_x + shadow_offset, card_y + shadow_offset, card_width, card_height),
                            border_radius=10)
                       
            pygame.draw.rect(screen, (45, 35, 25), 
                            (card_x, card_y, card_width, card_height),
                            border_radius=10)
                     
            pygame.draw.rect(screen, (120, 90, 60), 
                            (card_x, card_y, card_width, card_height),
                            width=2, border_radius=10)
                       
            icon_font = pygame.font.SysFont("Segoe UI Emoji", 28)
            lock_icon = icon_font.render("🔒", True, (255, 200, 100))
            screen.blit(lock_icon, (card_x + 15, card_y + card_height // 2 - lock_icon.get_height() // 2))
                       
            hint_text = info_font.render(f"Level {next_locked} locked • Complete Level {next_locked - 1} to unlock", 
                                        True, (255, 220, 180))
            screen.blit(hint_text, (card_x + 55, card_y + card_height // 2 - hint_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

def run_options_screen():
    slider = Slider(SCREEN_WIDTH//2 - 200, 250, 400, 15)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
            
            back_button = Button(50, 40, 120, 50, "← Back", "back")
            back_button.check_hover(mouse_pos)
            action, data = back_button.handle_event(event)
            if action == "back":
                return "back"
            
            slider.handle_event(event)
        
        draw_background("options")
        
        back_button = Button(50, 40, 120, 50, "← Back", "back")
        back_button.draw(screen)
        
        title = title_font.render("SETTINGS", True, TITLE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        slider.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)