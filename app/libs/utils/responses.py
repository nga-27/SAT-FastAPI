def response_handler(ep_type: str, operation: str, data, ticker=""):
    obj = {"ticker": ticker}
    obj['data'] = {"type": ep_type}
    obj['data']['op'] = operation
    obj['data']['payload'] = data
    return obj
