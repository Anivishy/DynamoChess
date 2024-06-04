from ui import UI
import ui
import chess
import re

class KingSafetyHeursitic:

    def __init__(self):
        pass

    def __getKingKernal(self,board:chess.Board,color):
        king_file = chess.square_file(board.king(color))
        king_rank = chess.square_rank(board.king(color))
        kernal = [] #move array
        for i in range (max(-2+king_file,0),min(2+king_file,7)):
            for j in range (max(-2+king_rank,0),min(2+king_rank,7)):
                cursquare = (i,j)
                kernal.append((cursquare,chess.square_distance(chess.square(i,j),board.king(color))))
        return kernal

    def getKingSafety (self, board: chess.Board, color):
        kernal = self.__getKingKernal(board,color)
        king_safety_constant = 0
        for square in kernal:
            dist_multiplier = 2
            if square[1]:
                dist_multiplier = 1/square[1]
            for attacker in board.attackers(color = not color,square=chess.square(*square[0])):   
                king_safety_constant -= ui.piece_value[str(board.piece_at(attacker).symbol()).lower()]*dist_multiplier  

            for defender in board.attackers(color = color,square=chess.square(*square[0])):
                king_safety_constant += ui.piece_value[str(board.piece_at(defender).symbol()).lower()]*dist_multiplier

        #normalize king_safety constant to 20 being the worst possible danger
        #the range of this normalization is [-2,2]

        if king_safety_constant<0:
            king_safety_constant = max(king_safety_constant,-60)/30
        else:
            king_safety_constant = min(king_safety_constant,60)/30
        if color == chess.BLACK:
            king_safety_constant*=-1

        return king_safety_constant