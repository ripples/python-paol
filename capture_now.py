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
from lec_sched import lec_scheduler


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    lec_scheduler.schedule_lectures('./lec_sched/Calendar.ics', None)
    return


if __name__ == '__main__':
    main()
