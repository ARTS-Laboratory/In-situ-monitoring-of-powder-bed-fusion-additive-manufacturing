#%% 
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2, 100)  # Sample data.

plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(x, x, label='linear')  # Plot some data on the (implicit) Axes.
plt.plot(x, x**2, label='quadratic')  # etc.
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()
plt.show()

'''
graph_data = np.linspace(x*w, mem_rec, spk_rec)  # Sample data.

# Time axis
time_axis = torch.arrange(0, num_steps) #tensor data type. Time starts at 0 and goes to num_steps. Stops at num_steps so that num of points is = num_steps

plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(graph_data, graph_data, label='linear')  # Plot some data on the (implicit) Axes.
plt.plot(graph_data, graph_data**2, label='quadratic')  # etc.
plt.plot(graph_data, graph_data**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("LIF Neuron Model With Weighted Step Voltage")
plt.legend()
plt.show()

'''