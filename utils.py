#!/usr/bin/env python

'''
utils.py:
    Helper Methods
'''

import icalendar
from datetime import datetime
import pytz
import sys
import socket


INFO = 'INFO'
ERR = 'ERR '
WARN = 'WARN'


def log(lvl, msg):
    '''logging'''
    str_log = '[%s] %s: %s' % (str(datetime.now().strftime("%y%m%d-%H%M%S")), lvl, msg)
    print(str_log)
    with open('./logs/general.log', 'a+') as f:
        f.write(str_log + '\n')


def utc_now():
    '''return absolute datetime object of datetime.now()'''
    return datetime.utcnow()


def print_progress(iteration, total, prefix='PROG', suffix='',
                   decimals=1, length=25, fill='>'):
    percent = ("{0:." +
               str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r[%s] %s: |%s| %s%% %s' % (str(datetime.now().strftime("%y%m%d-%H%M%S")),
                                                prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print("")


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


def writeINFO(save_path, wb, com, args):
    '''generate INFO at save_path'''
    now = datetime.now()
    with open(save_path + 'INFO', 'w+') as f:
        f.write('[course]' + '\n')
        f.write('id: ' + args[1] + '\n')
        f.write('term: ' + args[0] + '\n')
        f.write('' + '\n')
        f.write('[pres]' + '\n')
        f.write('start: ' + now.strftime('%y,%m,%d,%H,%M,%S') + '\n')
        f.write('duration: ' + str(int(args[2])) + '\n')
        f.write('source: ' + socket.gethostname() + '\n')
        f.write('timestamp: ' + str(int(now.timestamp())) + '\n')
        f.write('whiteboardCount: ' + str(wb) + '\n')
        f.write('computerCount: ' + str(com) + '\n')
