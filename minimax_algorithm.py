import chess
import pandas as pd
from copy import deepcopy
import math 
from CentControlHeuristic import CenterControlClass
from pgn_translator import Translator

import random

class ChessAI():
    def __init__(self,depth, translator, heuristic) -> None:
        self.max_depth = depth
        self.empty_board = chess.Board()
        self.translator = translator
        self.heuristic = heuristic
        self.center_contol = CenterControlClass()
        self.positions = 0
        self.positions_reg_search = 0

    def get_eval_bar(self,board, curTurn, move_object_moves):
        #TODO
        evaluation = 0
        material = self.heuristic.piece_values(board)
        num_legal_moves = board.legal_moves.count()
        center_control_heuristic = self.heuristic.get_center_control_value(board, self.center_contol, move_object_moves)
        #print(center_control_heuristic)
        if curTurn: # white
            #print("White")
            evaluation += num_legal_moves * 0.01
            evaluation += center_control_heuristic * 0.03
        else:
            #print("Black")
            evaluation += -num_legal_moves * 0.01
            evaluation += -center_control_heuristic * 0.03
        evaluation += material * 2
        #print(material * 2, num_legal_moves * 0.02, center_control_heuristic * 0.075)
        return evaluation

    def captures_only_search(self, curBoard, curTurn, depth, alpha, beta, move_object_moves):
        capture_legal_moves = self.heuristic.legal_move_manipulation(curBoard, self.translator.uci_to_coordinates)[1]
        #print(len(capture_legal_moves))
        #print(curBoard.move_stack, depth)
        if len(capture_legal_moves) == 0 or depth >= self.max_depth + 2:
            return (self.get_eval_bar(curBoard, curTurn, move_object_moves), self.first_move(curBoard.move_stack, depth))
        
        #print(capture_legal_moves, curBoard.move_stack)
        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = (-float(math.inf), self.first_move(move_stack, depth))
            for i in capture_legal_moves:
                curBoard.push(i)
                captures_only_minmax_val = self.captures_only_search(curBoard, not curTurn, depth+1, alpha, beta, move_object_moves)
                self.positions += 1
                if captures_only_minmax_val[0] > highestEval[0]:
                    highestEval = captures_only_minmax_val
                curBoard.pop()
                alpha = max(alpha, highestEval[0])
                if beta <= alpha:
                    break
            return highestEval
        else:
            move_stack = curBoard.move_stack
            lowestEval = (float(math.inf),self.first_move(curBoard.move_stack, depth + 1))
            for i in capture_legal_moves:
                curBoard.push(i)
                captures_only_minmax_val = self.captures_only_search(curBoard,not curTurn,depth+1, alpha, beta, move_object_moves)
                self.positions += 1
                if captures_only_minmax_val[0]<lowestEval[0]:
                    lowestEval = captures_only_minmax_val
                curBoard.pop()
                beta = min(beta, lowestEval[0])
                if beta <= alpha:
                    break
            return lowestEval

    def minimax_recursive(self,curBoard,curTurn,curDepth, alpha, beta, move_object_moves):
        if curDepth == self.max_depth:
            return (self.captures_only_search(curBoard, curTurn, curDepth, alpha, beta, move_object_moves))
            #return (self.get_eval_bar(curBoard, curTurn, move_object_moves),self.first_move(curBoard.move_stack, self.max_depth)) # TODO: Switch this to evluating all captures
        move_object_moves = self.center_contol.legal_move_manipulation(curBoard)
        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = (-float(math.inf),self.first_move(curBoard.move_stack, curDepth))
            for i in curBoard.legal_moves:
                curBoard.push(i)
                minmaxVal = self.minimax_recursive(curBoard, not curTurn,curDepth+1, alpha, beta, move_object_moves)
                self.positions_reg_search += 1
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
                minmaxVal = self.minimax_recursive(curBoard,not curTurn,curDepth+1, alpha, beta, move_object_moves)
                self.positions_reg_search += 1
                if minmaxVal[0]<lowestEval[0]:
                    lowestEval = minmaxVal
                curBoard.pop()
                beta = min(beta, lowestEval[0])
                if beta <= alpha:
                    break
            return lowestEval
        
    def get_ai_move(self,board,turn):
        self.positions = 0
        self.positions_reg_search = 0
        move_object_moves = self.center_contol.legal_move_manipulation(board)
        best_outcome = self.minimax_recursive(board,turn,0, float(-math.inf), float(math.inf), move_object_moves)
        print(best_outcome[0])
        print(self.positions, self.positions_reg_search)
        return best_outcome[1]
    
    def first_move(self, move_stack, depth):
        
        first_move = str(move_stack[int(len(move_stack) - depth)])
        return first_move