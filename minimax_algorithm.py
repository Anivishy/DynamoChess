import chess
import pandas as pd
from copy import deepcopy

import random

class ChessAI():
    def __init__(self,depth, translator, heuristic) -> None:
        self.max_depth = depth
        self.empty_board = chess.Board()
        self.translator = translator
        self.heuristic = heuristic
        

    def get_legal_moves(self,board:chess.Board)->chess.Board:
        moves = board.legal_moves
        allboards = []
        for i in moves:
            posBoard = deepcopy(board)
            posBoard.push(i)
            allboards.append(posBoard)
        return allboards

    def get_eval_bar(self,board):
        #TODO
        material = self.heuristic.piece_values(board)
        num_legal_moves = board.legal_moves.count()
        return material
    def minimax_recursive(self,curBoard,curTurn,curDepth):
        if curDepth == self.max_depth:
            return (self.get_eval_bar(curBoard),self.first_move(curBoard.move_stack)) # TODO: Switch this to evluating all captures

        if curTurn == chess.WHITE:
            highestEval = (-100000000000,None)
            for i in curBoard.legal_moves:
                curBoard.push(i)
                minmaxVal = self.minimax_recursive(curBoard, not curTurn,curDepth+1)
                if minmaxVal[0]>highestEval[0]:
                    highestEval = minmaxVal
                curBoard.pop()
            return highestEval
        else:
            lowestEval = (100000000000,None)
            for i in curBoard.legal_moves:
                curBoard.push(i)
                minmaxVal = self.minimax_recursive(curBoard,not curTurn,curDepth+1)
                if minmaxVal[0]<lowestEval[0]:
                    lowestEval = minmaxVal
                curBoard.pop()
            return lowestEval
        
    def get_ai_move(self,board,turn):
        best_outcome = self.minimax_recursive(board,turn,0)[1]
        return best_outcome
    
    def first_move(self, move_stack):
        first_move = str(move_stack[(len(move_stack) - self.max_depth)])
        return first_move