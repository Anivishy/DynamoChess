# this needs to be translation both ways
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Translator():
    def __init__(self, starting_position):
        self.start_pos = starting_position
        self.moves = self.start_pos.split(' ')
    
    def get_moves(self):
        return self.moves

    def parse_board(self):
        turn = 0 # 0 for white, 1 for black
        for move in self.moves:
            pass