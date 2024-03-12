from math import *
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Movemaker():
    def __init__(self):
        self.turn = 1
        self.mouse_state = 0 # 0: nothing clicked; 1: piece selected; can be changed with 1-val
        
    def change_state(self):
        self.mouse_state = 1 - self.mouse_state
    
    def get_state(self):
        return self.mouse_state
    
    def get_current_piece_pos(self, coords, board, square_size):
        x, y = floor(coords[0] / square_size), floor(coords[1] / square_size)
        cur_letter = letters[x - 1]
        return x, y, cur_letter
        


