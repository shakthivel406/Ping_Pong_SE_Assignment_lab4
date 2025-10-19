# game/ball.py

import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-6, 6])
        self.velocity_y = random.choice([-4, 4])

    def move(self):
        """Moves the ball and handles bounces off the top and bottom walls."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        """
        Task 1: Refined Collision
        Checks for collision with paddles. If a collision occurs, it reverses the
        ball's horizontal velocity and snaps its position to the paddle's edge
        to prevent it from getting stuck (tunneling).
        """
        ball_rect = self.rect()
        
        # Collision with player paddle
        if ball_rect.colliderect(player.rect()):
            # Snap the ball to the front of the paddle
            self.x = player.x + player.width
            self.velocity_x *= -1
            
        # Collision with AI paddle
        elif ball_rect.colliderect(ai.rect()):
            # Snap the ball to the front of the paddle
            self.x = ai.x - self.width
            self.velocity_x *= -1

    def reset(self):
        """Resets the ball to the center with a new random velocity."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-6, 6])
        self.velocity_y = random.choice([-4, 4])

    def rect(self):
        """Returns the ball's pygame.Rect object for collision and drawing."""
        return pygame.Rect(self.x, self.y, self.width, self.height)