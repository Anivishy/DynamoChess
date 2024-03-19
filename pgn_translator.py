# this needs to be translation both ways
import chess
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Translator:
    def __init__(self, starting_position):
        self.start_pos = starting_position
        self.moves = self.start_pos.split(' ')
    
    def get_moves(self):
        return self.moves
    
    def get_move_from_screen(self, first_pos, new_pos, board):
        castling = self.castle_detection(first_pos, new_pos, board)
        promotion = ''
        first_letter = letters[first_pos[0]]
        second_letter = letters[new_pos[0]]
        string = first_letter + str(8 - first_pos[1]) + second_letter + str(8 - new_pos[1])
        if (board[first_pos[1]][first_pos[0]] == 'P' and new_pos[1] == 0): # promotion
            string += 'q' # placeholder for queen
            promotion = 'Q'
        if (board[first_pos[1]][first_pos[0]] == 'p' and new_pos[1] == 7):
            string += 'q'
            promotion = 'q'
        if string[0:2] == string[2:4]:
            return '0000', promotion, castling
        return string, promotion, castling
           
    
    def castle_detection(self, first_pos, new_pos, board):
        if board[first_pos[1]][first_pos[0]].lower() == 'k':
            if abs(first_pos[0] - new_pos[0]) == 2:
                return new_pos[0] - first_pos[0]
        return None
    
    def pgn_to_uci(self, pgn_move, board):
        return str(board.parse_san(pgn_move))