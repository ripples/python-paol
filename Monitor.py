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
        self._scheduled = False
        self._running = False
        self.func = func
        self.args = args
        self.dt = dt

    def __str__(self):
        return self.func.__name__ + ' at ' + str(self.dt) + ' s'
               + str(int(self._scheduled))
               + 'r' + str(int(self._running))

    def start_task(self, func, args):
        utils.log('INFO', 'Initializing task: ' + func.__name__)
        utils.log('INFO', 'Running task: ' + func.__name__ + str(args))
        self._running = True
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
        self._running = False

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

        self._scheduled = True
        utils.log('INFO', 'Scheduled task: '
                  + func.__name__ + ' at ' + str(dt))

    def cancel_task(self):
        utils.log('INFO', 'Cancelling task '
                  + self.func.__name__ + ' at ' + str(self.dt))
        if self.t and not self._running:
            self.t.cancel()

            self._scheduled = False
            utils.log('INFO', 'Cancelled task '
                      + self.func.__name__ + ' at ' + str(self.dt))
            return 0
        else:
            utils.log('WARN', 'Unable to cancel running Task '
                      + self.func.__name__ + ' at ' + str(self.dt))
            return 1
