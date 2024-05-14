import chess
from CentControlHeuristic import CenterControlClass
import asyncio
import aiohttp


piece_material = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

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
    
    async def post_async(self, letter, number, board):
        material = 0
        square = letter + number
        piece = str(board.piece_at(chess.parse_square(square)))
        if piece.lower() != 'k' and piece != 'None':
            if piece.isupper():
                material += piece_material[piece]
            else:
                material -= piece_material[piece.upper()]
        return material
    
    async def calc_piece_score_final(self, letter, board, heuristic):
        async with aiohttp.ClientSession() as session:
            combined_material_num = 0
            tasks = [heuristic.post_async(letter, number, board) for number in numbers]
            #print(tasks)
            for coro in asyncio.as_completed(tasks):
                #results = await asyncio.gather(*tasks)
                result = await coro
                combined_material_num += result
            return combined_material_num

    
    async def calc_piece_score_intermediate(self, board, heuristic):
        async with aiohttp.ClientSession() as session:
            combined_material_letter = 0
            tasks = [heuristic.calc_piece_score_final(letter, board, heuristic) for letter in letters]
            #print(tasks)
            for coro in asyncio.as_completed(tasks):
                #results = await asyncio.gather(*tasks)
                result = await coro
                combined_material_letter += result
            return combined_material_letter

            

    def piece_values(self, board: chess.Board):
        heuristic = Heuristics()
        final_material = asyncio.run(heuristic.calc_piece_score_intermediate(board, heuristic))
        # for letter in letters:
        #     for number in numbers:
        #         square = letter + number
        #         piece = str(board.piece_at(chess.parse_square(square)))
        #         if piece.lower() != 'k' and piece != 'None':
        #             if piece.isupper():
        #                 material += piece_material[piece]
        #             else:
        #                 material -= piece_material[piece.upper()]
        return final_material
    
    def get_center_control_value(self, board: chess. Board, center_control, move_object_moves):
        return center_control.centerControl(board, move_object_moves)
    