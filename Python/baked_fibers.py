import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

dataPath = "Sensor fiber characterization/baked/"
palette= ['#ff5e45', '#7c003e', '#1b00cd', '#008383', '#c902e5','#4c3b01' ]
""" 
palette = [['#C902E5', '#AF02B3', '#93027E', '#750246','#5C0216'],
           ['#FF5E45', '#D35534', '#A84D24', "#794412",'#4C3B01'],
           ['#008383', '#066594', '#0E3FA9', '#151EBC', '#1B00CD']
           ]
cmap1 = LinearSegmentedColormap.from_list("orangebrown", palette[1])
"""

files = ["baked_2-synced.csv",
         "baked_3-synced.csv",
         "baked_4-synced.csv"
         ]

for i,file in enumerate(files):
    df = pd.read_csv(os.path.join(dataPath,file), header=None)

    df["res_change"] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
    x = 30*df[1]/df[1].max() #scale to 30
    name = f"Sensor Fiber # {i+1}"

    plt.plot(x,df["res_change"], color=palette[i], label=name)

# Plot design
plt.annotate("", xytext=(0, 2), xy=(1, 4), arrowprops=dict(arrowstyle="->"))
plt.title('Baked Fiber',fontsize=20)
plt.legend()
plt.xlabel('Strain (%)', fontsize=15)
plt.ylabel(u'Δ Resistance (%)',fontsize=15)
plt.grid()
plt.show()