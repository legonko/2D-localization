import pygame
import numpy as np
import sys
import config
import random
from level import Level
from robot import Robot


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('Robocraft')
        self.programIcon = pygame.image.load('./assets/logo.png')
        pygame.display.set_icon(self.programIcon)
        self.clock = pygame.time.Clock()
        self.screen.fill((198, 198, 198))
        self.gui()
        self.run()
    
    def gui(self):
        self.btn1 = Button(self.screen, 546, 34, 16, 16, 8, 6)
        self.btn2 = Button(self.screen, 578, 34, 16, 16, 19, 7)
        self.btn3 = Button(self.screen, 610, 34, 16, 16, 16, 4)
        self.lbl = Label(self.screen, 0)
        self.label_r = Label(self.screen, 0)
        label1 = self.label1 = Label(self.screen, 1)
        label2 = Label(self.screen, 1)
        label3 = Label(self.screen, 1)            
        label1.create_label("Change map", 544, 0, (61, 61, 61))            
        label2.create_label("Probability matrix", 544, 64, (61, 61, 61))
        label3.create_label("Orientation probability", 800, 0, (61, 61, 61))       
        
        # matrix
        pygame.draw.line(self.screen, (61, 61, 61), [544, 96], [1069, 96], 2)
        pygame.draw.line(self.screen, (61, 61, 61), [544, 96], [544, 347], 2)        

        pygame.draw.line(self.screen, (240, 240, 240), [546, 346], [1068, 346], 2)
        pygame.draw.line(self.screen, (240, 240, 240), [1068, 98], [1068, 346], 2)

        pygame.draw.line(self.screen, (240, 240, 240), [542, 97], [542, 347], 2)
        # vector
        pygame.draw.line(self.screen, (61, 61, 61), [800, 32], [933, 32], 2)
        pygame.draw.line(self.screen, (61, 61, 61), [800, 32], [800, 57], 2)

        pygame.draw.line(self.screen, (240, 240, 240), [802, 56], [933, 56], 2)
        pygame.draw.line(self.screen, (240, 240, 240), [932, 34], [932, 56], 2)
        
        pygame.draw.line(self.screen, (240, 240, 240), [798, 32], [798, 83], 2)
        # arrows
        pygame.draw.line(self.screen, (61, 61, 61), [800, 58], [933, 58], 2)
        pygame.draw.line(self.screen, (61, 61, 61), [800, 58], [800, 83], 2)

        pygame.draw.line(self.screen, (240, 240, 240), [800, 82], [933, 82], 2)
        pygame.draw.line(self.screen, (240, 240, 240), [932, 60], [932, 82], 2)

        self.arrow = pygame.image.load('./assets/Arrow.png').convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (14, 18))
        self.arrow_up = self.arrow
        self.arrow_down = pygame.transform.rotate(self.arrow, 180)
        self.arrow_left = pygame.transform.rotate(self.arrow, 90)
        self.arrow_right = pygame.transform.rotate(self.arrow, -90)

        self.screen.blit(self.arrow_down, (808, 62))
        self.screen.blit(self.arrow_left, (840, 64))
        self.screen.blit(self.arrow_up, (872, 62))
        self.screen.blit(self.arrow_right, (904, 64))
        
        
    def run(self):        
        self.level = Level(self.screen)                    
        robot = Robot(self, self.screen, config.START_POSITION[1], config.START_POSITION[0])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mx, my = pygame.mouse.get_pos()
                        if self.btn1.rect.collidepoint(mx, my):
                            self.new_map()
                            robot.restart()
                            self.level.mode = 'cave'
                        elif self.btn2.rect.collidepoint(mx, my):
                            self.new_map()
                            robot.restart()
                            self.level.mode = 'sand'
                        elif self.btn3.rect.collidepoint(mx, my):
                            self.new_map()
                            robot.restart()
                            self.level.mode = 'wood'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        robot.rotation_l()
                    if event.key == pygame.K_RIGHT:
                        robot.rotation_r()
                    if event.key == pygame.K_SPACE:
                        robot.move_sense()
                    if event.key == pygame.K_s:
                        robot.sense()
                    if event.key == pygame.K_m:
                        robot.move()

            self.level.draw()
            robot.draw()        
            pygame.display.update()
            self.clock.tick(config.FPS)

    def print_matrix(self, m, lbl):
        p = 0
        rows, columns = np.shape(m)
        m = m[2:(rows - 2), 2:(columns - 2)]
        for i in range(len(m)):
            res = ('  '.join(['{:.2f}'.format(x) for x in m[i]]))
            p += 20
            lbl.create_label(res, 554, 84 + p, (61, 61, 61))

    def print_vector(self, v, lbl):
        p = 0
        for i in v:
            res = ('  '.join(['{:.2f}'.format(i)]))
            p += 32
            lbl.create_label(res, 774 + p, 36, (61, 61, 61))

    def new_map(self):
        config.MAP = [['x'] * config.COLUMNS for _ in range(config.ROWS)]
        config.START_POSITION = (random.randint(0, config.ROWS - 1), 0)   
        self.level.noise(config.MAP, 0.4)     


class Label:
    def __init__(self, screen, s):
        self.screen = screen
        self.s = s

    def create_label(self, text, x, y, color):
        if self.s == 1:
            font = config.FONT
        else:
            font = config.FONT_SMALL

        text = font.render(text, 0, color, (198, 198, 198))
        w, h = text.get_size()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen.blit(text, (x, y))


class Button():
    def __init__(self, screen, x, y, w, h, c, r):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.r = r
        self.sheet = pygame.image.load('./assets/Blocks.png').convert_alpha()
        self.create_button()

    def create_button(self):
        img = pygame.Surface((16, 16)).convert_alpha()
        img.blit(self.sheet, (0, 0), (self.c * 16, self.r * 16, 16, 16))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.screen, (61, 61, 61), (self.x - 2, self.y - 2, self.w + 4, self.h + 2))
        pygame.draw.rect(self.screen, (240, 240, 240), (self.x, self.y, self.w + 2, self.h + 2))        
        self.screen.blit(img, (self.x, self.y))