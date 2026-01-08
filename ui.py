#ui.py
import pygame
from assets import (
    BUTTON_COLOR,
    BUTTON_HOVER,
    BUTTON_TEXT,
    SHADOW_COLOR,
    button_font
)

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, SHADOW_COLOR, self.rect, 4, border_radius=12)

        text_surf = button_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return self.action
        return None
    
