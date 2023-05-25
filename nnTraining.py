import numpy as np
import pandas as pd
import torch 
import torch.nn as nn


class bpRegressor(nn.Module):
    def __init__(self, layout):
        layers = []
        inSize = 21
        for size in layout:
            layers.append(nn.Linear(inSize, size))
            nn.init.xavier_uniform_(layers[-1].weight)
            layers[-1].bias.data.fill_(0)
            if size > 1:
                layers.append(nn.ReLU())
            inSize = size

        self.network = nn.Sequential(*layers)
        return

    def forward(self, x):
        return self.network(x)

# This takes in 3 tables. The Normalized PPG features, the matching SBP average values, the matching DBP average values.
def fit(self, PPG, SBP, DBP):
    reg = bpRegressor([21, 21, 2])
    optimizer = torch.optim.SDG(reg.parameters(), lr=0.1)
    lossFn = nn.MSELoss()
    loader = torch.utils.data.DataLoader

    for pulse, sbp, dbp in PPG, SBP, DBP:
        prediction = reg.forward(pulse)

        loss = lossFn(prediction, [sbp, dbp])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
