import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Load sprites
dragonfly_image = pygame.image.load('assets/dragonfly.png')
moth_image = pygame.image.load('assets/moth.png')
bat_image = pygame.image.load('assets/bat.png')

# Scale sprites
dragonfly_image = pygame.transform.scale(dragonfly_image, (50, 50))
moth_image = pygame.transform.scale(moth_image, (30, 30))
bat_image = pygame.transform.scale(bat_image, (40, 40))

# Load background image
background_image = pygame.image.load('assets/night_sky.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))