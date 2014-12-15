from __future__ import print_function, division
import json
import pandas as pd
from os.path import isdir, isfile, join, splitext
from os import listdir
from sys import stderr
from copy import deepcopy


def convert_yaml_to_hdf5(json_dir, hdf_filename):
    """Converts a NILM Metadata YAML instance to HDF5.

    Also does a set of sanity checks on the metadata.

    Parameters
    ----------
    yaml_dir : str
        Directory path of all *.YAML files describing this dataset.
    hdf_filename : str
        Filename and path of output HDF5 file.  If file exists then will 
        attempt to append metadata to file.  If file does not exist then 
        will create it.
    """

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



        # Load Dataset and MeterDevice metadata
        metadata = _load_file(yaml_dir, 'dataset.yaml')
        meter_devices = _load_file(yaml_dir, 'meter_devices.yaml')
        metadata['meter_devices'] = meter_devices
        store.root._v_attrs.metadata = metadata
    
        # Load buildings
        building_filenames = [fname for fname in listdir(yaml_dir)
                              if fname.startswith('building') 
                              and fname.endswith('.yaml')]
    
        for fname in building_filenames:
            building = splitext(fname)[0] # e.g. 'building1'
            try:
                group = store._handle.create_group('/', building)
            except:
                group = store._handle.get_node('/' + building)
            building_metadata = _load_file(yaml_dir, fname)
            elec_meters = building_metadata['elec_meters']
            _deep_copy_meters(elec_meters)
            _set_data_location(elec_meters, building)
            _sanity_check_meters(elec_meters, meter_devices)
            _sanity_check_appliances(building_metadata)
            group._f_setattr('metadata', building_metadata)
    print("Done converting YAML metadata to HDF5!")


def _load_file(yaml_dir, yaml_filename):
    yaml_full_filename = join(yaml_dir, yaml_filename)
    if isfile(yaml_full_filename):
        with open(yaml_full_filename) as fh:
            return yaml.load(fh)
    else:
        print(yaml_full_filename, "not found.", file=stderr)
