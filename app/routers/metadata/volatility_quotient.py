import os
import json
import pprint
import requests

VQ_API_BASE_URL = "https://sts.tradesmith.com/api/StsApiService/"
VQ_VALUES_PARAM = "get-sts-values/"
VQ_LOOKUP_PARAM = "search-symbol/"
VQ_DEEP_ANALYSIS_PARAM = "get-tmc-data/"

TRADESTOPS_URL = "https://tradestops.com/investment-calculator/"


def get_volatility(ticker_str: str, **kwargs) -> dict:
    """Get Volatility

    Arguments:
        ticker_str {str} -- ticker of fund

    Optional Args:
        max_close {float} -- highest close of a fund recently (default: {None})
        data {pd.DataFrame} -- fund dataset (default: {None})

    Returns:
        dict -- volatility quotient data object
    """
    max_close = kwargs.get('max_close', None)
    dataset = kwargs.get('data')

    TIMEOUT = 5
    is_SP500 = False
    vq = {}

    json_path = ''
    if os.path.exists('core.json'):
        json_path = 'core.json'
    elif os.path.exists('test.json'):
        json_path = 'test.json'

    if os.path.exists(json_path):
        with open(json_path) as json_file:
            core = json.load(json_file)
            key = core.get("Keys", {}).get("Volatility_Quotient", "")
            ticker_str = ticker_str.upper()

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
                    now = datetime.now()
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

            return vq

    return vq
