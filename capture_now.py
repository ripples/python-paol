#!/usr/bin/env python

'''
capture_now.py:
    Manual entry point of the capturing system.

    Argv[1]: {Current Semester}
    Argv[2]: {Current Course}
    Argv[3]: {Duration in sec}
'''

import sys
import os
import signal
import json


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    return


if __name__ == '__main__':
    main()


__author__ = "William He"
__copyright__ = "Copyright 2018, RIPPLE LV2 Project"
__credits__ = ["William He", ]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "William He"
__email__ = "ziweihe@umass.edu"
__status__ = "Development"
