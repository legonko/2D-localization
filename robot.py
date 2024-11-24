import numpy as np
import pygame
import random
import config
from scipy import signal

from utils import *


class Robot():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.k = 2
        self.p = np.zeros((12, 16))
        self.p[config.START_POSITION[0]][config.START_POSITION[1]] = 1
        self.p = np.pad(self.p, self.k)             
        self.image = pygame.image.load('./assets/Steve.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image_down = self.image
        self.image_up = pygame.transform.rotate(self.image, 180)
        self.image_left = pygame.transform.rotate(self.image, -90)
        self.image_right = pygame.transform.rotate(self.image, 90)
        self.images = [self.image_down, self.image_left, self.image_up, self.image_right]      
        self.p_angpos = np.zeros(4)
        self.p_angpos[0] = 1
        self.angpos = 0
        self.sense_under(self.p, self.x, self.y)

    def draw(self):
        self.screen.blit(self.images[self.angpos], (self.x * 32, self.y * 32))

    def reset(self):
        self.x = config.START_POSITION[1]
        self.y = config.START_POSITION[0]
        self.p = np.zeros((12, 16))
        self.p[config.START_POSITION[0]][config.START_POSITION[1]] = 1
        self.p = np.pad(self.p, 2)
        self.p_angpos = np.zeros(4)
        self.p_angpos[0] = 1
        self.angpos = 0
        self.draw()                

    def sense_under(self, p, x, y):
        pHit = 0.8
        pMiss = 0.1
        rows, columns = config.ROWS, config.COLUMNS
        prob = 0.8
        p_new = np.zeros(np.shape(p))
        if random.random() <= prob:
            z_under = config.MAP[y][x]
        else:
            if config.MAP[y][x] == 'x':
                z_under = 'r'
            else:
                z_under = 'x'

        for i in range(self.k, rows + self.k):
            for j in range(self.k, columns + self.k):
                p_new[i][j] = pHit * p[i][j] if z_under == config.MAP[i - self.k][j - self.k] else pMiss * p[i][j]

        s = np.sum(p_new)
        if s != 0:
            p_new = np.divide(p_new, s)
        return p_new
    

    def set_probs(self, p):

        kernel_r = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0.05, 0.9, 0.05],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])

        kernel_l = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0.05, 0.9, 0.05, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])

        kernel_u = np.array([
            [0, 0, 0.05, 0, 0],
            [0, 0, 0.9, 0, 0],
            [0, 0, 0.05, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])

        kernel_d = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0.05, 0, 0],
            [0, 0, 0.9, 0, 0],
            [0, 0, 0.05, 0, 0]])

        kernel = kernel_d * self.p_angpos[0]
        kernel += kernel_l * self.p_angpos[1]
        kernel += kernel_u * self.p_angpos[2]
        kernel += kernel_r * self.p_angpos[3]

        p = signal.convolve2d(p, kernel, mode='same')

        p[self.k:config.ROWS + self.k, config.COLUMNS + self.k - 1] += np.sum(
            p[self.k:config.ROWS + self.k, config.COLUMNS + self.k:(config.COLUMNS + 2 * self.k)], axis=1)
        p[self.k:config.ROWS + self.k, config.COLUMNS + self.k:(config.COLUMNS + 2 * self.k)] = 0

        p[self.k:config.ROWS + self.k, self.k] += np.sum(
            p[self.k:config.ROWS + self.k, 0:self.k], axis=1)
        p[self.k:config.ROWS + self.k, 0:self.k] = 0

        p[self.k, self.k:config.COLUMNS + self.k] += np.sum(
            p[0:self.k, self.k:config.COLUMNS + self.k], axis=0)
        p[0:self.k, self.k:config.COLUMNS + self.k] = 0

        p[self.k + config.ROWS - 1, self.k:config.COLUMNS + self.k] += np.sum(
            p[config.ROWS + self.k:config.ROWS + 2 * self.k, self.k:config.COLUMNS + self.k], axis=0)
        p[config.ROWS + self.k:config.ROWS + 2 * self.k, self.k:config.COLUMNS + self.k] = 0

        return p

    def sense(self):
        self.p = self.sense_under(self.p, self.x, self.y)
        self.gyro()

    def gyro(self):
        dice = random.random()
        w = self.angpos
        if dice < 0.1:
            w -= 1
        elif dice < 0.2:
            w += 1

        w_p = np.zeros(4)
        w_p[w % 4] = 0.8
        w_p[(w - 1) % 4] = 0.1
        w_p[(w + 1) % 4] = 0.1
        self.p_angpos *= w_p
        self.p_angpos /= self.p_angpos.sum()

    def move_sense(self):
        self.move()
        for _ in range(5):
            self.sense()

    def move(self):
        d = 0
        dice = random.random()
        if dice < 0.05:
            d = 2
        elif dice < 0.95:
            d = 1

        if self.angpos == 0:
            self.y += d
        elif self.angpos == 1:
            self.x -= d
        elif self.angpos == 2:
            self.y -= d
        else:
            self.x += d

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x >= config.COLUMNS:
            self.x = config.COLUMNS - 1
        if self.y >= config.ROWS:
            self.y = config.ROWS - 1

        self.p = self.set_probs(self.p)

    def rotation_r(self):
        kernel_rot_r = np.array([0.1, 0.8, 0.1, 0])
        dice = random.random()
        if dice < 0.1:
            self.angpos += 2
        elif dice < 0.8:
            self.angpos += 1

        self.angpos %= 4
        self.p_angpos = convolve(self.p_angpos, kernel_rot_r)

        for _ in range(5):
            self.sense()

    def rotation_l(self):
        kernel_rot_l = np.array([0.1, 0, 0.1, 0.8])
        dice = random.random()
        if dice < 0.1:
            self.angpos -= 2
        elif dice < 0.8:
            self.angpos -= 1

        self.angpos %= 4
        self.p_angpos = convolve(self.p_angpos, kernel_rot_l)
        for _ in range(5):
            self.sense()