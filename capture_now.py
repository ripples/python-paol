#!/usr/bin/env python

'''
capture_now.py:
    Manual entry point of the capturing system.

    Argv[1]: {Current Semester}
    Argv[2]: {Current Course}
    Argv[3]: {Duration in sec}
'''

import sys
import os
import signal
import json
import time
from datetime import datetime
from pathlib import Path

import utils
import config
import init_setup
import lec_cap, bb_cap, wb_cap, comp_cap

NOT_SET = 0
DISABLED = 1
LECTURE = 2
WHITEBOARD = 3
BLACKBOARD = 4
COMPUTER = 5
RECORDING_FOLDER = str(Path.home()) + '/recordings/'


def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    args = sys.argv[1:]
    if len(args) != 3:
        utils.log('ERR ', 'Invalid Arguments')
        return
    capture(args)
    return


def capture(args):
    '''captures according to config file'''
    if not config.load_all_config() or not config.is_config_valid():
        utils.log('WARN', 'Hardware not configured. Running init setup GUI...')
        init_setup.main()
        utils.log('WARN', 'Please restart the program.')
        exit(0)

    then = datetime.utcnow()

    utils.log('INFO', 'Preparing saving path...')
    time_str = then.strftime("%m-%d-%y--%H-%M-%S")
    save_path = RECORDING_FOLDER + 'readyToUpload/' + args[0] + '/' + args[1] + '/' + time_str + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        os.makedirs(save_path+'whiteboard/')
        os.makedirs(save_path+'blackboard/')
        os.makedirs(save_path+'computer/')
    elif not os.path.exists(save_path+'whiteboard/'):
        os.makedirs(save_path+'whiteboard/')
    elif not os.path.exists(save_path+'blackboard/'):
        os.makedirs(save_path+'blackboard/')
    elif not os.path.exists(save_path+'computer/'):
        os.makedirs(save_path+'computer/')
    utils.log('INFO', 'Saving to ' + save_path)


    utils.log('INFO', 'Start capturing ' + str(args))
    conf = config.load_all_config()
    wb_count = 0
    com_count = 0
    for value in conf.values():
        if str(value) is str(WHITEBOARD):
            wb_count += 1
        elif str(value) is str(COMPUTER):
            com_count += 1
    utils.writeINFO(save_path, wb_count, com_count, args)
    st = None

    for device, type in conf.items():
        utils.log('INFO', 'Triggerring ' + device)
        type = int(type)
        if type == LECTURE:
            utils.log('INFO', ' LECTURE')
            st = lec_cap.trigger_cap(device, args, save_path)
        elif type == WHITEBOARD:
            utils.log('INFO', ' WHITEBOARD')
            wb_cap.trigger_cap(device, args, save_path)
        elif type == BLACKBOARD:
            utils.log('INFO', ' BLACKBOARD')
            bb_cap.trigger_cap(device, args, save_path)
        elif type == COMPUTER:
            utils.log('INFO', ' COMPUTER')
            comp_cap.trigger_cap(device, args, save_path)

    if st:
        _, err = st.communicate()
        utils.log('INFO', 'LecCap Error: '+str(err))


    while (datetime.utcnow() - then).total_seconds() < args[2]:
        pass
    return '0'


if __name__ == '__main__':
    main()
