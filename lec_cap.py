#!/usr/bin/env python

'''
*_cap.py:
    capturing *.
'''
import time
import subprocess


COMM = 'ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 640x480 -r 25 -i /dev/video2 -t TIME out.avi'


def trigger_cap(device, args):
    subprocess.Popen(COMM.replace('TIME', time.strftime('%H:%M:%S', time.gmtime(args[2]))), stdout=subprocess.PIPE, shell=True)
    return
