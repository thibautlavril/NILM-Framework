# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 19:21:42 2014

@author: thibaut
"""

def load_data_window(store, key, start=None, end=None):
    """
    load only on window of data,
    start and end needs to be pd.Timestamp or
    a datetime.datetime
    """
    assert isfile(hdf_filename)
    key = join('/location{:d}'.format(location), 'phase{:s}'.format(phase))
    key_meter = join(key, name)

    if start is None:
        if end is None:
            with pd.get_store(hdf_filename) as store:
                meter = store.select(key_meter)
                return meter
        else:
            end = pd.Timestamp(end)
            with pd.get_store(hdf_filename) as store:
                meter = store.select(key_meter, 'index<end')
                return meter
    else:
        start = pd.Timestamp(start)
        if end is None:
            with pd.get_store(hdf_filename) as store:
                meter = store.select(key_meter, 'index>start')
                return meter
        else:
            end = pd.Timestamp(end)
            with pd.get_store(hdf_filename) as store:
                meter = store.select(key_meter, 'index<end & index>start')
                return meter