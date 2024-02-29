import chess
import pygame
pygame.init()
written_board = chess.Board()

def game_loop():
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
    
    print((written_board))
    written_board.push(chess.Move.from_uci("g1f3"))
    written_board.push(chess.Move.from_uci("e7e5"))
    written_board.push(chess.Move.from_uci("e2e4"))
    written_board.push(chess.Move.from_uci("b8c6"))
    written_board.push(chess.Move.from_uci("d2d4"))
    written_board.push(chess.Move.from_uci("e5d4"))
    print(written_board.move_stack)
    print((written_board))
    pygame.display.update()

if __name__ == '__main__':
    game_loop()
