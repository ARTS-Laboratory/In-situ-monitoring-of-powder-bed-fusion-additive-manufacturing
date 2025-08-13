'''
Code by Charlie Bure
Code from: https://snntorch.readthedocs.io/en/latest/tutorials/tutorial_3.html
           https://snntorch.readthedocs.io/en/latest/tutorials/tutorial_1.html
Notes: 
    - This is a test and first try
    - More will be added on
'''

# Setup
import snntorch as snn
from snntorch import spikeplot as splt
from snntorch import spikegen
from IPython.display import HTML

import torch
import torch.nn as nn
import matplotlib .pyplot as plt

import matplotlib.pyplot as plt
import numpy as np


# Implementing the neuron
def leaky_integrate_and_fire(mem, x, w, beta, threshold=1):
    spk = (mem > threshold) # if membrane exceeds threshold, spk=1, else, 0
    mem = beta * mem + w*x - spk*threshold
    return spk, mem
    

# set neuronal parmeters
delta_t = torch.tensor(1e-3)
tau = torch.tensor(5e-3)
beta = torch.exp(-delta_t/tau)

print(f"The decay rate is: {beta:.3f}")


# Something
num_steps = 200 #number of steps the SNN will do

# initialize inputs/outputs + small step current input
x = torch.cat((torch.zeros(10), torch.ones(190)*0.5), 0) #input current
mem = torch.zeros(1)
spk_out = torch.zeros(1)
mem_rec = []
spk_rec = []

# neuron parameters
w = 0.4
beta = 0.819

# neuron simulation
for step in range(num_steps):
  spk, mem = leaky_integrate_and_fire(mem, x[step], w=w, beta=beta)
  mem_rec.append(mem)
  spk_rec.append(spk)

# convert lists to tensors
mem_rec = torch.stack(mem_rec)
spk_rec = torch.stack(spk_rec)

## Graphing
#splt.plot_cur_mem_spk(x*w, mem_rec, spk_rec, threshold=1, ylim_max1=0.5, title="LIF Neuron Model With Weighted Step Voltage")

#plot one sample data, index into a single sample from batch (B) dimension of spike_data





