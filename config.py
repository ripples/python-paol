#!/usr/bin/env python

'''
config.py:
    Config R/W Utility

    format:
        [device:type_num, ]

    type:type_num
        'NOT_SET':0,
        'DISABLED':1,
        'LECTURE(w/ AUDIO)':2,
        'WHITEBOARD':3,
        'BLACKBOARD':4,
        'COMPUTER':5,
'''

import json
import os

import utils


CONFSRC = "conf.json"


def load_all_config():
    '''
        Load conf from @CONFSRC and return dict
        return None if no conf file is found
        return None if no conf entries is found
    '''
    utils.log('INFO', 'Loading all Conf...')
    j_file = None
    try:
        j_file = open(CONFSRC)
    except IOError:
        utils.log('WARN', 'No config file found.')
        return None
    j_str = j_file.read()
    j_data = json.loads(j_str)
    # Check if entries are empty
    if len(j_data) < 1:
        utils.log('WARN', 'Conf file contents no configs.')
        return None
    j_dict = j_data
    return j_dict


def is_config_invalid():
    '''Check if not all NOT_SET or out-dated'''
    utils.log('INFO', 'Checking Config')
    j_file = None
    try:
        j_file = open(CONFSRC)
    except IOError:
        utils.log('WARN', 'No config file found.')
        return None
    j_str = j_file.read()
    j_data = json.loads(j_str)
    # Check if entries are empty
    if len(j_data) < 1:
        utils.log('WARN', 'Conf file contents no configs.')
        return None
    j_dict = j_data

    dev_list = os.listdir('/dev')
    video_devices = [s for s in dev_list if "video" in s]

    # Check if device count matches config file count
    if len(video_devices) != len(j_dict.items()):
        utils.log('INFO', 'Config validation is outdated.')
        return False

    ret = False
    for entry in j_dict.values():
        if entry is not '0':
            ret = True
    utils.log('INFO', 'Config validation returns ' + str(ret))
    return ret


def load_config(key):
    '''
        Load conf from @CONFSRC and return corresponding val of @key
        return None if no conf file is found
        return None if no conf entries is found
    '''
    utils.log('INFO', 'Loading Conf...')
    j_file = None
    try:
        j_file = open(CONFSRC)
    except IOError:
        utils.log('WARN', 'No config file found.')
        return None
    j_str = j_file.read()
    j_data = json.loads(j_str)
    # Check if entries are empty
    if len(j_data) < 1:
        utils.log('WARN', 'Conf file contents no configs.')
        return None
    j_dict = j_data
    return j_dict.get(key)


def add_config(jdict):
    '''Add entries in @jdict to @CONFSRC'''
    with open(CONFSRC, 'w+') as f:
        j_data = json.load(f)
        j_data.update(jdict)
        json.dump(j_data, f)


def write_config(jdict):
    '''Write entries in @jdict to @CONFSRC'''
    with open(CONFSRC, 'w+') as f:
        json.dump(jdict, f)
