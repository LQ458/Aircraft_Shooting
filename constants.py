import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Game mechanics
PLAYER_SPEED = 8
BULLET_SPEED = 7
ENEMY_SPEED = 1
GAME_DURATION = 90  # seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
LIGHT_BLUE = (122, 186, 255)
NEON_PURPLE = (187, 134, 252)
DEEP_PURPLE = (98, 0, 238)
CARD_BG = (249, 250, 251)
CARD_SHADOW = (229, 232, 236)
CORRECT_GREEN = (75, 219, 106)
WRONG_RED = (219, 75, 75)

# UI
BACKGROUND_COLOR_TOP = (30, 30, 40)
BACKGROUND_COLOR_BOTTOM = (20, 20, 30)

# Fonts
pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 72)
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 32)
FONT_SMALL = pygame.font.Font(None, 24)