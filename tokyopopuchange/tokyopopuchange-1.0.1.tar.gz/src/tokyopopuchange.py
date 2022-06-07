import pandas as pd
import matplotlib.pyplot as plt
import sys,os


if os.path.exists("tokyo_population.csv"):
  df=pd.read_csv("tokyo_population.csv",encoding="shift-jis")
else:
  print("You need to download csv from the following site:")
  print("https://www.city.inagi.tokyo.jp/shisei/gyosei/opendata/opendata_catalogpage/zinkou.files/010.csv")


def main():
  data = df["年次"]
  y_data = df["人口総数（人）"]
  
  plt.plot(data, y_data, marker="o")

if __name__ == "__main__":
  main()