#!/usr/bin/env python

'''
*_cap.py:
    capturing *.
'''
import time
import subprocess


COMM = 'ffmpeg -y -strict -2 -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 640x480 -r 25 -i /dev/@DEVICE -t @TIME -strict -2 '


def trigger_cap(device, args, path):
    comm = COMM + path + 'videoLarge.mp4'
    comm = comm.replace('@TIME', time.strftime('%H:%M:%S', time.gmtime(args[2])))
    comm = comm.replace('@DEVICE', device)

    st = None
    with open('./logs/ffmpeg.log', 'w+') as f:
        st = subprocess.Popen(comm, stdout=f, stderr=f, shell=True)
    return st
