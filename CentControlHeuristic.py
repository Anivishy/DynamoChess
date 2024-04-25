from ui import UI
import chess
import re

class CenterControlClass:

    def __init__(self):
        pass

    def centerControl (self, board: chess.Board):
        self.center_control = CenterControlClass()
        move_object_moves = self.center_control.legal_move_manipulation(board) #check this
        center_moves = ["c3", "c4", "c5", "c6", "d3", "d4", "d5", "d6", "e3", "e4", "e5", "e6", "f3", "f4", "f5", "f6"]
        controlled = []
        control_score = 0
        for move in move_object_moves:
            for center_position in center_moves:
                move_uci = move.uci()
                to_square = re.search(r"\d", move_uci)
                to_square_index = to_square.start()
                #print(move_uci[to_square_index + 1:])
                if center_position in move_uci[to_square_index + 1:]:
                    if center_position not in controlled:
                        control_score += 1
                        controlled.append(center_position)
        print(controlled)
        return control_score

            
            # target_move = chess.Move.from_uci(str(target_sqare))
            # board.push(target_move)
            # coordinate_legal_moves_t, capture_legal_moves_t, uci_legal_moves_t, move_object_moves_t = legal_move_manipulation(board, game_ui)
            # for move in move_object_moves_t:
            #     if move.to_square in center_moves:
            #          contro
                    
    def legal_move_manipulation(self, board: chess.Board):
        coordinate_legal_moves = []
        capture_legal_moves = []
        uci_legal_moves = []
        move_object_moves = []
        for move in board.legal_moves:
            move_object_moves.append(move)
            # uci_legal_moves.append((str(move)[:2], str(move)[2:]))
            # coord_move = uci_translator(str(move))
            # coordinate_legal_moves.append(coord_move) # these are flipped
            # end_square = coord_move[1]
            # if board.piece_at(chess.parse_square(str(move)[2:])):
            #     capture_legal_moves.append(coord_move)

            
        return move_object_moves