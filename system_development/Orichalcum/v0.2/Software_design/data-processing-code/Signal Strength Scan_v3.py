#input: signal data file folder, heatmap dimensions
#output: signal strength heatmap

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Folder path

folder_path = r"C:\Users\mwhetham\Desktop\signal strength data\LayerScanV6 Experiments\Experiment5"
# Target heatmap dimensions
heatmap_dim = (100,100)


total_required = heatmap_dim[1] * heatmap_dim[0]

average_sig = []


# Loop through each file in the directory
i = 0
for file in sorted(os.listdir(folder_path)):  # Sorting ensures consistent ordering
    file_path = os.path.join(folder_path, file)
    
    try:
        # Read the file
        data = pd.read_csv(file_path, skiprows=24, header=None)
        Sigstrength = data.values[:, 1]
        #displacement = data.values[:, 2]  # Displacement column
        
        # Compute average displacement
        avg_signal = np.mean(Sigstrength)
        if  avg_signal >= 1.75:
            time= data.values[:,0]
            plt.figure(figsize=(10, 5))
           # plt.plot(time, displacement, label="displacement")
            plt.xlabel("Time (μs)")
            plt.ylabel("Amplitude")
            plt.title(f"{file}, {avg_signal}")
            plt.legend()
            #plt.grid()
            #plt.show()
            print('this one')
        else:
            print(f'no, {i}')
        average_sig.append(avg_signal)
        print (i)
        i = i + 1

    except Exception as e:
        print(f"Error processing {file}: {e}")

# Handle cases where we have too many or too few files
if len(avg_signal) < total_required:
    # Pad with NaNs if there are fewer values than needed
    avg_signal += [np.nan] * (total_required - len(avg_signal))
elif len(avg_signal) > total_required:
    # Trim extra values if more than needed
    avg_signal = avg_signal[:total_required]

# Reshape to 51x51
heatmap_avg_displacement = np.array(avg_signal).reshape(heatmap_dim)

# Plot heatmap of average displacements
plt.figure(figsize=(10, 8))
plt.imshow(heatmap_avg_displacement, cmap='viridis', interpolation='nearest', vmin=0, vmax=2)
plt.colorbar(label='Average Displacement')
#plt.title('100x100 Signal Strength Heatmap with Pulser Off')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
