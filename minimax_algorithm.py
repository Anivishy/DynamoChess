import chess
import pandas as pd
from copy import deepcopy

import random

class ChessAI():
    def __init__(self,depth, translator) -> None:
        self.max_depth = depth
        self.empty_board = chess.Board()
        self.translator = translator
        

    def get_legal_moves(self,board:chess.Board)->chess.Board:
        moves = board.legal_moves
        allboards = []
        for i in moves:
            posBoard = deepcopy(board)
            posBoard.push(i)
            allboards.append(posBoard)
        return allboards

    def get_eval_bar(self,board, game_ui):
        cur_board = deepcopy(game_ui.board)
        cur_chess_lib_board = deepcopy(board)
        moves = []
        for i in range(self.max_depth):
            moves.insert(0, str(cur_chess_lib_board.pop()))
        for move in moves:
            first_coord, second_coord = self.translator.uci_to_coordinates(move)
            screen_move, promotion, castle_detection = self.translator.get_move_from_screen(first_coord, second_coord, game_ui.board)
            chess_move = chess.Move.from_uci(move)
            game_ui.selected_piece_movement(second_coord, first_coord, promotion, castle_detection)
        #TODO
        material = game_ui.piece_values()
        
        print(material, moves[0], moves)
        #black_king, white_king = game_ui.king_safety()
        num_legal_moves = board.legal_moves.count()
        game_ui.board = cur_board
        return material
    def minimax_recursive(self,curBoard,curTurn,curDepth, game_ui):
        if curDepth == self.max_depth:
            return (self.get_eval_bar(curBoard, game_ui),curBoard) # TODO: Switch this to evluating all captures

        if curTurn == chess.WHITE:
            highestEval = (-100000000000,self.empty_board)
            for i in self.get_legal_moves(curBoard):
                minmaxVal = self.minimax_recursive(i, not curTurn,curDepth+1, game_ui)
                if minmaxVal[0]>highestEval[0]:
                    highestEval = minmaxVal

            return highestEval
        else:
            lowestEval = (100000000000,self.empty_board)
            for i in self.get_legal_moves(curBoard):
                minmaxVal = self.minimax_recursive(i,not curTurn,curDepth+1, game_ui)
                if minmaxVal[0]<lowestEval[0]:
                    lowestEval = minmaxVal
            return lowestEval
        
    def get_ai_move(self,board,turn, game_ui):
        best_outcome = self.minimax_recursive(board,turn,0, game_ui)[1]
        for i in range(self.max_depth-1):
            best_outcome.pop()
        return str(best_outcome.pop())