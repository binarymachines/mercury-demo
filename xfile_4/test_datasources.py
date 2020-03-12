#!/usr/bin/env python

import sys
import datetime


MONTH_INDEX = 0
DAY_INDEX = 1
YEAR_INDEX = 2


TODAY = datetime.date.today()

def calc_longevity(start_date, end_date):

    if end_date < TODAY:
        return (end_date - start_date).days
    return (TODAY - start_date).days


class TestDatasource(object):
    def __init__(self, service_object_registry):
        self.services = service_object_registry


    def lookup_longevity(self, target_field_name, source_record, field_value_map):
        # TODO: should probably screen inputs for end dates which precede start dates

        start_date_arr = field_value_map.get_value('start_date', source_record)
        end_date_arr = field_value_map.get_value('end_date', source_record)

        start_date = datetime.date(start_date_arr[YEAR_INDEX],
                                   start_date_arr[MONTH_INDEX],
                                   start_date_arr[DAY_INDEX])

        end_date = datetime.date(end_date_arr[YEAR_INDEX],
                                 end_date_arr[MONTH_INDEX],
                                 end_date_arr[DAY_INDEX])

        #print('Hello, net -- the start date is %s and the end date is %s.' % (start_date, end_date), file=sys.stderr)  

        longevity = calc_longevity(start_date, end_date)
        username = source_record['Email Address']

        event_db = self.services.lookup('events')
        suspension_event = event_db.find_suspension_event(username)
        if suspension_event:
            print('##----------- suspension event found for user %s on date %s.' % (suspension_event.user,
                                                                                   suspension_event.date))
            # recalc
        
        return longevity