# import wget
import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request

cmd = "wget https://raw.githubusercontent.com/HTuniv/CelsiusToFahrenheit/main/CtoF.csv"
sp.call(cmd, shell=True)



df = pd.read_csv("CtoF.csv")
clist = df['temperature_C'].to_list()
flist = []
for f in clist:
    f = (f * 1.8) + 32
    flist.append(round(f, 1))

# f = (c * 1.8) + 32

columns1 = ["temperature_F"]
df_f = pd.DataFrame(data=flist, columns=columns1)
df_edit = df.join(df_f)

def main():

    def TablePlot(df_edit,outputPath,w,h):
        df_edit["month"] = df_edit["month"].astype(str)
        df_edit["day"] = df_edit["day"].astype(str)
        fig, ax = plt.subplots(figsize=(w,h))
        ax.axis('off')
        ax.table(cellText=df_edit.values,
                colLabels=df_edit.columns,
                loc='center',
                bbox=[0,0,1,1])
        plt.savefig(outputPath)

    TablePlot(df_edit,"result.png",10,10)

if __name__ == "__main__":
    main()