#!/usr/bin/env python

'''
config.py:
    Config R/W Utility
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
    j_dict = j_data[0]
    return j_dict


def load_config(key):
    '''
        Load conf from @CONFSRC and return corresponding val of @key
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
    j_dict = j_data[0]
    return j_dict.get(key)


def write_config(jdict):
    '''Write entries in @jdict to @CONFSRC'''
    with open(CONFSRC, 'w+') as f:
        j_data = json.load(f)
        j_data.update(jdict)
        json.dump(j_data, f)
