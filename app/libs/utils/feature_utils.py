import numpy as np


def normalize_signals(signals: list) -> list:
    """Normalize Signals

    General function for normalizing all values to np.abs() maximum

    Arguments:
        signals {list} -- signal to normalize

    Returns:
        list -- normalized signal
    """
    max_ = 0.0
    for sig in signals:
        m = np.max(np.abs(sig))
        if m > max_:
            max_ = m

    if max_ != 0.0:
        for i in range(len(signals)):
            new_sig = []
            for pt in signals[i]:
                pt2 = pt / max_
                new_sig.append(pt2)
            signals[i] = new_sig.copy()

    return signals
