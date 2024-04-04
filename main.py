import chess
import chess.pgn
import pygame
from ui import UI
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 600
square_size = size / 8
movemaker = Movemaker()


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
        pygame.display.update()
        turn += 1
        

if __name__ == '__main__':
    game_loop()
