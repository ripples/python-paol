#!/usr/bin/env python

'''
*_cap.py:
    capturing *.
'''
import cv2
from datetime import datetime, timedelta
import threading

import utils
import imgutils

INTERVAL = 1
THRESHHOLD = 0.9


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
    last_img = None

    while((utils.utc_now() - then).total_seconds() < argv[2]):
        if (last_update is not None
            and (utils.utc_now()-last_update).total_seconds() < INTERVAL):
            continue
        # Capture frame-by-frame
        ret, frame = cap.read()
        # cv2.imshow('WHITEBOARD',frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # Our operations on the frame come here
        if last_img is not None and imgutils.im_diff(frame, last_img) > THRESHHOLD:
            continue

        cv2.imwrite(path + 'whiteboard/' + str(int(utils.utc_now().timestamp())) + '.png', frame)

        # Display the resulting frame
        last_update = utils.utc_now()
        last_img = frame

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return
