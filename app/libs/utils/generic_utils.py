import datetime


INDEXES = {
    "^GSPC": "S&P500",
    "^IRX": "3MO-TBILL"
}

SP500_TO_TICKER = {
    "S&P500": "^GSPC",
    "SP500": "^GSPC"
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


def sp500_map_to_ticker(ticker: str):
    return SP500_TO_TICKER.get(ticker, ticker)


def sp500_map_to_db(ticker_name: str):
    return INDEXES.get(ticker_name, ticker_name)
