from app.libs.utils.db_utils import patch_db, download_data, is_already_valid_data
from app.libs.utils.classes import Ticker


def generate_obv_signal(ticker: str) -> list:
    """Generate On Balance Value Signal

    Arguments:
        fund {pd.DataFrame} -- fund dataset

    Returns:
        list -- on balance volume signal for period of fund
    """
    ticker = Ticker(ticker=ticker)

    position = download_data(ticker)
    if is_already_valid_data(ticker, position, 'on_balance_volume'):
        return position['on_balance_volume']

    fund = position['ochl']

    obv = []
    obv.append(0.0)
    for i in range(1, len(fund['Close'])):
        if fund['Close'][i] > fund['Close'][i-1]:
            obv.append(obv[i-1] + fund['Volume'][i])
        elif fund['Close'][i] == fund['Close'][i-1]:
            obv.append(obv[i-1])
        else:
            obv.append(obv[i-1] - fund['Volume'][i])

    payload = {'signal': obv}
    patch_db(ticker, 'on_balance_volume', payload)

    return payload
