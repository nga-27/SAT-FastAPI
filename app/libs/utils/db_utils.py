import os
import json
import datetime

import yfinance as yf

from app import main
from .classes import Ticker


def download_data(ticker: Ticker):
    if ticker.ticker.upper() in main.DB:
        content = main.DB[ticker.ticker.upper()]
        if content.get('date') is not None:
            date = datetime.datetime.strptime(content['date'], "%Y%m%d")
            now = datetime.datetime.now().strftime("%Y%m%d")
            now = datetime.datetime.strptime(now, "%Y%m%d")
            if now <= date:
                print(
                    f"{ticker.ticker.upper()} already valid in DB, passing queued data.")
                return main.DB[ticker.ticker.upper()]

    pddata = yf.download(tickers=ticker.ticker,
                         period=ticker.period, interval=ticker.interval)
    data = {x: list(pddata[x]) for x in pddata.columns}
    data['dates'] = [x.strftime("%Y-%m-%d") for x in pddata.index]
    main.DB[ticker.ticker.upper()] = {
        "ochl": data, "date": datetime.datetime.now().strftime("%Y%m%d")}
    update_db(main.DB)
    return main.DB[ticker.ticker.upper()]


def update_db(db_obj):
    with open(main.DB_PATH, 'w') as dbf:
        json.dump(db_obj, dbf)
        dbf.close()
    return


def patch_db(ticker: Ticker, new_key: str, new_data):
    main.DB[ticker.ticker.upper()][new_key] = new_data
    update_db(main.DB)
    return


def is_already_valid_data(ticker: Ticker, position: dict, key: str, **kwargs) -> bool:
    period = kwargs.get('period')
    filter_type = kwargs.get('filter_type')
    weight_strength = kwargs.get('weight_strength')
    special_case = all([period, filter_type, weight_strength])

    if key in position:
        if special_case:
            if not isinstance(position[key], list) and \
                    period == position[key].get('period', 0) and \
                    filter_type == position[key].get('subFilter', "simple") and \
                    weight_strength == position[key].get('weight_strength', 2.0):
                print(
                    f"'{key}' already in DB for {ticker.ticker}, passing queued data.")
                return True
        elif period is None:
            if not isinstance(position[key], list):
                print(
                    f"'{key}' already in DB for {ticker.ticker}, passing queued data.")
                return True
        else:
            if not isinstance(position[key], list) and period == position[key].get('period', 0):
                print(
                    f"'{key}' already in DB for {ticker.ticker}, passing queued data.")
                return True
    return False
