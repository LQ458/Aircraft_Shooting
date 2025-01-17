import pygame
from constants import *
from utils import draw_neon_text, create_gradient_surface
import math
import shelve

class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    LEADERBOARD = 4

class MenuScreen:
    def __init__(self):
        self.background = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, 
                                               BACKGROUND_COLOR_TOP, 
                                               BACKGROUND_COLOR_BOTTOM)
        self.title_animation = 0
        
    def update(self):
        self.title_animation = (self.title_animation + 0.05) % (2 * math.pi)
        
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        # Animated title with glow effect
        title_offset = math.sin(self.title_animation) * 5
        draw_neon_text(screen, "Vocabulary Space",
                      FONT_TITLE, NEON_PURPLE,
                      (SCREEN_WIDTH//2 - 200, 150 + title_offset),
                      DEEP_PURPLE, 3)
        
        # Menu options with hover effect
        options = ["Press SPACE to Start", "Press H for Help", "Press L for Leaderboard"]
        for i, text in enumerate(options):
            draw_neon_text(screen, text,
                          FONT_MEDIUM, LIGHT_BLUE,
                          (SCREEN_WIDTH//2 - 150, 300 + i * 60),
                          BLUE, 2)

class PauseScreen:
    def draw(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BACKGROUND_COLOR_TOP)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        draw_neon_text(screen, "PAUSED",
                      FONT_LARGE, NEON_PURPLE,
                      (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50),
                      DEEP_PURPLE, 3)
        
        draw_neon_text(screen, "Press P to Resume",
                      FONT_MEDIUM, LIGHT_BLUE,
                      (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 30),
                      BLUE, 2)

class GameOverScreen:
    def draw(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BACKGROUND_COLOR_TOP)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        draw_neon_text(screen, "GAME OVER",
                      FONT_LARGE, NEON_PURPLE,
                      (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 80),
                      DEEP_PURPLE, 3)
        
        draw_neon_text(screen, f"Final Score: {score}",
                      FONT_MEDIUM, LIGHT_BLUE,
                      (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2),
                      BLUE, 2)
        
        draw_neon_text(screen, "Press SPACE to Play Again",
                      FONT_MEDIUM, LIGHT_BLUE,
                      (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 60),
                      BLUE, 2)

class LeaderboardScreen:
    def __init__(self):
        self.background = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, 
                                               BACKGROUND_COLOR_TOP, 
                                               BACKGROUND_COLOR_BOTTOM)
        self.scores = []
        self.page = 0
        self.load_scores()
        
    def load_scores(self):
        with shelve.open('leaderboard') as db:
            self.scores = db.get('scores', [])
        self.scores.sort(key=lambda x: x[1], reverse=True)
        
    def draw(self, screen):
        self.load_scores()  # Reload scores each time the leaderboard is drawn
        screen.blit(self.background, (0, 0))
        draw_neon_text(screen, "Leaderboard",
                      FONT_LARGE, NEON_PURPLE,
                      (SCREEN_WIDTH//2 - 150, 100),
                      DEEP_PURPLE, 3)
        
        # Display scores with pagination
        start_index = self.page * 10
        end_index = start_index + 10
        for i, (name, score) in enumerate(self.scores[start_index:end_index]):
            draw_neon_text(screen, f"{i + 1 + start_index}. {name}: {score}",
                          FONT_MEDIUM, LIGHT_BLUE,
                          (SCREEN_WIDTH//2 - 100, 200 + i * 40),
                          BLUE, 2)
        
        # Page navigation
        if self.page > 0:
            draw_neon_text(screen, "<- Prev",
                          FONT_SMALL, LIGHT_BLUE,
                          (50, SCREEN_HEIGHT - 50),
                          BLUE, 2)
        if end_index < len(self.scores):
            draw_neon_text(screen, "Next ->",
                          FONT_SMALL, LIGHT_BLUE,
                          (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50),
                          BLUE, 2)
        
        # Back to menu button
        draw_neon_text(screen, "Press SPACE to go back to Menu",
                      FONT_SMALL, LIGHT_BLUE,
                      (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 50),
                      BLUE, 2)
        
    def next_page(self):
        if (self.page + 1) * 10 < len(self.scores):
            self.page += 1
            
    def prev_page(self):
        if self.page > 0:
            self.page -= 1