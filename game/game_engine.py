# game/game_engine.py

import pygame
from .paddle import Paddle
from .ball import Ball

class GameEngine:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_score = 0
        self.ai_score = 0
        
        # Colors and Font
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.SysFont("Arial", 40)

        # Create game objects
        self.player = Paddle(30, self.screen_height // 2 - 50, 20, 100)
        self.ai = Paddle(self.screen_width - 50, self.screen_height // 2 - 50, 20, 100)
        self.ball = Ball(
            self.screen_width // 2 - 10, 
            self.screen_height // 2 - 10, 
            20, 
            20, 
            self.screen_width, 
            self.screen_height
        )

    def handle_input(self):
        """Handles player paddle movement based on keyboard input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.screen_height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.screen_height)

    def update(self):
        """Updates the state of all game objects."""
        # Move the ball
        self.ball.move()
        
        # Task 1: Refined Ball Collision
        # This checks for collisions and handles the physics.
        self.ball.check_collision(self.player, self.ai)

        # AI Paddle Logic
        self.ai.auto_track(self.ball, self.screen_height)

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.screen_width:
            self.player_score += 1
            self.ball.reset()

    def render(self, screen):
        """Draws all game objects to the screen."""
        # Draw paddles
        pygame.draw.rect(screen, self.WHITE, self.player.rect())
        pygame.draw.rect(screen, self.WHITE, self.ai.rect())
        
        # Draw ball
        pygame.draw.ellipse(screen, self.WHITE, self.ball.rect())

        # Draw a center line
        pygame.draw.aaline(screen, self.WHITE, (self.screen_width // 2, 0), (self.screen_width // 2, self.screen_height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, self.WHITE)
        screen.blit(player_text, (self.screen_width // 4, 20))
        
        ai_text = self.font.render(str(self.ai_score), True, self.WHITE)
        screen.blit(ai_text, (self.screen_width * 3 // 4, 20))