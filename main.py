import os
import pygame
from settings import *
from game_logic import Game

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("Updated Working Directory:", os.getcwd())

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moth Hunt")

# Clock for controlling frame rate
clock = pygame.time.Clock()

if __name__ == "__main__":
    game = Game(screen, clock)  # Pass both screen and clock to the Game class
    game.main()