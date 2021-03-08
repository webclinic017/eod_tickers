from cad_tickers.exchanges.tsx.get_tickers import get_all_tickers_data   
import pandas as pd
# TOCO read data file and produce another csv that contains this graphql ticker data

data_csv = pd.read_csv("data/us.csv")


def get_tmx_name(code, ex):
    # print(code, ex)
    return f"{code}:US"
    # map data from us tickers to something useful

data_csv = data_csv.dropna(subset=['Exchange'])
data_csv['tmx_name'] = data_csv.apply(lambda x: get_tmx_name(x["Code"], x["Exchange"]), axis=1)

us_stocks = data_csv["tmx_name"].tolist()


stock_df = get_all_tickers_data(us_stocks)

stock_df.to_csv("stock_df.csv")