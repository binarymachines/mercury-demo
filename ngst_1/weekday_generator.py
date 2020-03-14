#!/usr/bin/env python


def line_array_generator(**kwargs):
    data = ['"Monday"', '"Tuesday"', '"Wednesday"', '"Thursday"', '"Friday"', '"Saturday"', '"Sunday"']
    id = 1
    for day in data:
        yield [id, day]
        id += 1 