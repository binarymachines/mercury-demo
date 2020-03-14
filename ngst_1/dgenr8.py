#!/usr/bin/env python

'''
Usage:
    dgenr8 --sql --schema <schema> --dim-table <tablename> --columns <columns>... [--limit=<limit>]
    dgenr8 --csv --delimiter <delimiter> [--limit=<limit>]

'''

# dgenr8 (dimension table generator): generates SQl insert statements or CSV records to populate
# OLAP star-schema dimension tables


import os, sys
from collections import namedtuple
import docopt
import jinja2
from snap import snap, common


InsertLine = namedtuple('InsertLine', 'schema table ')


insert_statement_template = '''
INSERT INTO {{ schema }}.{{ table }}
({{ column_list }})
VALUES ({{ value_list_string }})
'''

sql_value_list_template = '''
{%- for value in line_array -%}{{ value }}, {% endfor -%}
'''

csv_line_template = '''
{%- for value in values -%}{{ value }}{{ delimiter }}{%- endfor -%}
'''

CSV_MODE = '--csv'
SQL_MODE = '--sql'


def line_array_generator(**kwargs):
    data = ['"Monday"', '"Tuesday"', '"Wednesday"', '"Thursday"', '"Friday"', '"Saturday"', '"Sunday"']
    id = 1
    for letter in data:
        yield [id, letter, 'NULL']
        id += 1 


def main(args):
    limit = int(args['--limit'] or -1)
    lines_generated = 0

    j2env = jinja2.Environment()

    if args[CSV_MODE]:
        delimiter = args['<delimiter>']
        for line in line_array_generator():
            if lines_generated == limit:
                break
                    
            sql_template = j2env.from_string(csv_line_template)
            output = sql_template.render(values=line, delimiter=delimiter)
            print(output.rstrip(delimiter))
            lines_generated += 1

    if args[SQL_MODE]:
        sql_template = j2env.from_string(insert_statement_template)
        values_template = j2env.from_string(sql_value_list_template)
        columns = args['<columns>']

        sql_template_params = {
            'schema': args['<schema>'],
            'table': args['<tablename>'],
            'column_list': ', '.join(columns)
        }

        for line_array in line_array_generator():
            if lines_generated == limit:
                break

            if len(line_array) != len(columns):
                raise Exception('You specified %d output columns (%s), but your line-array generator function returns %s values.' %
                                (len(columns), columns, len(line_array)))

            values_line = values_template.render(line_array=line_array).rstrip(', ')

            sql_template_params['value_list_string'] = values_line
            output = sql_template.render(**sql_template_params)
            print(output)
            lines_generated += 1



if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
