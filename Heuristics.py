import chess
from CentControlHeuristic import CenterControlClass


piece_material = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 50
}

table_base = {
    'P': [
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [5, 5, 5, 5, 5, 5, 5, 5], 
        [8, 8, 8, 4, 4, 2, 8, 8], 
        [9, 5, 10, 15, 15, 5, 9], 
        [15, 15, 15, 15, 15, 15, 15, 15], 
        [20, 20, 20, 20, 20, 20, 20, 20], 
        [30, 30, 30, 30, 30, 30, 30, 30], 
        [50, 50, 50, 50, 50, 50, 50, 50]
    ], 
    'N': [
        [0, 8, 0, 0, 0, 0, 8, 0], 
        [1, 1, 1, 1, 1, 1, 1, 1], 
        [4, 3, 10, 3, 3, 10, 3, 4], 
        [5, 5, 8, 8, 8, 8, 5, 5], 
        [], 
        [], 
        [], 
        []
    ], 
    'B': [

    ], 
    'K': [

    ],
    'Q': [

    ], 
    'R': [

    ]
}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
center_moves = ["c3", "c4", "c5", "c6", "d3", "d4", "d5", "d6", "e3", "e4", "e5", "e6", "f3", "f4", "f5", "f6"]
one_squares = ['b', 'c', 'f', 'g']

class Heuristics:
    def __init__(self):
        pass

    def legal_move_manipulation(self, board: chess.Board, uci_translator):
        coordinate_legal_moves = []
        capture_legal_moves = []
        uci_legal_moves = []
        move_object_moves = []
        for move in board.legal_moves:
            move_object_moves.append(move)
            uci_legal_moves.append((str(move)[:2], str(move)[2:]))
            coord_move = uci_translator(str(move))
            coordinate_legal_moves.append(coord_move) # these are flipped
            end_square = coord_move[1]
            if board.piece_at(chess.parse_square(str(move)[2:4])):
                capture_legal_moves.append(move)

            
        return coordinate_legal_moves, capture_legal_moves, uci_legal_moves, move_object_moves

    def piece_values(self, board: chess.Board):
        material = 0
        for letter in letters:
            for number in numbers:
                square = letter + number
                piece = str(board.piece_at(chess.parse_square(square)))
                if piece.lower() != 'k' and piece != 'None':
                    if piece.isupper():
                        material += piece_material[piece]
                    else:
                        material -= piece_material[piece.upper()]
        return material
    
    def get_center_control_value(self, board: chess. Board, center_control, move_object_moves):
        return center_control.centerControl(board, move_object_moves)
    
    def move_ordering(self, moves, board: chess.Board):
        moves_scores_list = []
        for move in moves:
            move_score = 0
            uci_move = str(move)
            from_square = str(board.piece_at(chess.parse_square(uci_move[:2]))).upper()
            to_square = str(board.piece_at(chess.parse_square(uci_move[2:4]))).upper()
            if to_square != 'NONE':
                move_score += piece_material[to_square] - piece_material[from_square]
            moves_scores_list.append((move, move_score))
        return moves_scores_list, len(moves_scores_list)
    
    def combined_eval(self, board: chess.Board, move_object_moves):
        material = 0
        center_control = 0
        for letter in letters:
            for number in numbers:
                square = letter + number
                piece = str(board.piece_at(chess.parse_square(square)))
                if piece.lower() != 'k' and piece != 'None':
                    if piece.isupper():
                        material += piece_material[piece]
                    else:
                        material -= piece_material[piece.upper()]
                moves = []
                for center_move in center_moves:
                    try:
                        moves.append(chess.Move.from_uci(square + center_move))
                    except:
                        pass
                    #moves = [chess.Move.from_uci(square + center_move) for center_move in center_moves
                #print(moves)
                for move in moves:
                    #try:
                        is_pawn = str(board.piece_at(chess.parse_square(str(move)[2:]))).capitalize() == "P"
                        if is_pawn:
                            if (square[0] == "d" or square[0] == "e") and move in move_object_moves:
                                #print("SQUARE" + str(square[0]))
                                center_control += 2
                            elif (square[0] in one_squares) and move in move_object_moves:
                                center_control += 1
                        else:
                            if move in move_object_moves:
                                #if center_position not in controlled:
                                center_control += 1
                                #controlled.append(center_position) # do we need this TODO
                        # if move in move_object_moves:
                        #     center_control += 1
                    #except:
                    #    pass
        #print("NUMBER " + str(center_control))         
        return (material, center_control)
    