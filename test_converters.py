# -*- coding: utf-8 -*-

from NILM import converter
from NILM import Meter

import pandas as pd

blued_path = '/Volumes/Stockage/DATA/DATA_BLUED/RAW'
store_path = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED'

# converter.blued_to_user(blued_path, store_path)

user_filename = 'user_blued.h5'
hdf_filename = "/".join((store_path, user_filename))

key = "/".join(("meter_blued", "measurements"))
with pd.get_store(hdf_filename) as store:
    df = store[key]

meter_filename = 'meter_blued.h5'
hdf_filename = "/".join((store_path, meter_filename))

converter.dataframe_to_meter(df, hdf_filename)

meter1 = Meter.from_meter_hdf(hdf_filename)

meter_filename = 'meter_blued_2.h5'
hdf_filename = "/".join((store_path, meter_filename))
meter2 = Meter.from_dataframe(df, hdf_filename)
