#!/usr/bin/env python

'''
Usage:
    ffilter.py --accept-to-file <filename> --delimiter <delimiter> <source_file>
    ffilter.py --reject-to-file <filename> --delimiter <delimiter> <source_file>
'''


import os, sys
import re
import csv
from collections import namedtuple
import docopt


DATE_REGEX_STRING = r'^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$'
EMAIL_REGEX_STRING = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

ACCEPT_TO_FILE_MODE = '--accept-to-file'
REJECT_TO_FILE_MODE = '--reject-to-file'


CSVRecord = namedtuple('CSVRecord', 'data line')

def pass_record(data, line, delimiter, **kwargs):
    
    field_tokens = line.split(delimiter)
    if len(field_tokens) != 10:
        return False

    signup_date = data.get('Signup Date', '')
    exp_date = data.get('Expiration Date', '')

    daterx = re.compile(DATE_REGEX_STRING)
    if not daterx.match(signup_date):
        return False

    if not daterx.match(exp_date):
        return False

    email = data.get('Email Address', '')
    emailrx = re.compile(EMAIL_REGEX_STRING)
    if not emailrx.match(email):
        return False

    return True


def record_generator(filename, delimiter):
    with open(filename, 'r') as csvsrc:
        csvreader = csv.DictReader(csvsrc, delimiter=delimiter)
        with open(filename, 'r') as linesrc:
            next(linesrc)
            for record in csvreader:
                yield CSVRecord(data=record, line=next(linesrc))


def read_file_header(filename):
    with open(filename, 'r') as f:
        return f.readline().strip()


def main(args):

    srcfile = args['<source_file>']
    delim = args['<delimiter>']
    target_filename = args['<filename>']

    mode = None
    if args[ACCEPT_TO_FILE_MODE]:
        mode = ACCEPT_TO_FILE_MODE
    
    if args[REJECT_TO_FILE_MODE]:
        mode = REJECT_TO_FILE_MODE

    hdr = read_file_header(srcfile)
    #print('### source file header: %s' % hdr)

    with open(target_filename, 'a') as f:
        print(hdr)
        f.write(hdr)

        if mode == ACCEPT_TO_FILE_MODE:
            for record in record_generator(srcfile, delim):
                if pass_record(record.data, record.line, delim):
                    f.write(record.line)          
                else:
                    print(record.line.strip())
                    
        if mode == REJECT_TO_FILE_MODE:
            for record in record_generator(srcfile, delim):
                if pass_record(record.data, record.line, delim):
                    print(record.line.strip())
                else:
                    f.write(record.line)
    

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)