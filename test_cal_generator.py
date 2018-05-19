#!/usr/bin/env python

'''
test_cal_generator.py:
    simple program that generate cal simple task within the next few minutes
'''

from datetime import datetime, timedelta
import icalendar

import schedule_now
import utils


TESTCALFNAME = 'CalendarTest.ics'
# Event Summary
SUMMARY = 'SPRING18 PAOL_001232_FA17_CNAC'


def init_test_eve():
    '''Create two intercepted simple tasks to '''
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar//umass.edu//')
    cal.add('version', '2.0')

    cal = add_eve2cal(cal, SUMMARY, 3, 15)
    cal = add_eve2cal(cal, SUMMARY, 25, 7)

    f = open(TESTCALFNAME, 'wb')
    f.write(cal.to_ical())
    f.close()

    schedule_now.main(TESTCALFNAME)


def add_eve2cal(gcal, summary, delay, duration):
    '''Add event to gcal with delay and duration'''
    if not gcal:
        return None
    event = icalendar.Event()
    event.add('summary', summary)
    b = utils.utc_now() + timedelta(0, delay)
    event.add('dtstart', b)
    event.add('dtend', b + timedelta(0, duration))
    event.add('dtstamp', utils.utc_now())

    event['uid'] = str(datetime.strftime(utils.utc_now(), '%c').strip())
    event.add('priority', 5)

    gcal.add_component(event)
    return gcal

init_test_eve()
