from __future__ import print_function, division
import json
import pandas as pd
from os.path import isdir, isfile, join, splitext
from os import listdir
from sys import stderr
from copy import deepcopy


def convert_json_to_hdf5(json_dir, hdf_filename):
    assert isdir(json_dir)
    with pd.get_store(hdf_filename, mode='a') as store:
        name = "/".join(json_dir, "user1.json")
        with open(name) as fh:
            metadata_user = json.load(fh)
        store.root._v_attrs.metadata = metadata_user

        name2 = "/".join(json_dir, "user1_meter1.json")
        with open(name2) as fh:
            metadata_meter = json.load(fh)
        lc_id = 1
        phase = 'A'
        key = '/'.join(('/location{:d}'.format(lc_id),
                                    'phase{:s}'.format(phase)))
                    key_df = join(key, 'meter')
        store.get_storer(key).attrs.metadata = metadata_meter

