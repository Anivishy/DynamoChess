from math import *
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Movemaker():
    def __init__(self):
        self.turn = 1
        self.mouse_state = 0 # 0: nothing clicked; 1: piece selected; can be changed with 1-val
        
    def change_state(self):
        self.mouse_state = 1 - self.mouse_state
    
    def set_current_piece_pos(self, coords, board, square_size):
        x, y = ceil(coords[0] / square_size), 9 - ceil(coords[1] / square_size)
        cur_letter = letters[x - 1]
        print(cur_letter, y)
        


