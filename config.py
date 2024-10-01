import pygame 
import random

pygame.font.init()

FPS = 60
SCREEN_WIDTH = 1104
SCREEN_HEIGHT = 384
ROWS = 12
COLUMNS = 16
MAP = [['x'] * COLUMNS for _ in range(ROWS)]  
FONT_NAME = "./fonts/minecraft_font.ttf"
FONT = pygame.font.Font(FONT_NAME, 20)
FONT_SMALL = pygame.font.Font(FONT_NAME, 10)
START_POSITION = (random.randint(0, ROWS - 1), 0)