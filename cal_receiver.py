#!/usr/bin/env python

'''
cal_receiver.py:
    listen to given port for new calendar file and overwrite old one
'''

import os
import posixpath
import BaseHTTPServer
import urllib
import shutil
import icalendar
import utils
import pytz
import datetime
from StringIO import StringIO

import lec_scheduler
import utils
import Monitor


def on_cal_changed(gcal):
    '''update scheduled lectures when calendar is changed'''
    utils.log('INFO', 'On Calendar Changed Callback...')
    timezone = pytz.timezone("US/Eastern")
    m_temp = []
    utils.log('INFO', 'Printing New Calendar Info...')
    utils.print_cal_events(gcal)
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
            if start_time < timezone.localize(datetime.now()):
                continue
            job = Monitor.Monitor(s, func, args, start_time)
            m_temp.append(job)

    # Cancel scheduled Tasks
    for mo in Monitor.MONITORS:
        status = mo.cancel_task()
        # remove task if cancelled
        if status == 0:
            Monitor.MONITORS.pop(mo)

    for mo in mo_temp:
        if mo.dt < timezone.localize(datetime.now()):
            continue
        Monitor.MONITORS.append(mo)

    for mo in Monitor.MONITORS:
        mo.schedule_task()


def CalHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''Simple HTTP Handler retrieve calendar file'''
    def do_POST(self):
        '''Serve a POST request'''
        utils.log('INFO', 'Incoming POST request...')
        r, info = self.process_post_data()
        f = StringIO()

        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")

        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()



def start_server(HandlerClass=CalHandler,
                 ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)
