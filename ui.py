import pygame
from math import *
import chess
BROWN = (100, 75, 50)
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

piece_value = {
    'r': 5, 
    'n': 3, 
    'b': 3, 
    'q': 8,
    'k': 10,
    'p': 1
}


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
    
    def selected_piece_movement(self, new_pos, first_pos, promotion, castle_detection):
        curr_pos = (new_pos[0],new_pos[1])
        piece = self.board[first_pos[1]][first_pos[0]]
        if promotion != '':
            piece = promotion
        self.board[curr_pos[1]][curr_pos[0]] = piece
        self.board[first_pos[1]][first_pos[0]] = ''
        self.move_rook_for_castle(castle_detection, curr_pos, first_pos)

    def move_rook_for_castle(self, castle_detection, curr_pos, first_pos):
        if castle_detection != None:
            if castle_detection > 0: # castling to the right
                self.board[first_pos[1]][curr_pos[0] - 1] = self.board[first_pos[1]][7]
                self.board[first_pos[1]][7] = ''
            elif castle_detection < 0: # castling to the left
                self.board[first_pos[1]][curr_pos[0] + 1] = self.board[first_pos[1]][0]
                self.board[first_pos[1]][0] = ''
    
    def set_selected_square(self, square):
        if square == None:
            self.selected_square = (None, None)
        else:
            self.selected_square = (square[0], square[1])

    def get_seleceted_square(self):
        return self.selected_square
    
    def find_king(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if color:
                    if self.board[i][j] == 'K':
                        return (i, j)
                else:
                    if self.board[i][j] == 'k':
                        return (i, j)
    
    
    def king_safety(self):
        black_king_pos = self.find_king(False)
        white_king_pos = self.find_king(True)
        black_king_adjusted = (abs(black_king_pos[0] - 4), abs(black_king_pos[1] - 4))
        white_king_adjusted = (abs(white_king_pos[0] + 1 - 4), abs(white_king_pos[1] - 4))
        print(black_king_adjusted, white_king_adjusted)
        black_king_score = black_king_adjusted[0]**2 + black_king_adjusted[1]**2
        white_king_score = white_king_adjusted[0]**2 + white_king_adjusted[1]**2
        return black_king_score, white_king_score
    
    
    
    
        