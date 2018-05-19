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
import time

import utils


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    args = sys.argv[1:]
    if len(args) != 3:
        utils.log('ERR ', 'Invalid Arguments')
        return
    capture(args)
    return


def capture(args):
    utils.log('INFO', 'Capturing ' + str(args))
    for i in range(int(args[2])):
        time.sleep(1)
        utils.log('INFO', 'Time elapsed: ' + str(i))

    return '1'


if __name__ == '__main__':
    main()
