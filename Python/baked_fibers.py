import os
import pandas as pd
import matplotlib.pyplot as plt
dataPath = "Sensor fiber characterization/baked/"
palette = ["#E69F00", "#0072B2", "#F0E442", "#009E73", "#D55E00", "#56B4E9"]

files = ["baked_2_2025-03-23_22-08-40.csv",
         "baked_2-dmm-11.csv",
         "oldthread_baked_3_2025-03-24_11-00-10.csv",
         "baked_3-dmm-11.csv",
         "baked_4_2025-03-24_13-02-55.csv",
         "baked_4-dmm-11.csv"]

dmm_df = pd.read_csv(os.path.join(dataPath,files[1]))
dmm_df["Time"] = pd.to_timedelta(dmm_df["Time"])
start = dmm_df["Time"].min()
dmm_df["delta-t"] = dmm_df["Time"]- dmm_df["Time"].min()
print(dmm_df["delta-t"])
""" 


for i,file in enumerate(files):
    df = pd.read_csv(os.path.join(dataPath,file), header=None)

    df["res_change"] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
    x = 30*df[1]/df[1].max() #scale to 30
    name = f"Sensor Fiber # {i}" if (i!=0) else f"Electroplated thread"
    plt.plot(x,df["res_change"], color=palette[i], label=name)

# Plot design
plt.arrow(0,2,2.25,2,head_width=.5,length_includes_head=False)
plt.title("5x 30 Percent Strain (Baked)")
plt.legend()
plt.xlabel("Strain (%)")
plt.ylabel("Percent Change in Resistance")
plt.grid()
plt.show() """