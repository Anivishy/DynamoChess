import torch
from torch import nn

# goal
# emulate different playstyles (not specific player)


# copied from v1
class MainModel(nn.Module):
    def __init__(self, deep_neuron_count = 512, num_hidden_layers = 3):
        super().__init__()
        self.input_layer = nn.Linear(1418, deep_neuron_count),
        
        self.hidden_layers = []
        for i in range(num_hidden_layers):
            self.hidden_layers.append(nn.Linear(deep_neuron_count, deep_neuron_count))
        
        self.output_layer = nn.Linear(deep_neuron_count, 11)
    
    def forward(self, x):
        x = torch.relu(self.input_layer(x))
        for layer in self.hidden_layers:
            x = torch.relu(layer(x))
        x = torch.sigmoid(self.output_layer(x))
        return x
        
    