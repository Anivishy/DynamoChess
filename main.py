import chess
import pygame
from ui import UI
from pgn_translator import Translator
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 1000
square_size = size / 8
movemaker = Movemaker()
all_moves = 'e4 e5 Nf3 Nc6 Bb5 g6 O-O Bg7 c3 a6 Ba4 b5 Bc2 Nf6 d4 d6 dxe5 Nxe5 Nxe5 dxe5 Qxd8+ Kxd8 a4 Bb7 f3 Nd7 Be3 h5 Nd2 Bh6 Bxh6 Rxh6 Rfd1 Ke7 Nb3 Rhh8 Na5 Rab8 axb5 axb5 b4 Rhd8 Kf2 Nb6 Rxd8 Kxd8 Bb3 Ke7 Ke3 Ba8 h4 f5 Bc2 f4+ Ke2 Rg8 Bd3 g5 hxg5 Rxg5 Kf2 c6 Nb3 Bb7 Ra7'
translator = Translator(all_moves)




def game_loop():
    
    turn = 1
    game_ui = UI(size)
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                movemaker.set_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                movemaker.change_state()
            if event.type == pygame.MOUSEBUTTONUP:
                movemaker.change_state()


        '''
        print((written_board))
        written_board.push(chess.Move.from_uci("g1f3"))
        written_board.push(chess.Move.from_uci("e7e5"))
        written_board.push(chess.Move.from_uci("e2e4"))
        written_board.push(chess.Move.from_uci("b8c6"))
        written_board.push(chess.Move.from_uci("d2d4"))
        written_board.push(chess.Move.from_uci("e5d4"))
        print(written_board.move_stack)
        print((written_board))'''
        game_ui.draw_grid()
        game_ui.draw_pieces()
        pygame.display.update()
        turn += 1
        

if __name__ == '__main__':
    game_loop()
