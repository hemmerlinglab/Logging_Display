##################################
# Imports
##################################

import os
import csv
import time
import glob
import sys
import numpy as np
import datetime
from time import mktime

from read_in_config import read_config
from helper_functions import *

from get_data import *



def make_error_table(status_all):

    my_str = '<html>'
    for k in status_all.keys():
        my_str += '<tr><th>' + status_all[k]['label'] + '</th>' + status_all[k]['val'] + '</th>' + status_all[k]['err'] + '</th></tr>'
    my_str += '</html>'

    return my_str


def check_errors(sensors, data):

    # walk through all sensors and check if sensors are out of bound and updated

    status_all = {}
    for s in data.keys():
        if s in sensors.keys():            
            conversion = lambda x : eval(sensors[s]['conversion'])
            label_conversion = lambda x : eval(sensors[s]['label_conversion'])
            
            last_val = conversion(np.float(data[s]['y'][-1]))
            min_val = np.float(sensors[s]['low'])
            max_val = np.float(sensors[s]['high'])

            status_all[s] = {}
            status_all[s]['label'] = sensors[s]['label']
            status_all[s]['val'] = str(label_conversion(np.float(data[s]['y'][-1])))
            status_all[s]['err'] = ''

            if last_val <= min_val:
                status_all[s]['err'] = 'Low'
            elif last_val >= max_val:
                status_all[s]['err'] = 'High'

    return status_all


if __name__ == '__main__':

    sensors = read_config()

    # get today's date
    my_today = datetime.datetime.today()
    today = str(my_today.strftime('%Y-%m-%d'))

    # get all data
    data = get_data(main_path = 'logging/')

    status_all = check_errors(sensors, data)

    errtable = make_error_table(status_all)

 


