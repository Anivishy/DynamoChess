# this needs to be translation both ways
import chess
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Translator:
    def __init__(self, starting_position):
        self.start_pos = starting_position
        self.moves = self.start_pos.split(' ')
    
    def get_moves(self):
        return self.moves
    
    def get_move_from_screen(self, first_pos, new_pos):
        first_letter = letters[first_pos[0]]
        second_letter = letters[new_pos[0]]
        string = first_letter + str(8 - first_pos[1]) + second_letter + str(8 - new_pos[1])
        return string