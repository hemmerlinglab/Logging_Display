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
import smtplib

from time import mktime

from read_in_config import read_config
from helper_functions import *

from get_data import *



def make_error_table(status_all):

    my_str = '<html><table>'
    for k in np.sort(status_all.keys()):
        my_str += '<tr><td>' \
            + status_all[k]['label']  \
            + '</td><td>' \
            + status_all[k]['val'] \
            + ' ' \
            + status_all[k]['unit'] \
            + '</td><td><font color="red">' \
            + status_all[k]['err'] \
            + '</font></td></tr>' \

    my_str += '</table></html>'

    return my_str


def check_errors(sensors, data):

    # walk through all sensors and check if sensors are out of bound and updated

    status_all = {}
    for s in data.keys():
        if s in sensors.keys():            
            conversion = lambda x : eval(sensors[s]['conversion'])
            label_conversion = lambda x : eval(sensors[s]['label_conversion'])
            
            raw_val = np.float(data[s]['y'][-1])
            last_val = conversion(raw_val)
            min_val = np.float(sensors[s]['low'])
            max_val = np.float(sensors[s]['high'])


            status_all[s] = {}
            status_all[s]['label'] = sensors[s]['label']
            status_all[s]['val'] = "{1:{0}}".format(sensors[s]['format'], conversion(raw_val))
            status_all[s]['unit'] = sensors[s]['unit']
            status_all[s]['err'] = ''

            if last_val <= min_val:
                status_all[s]['err'] = 'Low (limit: ' + str(min_val) + ')'
            elif last_val >= max_val:
                status_all[s]['err'] = 'High (limit: ' + str(max_val) + ')'

    return status_all

def send_email(status):

    # check if token file exists. if exists, don't send email

    exists = os.path.isfile('error_msg.log')

    if not exists:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("hemmerlinglab@gmail.com", "alcl261!!!")
        #text = msg.as_string()
    
        msg = ''
        for k in status.keys():
            if len(status[k]['err'])>0:
                msg +=  status[k]['label']  \
                + ' - ' \
                + status[k]['val'] \
                + ' ' \
                + status[k]['unit'] \
                + ' - ' \
                + status[k]['err'] \
                + "\n"
    
        mytext = 'Subject: {}\n\n{}'.format('Sensor Alert', msg)

        email_recipients = "boergeh@ucr.edu,jdaniel4103@gmail.com,kaylajrox@gmail.com"

        server.sendmail("lab", email_recipients.split(","), mytext)
    
        #  write file to stop the email alert
        f = open('error_msg.log', 'w')
        f.write(mytext)
        f.close()




if __name__ == '__main__':

    sensors = read_config()

    # get today's date
    my_today = datetime.datetime.today()
    today = str(my_today.strftime('%Y-%m-%d'))

    # get all data
    #data = get_data(main_path = 'logging/')
    data = get_data(main_path = '/home/lab-user/Lab/Group/Logs/')

    status_all = check_errors(sensors, data)

    errtable = make_error_table(status_all)

    send_email(status_all) 


