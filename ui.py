import pygame
from math import *
BROWN = (50, 50, 50)
WHITE = (255, 255, 255)

ROOK_W = 'PieceImages/white_rook.png'
KNIGHT_W = 'PieceImages/white_knight.png'
BISHOP_W = 'PieceImages/white_bishop.png'
QUEEN_W = 'PieceImages/white_queen.png'
KING_W = 'PieceImages/white_king.png'
PAWN_W = 'PieceImages/white_pawn.png'
ROOK = 'PieceImages/black_rook.png'
KNIGHT = 'PieceImages/black_knight.png'
BISHOP = 'PieceImages/black_bishop.png'
QUEEN = 'PieceImages/black_queen.png'
KING = 'PieceImages/black_king.png'
PAWN = 'PieceImages/black_pawn.png'


class UI:
    def __init__(self, size):
        self.size = size
        self.tile_size = (self.size / 8)
        self.positioner = 0.1
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
        self.piece_size = (int(self.tile_size - self.tile_size * self.positioner), int(self.tile_size - self.tile_size * self.positioner))
        self.piece_images = {
            'r': pygame.transform.scale(pygame.image.load(ROOK), self.piece_size), 
            'n': pygame.transform.scale(pygame.image.load(KNIGHT), self.piece_size), 
            'b': pygame.transform.scale(pygame.image.load(BISHOP), self.piece_size),
            'q': pygame.transform.scale(pygame.image.load(QUEEN), self.piece_size), 
            'k': pygame.transform.scale(pygame.image.load(KING), self.piece_size), 
            'p': pygame.transform.scale(pygame.image.load(PAWN), self.piece_size),
            'R': pygame.transform.scale(pygame.image.load(ROOK_W), self.piece_size), 
            'N': pygame.transform.scale(pygame.image.load(KNIGHT_W), self.piece_size), 
            'B': pygame.transform.scale(pygame.image.load(BISHOP_W), self.piece_size),
            'Q': pygame.transform.scale(pygame.image.load(QUEEN_W), self.piece_size), 
            'K': pygame.transform.scale(pygame.image.load(KING_W), self.piece_size), 
            'P': pygame.transform.scale(pygame.image.load(PAWN_W), self.piece_size)
        }
    
    def draw_grid(self):
        for key, value in self.board.items():
            for i in range(0, len(value)):
                if (key + i) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, (self.tile_size * i, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, BROWN, (self.tile_size * i, self.tile_size * abs(8 - key), self.tile_size, self.tile_size))

    def draw_pieces(self):
        for key, value in self.board.items():
            for i in range(0, len(value)):
                if value[i] != '':
                    self.screen.blit(self.piece_images[value[i]], 
                    (i * self.tile_size + self.tile_size * self.positioner / 2, (8 - key) * self.tile_size + self.tile_size * self.positioner / 2))
                