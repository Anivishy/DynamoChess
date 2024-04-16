import chess
import random
import numpy as np
import torch
import torch.nn as nn
import util
import time

class ValueNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.sequential = nn.Sequential(
            nn.Linear(13*8*8+1, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )
    
    def forward(self, x):
        x = self.sequential(x)
        return x

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def fully_expanded(self):
        return len(self.children) == len(list(self.state.legal_moves))

    def __str__(self):
        return str(self.state)

EXPLORATION_CONSTANT = 0.1

total_visits = 0


# upper confidence bound
def ucb(node):
    return node.value / node.visits + EXPLORATION_CONSTANT * np.sqrt(total_visits / node.visits + 1)


def mcts(root, board, network, num_simulations, states, outcomes):
    boardturn = board.turn
    global total_visits
    
    for _ in range(num_simulations):
        #print(f"{(_ / num_simulations * 100):.2f}%", end="\r")
        
        node = root

        # select
        if node.fully_expanded():
            node = max(node.children, key=ucb)
        # expand
        elif (node.visits > 0): 
            unexpanded_moves = list(set(node.state.legal_moves) - set([child.state.peek() for child in node.children]))
            move = random.choice(unexpanded_moves)
            new_state = node.state.copy()
            new_state.push(move)
            new_node = Node(new_state, node)
            node.add_child(new_node)
            node = new_node

        while not node.is_leaf():
            # select
            if node.fully_expanded():
                node = max(node.children, key=ucb)
            # expand
            elif (node.visits > 0): 
                unexpanded_moves = list(set(node.state.legal_moves) - set([child.state.peek() for child in node.children]))
                move = random.choice(unexpanded_moves)
                new_state = node.state.copy()
                new_state.push(move)
                new_node = Node(new_state, node)
                node.add_child(new_node)
                node = new_node

        # simulate value with rollout
        # total_value = 0
        nodeturn = node.state.turn
        # for k in range(1):
        #     board = node.state.copy()
        #     while not board.is_game_over():
        #         move = random.choice(list(board.legal_moves))
        #         board.push(move)
        #     result = board.outcome()
        #     #print(result.winner, boardturn, nodeturn)
        #     value = 1 if result.winner == boardturn else -1 if result.winner != boardturn else -.1

        #     #value = 1 if result.winner == node.state.turn else -1 if result.winner != node.state.turn else 0
        #     total_value += value
        # node.value = total_value


        # get value from nn
        state = util.one_hot_board(util.board_to_list(node.state))
        #print(state.shape)
        state = torch.cat((torch.flatten(state), torch.tensor([node.state.turn], dtype=torch.float32)))
        
        value = network(state)
        total_value = value.item()
        node.value = total_value


        node.visits += 1
        total_visits += 1


        # backpropagate
        while not node.is_root():
            node = node.parent

            # flip value if not current player
            v = total_value
            # if node.state.turn != nodeturn:
            #     v = -total_value


            node.value += v
            node.visits += 1
            total_visits += 1
    #return max(root.children, key=lambda node: node.visits).state.peek()

    # return sample from the distribution of visits
    visits = [child.visits for child in root.children]


    # softmax
    normed_visits = np.exp(visits)
    normed_visits /= normed_visits.sum()

    # print(visits)
    # print(values)
    
    return root.children[np.argmax(np.random.multinomial(n=1, pvals=normed_visits))].state.peek()

# update root
def update_root(root, move):
   for child in root.children:
       if str(child.state.peek()) == str(move):
           root = child
           root.parent = None
           print("updated")
           break

def self_play(board, network, states, outcomes):
    root = Node(board)
    start_time = time.time()
    moves = 0
    while not board.is_game_over():
        root = Node(board)
        move = mcts(root, board, network, 400, states, outcomes)
        board.push(move)
        state = util.one_hot_board(util.board_to_list(board))
        #print(state.shape)
        state = torch.cat((torch.flatten(state), torch.tensor([board.turn], dtype=torch.float32)))
        states.append()
        moves += 1
        # show the visual board
        # print(board)
        # print()
        print(moves, end='\r')
    end_time = time.time()
    print()
    print("game done ", end_time - start_time)
    print(board.result())
    print(board.outcome().winner)



if __name__ == "__main__":
    states = []
    outcomes = []
    nnet = ValueNetwork()

    #print(mcts(chess.Board()))
    self_play(chess.Board(), nnet)