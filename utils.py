#!/usr/bin/env python

'''
utils.py:
    Helper Methods
'''

import icalendar
from datetime import datetime
import sys


INFO = 'INFO'
ERR = 'ERR '
WARN = 'WARN'


def log(lvl, msg):
    '''logging'''
    print('[%s] %s: %s' % (str(datetime.now()), lvl, msg))


def print_progress(iteration, total, prefix='PROG', suffix='',
                   decimals=1, length=50, fill='>'):
    percent = ("{0:." +
               str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r[%s] %s: |%s| %s%% %s' % (str(datetime.now()),
                                                prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print("")
        log(INFO, "Job Done.")


def print_cal_events(gcal):
    ''' Get all details of all scheduled VEVENTs'''
    log(INFO, 'EVENT list of ICS file:')
    for component in gcal.walk():
        if component.name == "VEVENT":
            log(INFO, ' ' + component.get('summary'))
            log(INFO, '  start:' + str(component.get('dtstart').dt))
            log(INFO, '  end:  ' + str(component.get('dtend').dt))


def get_cal(filename):
    ''' return Calendar Object from .ics File'''
    log(INFO, 'LOADING GCAL from ' + filename)
    g = open(filename, 'rb')
    gcal = icalendar.Calendar.from_ical(g.read())
    if gcal:
        log(INFO, 'LOADING Successful.')
    else:
        log(ERR, 'UNABLE TO LOAD ICS FILE.')
    return gcal
