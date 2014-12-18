from __future__ import print_function
import pandas as pd
import numpy as np
import sys
import scipy.io
import dateutil.tz
import datetime
import os
from os.path import isdir, isfile, join
from dateutil.parser import parse
import json
try:
    from ..utils import utils_nilmtk
except ValueError:
    abspath = os.getcwd()
    NILMpath = os.path.dirname(os.path.dirname(abspath))
    sys.path.append(NILMpath)
    from NILM.utils import utils_nilmtk


def convert_blued(input_path, hdf_path):
    """
    Convert the matlab files of Blued into a pd.DataFrame. The dataframe is
    stored in a HDFS file (one file by user). IMPORTANT: The matlab files needs
    to be unzipped before converted and stored in there originally folder.

    Parameters
    ----------
    input_path: string
        The path where the "location001_dataset00x" folders are stored
    hdf_path: string
        The path of the folder where to store the HDFS files.
    """
    assert isdir(input_path)
    assert isdir(hdf_path)

    metadata_BLUED = _load_metadata_BLUED()
    _convert_metadata_blued(hdf_path, metadata_BLUED)
    _convert_data(input_path, hdf_path, metadata_BLUED)
    print("Convertion finished!")


def _load_metadata_BLUED():
    metadata_file = join(_give_path_script(), 'metadata', 'blued.json')
    assert isfile(metadata_file)
    with open(metadata_file) as fh:
        metadata_BLUED = json.load(fh)
    return metadata_BLUED


def _give_path_script():
    try:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        print(dir_path)
    except NameError:
        dir_path = os.getcwd()
    return dir_path


def _convert_metadata_blued(hdf_path, metadata_BLUED):
    with pd.get_store(hdf_filename) as store:
        store.root._v_attrs.metadata = metadata_BLUED


def _convert_data(input_path, hdf_path, metadata_BLUED):
    for user in metadata_BLUED['users'].keys():
        metadata_user = metadata_BLUED["users"][user]
        print("Loading", user, end=" ")
        sys.stdout.flush()
        _convert_user(input_path, hdf_path, metadata_user)


def _convert_user(input_path, hdf_path, metadata_user):
    for meter in metadata_user['meters'].keys():
        metadata_meter = metadata_user["meters"][meter]
        print(meter, end="... ")
        sys.stdout.flush()
        _convert_meter(input_path, hdf_path, metadata_meter)


def _convert_meter(input_path, hdf_path, metadata_meter):
    number_datasets = metadata_meter["number_datasets"]
    meter = metadata_meter["meter_id"]
    user = metadata_meter["user_id"]
    hdf_filename = _make_hdf_file(user, hdf_path)
    if os.path.exists(hdf_filename):
            os.remove(hdf_filename)
    key_measurements = _make_key_measurements(meter)
    tz = metadata_meter["tz"]
    start = _find_start(meter, input_path, tz)
    with pd.get_store(hdf_filename) as store:
        for dataset in np.arange(1, number_datasets + 1):
            print(dataset, end=" ")
            sys.stdout.flush()
            df = _load_dataset(dataset, input_path, metadata_meter, start)
            store.append(str(key_measurements), df, format='table')
            store.flush()
    print()


def _load_dataset(dataset, input_path, metadata_meter, start):
    measurements = metadata_meter["measurements"]
    meter = metadata_meter["meter_id"]
    path = _make_input_path(meter, dataset, input_path)
    assert isdir(path)
    index = None
    data = None
    sub_files = _make_list_subfiles(dataset)
    for sub_file in sub_files:
        measures, timestamps = _load_subfile(sub_file, dataset,
                                             meter, path)
        if index is None:
            data = measures
            index = timestamps
        else:
            data = np.concatenate((data, measures), axis=0)
            index = np.concatenate((index, timestamps), axis=0)
    tz = metadata_meter["tz"]
    index = _sec_since_start_to_Datetime(index, start, tz)
    cols = pd.MultiIndex.from_tuples(measurements, names=['phase', 'type'])
    df = pd.DataFrame(data, columns=cols, index=index, dtype='float32')
    return df


def _load_subfile(sub_file, dataset, meter, path):
    input_file = _make_input_file(sub_file, dataset, meter, path)
    assert isfile(input_file)
    mat = scipy.io.loadmat(input_file)
    t = mat['data'][0][0][2]
    t = t.reshape(len(t))
    tt = mat['data'][0][0][3].reshape(len(t))
    Qa = mat['data'][0][0][4][0].reshape(len(t), 1)
    Qb = mat['data'][0][0][5][0].reshape(len(t), 1)
    Pa = mat['data'][0][0][6][0].reshape(len(t), 1)
    Pb = mat['data'][0][0][7][0].reshape(len(t), 1)
    measures = np.concatenate((Pa, Qa, Pb, Qb), axis=1)
    timestamps = tt
    return measures, timestamps


def _sec_since_start_to_Datetime(index, start, tz):
    """
    Compute the pd.DatetimeIndex in timezone tz. The index is
    the time elapsed since start. start is given in the timezone
    tz.
    """
    zero = datetime.datetime(1970, 1, 1)
    zero = zero.replace(tzinfo=dateutil.tz.gettz('UTC'))
    start_int = (start-zero).total_seconds()
    index = index + start_int
    index = pd.to_datetime(index, unit='s', utc=True)
    index = index.tz_convert(tz)
    return index


def _make_input_file(sub_file, dataset, meter, path):
    meter_path = 'location_00{:d}'.format(meter)
    filename = "_".join((meter_path,
                         'matlab_{:d}.mat'.format(sub_file)))
    filename = "/".join((path, filename))
    return filename


def _make_input_path(meter, dataset, input_path):
    meter_path = 'location_00{:d}'.format(meter)
    dataset_path = "_".join((meter_path, 'dataset_00{:d}'.format(dataset)))
    path = "/".join((input_path, dataset_path))
    return path


def _make_list_subfiles(dataset):
    first_subfile = (dataset-1)*4 + 1
    last_subfile = first_subfile + 4
    return range(first_subfile, last_subfile)


def _make_hdf_file(user, hdf_path):
    filename = "user{:d}.h5".format(user)
    hdf_filename = "".join((hdf_path, filename))
    return hdf_filename


def _make_key_measurements(meter):
    return "/meter{:d}/measurements".format(meter)


def _find_start(meter, input_path, tz):
    name_dir = "_".join(('/location_00{:d}'.format(meter), 'dataset_001/'))
    start_end_path = "".join((input_path, name_dir))
    start_end_file = "".join((start_end_path, 'start_end.txt'))
    with open(start_end_file) as f:
        l = [line.strip() for line in f]
    start_date = l[1].split(",")[1]
    start_time = l[2].split(",")[1]
    start = parse(start_date+' '+start_time)
    start = start.replace(tzinfo=dateutil.tz.gettz(tz))
    return start


if __name__ == "__main__":
    hdf_path = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/'
    input_path = '/Volumes/Stockage/DATA/DATA_BLUED/RAW'
    convert_blued(input_path, hdf_path)
    hdf_filename = _make_hdf_file(1, hdf_path)
    key = _make_key_measurements(1)
    with pd.get_store(hdf_filename) as store:
        df = store[key]
        metadata_dict = store.root._v_attrs.metadata
    import matplotlib.pyplot as plt
    plt.plot(df.index)
