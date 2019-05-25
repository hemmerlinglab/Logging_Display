import os
import numpy as np
import csv
import sys
import glob
import time
#from bokeh.plotting import figure, show, output_file, save, gridplot
#from bokeh.models import Range1d
import datetime
from time import mktime
from scipy.interpolate import interp1d
import fileinput
from read_in_config import read_config

def conv_dt_to_epoch(dt):
    # dt is an array of datetimes

    #2018-05-02T23:10:02.000000000-0000
    dt2 = [datetime.datetime.strptime(m, '%Y-%m-%dT%H:%M:%S.000000000-0000') for m in dt]
    
    tarr = 1000.0 * np.array([mktime(m.timetuple()) + m.microsecond/1000.0 for m in dt2])

    return tarr

def readin_data(main_path, filename, extension = '.log', unit = ''):
    
    # reads in csv file with data
    # 2018/08/30-17:38:01,cool_in,74.267998,cool_out,73.693001,dc_power_status,1,he_high_pressure,224.000000,he_low_pressure,223.000000,he_temp,75.325996,motor_current,0.222085,msg,Ready To Start,msg_urgent,0,oil_temp,74.403000,three_phase_power,1
    # 2018/08/30-17:39:01,cool_in,74.267998,cool_out,73.707001,dc_power_status,1,he_high_pressure,224.000000,he_low_pressure,224.000000,he_temp,75.334999,motor_current,0.234595,msg,Ready To Start,msg_urgent,0,oil_temp,74.412003,three_phase_power,1

    compl_file = main_path + filename + extension
    x = []
    y = np.array([])

    output = {} # dictionary for data on all sensors in the file
    
    if os.path.isfile(compl_file):
        with open(compl_file, 'r') as f:
           for line in f.readlines():
               if not line.isspace():
                   l = line[:-1].split(',') # line[:-1] chops off the \n at the end of the line
                   hlp = l[0].split('-')[1]
                   dat = l[0].split('-')[0].replace('/','-')
                   hlp = list(hlp)
                   
                   hlp = [dat + 'T'] + hlp[0:] + ['.000000000-0000']

                   # get time stamp
                   x = "".join(hlp) # time stamp
        
                   # read in sensor data
                   sensor_data = l[1:]
        
                   for k in range(0, len(sensor_data), 2):
                        key = sensor_data[k]
                        
                        try:
                            val = sensor_data[k+1].strip() # trim white spaces
                        except:
                            key = 'N/A'
                            val = np.nan

                        # check if key already exists
                        if key in output:
                            output[key]['x'].append(x)
                            output[key]['y'].append(val)
                        else:
                            output[key] = {}
                            output[key]['x'] = [x]
                            output[key]['y'] = [val]
                            output[key]['title'] = filename
                        
    else:
        output = {}
        print('File ' + compl_file + ' does not exist.')
   
    return output

def readin_chilled_data(main_path, filename, extension = '.log', unit = '', allowed_keys = []):
    
    # reads in csv file with data
    # 2018/08/30-17:38:01,cool_in,74.267998,cool_out,73.693001,dc_power_status,1,he_high_pressure,224.000000,he_low_pressure,223.000000,he_temp,75.325996,motor_current,0.222085,msg,Ready To Start,msg_urgent,0,oil_temp,74.403000,three_phase_power,1
    # 2018/08/30-17:39:01,cool_in,74.267998,cool_out,73.707001,dc_power_status,1,he_high_pressure,224.000000,he_low_pressure,224.000000,he_temp,75.334999,motor_current,0.234595,msg,Ready To Start,msg_urgent,0,oil_temp,74.412003,three_phase_power,1

    compl_file = main_path + filename + extension
    x = []
    y = np.array([])

    output = {} # dictionary for data on all sensors in the file
    
    if os.path.isfile(compl_file):
        with open(compl_file, 'r') as f:
           for line in f.readlines():
               if not line.isspace():
                   l = line[:-1].split(',') # line[:-1] chops off the \n at the end of the line
                   hlp = l[0].split('-')[1]
                   dat = l[0].split('-')[0].replace('/','-')
                   hlp = list(hlp)
                   
                   hlp = [dat + 'T'] + hlp[0:] + ['.000000000-0000']

                   # get time stamp
                   x = "".join(hlp) # time stamp
        
                   # read in sensor data
                   sensor_data = l[1:]
        
                   for k in range(0, len(sensor_data), 2):
                        key = sensor_data[k]
                        
                        try:
                            val = sensor_data[k+1].strip() # trim white spaces
                        except:
                            key = 'N/A'
                            val = np.nan

                        # check if key already exists
                        if key in output:
                            output[key]['x'].append(x)
                            output[key]['y'].append(val)
                        else:
                            # check if key is an allowed key
                            if key in allowed_keys:
                                output[key] = {}
                                output[key]['x'] = [x]
                                output[key]['y'] = [val]
                                output[key]['title'] = filename
                        
    else:
        output = {}
        print('File ' + compl_file + ' does not exist.')
   
    return output

def readin_lab_temp_file(main_path, filename, extension = '.log', curr_weather = False):
    
    # reads in csv file with temperatures
    # 2018/04/30-00:00:37,0,283B3BAE090000CD,18.81,1,283B3BFE090000CD,38.81
    # change to read in log files
    # 2018/07/18-13:46:32,0,28D8CDAC09000080,24.62
    # 2018/07/18-13:46:33,1,285218AE0900002E,25.56      
    # 2018/07/18-13:46:34,2,28FECFAD09000088,25.62
    # 2018/07/18-13:46:35,3,283B3BAE090000CD,25.00

    x = []
    y = np.array([])

    output = {} # dictionary for data on all sensors in the file
    
    if not curr_weather:
        compl_file = main_path + filename + extension
    else:
        compl_file = main_path + filename + "_weather.csv"

    counter = 0
    flag = 0
    lst = []
    if os.path.isfile(compl_file):
        with open(compl_file, 'r') as f:
           for line in f.readlines():
               if not line.isspace():
                   l = line.split(',')
                   hlp = l[0].split('-')[1]
                   dat = l[0].split('-')[0].replace('/','-')
                   hlp = list(hlp)
                  
                   hlp = [dat + 'T'] + hlp[0:] + ['.000000000-0000']

                   #x.append("".join(hlp))
                   x = "".join(hlp)
        
                   # read in sensor data
                   # data format is assumed to be: NO0, ID0, T0, NO1, ID1, T1, ...
                   sensor_data = l[1:]
        
                   for k in range(0, len(sensor_data), 3):
                        s_no = sensor_data[k]
                        s_id = sensor_data[k+1]
                        s_T = np.float64(sensor_data[k+2])
        
                        # check if key already exists
                        if s_id in output:
                            output[s_id]['x'].append(x)
                            output[s_id]['y'].append(s_T)
                        else:
                            output[s_id] = {}
                            output[s_id]['x'] = [x]
                            output[s_id]['y'] = [s_T]
                            output[s_id]['title'] = filename
                        
                   #hlp = np.float64(l[1:])
            
                   #y = np.vstack((y, hlp)) if y.size else hlp
    else:
        output = {}
        print('File ' + compl_file + ' does not exist.')
    
    return output


def get_lab_temperatures(main_path = 'logging/Temperatures_Lab/', my_today = datetime.datetime.today()):

    filename = my_today.strftime('%Y-%m-%d')

    # read in data
    data = readin_lab_temp_file(main_path, filename)
    data.update(readin_lab_temp_file(main_path, filename, curr_weather = True))

    return (data)


def get_dewar_temperatures(main_path = 'logging/Dewar_Temperatures/', my_today = datetime.datetime.today()):

    filename = my_today.strftime('%Y-%m-%d') + '_dewar'

    # read in data
    data = readin_data(main_path, filename)

    return data

def get_chilled_water(main_path = 'logging/PulseTube_Chilled_Water/', my_today = datetime.datetime.today()):

    filename = my_today.strftime('%Y-%m-%d') + '_chilled_water_pulsetube'

    # read in data
    data = readin_chilled_data(main_path, filename, allowed_keys = ['temp','flow','pressure','hornet_pressure','UCR_in','UCR_out'])

    return data

def get_pulsetube(main_path = 'logging/PulseTube/', my_today = datetime.datetime.today()):

    filename = my_today.strftime('%Y-%m-%d') + '_pulsetube'

    # read in data
    data = readin_data(main_path, filename)

    return data


def get_temperatures():

    data = []

    data.append(get_lab_temperatures())
    data.append(get_dewar_temperatures())    
    data.append(get_chilled_water())
    data.append(get_pulsetube())

    # combine all data
    all_data = data[0].copy()
    for k in range(len(data)):
        #print(all_data.keys())
        all_data.update(data[k])

    return (all_data)



