#!/usr/bin/env python

'''
Monitor.py:
    Class of managing tasks
'''

from datetime import datetime
from threading import Timer
import pytz

import utils


MONITORS = []


class Monitor:
    '''
        Class to manage scheduled events
        @s: Schedule object for scheduling events
        @func: The function that will be run
        @args: The arguments for the function as a list
        @dt: Time to run the task as datetime obj
    '''
    def __init__(self, s, func, args, dt):
        self.schedule = s
        self._running = False
        self.func = func
        self.args = args
        self.dt = dt

    def __str__(self):
        return str(self.dt)

    def start_task(self, func, args):
        utils.log('INFO', 'Initializing task: ' + func.__name__)
        utils.log('INFO', 'Running task: ' + func.__name__ + str(args))
        ret = self.func(args)
        if ret is '0':
            utils.log('INFO', 'Task ' + func.__name__ + ' Done.')
            # pu = subprocess.Popen("~/paol-code/scripts/upload/uploadAll.sh",
            # stdout=subprocess.PIPE, shell=True)
            # print("==>Uploading...")
            # _, er = pu.funcunicate()
            # print("==>Return code: "+str(pu.returncode))
        else:
            utils.log('ERR ', 'Error ' + ret + ' encountered during Task'
                      + func.__name__)
        utils.log('INFO', 'Finishing task: ' + func.__name__)
        return

    def schedule_task(self):
        func = self.func
        args = self.args
        dt = self.dt
        utils.log('INFO', 'Scheduling task: '
                  + func.__name__ + ' at ' + str(dt))
        timezone = pytz.timezone("US/Eastern")
        self.t = Timer((dt-timezone.localize(datetime.now())).total_seconds(),
                       self.start_task, args=(func, args))
        self.t.start()
        utils.log('INFO', 'Task '
                  + func.__name__ + ' scheduled at ' + str(dt))

    def start(self):
        self._running = True
        self.schedule_task()

    def stop(self):
        self._running = False
        if self.t:
            self.t.cancel()
        utils.log('INFO', 'Stopped task '
                  + self.func.__name__ + ' at ' + str(self.dt))
