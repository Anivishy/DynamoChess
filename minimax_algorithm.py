import chess
import pandas as pd
from copy import deepcopy
import math 
from CentControlHeuristic import CenterControlClass
import Heuristics
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
        self.positions = 0
        self.positions_reg_search = 0
        self.pruning = 0
        self.pruning_captures = 0


    def sort_partition(self, moves_scores_list, low, high):
        pivot = moves_scores_list[high]
        compare_index = low - 1
        for i in range(low, high + 1):
            if moves_scores_list[i][1] < pivot[1]:
                compare_index += 1 # move pointer only if it needs to be used
                moves_scores_list[i], moves_scores_list[compare_index] = moves_scores_list[compare_index], moves_scores_list[i]
        moves_scores_list[compare_index + 1], moves_scores_list[high] = moves_scores_list[high], moves_scores_list[compare_index + 1]
        return compare_index + 1

    def quick_sort(self, moves_scores_list, low, high):
        if low < high:
            index = self.sort_partition(moves_scores_list, low, high)
            #rint(moves_scores_list)
            self.quick_sort(moves_scores_list, low, index - 1)
            self.quick_sort(moves_scores_list, index + 1, high)


    def get_eval_bar(self,board:chess.Board, curTurn, move_object_moves):
        #TODO
        evaluation = 0
        material = self.heuristic.piece_values(board)

        init_turn = board.turn

        board.turn = chess.WHITE
        num_legal_moves_white = board.legal_moves.count()

        board.turn = chess.BLACK
        num_legal_moves_black = board.legal_moves.count()

        board.turn = init_turn

        evaluation += (num_legal_moves_white-num_legal_moves_black)* 0.1

        center_control_heuristic = self.heuristic.get_center_control_value(board, self.center_contol, move_object_moves)
        evaluation += center_control_heuristic*0.01

        king_safety_measurment = self.heuristic.get_king_safety_value(board)
        evaluation += king_safety_measurment

        evaluation += material * 2
        #print(material * 2, num_legal_moves * 0.02, center_control_heuristic * 0.075)
        return evaluation, (material * 2, (num_legal_moves_white-num_legal_moves_black) * 0.01, curTurn,  deepcopy(board))

    def captures_only_search(self, curBoard, curTurn, depth, alpha, beta, move_object_moves):
        capture_legal_moves = self.heuristic.legal_move_manipulation(curBoard, self.translator.uci_to_coordinates)[1]
        
        #print(len(capture_legal_moves))
        #print(curBoard.move_stack, depth)
        if len(capture_legal_moves) == 0 or depth >= self.max_depth + 4:
            return (self.get_eval_bar(curBoard, curTurn, move_object_moves), self.first_move(curBoard.move_stack, depth))
        moves_scores_list, moves_length = self.heuristic.move_ordering(capture_legal_moves, curBoard)
        self.quick_sort(moves_scores_list, 0, moves_length - 1)
        #print(capture_legal_moves, curBoard.move_stack)
        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = (self.get_eval_bar(curBoard, curTurn, move_object_moves), self.first_move(curBoard.move_stack, depth), self.first_move(move_stack, depth))
            for i in moves_scores_list:
                curBoard.push(i[0])
                captures_only_minmax_val = self.captures_only_search(curBoard, not curTurn, depth+1, alpha, beta, move_object_moves)
                self.positions += 1
                if captures_only_minmax_val[0][0] > highestEval[0][0]:
                    highestEval = captures_only_minmax_val
                curBoard.pop()
                alpha = max(alpha, highestEval[0][0])
                if beta <= alpha:
                    self.pruning_captures += 1
                    break
            return highestEval
        else:
            move_stack = curBoard.move_stack
            lowestEval = (self.get_eval_bar(curBoard, curTurn, move_object_moves), self.first_move(curBoard.move_stack, depth),self.first_move(curBoard.move_stack, depth + 1))
            for i in moves_scores_list:
                curBoard.push(i[0])
                captures_only_minmax_val = self.captures_only_search(curBoard,not curTurn,depth+1, alpha, beta, move_object_moves)
                self.positions += 1
                if captures_only_minmax_val[0][0]<lowestEval[0][0]:
                    lowestEval = captures_only_minmax_val
                curBoard.pop()
                beta = min(beta, lowestEval[0][0])
                if beta <= alpha:
                    self.pruning_captures += 1
                    break
            return lowestEval

    def minimax_recursive(self,curBoard,curTurn,curDepth, alpha, beta, move_object_moves):
        if curDepth == self.max_depth:
            return (self.captures_only_search(curBoard, curTurn, curDepth, alpha, beta, move_object_moves))
            #return (self.get_eval_bar(curBoard, curTurn, move_object_moves),self.first_move(curBoard.move_stack, self.max_depth)) # TODO: Switch this to evluating all captures
        move_object_moves = self.center_contol.legal_move_manipulation(curBoard)
        test = [(None, 12), (None, 20), (None, 10), (None, 20), (None, 33), (None, 2), (None, 112), (None, 43), (None, 20)]
        #self.quick_sort(test, 0, len(test) - 1)
        moves_scores_list, moves_length = self.heuristic.move_ordering(curBoard.legal_moves, curBoard)
        self.quick_sort(moves_scores_list, 0, moves_length - 1)
        if curTurn == chess.WHITE:
            move_stack = curBoard.move_stack
            highestEval = ((-float(math.inf), None),self.first_move(curBoard.move_stack, curDepth))
            for i in moves_scores_list:
                curBoard.push(i[0])
                #################
                #white_minmax_thread = ThreadWithReturnValue(target = self.minimax_recursive, 
                                                            #args = [curBoard, not curTurn, curDepth + 1, alpha, beta, move_object_moves])
                #white_minmax_thread.start()
                #self.white_minmax.append(white_minmax_thread)
                #minmaxVal = white_minmax_thread.join()
                self.positions_reg_search += 1
                minmaxVal = self.minimax_recursive(curBoard, not curTurn,curDepth+1, alpha, beta, move_object_moves)
                if minmaxVal[0][0]>highestEval[0][0]:
                    highestEval = minmaxVal
                curBoard.pop()
                alpha = max(alpha, highestEval[0][0])
                if beta <= alpha:
                    self.pruning += len(moves_scores_list) ** (curDepth)
                    break
            return highestEval
        else:
            move_stack = curBoard.move_stack
            lowestEval = ((float(math.inf), None),self.first_move(curBoard.move_stack, curDepth + 1))
            for i in moves_scores_list:
                curBoard.push(i[0])
                ################
                #black_minmax_thread = ThreadWithReturnValue(target = self.minimax_recursive, 
                                                            #args = [curBoard, not curTurn, curDepth + 1, alpha, beta, move_object_moves])
                #black_minmax_thread.start()
                #self.black_minmax.append(black_minmax_thread)
                #minmaxVal = black_minmax_thread.join()
                self.positions_reg_search += 1
                minmaxVal = self.minimax_recursive(curBoard,not curTurn,curDepth+1, alpha, beta, move_object_moves)
                #print(minmaxVal)
                if minmaxVal[0][0]<lowestEval[0][0]:
                    lowestEval = minmaxVal
                curBoard.pop()
                beta = min(beta, lowestEval[0][0])
                if beta <= alpha:
                    self.pruning += len(moves_scores_list) ** (curDepth)
                    break
            return lowestEval
        
    def get_ai_move(self,board,turn):
        self.positions = 0
        self.positions_reg_search = 0
        self.pruning = 0
        move_object_moves = self.center_contol.legal_move_manipulation(board)
        best_outcome = self.minimax_recursive(board,turn,0, float(-math.inf), float(math.inf), move_object_moves)
        if best_outcome[0][1] != None:
            print(best_outcome[0])
            print(best_outcome[0][1][-1])
        print(self.positions, self.positions_reg_search)
        print(self.pruning_captures, self.pruning)
        return best_outcome[1]
    
    def first_move(self, move_stack, depth):
        if len(move_stack) == 0:
            return None
        first_move = str(move_stack[int(len(move_stack) - depth)])
        return first_move