#!/usr/bin/env python

'''
cal_receiver.py:
    listen to given port for new calendar file and overwrite old one
'''

import os
import posixpath
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import shutil
import icalendar
import utils
import pytz
import datetime
from io import StringIO

import lec_scheduler
import utils
import Monitor


PORT = 8000


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
            job = Monitor.Monitor(Monitor.SCHED, Monitor.FUNC, args, start_time)
            m_temp.append(job)

    # Cancel scheduled Tasks
    for mo in Monitor.MONITORS:
        status = mo.cancel_task()
        # remove task if cancelled
        if status == 0:
            Monitor.MONITORS.pop(mo)

    for mo in m_temp:
        if mo.dt < timezone.localize(datetime.now()):
            continue
        Monitor.MONITORS.append(mo)

    for mo in Monitor.MONITORS:
        mo.schedule_task()


class CalHandler(BaseHTTPRequestHandler):
    '''Simple HTTP Handler retrieve calendar file'''
    def do_POST(self):
        '''Serve a POST request'''
        utils.log('INFO', 'Incoming POST request...')
        r, info = self.process_post_data()
        f = StringIO()

        if r:
            utils.log('INFO', info)
            f.write("<strong>Success:</strong>")
        else:
            utils.log('ERR ', info)
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

    def process_post_data(self):
        utils.log('INFO', self.headers)
        boundary = self.headers.plisttext.split("=")[1]
        utils.log('INFO', 'Boundary %s' % boundary)
        remainbytes = int(self.headers['content-length'])
        utils.log('INFO', "Remain Bytes %s" % remainbytes)
        line = self.rfile.readline()
        remainbytes -= len(line)
        if boundary not in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = Monitor.CAL_FILE
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "No Write Permission")

        if line.strip():
            preline = line
        else:
            preline = self.rfile.readline()
        remainbytes -= len(preline)
        while 1:
            line = self.rfile.readline()
            # print(line)
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()

                g = open(fn, 'rb')
                gcal = icalendar.Calendar.from_ical(g.read())
                on_cal_changed(gcal)

                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)


def start_server(HandlerClass=CalHandler,
                 ServerClass=HTTPServer):
    utils.log('INFO', 'Serving POST on port ' + str(PORT) + '...')
    server_address = ('', PORT)
    httpd = ServerClass(server_address, HandlerClass)
    httpd.serve_forever()
