from cad_tickers.exchanges.tsx.get_ticker_data import get_ticker_data   
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
import json
from tqdm import tqdm
from _utils import tickers_to_skip

max_iterations = 50
# read data.db.json
with open('data/db.json') as f:
    database = json.load(f)

# TOCO read data file and produce another csv that contains this graphql ticker data

data_csv = pd.read_csv("data/us.csv")


def get_tmx_name(code, ex):
    # print(code, ex)
    return f"{code}:US"
    # map data from us tickers to something useful

total_rows = len(data_csv)
print(total_rows)
# data_csv = data_csv.dropna(subset=['Exchange'])
data_csv['tmx_name'] = data_csv.apply(lambda x: get_tmx_name(x["Code"], x["Exchange"]), axis=1)

us_stocks = data_csv["tmx_name"].tolist()
iteration = database["iteration"] + 10
# seems to start timing out around 50 tries
split_amount = total_rows // max_iterations
# split us_stocks into chunks of total_rows / 25
# get iteration by split_amount * iteration from slicing us_stocks
split_stocks = [us_stocks[i:i + split_amount] for i in range(0, len(us_stocks), split_amount)]
split_stocks = split_stocks[iteration]
def get_data(symbol=str):
    time.sleep(0.2)
    return get_ticker_data(symbol)
missed_tickers = []
ticker_data = []

def get_data(stock: str):
    ticker_info = get_ticker_data(stock)
    time.sleep(1)
    if ticker_info == None:
        print("FAILED TO GET DATA FOR: ", stock)
        missed_tickers.append(stock)
        pass
        # ticker_info = get_ticker_data(stock)
    else:
        ticker_data.append(ticker_info)

for stock in tqdm(split_stocks):
    # skip tickers_to_skip
    if stock in tickers_to_skip:
        continue
    try:
       get_data(stock)
    except Exception as e:
        print(e)
        print("FAILED TO GET DATA FOR: ", stock)
        missed_tickers.append(stock)
        time.sleep(60)
        try:
            get_data(stock)
        except Exception as e:
            print(e)

# using list comprehension
# to remove None values in list
ticker_data = [i for i in ticker_data if i]

ticker_df = pd.DataFrame(ticker_data)

# grab old ticker data from data/us_stock_data.csv 
# and merge with ticker_df
old_ticker_df = pd.read_csv("data/us_stock_data.csv")
ticker_df = pd.concat([old_ticker_df, ticker_df])
# remove duplicates in ticker_df
ticker_df = ticker_df.drop_duplicates(subset=['symbol'])
# sort ticker_df by symbol
ticker_df = ticker_df.sort_values(by=['symbol'])
ticker_df.to_csv("data/us_stock_data.csv")
# save missed tickers to data/us_stock_data_missed.txt 
with open("data/us_stock_data_missed.txt", "w") as f:
    for ticker in missed_tickers:
        f.write('"'+ ticker + '"' + ",\n")

database["iteration"] = database["iteration"] + 1
if database["iteration"] >= 50:
    database["iteration"] = 0
# write to data/db.json
with open('data/db.json', 'w') as f:
    json.dump(database, f)
