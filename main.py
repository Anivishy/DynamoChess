import chess
import pygame
import time
from ui import UI
import random
from pgn_translator import Translator
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 800
square_size = size / 8
movemaker = Movemaker()
all_moves = 'd4 b6 Nc3 Bb7 Bf4 Nf6 e3 e6 Nf3 Bb4 Bd3 Bxc3+ bxc3 d6 O-O Nbd7 Re1 Qe7 e4 e5 Bg5 h6 Bxf6 Nxf6 c4 O-O d5 Nd7 g3 Nc5 Nh4 Bc8 Qf3 g5 Nf5 Qf6 g4 Bxf5 Qxf5 Qxf5 gxf5 Kg7 a4 Kf6 a5 bxa5 Rxa5 a6 Rea1 Rfb8 R5a2 g4 Kg2 Kg5 Kg3 h5 h4+ gxh3 Rh1 h4+ Kf3 a5 Rxh3 a4 Bf1 a3 Kg2 Nxe4 Raxa3 Rxa3 Rxa3 Nc5 Ra7 Rb7 Ra8 Rb2 Rh8 Rxc2 Rh7 e4 Kg1 f6 Bh3 Rxc4 Rg7+ Kf4 Rg4+ Ke5 Rxh4 Kxd5 Rh6 Ke5 Rh7 c6 Re7+ Kf4 Rf7 Rc1+ Kg2 Rc2 Kg1 Nd3 Rxf6 Nxf2 Bg2 d5 Rf8 Kg3 Rg8+ Ng4 f6 Rxg2+ Kf1 Rf2+ Ke1 Rxf6 Kd2 Kf3 Kc3 e3 Kb4 e2 Re8 Rf4+ Kc5 Re4 Rf8+ Ke3 Rg8 Ne5 Kb6 Nd3 Kc7 e1=Q Rg3+ Kd4 Rh3 Re7+ Kb6 Qb4+ Ka6 Qb5#'
translator = Translator(all_moves)


def automated_move(turn, moves, game_ui):
    if turn < len(moves):
        move = moves[turn]
        #uci = translator.pgn_to_uci(move, written_board)
        uci = None
        ind = random.randint(0, (written_board.legal_moves.count() - 1))
        for move in written_board.legal_moves:
            if ind > 0:
                pass
            else:
                uci = move.uci()
                break
            ind -= 1
        #print(written_board.legal_moves[ind])
        chess_move = chess.Move.from_uci(uci)
        first_coord, second_coord = translator.uci_to_coordinates(uci)
        screen_move, promotion, castle_detection = translator.get_move_from_screen(first_coord, second_coord, game_ui.board)
        if chess_move in written_board.legal_moves:
            game_ui.selected_piece_movement(second_coord, first_coord, promotion, castle_detection)
            written_board.push(chess_move)
        time.sleep(0.75)
        

def game_loop():
    pgn_moves = []
    turn = 0
    game_ui = UI(size)
    game_over = False
    selected_piece = None
    ai_move = False
    moves = all_moves.split(' ')
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if movemaker.get_state() == 0:
                    selected_piece = movemaker.get_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                    game_ui.set_selected_square([selected_piece[0], (selected_piece[1])]) # needs to be converted to indices
                    movemaker.change_state()
                else:
                    new_pos = movemaker.get_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                    screen_move, promotion, castle_detection = translator.get_move_from_screen(game_ui.get_seleceted_square(), new_pos, game_ui.board)
                    chess_move = chess.Move.from_uci(screen_move)
                    if chess_move in written_board.legal_moves:
                        game_ui.selected_piece_movement(new_pos, selected_piece, promotion, castle_detection)
                        pgn_moves.append(written_board.san(chess_move))
                        written_board.push(chess_move)
                        turn += 1
                        ai_move = True
                    game_ui.set_selected_square(None)
                    movemaker.change_state()
                    
                    
                    
        
        #automated_move(turn, moves, game_ui)
        game_ui.draw_grid()
        game_ui.draw_pieces()
        pygame.display.update()

        if ai_move:
            automated_move(turn, moves, game_ui)
            ai_move = False

        
        
        

if __name__ == '__main__':
    game_loop()
