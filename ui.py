import pygame
from math import *
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class UI:
    def __init__(self, size):
        self.size = size
        self.tile_size = (self.size / 8)
        self.board = {
            8: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            7: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            6: ['', '', '', '', '', '', '', ''],
            5: ['', '', '', '', '', '', '', ''],
            4: ['', '', '', '', '', '', '', ''],
            3: ['', '', '', '', '', '', '', ''],
            2: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            1: ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        }
        self.screen = pygame.display.set_mode((size, size))
    
    def draw_grid(self):
        for key, value in self.board.items():
            for i in range(0, len(value)):
                if (key + i) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, (self.tile_size * i, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, BLACK, (self.tile_size * i, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))

