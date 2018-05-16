#!/usr/bin/env python

'''
lec_scheduler.py:
    reads the stored calendar and schedule capturing tasks;
    also kick off the calendar receiver route
    will stay awake all time.
'''

import json
import os
import signal


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def schedule_lectures(ics_path):
