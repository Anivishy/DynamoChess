import chess
import torch

piece_to_index = {
    "p": 0,
    "n": 1,
    "b": 2,
    "r": 3,
    "q": 4,
    "k": 5,
    "P": 6,
    "N": 7,
    "B": 8,
    "R": 9,
    "Q": 10,
    "K": 11
}

def board_to_list(board):
    board_list = []
    for i in range(64):
        piece = board.piece_at(i)
        
        if piece is not None:
            board_list.append(piece.piece_type + 6 * piece.color) 
        else:
            board_list.append(0)
        


    return board_list

def uci_to_onehot_tensor(move):
    tensor = torch.zeros(8*4+6, dtype=torch.float32)
    tensor[ord(move[0])-97] = 1.0
    tensor[int(move[1]) + 8] = 1.0
    tensor[ord(move[2])-97 + 16] = 1.0
    tensor[int(move[3]) + 24] = 1.0
    if len(move) == 5:
        tensor[piece_to_index[move[4]] + 32] = 1.0
    return tensor

def uci_to_5d_tensor(move):
    tensor = torch.zeros(8*4+6, 8, 8, dtype=torch.float32)
    tensor[ord(move[0])-97, int(move[1]), int(move[2])] = 1.0
    tensor[ord(move[2])-97 + 16, int(move[3]), int(move[2])] = 1.0
    if len(move) == 5:
        tensor[piece_to_index[move[4]] + 32, int(move[1]), int(move[2])] = 1.0
    return tensor

def onehot_tensor_to_uci(tensor):
    move = ""
    move += chr(torch.argmax(tensor[:8]).item() + 97)
    move += str(torch.argmax(tensor[8:16]).item())
    move += chr(torch.argmax(tensor[16:24]).item() + 97)
    move += str(torch.argmax(tensor[24:32]).item())
    # if torch.argmax(tensor[32:]) != 0:
    #     move += list(piece_to_index.keys())[list(piece_to_index.values()).index(torch.argmax(tensor[32:]))]
    return move


def one_hot_board(list_board):
    
    #print(list_board)

    one_hot = torch.zeros(13, 8, 8, dtype=torch.float32)
    for i in range(64):
        piece = list_board[i]
        
        one_hot[piece, i // 8, i % 8] = 1.0

    return one_hot

def one_hot_to_board(one_hot):
    board = chess.Board()
    for i in range(64):
        for j in range(12):
            if one_hot[j, i // 8, i % 8] == 1.0:
                piece = chess.Piece(j % 6 + 1, j // 6)
                board.set_piece_at(i, piece)
    return board

def return_model_input(current_position, checking_position, checking_position_mat_heuristic):
    twoboard = torch.cat((one_hot_board(board_to_list(current_position)), one_hot_board(board_to_list(checking_position))), dim=0).unsqueeze(0)
    checking_position_mat_heuristic /= 103.0 # max points possible

    # flatten twoboard
    twoboard = twoboard.view(1, 13*8*8*2)

    # add checking_position_mat_heuristic
    twoboard = torch.cat((twoboard, torch.tensor(checking_position_mat_heuristic).view(1, 1)), dim=1)

    return twoboard
