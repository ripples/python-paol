#!/usr/bin/env python

'''
*_cap.py:
    capturing *.
'''
import cv2
from datetime import datetime, timedelta
import threading

import utils

INTERVAL = 1


def trigger_cap(device, argp, path):
    th = threading.Thread(target=capture, args=(device, argp, path,))
    th.start()

def capture(*args):
    device = args[0]
    argv = args[1]
    path = args[2]

    cap = cv2.VideoCapture(int(device[-1]))

    then = utils.utc_now()

    last_update = None

    while((utils.utc_now() - then).total_seconds() < argv[2]):
        if (last_update is not None
            and (utils.utc_now()-last_update).total_seconds() < INTERVAL):
            continue
        utils.log('INFO', 'Grabbing frame...')
        last_update = utils.utc_now()
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize()

        # Display the resulting frame
        cv2.imshow('COMPUTER',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return
