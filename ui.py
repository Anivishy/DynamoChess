import pygame
from math import *
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

def UI():
    def __init__(self, size):
        self.size = size
        self.tile_size = (self.size / 8)
        self.board = {
            8: ['', '', '', '', '', '', '', ''],
            7: ['', '', '', '', '', '', '', ''],
            6: ['', '', '', '', '', '', '', ''],
            5: ['', '', '', '', '', '', '', ''],
            4: ['', '', '', '', '', '', '', ''],
            3: ['', '', '', '', '', '', '', ''],
            2: ['', '', '', '', '', '', '', ''],
            1: ['', '', '', '', '', '', '', ''],
        }
        self.screen = pygame.display.set_mode((size, size))
    
    def draw_grid(self, window):
        for key, value in self.board.items():
            for square in value:
                square_index = value.index(square)
                if (key + square_index) % 2 == 0:
                    pygame.rect.draw(window, WHITE, (self.tile_size * square_index, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))
                else:
                    pygame.rect.draw(window, BLACK, (self.tile_size * square_index, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))
        

