import torch
from torch import nn



# simple value mlp
class SimpleValueNetwork(nn.Module):
    def __init__(self, neurons):
        super(SimpleValueNetwork, self).__init__()

        self.fc = nn.Sequential( 
            nn.Linear(13*8*8*2+1, neurons),
            nn.LeakyReLU(),
            nn.Linear(neurons, neurons),
            nn.LeakyReLU(),
            nn.Linear(neurons, neurons),
            nn.LeakyReLU(),
            nn.Linear(neurons, neurons),
            nn.LeakyReLU(),
            nn.Linear(neurons, 1), 
        )

    def forward(self, x):
        x = self.fc(x)

        return x



# resnet block
class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResBlock, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.leaky1 = nn.LeakyReLU()
        self.leaky2 = nn.LeakyReLU()

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        #out = self.bn1(out)
        out = self.leaky1(out)
        out = self.conv2(out)
        #out = self.bn2(out)
        out += residual
        out = self.leaky2(out)
        return out

# value network
class ValueNetwork(nn.Module):
    def __init__(self):
        super(ValueNetwork, self).__init__()

        self.conv1 = nn.Conv2d(14, 254, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(254)
        self.res1 = ResBlock(254, 254)
        self.res2 = ResBlock(254, 254)
        self.res3 = ResBlock(254, 254)
        self.res4 = ResBlock(254, 254)
        self.res5 = ResBlock(254, 254)

        self.conv2 = nn.Conv2d(254, 32, kernel_size=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc1 = nn.Linear(64*32, 64*32)
        self.fc2 = nn.Linear(64*32, 64*32)
        self.fc3 = nn.Linear(64*32, 64*32)
        self.fc6 = nn.Linear(64*32, 1)

        self.leaky1 = nn.LeakyReLU()
        self.leaky2 = nn.LeakyReLU()
        self.leaky3 = nn.LeakyReLU()
        self.leaky4 = nn.LeakyReLU()
        self.leaky5 = nn.LeakyReLU()
        self.leaky6 = nn.LeakyReLU()
        self.leaky7 = nn.LeakyReLU()
    
    def forward(self, x):
        x = self.conv1(x)
        #x = self.bn1(x)
        x = self.leaky1(x)
        x = self.res1(x)
        x = self.res2(x)
        x = self.res3(x)
        x = self.res4(x)
        x = self.res5(x)


        x = self.conv2(x)
        #x = self.bn2(x)
        x = self.leaky2(x)
        x = x.view(-1, 64*32)



        x = self.fc1(x)
        x = self.leaky3(x)
        x = self.fc2(x)
        x = self.leaky4(x)
        x = self.fc3(x)
        x = self.leaky5(x)
        x = self.fc6(x)


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