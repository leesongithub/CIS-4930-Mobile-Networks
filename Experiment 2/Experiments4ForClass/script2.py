import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(
    r'outputwireless-logs-20120407.DHCP_ANON.csv')['endTime'].subtract(1333929823)

#fig, ax = plt.subplots(ncols=6, nrows=1)
timeFrames = [15, 1, 5, 10, 30, 60]
for index, time in enumerate(timeFrames):
    binAmt = 86238 // (time * 60)
    heights, bins = np.histogram(df, bins=binAmt)
    fig = plt.figure()
    plt.bar(bins[:-1], heights, width=bins[1] - bins[0])
    ax = plt.gca()
    ax.set_title(str(time) + ' minute(s)')
    if time >= 30:
        rects = ax.patches
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 5, height,
                    ha='center', va='bottom')
    plt.savefig('plt' + str(index))