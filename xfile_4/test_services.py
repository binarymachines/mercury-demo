#!/usr/bin/env python

import os, sys
import yaml
from snap import common
from collections import namedtuple
import datetime


SuspensionEvent = namedtuple('SuspensionEvent', 'user date')

MONTH_INDEX = 0
DAY_INDEX = 1
YEAR_INDEX = 2



def parse_date(date_string):
    tokens = [int(token) for token in date_string.split("/")]
    return datetime.date(tokens[YEAR_INDEX],
                         tokens[MONTH_INDEX],
                         tokens[DAY_INDEX])


class BusinessEventDB(object):
    def __init__(self, **kwargs):

        location = kwargs['location']
        datafile = kwargs['datafile']

        datapath = os.path.join(location, datafile)

        self.db = {}
        self.data = None
        with open(datapath, 'r') as f:
            self.data = yaml.safe_load(f)

        #print(common.jsonpretty(self.data))

        for s in self.data['suspension_events']:
            self.db[s['user']] = SuspensionEvent(user=s['user'], date=parse_date(s['date']))

        print(self.db)


    def find_suspension_event(self, username):
        return self.db.get(username)
