import os
import pandas as pd 


all_usd = os.path.join('data', 'all_usd.csv')
all_usd_stocks = os.path.join('data', 'us.csv')
all_usd_df = pd.read_csv(all_usd)

tickers =  all_usd_df[~all_usd_df['Type'].isin(['ETF', 'FUND', 'Fund', 'Mutual Fund', 'BOND'])]
tickers.to_csv(all_usd_stocks)
