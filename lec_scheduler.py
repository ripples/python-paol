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
import sched
import pytz
import time
from datetime import datetime, timedelta

import utils
import cal_receiver
import Monitor


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def schedule_lectures(ics_path, func):
    '''read ICS from @ics_path and schedule @func at given time'''
    utils.log('INFO', 'Starting scheduling capturing...')
    gcal = utils.get_cal(ics_path)
    utils.print_cal_events(gcal)
    Monitor.FUNC = func

    # initialize scheduler for events
    Monitor.SCHED = sched.scheduler(time.time, time.sleep)

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            time_delta = end_time - start_time
            seconds = time_delta.total_seconds()
            args = summary.split(' ')
            args.append(seconds)

            # create new Monitor
            if start_time < utils.utc_now():
                continue
            job = Monitor.Monitor(Monitor.SCHED, func, args, start_time)
            Monitor.MONITORS.append(job)

    # Schedule all events
    for mo in Monitor.MONITORS:
        mo.schedule_task()
    utils.log('INFO', 'Finished scheduling capturing...')

    cal_receiver.start_server()

    while 1:
        pass
