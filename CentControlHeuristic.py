from ui import UI
import chess
import re
import asyncio
import aiohttp

class CenterControlClass:

    def __init__(self):
        # self.control_score = 0
        self.center_moves = ["c3", "c4", "c5", "c6", "d3", "d4", "d5", "d6", "e3", "e4", "e5", "e6", "f3", "f4", "f5", "f6"]
        self.one_squares = ['b', 'c', 'f', 'g']
        

    async def post_async(self, move, board):
        #center_moves = ["c3", "c4", "c5", "c6", "d3", "d4", "d5", "d6", "e3", "e4", "e5", "e6", "f3", "f4", "f5", "f6"]
        move_score = 0
        for center_position in self.center_moves:
            #print("Current Center Control Score: " + str(self.control_score))
            move_uci = move.uci()
            #print(move_uci)
            to_square_str = re.search(r"\d", move_uci)
            to_square_index = to_square_str.start()
            from_square_str = move_uci[:to_square_index + 1]
            #print("TO: " + move_uci[to_square_index + 1:])
            #print("FROM: " + from_square)
            # from_square_square = move.from_square
            # print(from_square_square)
            #print(str(board.piece_at(chess.parse_square(str(move)[2:]))))
            is_pawn = str(board.piece_at(chess.parse_square(str(move)[2:]))).capitalize() == "P"
            if is_pawn:
                if (from_square_str[0] == "d" or from_square_str[0] == "e") and center_position in move_uci[to_square_index + 1:]:
                    move_score += 2
                elif (from_square_str[0] == "c" or from_square_str[0] == "f") and center_position in move_uci[to_square_index + 1:]:
                    move_score += 1
            else:
                if center_position in move_uci[to_square_index + 1:]:
                    #if center_position not in controlled:
                        move_score += 1
                        #controlled.append(center_position) # do we need this TODO
        return move_score

    async def calc_score(self, moves: list, board, ccc):
        control_score = 0
        async with aiohttp.ClientSession() as session:
            tasks = [ccc.post_async(move, board) for move in moves]
            #print(tasks)
            for coro in asyncio.as_completed(tasks):
                #results = await asyncio.gather(*tasks)
                result = await coro
                control_score += result 
            return control_score

    def centerControl (self, board: chess.Board, move_object_moves):
        seen_starting_squares = []
        control_score = 0
        for move in move_object_moves[0]:
            move_uci = move.uci()
            to_square_str = re.search(r"\d", move_uci)
            to_square_index = to_square_str.start()
            from_square_str = move_uci[:to_square_index + 1]
            is_pawn = str(board.piece_at(chess.parse_square(str(move)[2:]))).capitalize() == "P"
            if from_square_str in seen_starting_squares and is_pawn:
                continue
            else:
                seen_starting_squares.append(from_square_str)
                if is_pawn:
                    if (from_square_str[0] == "d" or from_square_str[0] == "e") and move_uci[to_square_index + 1:] in self.center_moves:
                        control_score += 2
                    elif (from_square_str[0] in self.one_squares) and move_uci[to_square_index + 1:] in self.center_moves:
                        control_score += 1
                else:
                    if move_uci[to_square_index + 1:] in self.center_moves:
                        #if center_position not in controlled:
                        control_score += 1
                        #controlled.append(center_position) # do we need this TODO

        seen_starting_squares_black = []

        for move in move_object_moves[1]:
            move_uci = move.uci()
            to_square_str = re.search(r"\d", move_uci)
            to_square_index = to_square_str.start()
            from_square_str = move_uci[:to_square_index + 1]

            is_pawn = str(board.piece_at(chess.parse_square(str(move)[2:]))).capitalize() == "P"
            if from_square_str in seen_starting_squares_black and is_pawn:
                continue
            else:
                seen_starting_squares_black.append(from_square_str)
                if is_pawn:
                    if (from_square_str[0] == "d" or from_square_str[0] == "e") and move_uci[to_square_index + 1:] in self.center_moves:
                        control_score -= 2
                    elif (from_square_str[0] in self.one_squares) and move_uci[to_square_index + 1:] in self.center_moves:
                        control_score -= 1
                else:
                    if move_uci[to_square_index + 1:] in self.center_moves:
                        control_score -= 1
        return control_score

                    
    def legal_move_manipulation(self,board: chess.Board):
        coordinate_legal_moves = []
        capture_legal_moves = []
        uci_legal_moves = []
        move_object_moves = [set(),set()]
        board.turn = chess.WHITE
        for move in board.legal_moves:
            move_object_moves[0].add(move)
        board.turn = not board.turn
        for move in board.legal_moves:
            move_object_moves[1].add(move)
            # uci_legal_moves.append((str(move)[:2], str(move)[2:]))
            # coord_move = uci_translator(str(move))
            # coordinate_legal_moves.append(coord_move) # these are flipped
            # end_square = coord_move[1]
            # if board.piece_at(chess.parse_square(str(move)[2:])):
            #     capture_legal_moves.append(coord_move)

            
        return move_object_moves