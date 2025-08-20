import os
import pandas as pd
import matplotlib.pyplot as plt
dataPath = "Sensor fiber characterization/5x runs/"
palette = ['#4c3b01', '#7c003e', '#1b00cd', '#008383', '#c902e5', '#ff5e45']

files = ["oldthread_30percent_5x_synced.csv",
         "oldthread_sensorfiber_5x_1_synced.csv",
         "oldthread_sensorfiber_5x_3_synced.csv",
         "oldthread_sensorfiber_5x_4_synced.csv",
         "oldthread_sensorfiber_5x_5_synced.csv",
         "oldthread_sensorfiber_5x_6_synced.csv"]

""" for i,file in enumerate(files):
    df = pd.read_csv(os.path.join(dataPath,file), header=None)
    df["res_change"] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
    x = 30*df[1]/df[1].max() #scale to 30
    name = f"Sensor Fiber # {i}" if (i!=0) else f"Electroplated thread"

    #valleys /\,/\,/\,/\,/\
    valleys = df.index[(df[1].shift(1)>= df[1]) & (df[1]< df[1].shift(-1))].to_list()
    df["plot"] = False
    df.loc[valleys[-1]:, "plot"] = True
    plt.plot(x[df["plot"]],df[df["plot"]]["res_change"], color=palette[i], label=name) """

df = pd.read_csv(os.path.join(dataPath,files[4]), header=None)
df["res_change"] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
x = 30*df[1]/df[1].max() #scale to 30

#valleys /\,/\,/\,/\,/\
valleys = df.index[(df[1].shift(1)>= df[1]) & (df[1]< df[1].shift(-1))].to_list()
df["color"] = 0
df.loc[valleys[0]:valleys[1], "color"] = 1
df.loc[valleys[1]:valleys[2], "color"] = 2
df.loc[valleys[2]:valleys[3], "color"] = 3
df.loc[valleys[3]:, "color"] = 4
for c in df["color"].unique():
    cycle = df[df["color"] == c]
    plt.plot(x[cycle.index], cycle["res_change"], color=palette[c], label=f" cycle {c+1}")


# Plot design
plt.arrow(0,2,2.25,2,head_width=.5,length_includes_head=False)
plt.title("Sensor Fiber # 4")
plt.legend()
plt.xlabel("Strain (%)")
plt.ylabel("Percent Change in Resistance")
plt.grid()
plt.show()