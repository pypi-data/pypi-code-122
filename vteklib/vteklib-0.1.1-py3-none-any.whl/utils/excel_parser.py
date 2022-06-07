import numpy as np
import pandas
import pandas as pd


class ExcelFile:
    def __init__(self, excel_fp: str):
        self.df = pandas.read_excel(excel_fp)
        self.df = pandas.read_excel('/Users/new/PycharmProjects/vteklib/219.xlsx')
        self.series = dict()
        for col in self.df.columns:
            name = col
            vals = []
            pt = 0
            curr = self.df[col][pt]
            while not pd.isna(curr) or type(curr) == str:
                vals.append(curr)
                pt += 1
                curr = self.df[col][pt]
            if vals:
                self.series[name] = vals

# every excel table contains some columns and its names, so the main issue is to parse all data in table into some
# pandas Series objs with proper names, and then create a Plot data objs of them (in some way)


if __name__ == '__main__':
    ef = ExcelFile('/Users/new/PycharmProjects/vteklib/219.xlsx')
