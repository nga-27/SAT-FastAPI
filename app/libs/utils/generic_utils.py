import datetime

import pandas as pd
import numpy as np


INDEXES = {
    "^GSPC": "S&P500",
    "^IRX": "3MO-TBILL"
}

INDEX_TO_TICKER = {
    "S&P500": "^GSPC",
    "SP500": "^GSPC",
    "GSPC": "^GSPC",
    "TBILL": "^IRX",
    "3MO-TBILL": "^IRX",
    "T-BILL": "^IRX"
}


def date_extractor(date, _format=None):
    """Date Extractor

    Converts a date object into either a string date ('%Y-%m-%d'), an iso-format datetime object,
    or a normal datetime object.

    Arguments:
        date {datetime} -- datetime object, typically

    Keyword Arguments:
        _format {str} -- either 'str' or 'iso' to control output format (default: {None})

    Returns:
        str, datetime -- either a string or datetime object
    """
    date = str(date)
    date1 = date.split(' ')[0]
    date2 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    if _format == 'str':
        dateX = date1
    elif _format == 'iso':
        dateX = date2.isoformat()
    else:
        dateX = date2
    return dateX


def date_extractor_list(df: pd.DataFrame) -> list:
    """Dates Extractor to List

    Arguments:
        df {pd.DataFrame, list} -- dataframe with dates as the 'index'

    Returns:
        list -- list of dates separated '%Y-%m-%d' or indexes (for a list)
    """
    dates = []
    if type(df) == list:
        for i in range(len(df)):
            dates.append(i)

    else:
        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)
            df = df.set_index('dates')
        for i in range(len(df.index)):
            date = str(df.index[i])
            date = date.split(' ')[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            dates.append(date)

    return dates


def index_map_to_ticker(ticker: str):
    return INDEX_TO_TICKER.get(ticker, ticker)


def index_map_to_db(ticker_name: str):
    return INDEXES.get(ticker_name, ticker_name)
