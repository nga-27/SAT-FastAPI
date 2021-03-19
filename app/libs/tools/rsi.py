import numpy as np

from app.libs.utils.classes import Ticker
from app.libs.utils.db_utils import download_data, patch_db


def generate_rsi_signal(ticker: str, **kwargs) -> list:
    """Generate RSI Signal

    Arguments:
        position {pd.DataFrame}

    Keyword Arguments:
        period {int} -- (default: {14})
        p_bar {ProgressBar} -- (default: {None})

    Returns:
        list -- RSI signal
    """
    period = kwargs.get('period', 14)
    p_bar = kwargs.get('p_bar')

    if period is None:
        period = 14
    ticker = Ticker(ticker=ticker)

    position = download_data(ticker)
    if 'rsi' in position:
        if not isinstance(position['rsi'], list) and period == position['rsi'].get('period', 0):
            print(
                f"'RSI' already in DB for {ticker.ticker}, passing queued data.")
            return position['rsi']

    position = position['ochl']

    PERIOD = period
    change = []
    change.append(0.0)
    for i in range(1, len(position['Close'])):
        per = (position['Close'][i] - position['Close']
               [i-1]) / position['Close'][i-1] * 100.0
        change.append(np.round(per, 6))

    RSI = []
    # gains, losses, rs
    RS = []

    for i in range(0, PERIOD):
        RSI.append(50.0)
        RS.append([0.0, 0.0, 1.0])

    # Calculate RS for all future points
    for i in range(PERIOD, len(change)):
        pos = 0.0
        neg = 0.0
        for j in range(i-PERIOD, i):
            if change[j] > 0.0:
                pos += change[j]
            else:
                neg += np.abs(change[j])

        if i == PERIOD:
            if neg == 0.0:
                rs = float('inf')
            else:
                rs = np.round(pos / neg, 6)
            RS.append([np.round(pos/float(PERIOD), 6),
                       np.round(neg/float(PERIOD), 6), rs])
        else:
            if change[i] > 0.0:
                if RS[i-1][1] == 0.0:
                    rs = float('inf')
                else:
                    rs = (((RS[i-1][0] * float(PERIOD-1)) + change[i]) / float(PERIOD)
                          ) / (((RS[i-1][1] * float(PERIOD-1)) + 0.0) / float(PERIOD))
            else:
                if RS[i-1][1] == 0.0:
                    rs = float('inf')
                else:
                    rs = (((RS[i-1][0] * float(PERIOD-1)) + 0.00) / float(PERIOD)) / \
                        (((RS[i-1][1] * float(PERIOD-1)) +
                          np.abs(change[i])) / float(PERIOD))

            RS.append([np.round(pos/float(PERIOD), 6),
                       np.round(neg/float(PERIOD), 6), rs])

        rsi = 100.0 - (100.0 / (1.0 + RS[i][2]))
        RSI.append(np.round(rsi, 6))

    payload = {'period': period, 'signal': RSI}
    patch_db(ticker, 'rsi', payload)

    return payload
