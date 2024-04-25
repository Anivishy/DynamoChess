import chess
import pandas as pd
from copy import deepcopy
import math 

import random

class ChessAI():
    def __init__(self,depth, translator, heuristic) -> None:
        self.max_depth = depth
        self.empty_board = chess.Board()
        self.translator = translator
        self.heuristic = heuristic

    def get_eval_bar(self,board, curTurn):
        #TODO
        evaluation = 0
        material = self.heuristic.piece_values(board)
        num_legal_moves = board.legal_moves.count()
        if curTurn: # white
            evaluation += num_legal_moves * 0.1
        else:
            evaluation += -num_legal_moves * 0.1
        evaluation += material
        #print(evaluation)
        return evaluation
    def minimax_recursive(self,curBoard,curTurn,curDepth, alpha, beta):
        if curDepth == self.max_depth:
            return (self.get_eval_bar(curBoard, curTurn),self.first_move(curBoard.move_stack, self.max_depth)) # TODO: Switch this to evluating all captures

        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = (-float(math.inf),self.first_move(curBoard.move_stack, curDepth))
            for i in curBoard.legal_moves:
                curBoard.push(i)
                minmaxVal = self.minimax_recursive(curBoard, not curTurn,curDepth+1, alpha, beta)
                if minmaxVal[0]>highestEval[0]:
                    highestEval = minmaxVal
                curBoard.pop()
                alpha = max(alpha, highestEval[0])
                if beta <= alpha:
                    break
            return highestEval
        else:
            move_stack = curBoard.move_stack
            lowestEval = (float(math.inf),self.first_move(curBoard.move_stack, curDepth + 1))
            for i in curBoard.legal_moves:
                curBoard.push(i)
                minmaxVal = self.minimax_recursive(curBoard,not curTurn,curDepth+1, alpha, beta)
                if minmaxVal[0]<lowestEval[0]:
                    lowestEval = minmaxVal
                curBoard.pop()
                beta = min(beta, lowestEval[0])
                if beta <= alpha:
                    break
            return lowestEval
        
    def get_ai_move(self,board,turn):
        best_outcome = self.minimax_recursive(board,turn,0, float(-math.inf), float(math.inf))
        print(best_outcome[0])
        return best_outcome[1]
    
    def first_move(self, move_stack, depth):
        first_move = str(move_stack[(len(move_stack) - depth)])
        return first_move