import pygame
from math import *
BROWN = (50, 50, 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

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
        self.selected_square = (None, None)
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
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
        for y in range(len(self.board)):
            for x in range(0, len(self.board[y])):
                if x == self.selected_square[0] and y == self.selected_square[1]:
                    pygame.draw.rect(self.screen, BLUE, (self.tile_size * x, self.tile_size * y, self.tile_size, self.tile_size))
                elif (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, (self.tile_size * x, self.tile_size * y, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, BROWN, (self.tile_size * x, self.tile_size * y, self.tile_size, self.tile_size))

    def draw_pieces(self):
        for y in range(len(self.board)):
            for x in range(0, len(self.board[y])):
                if self.board[y][x] != '':
                    self.screen.blit(self.piece_images[self.board[y][x]], 
                    (x * self.tile_size + self.tile_size * self.positioner / 2, y * self.tile_size + self.tile_size * self.positioner / 2))
    
    def selected_piece_movement(self, new_pos, screen_move, promotion):
        curr_pos = (new_pos[0],new_pos[1])
        piece = self.board[self.selected_square[1]][self.selected_square[0]]
        if promotion != '':
            piece = promotion
        self.board[curr_pos[1]][curr_pos[0]] = piece
        self.board[self.selected_square[1]][self.selected_square[0]] = ''
    
    def set_selected_square(self, square):
        if square == None:
            self.selected_square = (None, None)
        else:
            self.selected_square = (square[0], square[1])

    def get_seleceted_square(self):
        return self.selected_square