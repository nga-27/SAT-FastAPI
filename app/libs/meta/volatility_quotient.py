import requests
import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np

from app.libs.utils.classes import Ticker
from app.libs.utils.db_utils import download_data, patch_db, is_already_valid_data
from app.libs.utils.generic_utils import sp500_map_to_ticker, sp500_map_to_db


VQ_API_BASE_URL = "https://sts.tradesmith.com/api/StsApiService/"
VQ_VALUES_PARAM = "get-sts-values/"
VQ_LOOKUP_PARAM = "search-symbol/"
VQ_DEEP_ANALYSIS_PARAM = "get-tmc-data/"

TRADESTOPS_URL = "https://tradestops.com/investment-calculator/"


def get_volatility(ticker_str: str, vq_key: str, **kwargs) -> dict:
    """Get Volatility

    Arguments:
        ticker_str {str} -- ticker of fund

    Optional Args:
        max_close {float} -- highest close of a fund recently (default: {None})
        data {pd.DataFrame} -- fund dataset (default: {None})

    Returns:
        dict -- volatility quotient data object
    """
    # max_close = kwargs.get('max_close', None)
    # dataset = kwargs.get('data')

    ticker = Ticker(ticker=ticker_str)

    position = download_data(ticker)
    if is_already_valid_data(ticker, position, 'vq'):
        return position['vq']

    dataset = position['ochl']
    max_close = max(position['ochl']['Close'])

    TIMEOUT = 5
    is_SP500 = False
    vq = {}

    key = vq_key

    ticker_str = sp500_map_to_ticker(ticker_str)
    if ticker_str == '^GSPC':
        ticker_str = 'SPY'
        is_SP500 = True

    url = f"{VQ_API_BASE_URL}{VQ_VALUES_PARAM}{key}/{ticker_str}"

    try:
        response = requests.get(url, timeout=TIMEOUT)
    except:
        print(
            f"{WARNING}Exception: VQ Server failed to respond on initial VQ inquiry. " +
            f"No data returned.{NORMAL}\r\n")
        return vq

    try:
        r = response.json()
    except:
        r = {}

    if response.status_code != 200:
        print("")
        print(f"{WARNING}Volatility Quotient failed on {ticker_str} request: " +
              f"'{r.get('ErrorMessage', 'Failure.')}'. Check valid key.{NORMAL}\r\n")
        print("")
        return vq

    r = response.json()

    vq = {"VQ": r.get("StsPercentValue", ""), "stop_loss": r.get(
        "StopPriceLong", ""), "latest_price": r.get("LatestClose")}
    vq['last_max'] = r.get('LastMax')
    if vq['last_max'] is None:
        vq['last_max'] = {"Date": "n/a", "Price": "n/a"}

    if is_SP500 and max_close is not None:
        max_close = np.round(max_close, 2)
        if vq.get('last_max', {}).get('Price') is not None:
            # Adjust for converting back from SPY to ^GSPC
            multiplier = max_close / vq['last_max']['Price']
            vq['latest_price'] = vq['latest_price'] * multiplier

        vq['last_max'] = {"Date": "n/a", "Price": max_close}
        ratio = (100.0 - vq['VQ']) / 100.0
        vq['stop_loss'] = np.round(ratio * vq['last_max']['Price'], 2)

    url = f"{VQ_API_BASE_URL}{VQ_LOOKUP_PARAM}{key}/{ticker_str}/20"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except:
        print(
            f"{WARNING}Exception: VQ Server failed to respond for ticker lookup. " +
            f"No data returned.{NORMAL}\r\n")
        return vq

    r = response.json()
    if response.status_code == 200:
        val = None
        for tick in r.get('Symbols', []):
            if tick['Symbol'] == ticker_str:
                val = tick["SymbolId"]
                break

        if val is not None:
            now = datetime.datetime.now()
            start = now - relativedelta(years=10)
            start_str = start.strftime('%Y-%m-%d')
            now_str = now.strftime('%Y-%m-%d')

            url = \
                f"{VQ_API_BASE_URL}{VQ_DEEP_ANALYSIS_PARAM}{key}/{val}/{start_str}/{now_str}"
            try:
                response = requests.get(url, timeout=TIMEOUT)
            except:
                print(
                    f"{WARNING}Exception: VQ Server failed to respond for deep analysis. " +
                    f"No data returned.{NORMAL}\r\n")
                return vq

            r = response.json()
            if response.status_code == 200:
                vq['analysis'] = r

            vq['stopped_out'] = vq_stop_out_check(dataset, vq)
            status, color, _ = vq_status_print(vq, ticker_str)
            vq['status'] = {'status': status, 'color': color}

    payload = {'signal': vq}
    patch_db(ticker, 'vq', payload)

    return vq


def vq_stop_out_check(dataset: pd.DataFrame, vq_obj: dict) -> str:
    """VQ Stop Out Check

    Arguments:
        dataset {pd.DataFrame} -- fund dataset
        vq_obj {dict} -- volatility quotient object

    Returns:
        str -- 'OK' or 'Stopped Out' (or 'n/a') status
    """
    stop_loss = vq_obj.get('stop_loss', 'n/a')
    max_date = vq_obj.get('last_max', {}).get('Date')

    if isinstance(dataset, dict):
        dataset = pd.DataFrame.from_dict(dataset)
        dataset = dataset.set_index('dates')
        dataset.index = pd.to_datetime(dataset.index)

    if (max_date == 'n/a') or (stop_loss == 'n/a') or dataset is None:
        return 'n/a'

    max_date = datetime.datetime.strptime(max_date, '%m/%d/%Y')
    for i in range(len(dataset['Close'])-1, -1, -1):
        if dataset.index[i] < max_date:
            return 'OK'
        if dataset['Close'][i] < stop_loss:
            return 'Stopped Out'
    return 'OK'


def vq_status_print(vq: dict, fund: str) -> list:
    """VQ Status Print

    Arguments:
        vq {dict} -- volatility quotient data object
        fund {str} -- fund name

    Returns:
        list -- status message, status color, and % away from highest close
    """
    if not vq:
        return

    last_max = vq.get('last_max', {}).get('Price')
    stop_loss = vq.get('stop_loss')
    latest = vq.get('latest_price')
    stop_status = vq.get('stopped_out')

    mid_pt = (last_max + stop_loss) / 2.0
    amt_latest = latest - stop_loss
    amt_max = last_max - stop_loss
    percent = np.round(amt_latest / amt_max * 100.0, 2)

    if stop_status == 'Stopped Out':
        status_color = 'red'
        status_message = "AVOID - Stopped Out"
    elif latest < stop_loss:
        status_color = 'red'
        status_message = "AVOID - Stopped Out"
    elif latest < mid_pt:
        status_color = 'yellow'
        status_message = "CAUTION - Hold"
    else:
        status_color = 'green'
        status_message = "GOOD - Buy / Maintain"

    return status_message, status_color, percent
