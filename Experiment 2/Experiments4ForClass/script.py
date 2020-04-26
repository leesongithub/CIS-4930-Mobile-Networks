import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(
    r'outputwireless-logs-20120409.DHCP_ANON.csv')['endTime'].subtract(1333929823)
fig, axs = plt.subplots(ncols=3, nrows=2)
timeFrames = [15, 1, 5, 10, 30, 60]
for time in timeFrames:
    bins = 86606 / (time * 60)
    fig.add_subplot(pd.DataFrame.hist(df, bins=bins))
plt.show()
#
# fig.add_subplot(df.hist(bins=97))  # 15min
# fig.add_subplot(df.hist(bins=1444))  # 1min
# fig.add_subplot(df.hist(bins=289))  # 5min
# fig.add_subplot(df.hist(bins=144))  # 10min
# fig.add_subplot(df.hist(bins=49))  # 30min
# fig.add_subplot(df.hist(bins=24))  # 60min
# fig.tight_layout()
 
# plt.show()
 
df.plot.hist(bins=97)
plt.show()
