import pandas as pd
from pandas.tseries.offsets import Micro, Second


def resample(df, sampling_period=1):
    assert isinstance(df, pd.DataFrame)
    assert isinstance(df.index, pd.DatetimeIndex)

    if isinstance(sampling_period, int):
        df = df.resample(Second(sampling_period), how='last', label='right', closed='right')
    else:
        period = sampling_period*(10**6)
        df = df.resample(Micro(period), how='last',
                         label='right', closed='right')
    return df
