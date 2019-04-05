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

def readin_file(main_path, filename, extension = '.log', curr_weather = False):
    
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



###########################################################
# main
###########################################################

def get_lab_temperatures(main_path = '/home/molecules/logging/Temperatures_Lab/'):

    # get today's date
    my_today = datetime.datetime.today()


    filename = my_today.strftime('%Y-%m-%d')

    # read in data
    data = readin_file(main_path, filename)
    data_outside = readin_file(main_path, filename, curr_weather = True)
  
   
    sensors = read_config()

    print(sensors) 


    ## list of sensors with their properties
    ## location, low_T, high_T
    #sensor_table = {
    #    	'283825AD090000C2' : {'location':'Room5','low_T':15.0,'high_T':25.0},
    #    	'289AB0AE0900001D' : {'location':'Room55','low_T':15.0,'high_T':25.0},
    #    	'28D8CDAC09000080' : {'location':'A/C Outlet','low_T':15.0,'high_T':25.0},
    #    '285218AE0900002E' : {'location':'Electron Table (5x12)','low_T':15.0,'high_T':25.0},
    #    '28FECFAD09000088' : {'location':'Molecule Table (5x10)','low_T':15.0,'high_T':25.0},
    #    '283B3BAE090000CD' : {'location':'Server/Room','low_T':15.0,'high_T':25.0},
    #    'currT' : {'location':'Riverside - T','low_T':5.0,'high_T':25.0},
    #    'currH' : {'location':'Riverside - H','low_T':15.0,'high_T':25.0}
    #    }


    #s.line(xd, y, line_color = colors[n], legend = sensor_table[s_id]['location'])

    


    return data
