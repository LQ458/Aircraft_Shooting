import pygame
import random
from typing import List
import asyncio
from constants import *
from sprites import ModernPlayer, ModernBullet
from game_states import GameState, MenuScreen, PauseScreen, GameOverScreen
from effects import ExplosionEffect, FeedbackText
from utils import create_gradient_surface
from js import document

vocab_list = {
"criticism": "making an unfavorable remark",
"unique": "the only one",
"flimsy": "frail or weak",
"tiresome": "boring or dull",
"considerate": "thoughtful",
"fatigue": "tired or weariness",
"ridiculous": "silly",
"vigor": "strength or energy",
"sluggish": "slow",
"substantial": "solid or firm",
"heedless": "inconsiderate",
"oasis": "a fertile place in a desert where there are water, trees, and other plants",
"flabbergast": "surprising someone",
"clarify": "making something clear",
"malfunction": "when something doesn't work",
"irrational": "not thinking clearly",
"accusation": "a charge against someone",
"commiserate": "feeling sorrow for someone's troubles",
"tangerine": "an orange-colored citrus fruit",
"blunder": "a mistake"
}

class ModernEnemy:
    def __init__(self, x: int, y: int, word: str, is_correct: bool):
        self.width = 180
        self.height = 60
        self.x = x
        self.y = y
        self.word = word
        self.is_correct = is_correct
        self.speed = ENEMY_SPEED
        self.active = True
        self.hit = False
        self.hit_animation = 0
        
    def update(self):
        if self.hit:
            self.hit_animation += 1
            if self.hit_animation >= 30:
                self.active = False
        
    def move(self):
        if not self.hit:
            self.y += self.speed
        
    def draw(self, screen):
        if self.active:
            # Card effect with 3D shadow
            shadow_offset = 4 if not self.hit else 2
            for i in range(shadow_offset):
                pygame.draw.rect(screen, CARD_SHADOW,
                               (self.x + i, self.y + i, self.width, self.height),
                               border_radius=10)
            
            # Main card
            color = CARD_BG if not self.hit else (
                CORRECT_GREEN if self.is_correct else WRONG_RED
            )
            pygame.draw.rect(screen, color,
                           (self.x, self.y, self.width, self.height),
                           border_radius=10)
            
            # Word with slight 3D effect
            if not self.hit:
                shadow_text = FONT_SMALL.render(self.word, True, CARD_SHADOW)
                screen.blit(shadow_text, 
                           (self.x + self.width/2 - shadow_text.get_width()/2 + 1,
                            self.y + self.height/2 - shadow_text.get_height()/2 + 1))
            
            text = FONT_SMALL.render(self.word, True, BLACK)
            screen.blit(text,
                       (self.x + self.width/2 - text.get_width()/2,
                        self.y + self.height/2 - text.get_height()/2))

class ModernGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vocabulary Space")
        self.clock = pygame.time.Clock()
        
        self.background = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT,
                                               BACKGROUND_COLOR_TOP,
                                               BACKGROUND_COLOR_BOTTOM)
        
        self.reset_game()
        self.game_state = GameState.MENU
        self.menu_screen = MenuScreen()
        self.pause_screen = PauseScreen()
        self.game_over_screen = GameOverScreen()
        
        # 添加游戏加载完成事件
        load_event = document.createEvent('Event')
        load_event.initEvent('game-loaded', True, True)
        document.dispatchEvent(load_event)
        
    def reset_game(self):
        self.player = ModernPlayer()
        self.bullets = []
        self.enemies = []
        self.effects = []
        self.feedback_texts = []
        self.score = 0
        self.current_word = ""
        self.current_definition = ""
        self.time_left = GAME_DURATION
        self.running = True
        
    def generate_round(self):
        self.enemies.clear()
        self.current_word = random.choice(list(vocab_list.keys()))
        self.current_definition = vocab_list[self.current_word]
        
        words = [self.current_word]
        decoys = list(vocab_list.keys())
        decoys.remove(self.current_word)
        words.extend(random.sample(decoys, 3))
        random.shuffle(words)
        
        spacing = SCREEN_WIDTH // 4
        for i, word in enumerate(words):
            x = spacing * (i + 0.5) - 90
            is_correct = word == self.current_word
            self.enemies.append(ModernEnemy(x, 50, word, is_correct))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p and self.game_state == GameState.PLAYING:
                    self.game_state = GameState.PAUSED
                elif event.key == pygame.K_p and self.game_state == GameState.PAUSED:
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.game_state = GameState.PLAYING
                        self.reset_game()
                        self.generate_round()
                    elif self.game_state == GameState.GAME_OVER:
                        self.game_state = GameState.MENU
                    elif self.game_state == GameState.PLAYING:
                        bullet = ModernBullet(
                            self.player.x + self.player.width//2 - 2,
                            self.player.y
                        )
                        self.bullets.append(bullet)
        
        if self.game_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT]:
                self.player.move(1)
            
    def update(self):
        if self.game_state == GameState.MENU:
            self.menu_screen.update()
        elif self.game_state == GameState.PLAYING:
            self.player.update()
            
            # Update time
            self.time_left -= 1/FPS
            if self.time_left <= 0:
                self.game_state = GameState.GAME_OVER
            
            # Update game objects
            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)
                    
            for enemy in self.enemies:
                if enemy.active:
                    enemy.update()
                    enemy.move()
                    if enemy.y > SCREEN_HEIGHT:
                        self.generate_round()
                        self.score -= 5
                        break
                        
            # Update effects
            for effect in self.effects[:]:
                effect.update()
                if not effect.active:
                    self.effects.remove(effect)
                    
            for text in self.feedback_texts[:]:
                text.update()
                if not text.active:
                    self.feedback_texts.remove(text)
                    
            # Check collisions
            for bullet in self.bullets[:]:
                for enemy in self.enemies:
                    if (enemy.active and not enemy.hit and
                        bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        
                        enemy.hit = True
                        if enemy.is_correct:
                            self.score += 10
                            self.effects.append(
                                ExplosionEffect(enemy.x + enemy.width/2,
                                              enemy.y + enemy.height/2,
                                              CORRECT_GREEN)
                            )
                            self.feedback_texts.append(
                                FeedbackText("Correct! +10",
                                           enemy.x + enemy.width/2,
                                           enemy.y - 20,
                                           CORRECT_GREEN)
                            )
                            self.generate_round()
                        else:
                            self.score -= 5
                            self.effects.append(
                                ExplosionEffect(enemy.x + enemy.width/2,
                                              enemy.y + enemy.height/2,
                                              WRONG_RED)
                            )
                            self.feedback_texts.append(
                                FeedbackText("Wrong! -5",
                                           enemy.x + enemy.width/2,
                                           enemy.y - 20,
                                           WRONG_RED)
                            )
                        
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
                    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if self.game_state == GameState.MENU:
            self.menu_screen.draw(self.screen)
        elif self.game_state == GameState.PLAYING or self.game_state == GameState.PAUSED:
            # Draw game elements
            pygame.draw.rect(self.screen, CARD_BG,
                           (20, 20, SCREEN_WIDTH - 40, 70),
                           border_radius=15)
            
            text = FONT_MEDIUM.render(f"Definition: {self.current_definition}",
                                    True, BLACK)
            self.screen.blit(text, (35, 40))
            
            # Draw time and score
            time_text = FONT_MEDIUM.render(f"Time: {int(self.time_left)}s",
                                         True, LIGHT_BLUE)
            self.screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
            
            score_text = FONT_LARGE.render(f"Score: {self.score}",
                                         True, LIGHT_BLUE)
            self.screen.blit(score_text, (20, SCREEN_HEIGHT - 60))
            
            # Draw game objects
            self.player.draw(self.screen)
            for bullet in self.bullets:
                bullet.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
                
            # Draw effects
            for effect in self.effects:
                effect.draw(self.screen)
            for text in self.feedback_texts:
                text.draw(self.screen)
            
            if self.game_state == GameState.PAUSED:
                self.pause_screen.draw(self.screen)
        elif self.game_state == GameState.GAME_OVER:
            self.game_over_screen.draw(self.screen, self.score)
            
        pygame.display.flip()
        
    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
            
        pygame.quit()

game = ModernGame()
asyncio.run(game.run())