# -*- coding: utf-8 -*-
class meter(object):

    def __init__(self):
        meter.metadata = dict()
        meter.address = dict()

    def load(self, user):
            self.address = {'file': user.file, 'key': key}
            meter_data = {'phases': 2, 'sampling':1}
            location_data = {}  