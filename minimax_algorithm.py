import chess
import pandas as pd
from copy import deepcopy
import math 
from CentControlHeuristic import CenterControlClass
from pgn_translator import Translator
from threading import Thread
import threading
import random

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

class ChessAI():
    def __init__(self,depth, translator, heuristic) -> None:
        self.max_depth = depth
        self.empty_board = chess.Board()
        self.translator = translator
        self.heuristic = heuristic
        self.center_contol = CenterControlClass()
        self.white_minmax = []
        self.black_minmax = []

    def get_eval_bar(self,board, curTurn, move_object_moves):
        #TODO
        evaluation = 0
        material = self.heuristic.piece_values(board)
        num_legal_moves = board.legal_moves.count()
        center_control_heuristic = self.heuristic.get_center_control_value(board, self.center_contol, move_object_moves)
        #print(center_control_heuristic)
        if curTurn: # white
            #print("White")
            evaluation += num_legal_moves * 0.02
            evaluation += center_control_heuristic * 0.01
        else:
            #print("Black")
            evaluation += -num_legal_moves * 0.02
            evaluation += center_control_heuristic * -0.01
        evaluation += material * 2
        #print(material * 2, num_legal_moves * 0.02, center_control_heuristic * 0.075)
        
        return evaluation
    def minimax_recursive(self,curBoard,curTurn,curDepth, alpha, beta, move_object_moves):
        if curDepth == self.max_depth:
            return (self.get_eval_bar(curBoard, curTurn, move_object_moves),self.first_move(curBoard.move_stack, self.max_depth)) # TODO: Switch this to evluating all captures
        move_object_moves = self.center_contol.legal_move_manipulation(curBoard)
        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = (-float(math.inf),self.first_move(curBoard.move_stack, curDepth))
            for i in curBoard.legal_moves:
                curBoard.push(i)
                #################
                white_minmax_thread = ThreadWithReturnValue(target = self.minimax_recursive, 
                                                            args = [curBoard, not curTurn, curDepth + 1, alpha, beta, move_object_moves])
                white_minmax_thread.start()
                self.white_minmax.append(white_minmax_thread)
                minmaxVal = white_minmax_thread.join()
                #minmaxVal = self.minimax_recursive(curBoard, not curTurn,curDepth+1, alpha, beta, move_object_moves)
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
                ################
                black_minmax_thread = ThreadWithReturnValue(target = self.minimax_recursive, 
                                                            args = [curBoard, not curTurn, curDepth + 1, alpha, beta, move_object_moves])
                black_minmax_thread.start()
                self.black_minmax.append(black_minmax_thread)
                minmaxVal = black_minmax_thread.join()
                #minmaxVal = self.minimax_recursive(curBoard,not curTurn,curDepth+1, alpha, beta, move_object_moves)
                if minmaxVal[0]<lowestEval[0]:
                    lowestEval = minmaxVal
                curBoard.pop()
                beta = min(beta, lowestEval[0])
                if beta <= alpha:
                    break
            return lowestEval
        
    def get_ai_move(self,board,turn):
        move_object_moves = self.center_contol.legal_move_manipulation(board)
        best_outcome = self.minimax_recursive(board,turn,0, float(-math.inf), float(math.inf), move_object_moves)
        print(best_outcome[0])
        #print(turn)
        return best_outcome[1]
    
    def first_move(self, move_stack, depth):
        first_move = str(move_stack[(len(move_stack) - depth)])
        return first_move