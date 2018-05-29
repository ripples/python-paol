#!/usr/bin/env python

'''
init_setup.py:
    Setup Hardware Config.
    Only works under Ubuntu Python 3
'''

from PIL import Image as Im
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import threading
import datetime
import imutils
import cv2
import numpy as np
import os
import time
import subprocess

import utils
import config

SELECTIONS = {
    'NOT_SET':0,
    'DISABLED':1,
    'LECTURE(w/ AUDIO)':2,
    'WHITEBOARD':3,
    'BLACKBOARD':4,
    'COMPUTER':5,
}


class SetupGUI:
    def __init__(self):
        # Get available video devices
        utils.log('INFO', 'Searching for available video devices...')
        dev_list = os.listdir('/dev')
        video_devices = [s for s in dev_list if "video" in s]
        video_devices.sort()
        self.devices = video_devices
        utils.log('INFO', 'Found ' + str(len(video_devices)) + ' video devices:')
        for item in video_devices:
            utils.log('INFO', ' ' + item)

        self.count = len(video_devices)
        self.caps = []
        self.frames = []
        self.threads = []
        self.stop_event = None

        # initialize the root window and widgets
        self.res = self.get_res()
        self.root = Tk()
        self.root.title('Setup GUI')
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        # Add a grid
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack()

        self.panels = []
        self.type_vars = []
        self.setup_menus = []
        for i in range(len(video_devices)):
            self.panels.append(None)

            self.type_vars.append(StringVar())
            self.type_vars[i].set('NOT_SET')
            self.type_vars[i].trace('w', self.type_selected)

            self.setup_menus.append(OptionMenu(self.mainframe, self.type_vars[i], *SELECTIONS))

        # Grid widgets
        for c in range(len(video_devices)):
            self.setup_menus[c].grid(row=1, column=c)

        # Start threads constantly pulling image from all video devices
        self.stop_event = threading.Event()
        for i in range(len(video_devices)):
            self.caps.append(cv2.VideoCapture(int(self.devices[i][-1])))
            self.frames.append(None)
            self.threads.append(threading.Thread(target=self.video_loop, args=(i,)))
            self.threads[i].start()

    def get_res(self):
        output = subprocess.Popen('xrandr | grep \* | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
        resolution = output.split()[0].split(b'x')
        utils.log('INFO', 'current Resolution: ' + str(resolution[0]) + 'x' + str(resolution[1]))
        return int(resolution[0]), int(resolution[1])


    def type_selected(self, *args):
        utils.log('INFO', 'Config updated:')
        j_dict = {}
        for i in range(len(self.type_vars)):
            utils.log('INFO', str(self.devices[i]) + ' caps ' + self.type_vars[i].get())
            j_dict[self.devices[i]] = SELECTIONS[self.type_vars[i].get()]
        config.write_config(j_dict)


    def video_loop(self, *args):
        f = open("./logs/gui_err.log", "w+")
        sto = sys.stderr
        sys.stderr = f
        i = args[0]
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stop_event.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of WIDTH/count pixels
                ret, self.frames[i] = self.caps[i].read()
                ratio = ((1.0 * self.res[0])/self.count)/self.frames[i].shape[0]
                self.frames[i] = cv2.resize(self.frames[i], (int(self.frames[i].shape[0]*ratio), int(self.frames[i].shape[1]*ratio)))
                # utils.log('INFO', 'Resized: ' + str(self.frames[i].shape))

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frames[i], cv2.COLOR_BGR2RGB)
                image = Im.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panels[i] is None:
                    self.panels[i] = Label(self.mainframe, image=image)
                    self.panels[i].image = image
                    self.panels[i].grid(row=0, column=i)

                # otherwise, simply update the panel
                else:
                    self.panels[i].configure(image=image)
                    self.panels[i].image = image
            exit
        except RuntimeError as e:
            utils.log('WARN', 'RuntimeError on GUI.')
            utils.log('INFO', 'Check logs/gui_err.log for details.')

    def on_close(self):
        utils.log('INFO', 'Closing SETUP Window...')
        self.stop_event.set()
        self.root.quit()
        # for c in self.caps:
        #     c.release()


def main():
    sg = SetupGUI()
    sg.root.mainloop()

if __name__=="__main__":
    main()
