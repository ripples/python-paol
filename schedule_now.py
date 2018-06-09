#!/usr/bin/env python

'''
schedule_now.py:
    Manual entry point of the capturing system.
'''

import sys
import os
import signal
import json
import time

import lec_scheduler
import capture_now
import utils
import config
import Monitor


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main(cal_path):
    if not config.load_all_config() or not config.is_config_valid():
        utils.log('WARN', 'Hardware not configured. Running init setup GUI...')
        init_setup.main()
        utils.log('WARN', 'Please restart the program.')
        exit(0)
    lec_scheduler.schedule_lectures(cal_path, capture_now.capture)


if __name__ == '__main__':
    main(Monitor.CAL_FILE)
