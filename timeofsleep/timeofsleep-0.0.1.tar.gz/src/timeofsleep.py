import pandas as pd
import sys,os
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
df = pd.read_csv("https://raw.githubusercontent.com/kyohei-2022029/timeofsleep/7e82540a540f3bab379e5fa1bb1559664337f603/data/sleepdata.csv", sep=';', header=0, encoding='utf-8')


df = df.drop(["Wake up","Sleep Notes", "Heart rate"], axis=1)
# 正規表現で部分一致置換
df["Time in bed"] = df["Time in bed"].replace(":", ".", regex=True)
df["Sleep quality"] = df["Sleep quality"].replace("%", "", regex=True)

# キャスト
df["Time in bed"] = df["Time in bed"].astype(float)
df["Sleep quality"] = df["Sleep quality"].astype(int)

    

x = df["Time in bed"]
y = df["Sleep quality"]

fig = plt.figure(figsize=(12,4))


ax = fig.add_subplot(1,1,1)

ax.grid(which = "both", axis="y")
ax.grid(axis="x")
ax.scatter(x,y)

ax.set_title('Hourly sleep quality [%]')
ax.set_xlabel('time of sleeping [h]')
ax.set_ylabel('Sleep quality')

ax.set_xlim(0, df["Time in bed"].max())
ax.set_xticks([0, 5, 6, 7, 8, 9, 10, 11])


fig.show()

def main():
    fig.savefig('timeofsleep.jpg')
    
main()