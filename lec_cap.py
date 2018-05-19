#!/usr/bin/env python

'''
*_cap.py:
    capturing *.
'''
# ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 640x480 -r 25 -i /dev/video2 -t 00:00:01 out.avi



def trigger_cap(device, args):
    return
