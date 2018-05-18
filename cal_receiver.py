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
