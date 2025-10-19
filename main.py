# main.py

import pygame
import sys
import os

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors and Clock
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

# --- Load Sound Feedback (Robust Pathing) ---
# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Join the script directory path with the 'assets' folder name
assets_dir = os.path.join(script_dir, 'assets')

# Load sound files using the absolute path
try:
    paddle_sound = pygame.mixer.Sound(os.path.join(assets_dir, "paddle_hit.wav"))
    wall_sound = pygame.mixer.Sound(os.path.join(assets_dir, "wall_bounce.wav"))
    score_sound = pygame.mixer.Sound(os.path.join(assets_dir, "score.wav"))
except pygame.error as e:
    print(f"⚠️  Sound file error: {e}. Game will run without sound.")
    paddle_sound = wall_sound = score_sound = None

# Dynamically import the GameEngine after setting up paths
from game.game_engine import GameEngine

# Helper function to draw text on screen
def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)

def main():
    engine = GameEngine(WIDTH, HEIGHT)
    target_score = 5  # Initial winning score
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # --- Game is active ---
            engine.handle_input()

            # Store previous state to detect changes for sounds
            prev_vx, prev_vy = engine.ball.velocity_x, engine.ball.velocity_y
            prev_player_score, prev_ai_score = engine.player_score, engine.ai_score

            # Update game state
            engine.update()

            # --- Play Sound Feedback ---
            if paddle_sound and engine.ball.velocity_x != prev_vx:
                paddle_sound.play()
            if wall_sound and engine.ball.velocity_y != prev_vy:
                wall_sound.play()
            if score_sound and (engine.player_score != prev_player_score or engine.ai_score != prev_ai_score):
                score_sound.play()
            
            # Render graphics
            SCREEN.fill(BLACK)
            engine.render(SCREEN)
            pygame.display.flip()

            # Check for Game Over Condition
            if engine.player_score >= target_score or engine.ai_score >= target_score:
                game_over = True
                pygame.time.delay(500)
        
        else:
            # --- Game Over Screen ---
            SCREEN.fill(BLACK)

            # Determine winner, loser, and final scores
            if engine.player_score >= target_score:
                winner_text = "Player Wins!"
                winner_score = engine.player_score
                loser_score = engine.ai_score
            else:
                winner_text = "AI Wins!"
                winner_score = engine.ai_score
                loser_score = engine.player_score
            
            final_score_text = f"Final Score: {winner_score} - {loser_score}"

            # Display winner and final score
            draw_text(SCREEN, winner_text, 60, WIDTH // 2, HEIGHT // 2 - 120)
            draw_text(SCREEN, final_score_text, 40, WIDTH // 2, HEIGHT // 2 - 60)
            
            # Display replay options in a clean, ordered layout
            draw_text(SCREEN, "Play Again?", 30, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text(SCREEN, "[3] Best of 3", 22, WIDTH // 2, HEIGHT // 2 + 70)
            draw_text(SCREEN, "[5] Best of 5", 22, WIDTH // 2, HEIGHT // 2 + 100)
            draw_text(SCREEN, "[7] Best of 7", 22, WIDTH // 2, HEIGHT // 2 + 130)
            draw_text(SCREEN, "[ESC] Exit", 22, WIDTH // 2, HEIGHT // 2 + 180)
            
            pygame.display.flip()

            # Handle Replay Input
            keys = pygame.key.get_pressed()
            new_game = False
            if keys[pygame.K_3]:
                target_score = 3
                new_game = True
            elif keys[pygame.K_5]:
                target_score = 5
                new_game = True
            elif keys[pygame.K_7]:
                target_score = 7
                new_game = True
            elif keys[pygame.K_ESCAPE]:
                running = False

            if new_game:
                engine.player_score = 0
                engine.ai_score = 0
                engine.ball.reset()
                game_over = False

        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()