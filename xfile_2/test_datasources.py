#!/usr/bin/env python

from snap import common
import arrow
import datetime


class TestDatasource(object):
    def __init__(self, service_object_registry):
        self.services = service_object_registry


    def lookup_longevity(self, target_field_name, source_record, field_value_map):
        '''
        print('target field name is: %s' % target_field_name)
        print('source record is: %s' % source_record)

        print('the value of the field "status" is %s' % (field_value_map.get_value('status', source_record)))

        raw_start_date = field_value_map.get_value('start_date', source_record)
        raw_end_date = field_value_map.get_value('end_date', source_record)

        start_date = arrow.get(raw_start_date, 'MM/DD/YYYY')
        end_date = arrow.get(raw_end_date, 'MM/DD/YYYY')

        print('date value of "start_date" is %s' % start_date)
        print('date value of "end_date" is %s' % end_date)
        '''
        
        datetokens = field_value_map.get_value('start_date', source_record)
        print('transformed start date is: %s' % datetime.date(datetokens[2], datetokens[0], datetokens[1]))

        return '###'

