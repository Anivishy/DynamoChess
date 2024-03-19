import chess
import pygame
from ui import UI
from pgn_translator import Translator
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 800
square_size = size / 8
movemaker = Movemaker()
all_moves = 'e4 e5 Nf3 Nc6 Bb5 g6 O-O Bg7 c3 a6 Ba4 b5 Bc2 Nf6 d4 d6 dxe5 Nxe5 Nxe5 dxe5 Qxd8+ Kxd8 a4 Bb7 f3 Nd7 Be3 h5 Nd2 Bh6 Bxh6 Rxh6 Rfd1 Ke7 Nb3 Rhh8 Na5 Rab8 axb5 axb5 b4 Rhd8 Kf2 Nb6 Rxd8 Kxd8 Bb3 Ke7 Ke3 Ba8 h4 f5 Bc2 f4+ Ke2 Rg8 Bd3 g5 hxg5 Rxg5 Kf2 c6 Nb3 Bb7 Ra7'
translator = Translator(all_moves)

#print(chess.Move.from_uci("e2e5") in written_board.legal_moves)
#print(written_board.san(chess.Move.from_uci("g1f3")))
#print(written_board.parse_san('e4'))



def game_loop():
    pgn_moves = []
    turn = 0
    game_ui = UI(size)
    game_over = False
    selected_piece = None
    moves = all_moves.split(' ')
    for move in moves:
        uci = translator.pgn_to_uci(move, written_board)
        print(uci)
        written_board.push(chess.Move.from_uci(uci))
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
                        game_ui.selected_piece_movement(new_pos, screen_move, promotion, castle_detection)
                        pgn_moves.append(written_board.san(chess_move))
                        written_board.push(chess_move)
                    game_ui.set_selected_square(None)
                    movemaker.change_state()
                    print(pgn_moves)
        

        game_ui.draw_grid()
        game_ui.draw_pieces()
        pygame.display.update()
        turn += 1
        

if __name__ == '__main__':
    game_loop()
