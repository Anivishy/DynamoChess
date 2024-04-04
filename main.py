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

pgn = [Event "Live Chess"]\n[Site "Chess.com"]\n[Date "2023.03.02"]\n[Round "-"]\n[White "ActorXu"]\n[Black "Bigfish1995"]\n[Result "0-1"]\n[CurrentPosition "1R6/8/7p/8/5K1P/k7/8/1q1r4 w - -"]\n[Timezone "UTC"]\n[ECO "B52"]\n[ECOUrl "https://www.chess.com/openings/Sicilian-Defense-Canal-Main-Line...5.O-O-Ngf6-6.Qe2-e6-7.b3"]\n[UTCDate "2023.03.02"]\n[UTCTime "15:31:54"]\n[WhiteElo "2462"]\n[BlackElo "2614"]\n[TimeControl "600+2"]\n[Termination "Bigfish1995 won by resignation"]\n[StartTime "15:31:54"]\n[EndDate "2023.03.02"]\n[EndTime "15:53:53"]\n[Link "https://www.chess.com/game/live/71510168275"]\n\n1. e4 {[%clk 0:09:59.8]} 1... c5 {[%clk 0:09:52.5]} 2. Nf3 {[%clk 0:09:27.6]} 2... d6 {[%clk 0:09:52.9]} 3. Bb5+ {[%clk 0:09:27.4]} 3... Bd7 {[%clk 0:09:41.2]} 4. Bxd7+ {[%clk 0:09:27.6]} 4... Nxd7 {[%clk 0:09:40.5]} 5. O-O {[%clk 0:09:28.4]} 5... Ngf6 {[%clk 0:09:39.4]} 6. Qe2 {[%clk 0:09:29]} 6... e6 {[%clk 0:09:01.5]} 7. b3 {[%clk 0:09:05.4]} 7... b5 {[%clk 0:07:45.3]} 8. Bb2 {[%clk 0:08:29.3]} 8... a6 {[%clk 0:07:17.5]} 9. a4 {[%clk 0:08:14.9]} 9... b4 {[%clk 0:07:08.9]} 10. d3 {[%clk 0:08:06.2]} 10... Be7 {[%clk 0:07:05]} 11. Nbd2 {[%clk 0:08:06.9]} 11... O-O {[%clk 0:07:03.4]} 12. Rae1 {[%clk 0:06:12.8]} 12... d5 {[%clk 0:06:02.1]} 13. exd5 {[%clk 0:05:11.2]} 13... Nxd5 {[%clk 0:06:01.6]} 14. Nc4 {[%clk 0:05:09.6]} 14... Rc8 {[%clk 0:05:49.9]} 15. Nfe5 {[%clk 0:04:59.6]} 15... Nxe5 {[%clk 0:05:48.1]} 16. Qxe5 {[%clk 0:04:41.3]} 16... Bf6 {[%clk 0:05:43.3]} 17. Qg3 {[%clk 0:04:28.8]} 17... Nc3 {[%clk 0:05:23.1]} 18. Bxc3 {[%clk 0:04:20.1]} 18... Bxc3 {[%clk 0:05:21.6]} 19. Re4 {[%clk 0:04:18.5]} 19... Rc7 {[%clk 0:05:14]} 20. f4 {[%clk 0:04:10.7]} 20... Re7 {[%clk 0:05:12.3]} 21. h3 {[%clk 0:03:58.5]} 21... Rfe8 {[%clk 0:05:06.2]} 22. Kh1 {[%clk 0:03:58.5]} 22... f6 {[%clk 0:04:51.8]} 23. Qf3 {[%clk 0:03:56.7]} 23... Qc7 {[%clk 0:04:45.4]} 24. Re2 {[%clk 0:03:39.4]} 24... g6 {[%clk 0:04:45.9]} 25. Re4 {[%clk 0:03:39.8]} 25... Kg7 {[%clk 0:04:46.3]} 26. Re2 {[%clk 0:03:36.3]} 26... Qd8 {[%clk 0:04:46.3]} 27. Re4 {[%clk 0:03:37]} 27... Qd5 {[%clk 0:04:38.7]} 28. Re2 {[%clk 0:03:27.2]} 28... Qxf3 {[%clk 0:04:34.3]} 29. Rxf3 {[%clk 0:03:28.2]} 29... f5 {[%clk 0:04:36]} 30. g4 {[%clk 0:02:52]} 30... h6 {[%clk 0:04:24.2]} 31. Kg2 {[%clk 0:02:51.7]} 31... Kf6 {[%clk 0:04:23.5]} 32. Kg3 {[%clk 0:02:48.1]} 32... e5 {[%clk 0:04:08.7]} 33. fxe5+ {[%clk 0:02:06.3]} 33... Bxe5+ {[%clk 0:04:07.4]} 34. Nxe5 {[%clk 0:02:05]} 34... Rxe5 {[%clk 0:04:06.9]} 35. Ref2 {[%clk 0:02:00.2]} 35... Re3 {[%clk 0:03:51.7]} 36. gxf5 {[%clk 0:01:45]} 36... gxf5 {[%clk 0:03:51.5]} 37. Kg2 {[%clk 0:01:30.4]} 37... Rg8+ {[%clk 0:03:39.4]} 38. Kf1 {[%clk 0:01:29.7]} 38... Rxf3 {[%clk 0:03:40.5]} 39. Rxf3 {[%clk 0:01:30.9]} 39... Ke5 {[%clk 0:03:42.1]} 40. Rf2 {[%clk 0:01:09.5]} 40... Rg3 {[%clk 0:03:38.3]} 41. Re2+ {[%clk 0:00:50.7]} 41... Kd4 {[%clk 0:03:30.1]} 42. Re6 {[%clk 0:00:51.4]} 42... Kc3 {[%clk 0:03:22.9]} 43. Rxa6 {[%clk 0:00:39.5]} 43... Kxc2 {[%clk 0:03:23.9]} 44. Rc6 {[%clk 0:00:37]} 44... Kxb3 {[%clk 0:03:22.9]} 45. a5 {[%clk 0:00:34.5]} 45... Rxd3 {[%clk 0:02:53.9]} 46. Rxc5 {[%clk 0:00:28.8]} 46... Rd6 {[%clk 0:02:38.6]} 47. Rxf5 {[%clk 0:00:22.9]} 47... Ka4 {[%clk 0:02:32.3]} 48. Ke2 {[%clk 0:00:11.3]} 48... b3 {[%clk 0:02:33]} 49. Rf8 {[%clk 0:00:06.9]} 49... Kxa5 {[%clk 0:02:29.4]} 50. Rb8 {[%clk 0:00:06.9]} 50... Ka4 {[%clk 0:02:29.1]} 51. Ke3 {[%clk 0:00:06.3]} 51... Rd5 {[%clk 0:02:27.2]} 52. Ke4 {[%clk 0:00:03.7]} 52... Rd6 {[%clk 0:02:19.6]} 53. Ke5 {[%clk 0:00:04]} 53... Rd2 {[%clk 0:02:19.9]} 54. h4 {[%clk 0:00:04]} 54... b2 {[%clk 0:02:19]} 55. Ke4 {[%clk 0:00:04.7]} 55... Ka3 {[%clk 0:02:19]} 56. Ke3 {[%clk 0:00:05.5]} 56... Rd1 {[%clk 0:02:15.9]} 57. Kf4 {[%clk 0:00:04.8]} 57... b1=Q {[%clk 0:02:16.5]} 0-1\n
game = chess.pgn.read_game(pgn)
board = game.board()
for move in game.mainline_moves():
    board.push(move)
board

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
