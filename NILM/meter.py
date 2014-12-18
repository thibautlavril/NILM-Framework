# -*- coding: utf-8 -*-
class Meter(object):

    def __init__(self, user, meter_name):
        self.user = user
        assert meter_name in user.metadata['meters']
        self.metadata = user.metadata['meters'][meter_name]

    @property
    def store(self):
        """ Get the store"""
        return self.user.store

    def load_measurements(sampling_period=1):
        """
        Load the measurments in a pd.DataFrame. The elapsed time between each
        sample is given by sampling_period in seconds
        """
        raise NotImplementedError

    def __repr__(self):
        s = "Meter: meter_id: {:d}, user_id: {:d}"\
            .format(self.metadata['meter_id'], self.metadata['user_id'])
        return s


if __name__ == '__main__':
    from user import User
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
    user1 = User()
    user1.load(hdf_filename)
    meter1_name = user1.metadata['meters'].keys()[0]
    meter1 = Meter(user1, meter1_name)
