#!/usr/bin/env python

'''
schedule_now.py:
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

import lec_scheduler
import utils


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main(cal_path):
    lec_scheduler.schedule_lectures(cal_path, func)
    return


def func(args):
    utils.log('INFO', 'Capturing ' + str(args))
    time.sleep(args[2])
    return '1'


if __name__ == '__main__':
    main('./Calendar.ics')
