import numpy as np
import pygame
import config
import random
from utils import *


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.create_blocks()
        self.mode = 'cave'
        self.noise(config.MAP, 0.4)        

    def noise(self, arr, prob):
        height, width = np.shape(arr)        
        for i in range(height):
            for j in range(width):
                rdn = random.random()
                if rdn < prob:
                    arr[i][j] = 'r'        

    def draw(self):
        self.create_map(self.mode)

    def get_image(self, sheet, row, column, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), (column * width, row * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

    def create_blocks(self):
        self.sprite_sheet_image = pygame.image.load('./assets/Blocks.png').convert_alpha()
        self.earth = self.get_image(self.sprite_sheet_image, 6, 8, 16, 16, 2)
        self.rock = self.get_image(self.sprite_sheet_image, 5, 3, 16, 16, 2)        
        self.img = pygame.image.load('./assets/Steve.png').convert_alpha()
        self.steve = self.get_image(self.img, 0, 0, 16, 16, 2)    
        self.sand = self.get_image(self.sprite_sheet_image, 7, 19, 16, 16, 2)        
        self.gravel = self.get_image(self.sprite_sheet_image, 11, 0, 16, 16, 2)
        self.spruce = self.get_image(self.sprite_sheet_image, 5, 16, 16, 16, 2)
        self.oak = self.get_image(self.sprite_sheet_image, 4, 16, 16, 16, 2)
                
    def create_map(self, mode):
        for row_index, row in enumerate(config.MAP):
            for col_index, col in enumerate(row):
                x = col_index * 32
                y = row_index * 32
                blocks = {'cave':(self.earth, self.rock), 
                          'sand':(self.sand, self.gravel), 
                          'wood':(self.oak, self.spruce)}
                if col == 'x':
                    self.screen.blit(blocks[mode][0], (x, y))
                elif col == 'r':
                    self.screen.blit(blocks[mode][1], (x, y))   