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
import config
import init_setup


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
    '''captures according to config file'''
    if not config.load_all_config() or config.is_config_invalid():
        utils.log('WARN', 'Hardware not configured. Running init setup GUI...')
        init_setup.main()
        utils.log('WARN', 'Please restart the program.')
        return


    utils.log('INFO', 'Start capturing ' + str(args))
    for i in range(int(args[2])):
        time.sleep(1)
        utils.log('INFO', 'Time elapsed: ' + str(i))

    return '0'


if __name__ == '__main__':
    main()
