#!/usr/bin/env python


class TestDatasource(object):
    def __init__(self, service_object_registry):
        self.services = service_object_registry


    def lookup_subscriber_status(self, target_field_name, source_record, field_value_map):
        print(field_value_map)
        return ''

