import chess
import pygame
import time
from ui import UI
from pgn_translator import Translator
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 800
square_size = size / 8
movemaker = Movemaker()
all_moves = 'e4 g6 d4 Bg7 Nc3 c6 Nf3 d6 Be3 Nf6 Qd2 b5 Bh6 Bxh6 Qxh6 b4 Ne2 Nxe4 Qg7 Rf8 Ng3 Nf6 O-O-O Be6 Ng5 Bxa2 Nxh7 Nxh7 Qxh7 Nd7 h4 Qa5 h5 Nf6 Qh6 g5 d5 Bxd5 Qxg5 Qa1+ Kd2 Qxb2 Qe3 a5 h6 Ng4 Qf4 Qc3+ Kc1 b3 Bd3 b2+ Kb1 a4 Ne2 Qa3 c4 Ne5 Qd4 Nxd3 Rxd3 Qa1+ Kc2 Qxh1 cxd5 b1=Q+ Kd2 Qhd1+ Ke3 Qdxd3+ Qxd3 Qxd3+ Kxd3 a3 h7 a2 h8=Q Rxh8'
translator = Translator(all_moves)

#print(chess.Move.from_uci("e2e5") in written_board.legal_moves)
#print(written_board.san(chess.Move.from_uci("g1f3")))
#print(written_board.parse_san('e4'))

def automated_move(turn, moves, game_ui):
    if turn < len(moves):
        move = moves[turn]
        uci = translator.pgn_to_uci(move, written_board)
        chess_move = chess.Move.from_uci(uci)
        first_coord, second_coord = translator.uci_to_coordinates(uci)
        screen_move, promotion, castle_detection = translator.get_move_from_screen(first_coord, second_coord, game_ui.board)
        print(first_coord, second_coord, promotion, castle_detection, uci, move, chess_move)
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
    moves = all_moves.split(' ')
    print(translator.uci_to_coordinates('e2e4'))
    #for move in moves:
        #uci = translator.pgn_to_uci(move, written_board)
        #print(uci)
        #written_board.push(chess.Move.from_uci(uci))
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
                    print(selected_piece)
                else:
                    new_pos = movemaker.get_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                    screen_move, promotion, castle_detection = translator.get_move_from_screen(game_ui.get_seleceted_square(), new_pos, game_ui.board)
                    print(screen_move)
                    chess_move = chess.Move.from_uci(screen_move)
                    if chess_move in written_board.legal_moves:
                        game_ui.selected_piece_movement(new_pos, selected_piece, promotion, castle_detection)
                        pgn_moves.append(written_board.san(chess_move))
                        written_board.push(chess_move)
                    game_ui.set_selected_square(None)
                    movemaker.change_state()
                    print(pgn_moves)
        '''
        if turn < len(moves):
            move = moves[turn]
            uci = translator.pgn_to_uci(move, written_board)
        '''
        automated_move(turn, moves, game_ui)
        game_ui.draw_grid()
        game_ui.draw_pieces()
        pygame.display.update()
        turn += 1
        

if __name__ == '__main__':
    game_loop()
