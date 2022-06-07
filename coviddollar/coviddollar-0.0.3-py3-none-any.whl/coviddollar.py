# import library
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import subprocess as sp

sp.call("wget https://www.mizuhobank.co.jp/market/csv/quote.csv",shell=True)
print('quote.csv downloaded!')
# sp.call("cat quote.csv|sed '2,$s/,-/,/g' >new",shell=True)
# sp.call("mv new quote.csv",shell=True)
exchange = pd.read_csv('./quote.csv', encoding='shift-jis', header=2)
exchange_dollar = exchange.iloc[:, :2]
exchange_dollar.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
sp.call("rm quote.csv",shell=True)

sp.call('wget https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv', shell=True)
covid = pd.read_csv('./newly_confirmed_cases_daily.csv')
covid_total = covid.iloc[:, :2]
covid_total.rename(columns={'ALL': 'number of New-positive'}, inplace=True)
sp.call('rm newly_confirmed_cases_daily.csv', shell=True)
print('newly_confirmed_cases_daily.csv downloaded!')
covid_exchange = pd.merge(covid_total, exchange_dollar, how='inner', on='Date')

class main:
    def main(self, days=100):
        date = covid_exchange.iloc[days*-1:,0].values.tolist()
        positive = covid_exchange.iloc[days*-1:,1].values.tolist()
        usd = covid_exchange.iloc[days*-1:,2].values.tolist()
        
        if days >= 50:
            date = date[::5]
            positive = positive[::5]
            usd = usd[::5]
        fig, ax1 = plt.subplots(1,1, figsize=(15,8), facecolor='w')
        ax2 = ax1.twinx()
        ax1.bar(date, positive ,color="lightblue",label="number of New-positive(covid-19)")
        ax2.plot(usd, linestyle="solid", color="k", marker="^", label="us_dollar-to-yen")
        ax2.set_ylim(100, 140)
        fig.autofmt_xdate(rotation=45)
        ax2.set_title(f'covid-19/exchange(dollar-to-yen){days}-days')
        handler1, label1 = ax1.get_legend_handles_labels()
        handler2, label2 = ax2.get_legend_handles_labels()
        ax1.legend(handler1+handler2,label1+label2,borderaxespad=0)
        # ax1.grid(True)
        fig.tight_layout()
        fig.show()
        # now = datetime.datetime.now()
        # filename = './output/log_' + now.strftime('%Y%m%d_%H%M%S') + '.png'
        fig.savefig('./result.png', dpi=200)
days=100    
m = main()
m.main(days=days)