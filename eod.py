import os
import requests
import pandas as pd
from io import StringIO
from _utils import (_init_session, _format_date,
                     _sanitize_dates, _url, RemoteDataError)

EOD_HISTORICAL_DATA_API_KEY_ENV_VAR = "EOD_HISTORICAL_API_KEY"
EOD_HISTORICAL_DATA_API_KEY_DEFAULT = "60217faa3e5ac5.45616162"
EOD_HISTORICAL_DATA_API_URL = "https://eodhistoricaldata.com/api"


def get_api_key(env_var=EOD_HISTORICAL_DATA_API_KEY_ENV_VAR):
    """
    Returns API key from environment variable
    API key must have been set previously
    bash> export EOD_HISTORICAL_API_KEY="YOURAPI"
    Returns default API key, if environment variable is not found
    """
    return os.environ.get(env_var, EOD_HISTORICAL_DATA_API_KEY_DEFAULT)


def get_exchange_symbols(exchange_code,
                         api_key=EOD_HISTORICAL_DATA_API_KEY_DEFAULT,
                         session=None):
    """
    Returns list of symbols for a given exchange
    """
    session = _init_session(session)
    endpoint = "/exchanges/{exchange_code}".format(exchange_code=exchange_code)
    url = EOD_HISTORICAL_DATA_API_URL + endpoint
    params = {
        "api_token": api_key
    }
    r = session.get(url, params=params)
    if r.status_code == requests.codes.ok:
        df = pd.read_csv(StringIO(r.text), skipfooter=1, index_col=0)
        return df
    else:
        params["api_token"] = "YOUR_HIDDEN_API"
        raise RemoteDataError(r.status_code, r.reason, _url(url, params))


def get_exchanges():
    """
    Returns list of exchanges
    https://eodhistoricaldata.com/knowledgebase/list-supported-exchanges/
    """
    data = """ID	Exchange Name	Exchange Code
1	Munich Exchange	MU
2	Berlin Exchange	BE
3	Frankfurt Exchange	F
4	Stuttgart Exchange	STU
5	Mexican Exchange	MX
6	Hanover Exchange	HA
8	Australian Exchange	AU
9	Singapore Exchange	SG
10	Indexes	INDX
11	USA Stocks	US
12	Kuala Lumpur Exchange	KLSE
13	Funds	FUND
14	Bombay Exchange	BSE
15	Dusseldorf Exchange	DU
16	London Exchange	LSE
17	Euronext Paris	PA
18	XETRA Exchange	XETRA
19	NSE (India)	NSE
20	Hong Kong Exchange	HK
21	Borsa Italiana	MI
22	SIX Swiss Exchange	SW
23	Hamburg Exchange	HM
24	Toronto Exchange	TO
25	Stockholm Exchange	ST
26	Oslo Stock Exchange	OL
27	Euronext Amsterdam	AS
28	Coppenhagen Exchange	CO
29	Euronext Lisbon	LS
30	Korea Stock Exchange	KO
31	Shanghai Exchange	SS
32	Taiwan Exchange	TW
33	Sao Paolo Exchange	SA
34	Euronext Brussels	BR
35	Madrid Exchange	MC
36	Vienna Exchange	VI
37	New Zealand Exchange	NZ
38	FOREX	FX
39	London IL	IL
40	Irish Exchange	IR
41	MICEX Russia	MCX
42	OTC Market	OTC
43	ETF-Euronext	NX
44	Johannesburg Exchange	JSE"""
    df = pd.read_csv(StringIO(data), sep="\t")
    df = df.set_index("ID")
    return(df)
api_key = get_api_key(env_var=EOD_HISTORICAL_DATA_API_KEY_ENV_VAR)
us_stocks = get_exchange_symbols("US", api_key)

all_usd = os.path.join('data', 'all_usd.csv')
us_stocks.to_csv(all_usd)
# remove etfs and funds