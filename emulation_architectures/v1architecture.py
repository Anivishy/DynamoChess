import torch
from torch import nn

# goal
# emulate elo rating


# naive structure
# features
# (64 * 13) current board state + current color + elo

# output should be predicted next move


class MainModel(nn.Module):
    def __init__(self, hidden_neuron_count = 1024, num_hidden_layers = 3):
        super().__init__()
        self.input_layer = nn.Linear(2 + 832, hidden_neuron_count)
        
        self.hidden_layers = []
        for i in range(num_hidden_layers):
            self.hidden_layers.append(nn.Linear(hidden_neuron_count, hidden_neuron_count))
            self.hidden_layers.append(nn.ReLU())
        
        self.output_layer = nn.Linear(hidden_neuron_count, 38) # 32 for move + 6 for promote piece (p, n, b, r, q, k)
    
    def forward(self, x):
        x = self.input_layer(x)
        for layer in self.hidden_layers:
            x = layer(x)
        x =  self.output_layer(x)
        return x
        
    