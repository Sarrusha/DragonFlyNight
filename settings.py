import pygame

# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

# Playable area (30 pixels smaller on all sides)
PLAYABLE_WIDTH = SCREEN_WIDTH - 60
PLAYABLE_HEIGHT = SCREEN_HEIGHT - 60
PLAYABLE_OFFSET_X = 30
PLAYABLE_OFFSET_Y = 30

# Colors
DARK_BLUE = (25, 25, 112)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # RGB value for green
DARK_GREEN = (0, 100, 0)  # Define DARK_GREEN as a darker shade of green

# Initialize Pygame
pygame.init()

# Fonts
font = pygame.font.Font(None, 36)