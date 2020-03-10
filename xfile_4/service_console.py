#!/usr/bin/env python

'''
Usage:
    service_console.py --config <configfile> --svc-name <service> 
'''


import docopt
from snap import snap, common


def main(args):
    configfile = args['<configfile>']
    yaml_config = common.read_config_file(configfile)
    services = common.ServiceObjectRegistry(snap.initialize_services(yaml_config))
    event_service = services.lookup(args['<service>'])


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)

