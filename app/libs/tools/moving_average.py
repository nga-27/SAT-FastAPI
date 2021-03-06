import numpy as np

from app.libs.utils.db_utils import patch_db, download_data, is_already_valid_data
from app.libs.utils.classes import Ticker


def simple_moving_avg(ticker: str, **kwargs) -> list:
    """Simple Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to windowed moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})

    Returns:
        list -- filtered data
    """
    period = kwargs.get('period', 7)

    if period is None or period == 0:
        period = 7
    ticker = Ticker(ticker=ticker)

    position = download_data(ticker)
    if is_already_valid_data(ticker, position, 'simple_moving_average', period=period):
        return position['simple_moving_average']

    position = position['ochl']
    interval = period

    data = position['Close']

    ma = []
    for i in range(interval-1):
        ma.append(data[i])
    for i in range(interval-1, len(data)):
        av = np.mean(data[i-(interval-1):i+1])
        ma.append(av)

    payload = {'period': interval, 'signal': ma}
    patch_db(ticker, 'simple_moving_average', payload)

    return payload


def simple_moving_avg_generic(dataset, interval: int, **kwargs) -> list:
    """Simple Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to windowed moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})

    Returns:
        list -- filtered data
    """
    data_type = kwargs.get('data_type', 'DataFrame')
    key = kwargs.get('key', 'Close')

    if data_type == 'DataFrame':
        data = list(dataset[key])
    else:
        data = dataset

    ma = []
    for i in range(interval-1):
        ma.append(data[i])
    for i in range(interval-1, len(data)):
        av = np.mean(data[i-(interval-1):i+1])
        ma.append(av)

    return ma


def exponential_moving_avg(ticker: str, **kwargs) -> list:
    """Exponential Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to exponential moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})

    Returns:
        list -- filtered data
    """
    period = kwargs.get('period', 7)

    if period is None or period == 0:
        period = 7
    ticker = Ticker(ticker=ticker)

    position = download_data(ticker)
    if is_already_valid_data(ticker, position, 'exponential_moving_average', period=period):
        return position['exponential_moving_average']

    position = position['ochl']
    interval = period

    data = position['Close']

    ema = []
    k = 2.0 / (float(interval) + 1.0)
    for i in range(interval-1):
        ema.append(data[i])
    for i in range(interval-1, len(data)):
        ema.append(np.mean(data[i-(interval-1):i+1]))
        if i != interval-1:
            ema[i] = ema[i-1] * (1.0 - k) + data[i] * k

    payload = {'period': interval, 'signal': ema}
    patch_db(ticker, 'exponential_moving_average', payload)

    return payload


def exponential_moving_avg_generic(dataset, interval: int, **kwargs) -> list:
    """Exponential Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to exponential moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})

    Returns:
        list -- filtered data
    """
    data_type = kwargs.get('data_type', 'DataFrame')
    key = kwargs.get('key', 'Close')

    if data_type == 'DataFrame':
        data = list(dataset[key])
    else:
        data = dataset

    ema = []
    k = 2.0 / (float(interval) + 1.0)
    for i in range(interval-1):
        ema.append(data[i])
    for i in range(interval-1, len(data)):
        ema.append(np.mean(data[i-(interval-1):i+1]))
        if i != interval-1:
            ema[i] = ema[i-1] * (1.0 - k) + data[i] * k

    return ema


def windowed_moving_avg(ticker: str, **kwargs) -> list:
    """Windowed Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to windowed moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})
        filter_type {str} -- either 'simple' or 'exponential' (default: {'simple'})
        weight_strength {float} -- numerator for ema weight (default: {2.0})

    Returns:
        list -- filtered data
    """
    period = kwargs.get('period', 7)

    if period is None or period == 0:
        period = 7
    ticker = Ticker(ticker=ticker)

    filter_type = kwargs.get('filter_type', 'simple')
    weight_strength = kwargs.get('weight_strength', 2.0)

    position = download_data(ticker)
    if is_already_valid_data(ticker, position, 'windowed_moving_average',
                             period=period, filter_type=filter_type, weight_strength=weight_strength):
        return position['windowed_moving_average']

    position = position['ochl']
    interval = period

    data = position['Close']

    wma = []

    if filter_type == 'simple':
        left = int(np.floor(float(interval) / 2))
        if left == 0:
            return data
        for i in range(left):
            wma.append(data[i])
        for i in range(left, len(data)-left):
            wma.append(np.mean(data[i-(left):i+(left)]))
        for i in range(len(data)-left, len(data)):
            wma.append(data[i])

    elif filter_type == 'exponential':
        left = int(np.floor(float(interval) / 2))
        weight = weight_strength / (float(interval) + 1.0)
        if weight > 1.0:
            weight = 1.0
        for i in range(left):
            wma.append(data[i])
        for i in range(left, len(data)-left):
            sum_len = len(data[i-(left):i+(left)]) - 1
            sum_vals = np.sum(data[i-(left):i+(left)])
            sum_vals -= data[i]
            sum_vals = sum_vals / float(sum_len)
            sum_vals = data[i] * weight + sum_vals * (1.0 - weight)
            wma.append(sum_vals)
        for i in range(len(data)-left, len(data)):
            wma.append(data[i])

    payload = {'period': interval, 'signal': wma,
               'weight_strength': weight_strength, 'subFilter': filter_type}
    patch_db(ticker, 'windowed_moving_average', payload)

    return payload


def windowed_moving_avg_generic(dataset, interval: int, **kwargs) -> list:
    """Windowed Moving Average

    Arguments:
        dataset -- tabular data, either list or pd.DataFrame
        interval {int} -- window to windowed moving average

    Optional Args:
        data_type {str} -- either 'DataFrame' or 'list' (default: {'DataFrame'})
        key {str} -- column key (if type 'DataFrame'); (default: {'Close'})
        filter_type {str} -- either 'simple' or 'exponential' (default: {'simple'})
        weight_strength {float} -- numerator for ema weight (default: {2.0})

    Returns:
        list -- filtered data
    """
    data_type = kwargs.get('data_type', 'DataFrame')
    key = kwargs.get('key', 'Close')
    filter_type = kwargs.get('filter_type', 'simple')
    weight_strength = kwargs.get('weight_strength', 2.0)

    if data_type == 'DataFrame':
        data = list(dataset[key])
    else:
        data = dataset

    wma = []

    if filter_type == 'simple':
        left = int(np.floor(float(interval) / 2))
        if left == 0:
            return data
        for i in range(left):
            wma.append(data[i])
        for i in range(left, len(data)-left):
            wma.append(np.mean(data[i-(left):i+(left)]))
        for i in range(len(data)-left, len(data)):
            wma.append(data[i])

    elif filter_type == 'exponential':
        left = int(np.floor(float(interval) / 2))
        weight = weight_strength / (float(interval) + 1.0)
        if weight > 1.0:
            weight = 1.0
        for i in range(left):
            wma.append(data[i])
        for i in range(left, len(data)-left):
            sum_len = len(data[i-(left):i+(left)]) - 1
            sum_vals = np.sum(data[i-(left):i+(left)])
            sum_vals -= data[i]
            sum_vals = sum_vals / float(sum_len)
            sum_vals = data[i] * weight + sum_vals * (1.0 - weight)
            wma.append(sum_vals)
        for i in range(len(data)-left, len(data)):
            wma.append(data[i])

    return wma
