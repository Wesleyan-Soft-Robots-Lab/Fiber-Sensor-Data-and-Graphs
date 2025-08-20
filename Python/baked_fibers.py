import os
import pandas as pd
import matplotlib.pyplot as plt
dataPath = "Sensor fiber characterization/baked/"
palette = ["#E69F00", "#0072B2", "#F0E442", "#009E73", "#D55E00", "#56B4E9"]

files = ["baked_2-synced.csv"]


for i,file in enumerate(files):
    df = pd.read_csv(os.path.join(dataPath,file), header=None)

    df["res_change"] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
    x = 30*df[1]/df[1].max() #scale to 30
    name = f"Sensor Fiber # {i}" if (i!=0) else f"Electroplated thread"
    plt.plot(x,df["res_change"], color=palette[i], label=name)

# Plot design
plt.annotate("", xytext=(0, 1), xy=(1, 2.5), arrowprops=dict(arrowstyle="->"))
plt.title("5x 30 Percent Strain (Baked)")
plt.legend()
plt.xlabel("Strain (%)")
plt.ylabel("Percent Change in Resistance")
plt.grid()
plt.show()