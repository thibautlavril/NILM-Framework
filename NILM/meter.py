# -*- coding: utf-8 -*-
from measurements import Measurements

class Meter(object):

    def __init__(self, user, meter_name):
        self._user = user
        assert meter_name in user.metadata['meters']
        self.name = meter_name
        self.metadata = user.metadata['meters'][meter_name]
        self.state = dict()

    @property
    def store(self):
        """ Get the store"""
        return self._user.store

    @property
    def user(self):
        """ Get the user"""
        return self._user

    def _load_measurements(self, sampling_period=1):
        """
        Load the measurments in a pd.DataFrame. The elapsed time between each
        sample is given by sampling_period in seconds
        """
        self.measurements = Measurements(self, sampling_period)
        self.measurements.load_data()
        self.state['measurements']='sampled ({:d}s)'.format(sampling_period)

    def __repr__(self):
        s = "(meter_id: {:d}, user_id: {:d})"\
            .format(self.metadata['meter_id'], self.metadata['user_id'])
        return s


if __name__ == '__main__':
    from tools import create_user
    user1 = create_user()
    meter1_name = user1.metadata['meters'].keys()[0]
    meter1 = Meter(user1, meter1_name)
    meter1._load_measurements(sampling_period=10)
