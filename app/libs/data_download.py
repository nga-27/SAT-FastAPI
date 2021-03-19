import os
import json
import datetime

import yfinance as yf

from app import main
from .classes import Ticker


def download_data(ticker: Ticker):
    if ticker.ticker in main.DB:
        content = main.DB[ticker.ticker]
        if content.get('date') is not None:
            date = datetime.datetime.strptime(content['date'], "%Y%m%d")
            now = datetime.datetime.now().strftime("%Y%m%d")
            now = datetime.datetime.strptime(now, "%Y%m%d")
            if now <= date:
                print(f"{ticker.ticker} already valid in DB, passing queued data.")
                return main.DB[ticker.ticker]

    pddata = yf.download(tickers=ticker.ticker,
                         period=ticker.period, interval=ticker.interval)
    data = {x: list(pddata[x]) for x in pddata.columns}
    main.DB[ticker.ticker] = {
        "data": data, "date": datetime.datetime.now().strftime("%Y%m%d")}
    update_db(main.DB)
    return data


def update_db(db_obj):
    with open(main.DB_PATH, 'w') as dbf:
        json.dump(db_obj, dbf)
        dbf.close()
    return
