# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:04:36 2015

@author: thibaut
"""
from __future__ import print_function, division
import pandas as pd
import numpy as np


def simple_edge(df, edge_threshold=70):
    """Implements simple edge detection

    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame containing the measurements
            index: DateTimeIndex, timestamps
            attributes: power measured (depending on powers available)

    edge_threshold: int or float
        Threshold on a the active power (first power) to classify
        detect an event between two consecutive measurements.

    Returns
    -------
    events: pandas.DataFrame
        DataFrame containing the events
            index: DateTimeIndex, timestamps
            attributes: power types availabes
    """
    # PART I: t to delta t
    columns = df.columns

    df_t1 = df.values[1:]
    df_t0 = df.values[:-1]
    df_dt = df_t1-df_t0
    index_dt = df.index[1:]
    events = pd.DataFrame(df_dt, columns=columns, index=index_dt)
    # PART II: Application of edge_threshold
    events = events[np.abs(events[columns[0]]) > edge_threshold]
    events.index.name = df.index.name
    return events
