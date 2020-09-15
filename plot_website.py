##################################
# Imports
##################################

import os
import csv
import time
import glob
import sys
import numpy as np
from bokeh.plotting import figure, show, output_file, save, gridplot
from bokeh.models import Range1d, LinearAxis, Span, Label
from bokeh.io import export_png
import datetime
from datetime import timedelta
from time import mktime
from scipy.interpolate import interp1d
import fileinput

from read_in_config import read_config
from helper_functions import *
from get_data import *
from check_errors import *


def replace_invalid_values(arr, sensor):

    # this function replaces all values which are invalid with np.nan
    # e.g. sensor['invalid_values'] = [[1.0e2, 1.0e7]]

    # check if invalid values are given
    for inv_interval in sensor['invalid_values']:

        low = inv_interval[0]
        high = inv_interval[1]

        # check if values are inside the invalid values interval
        arr[(arr > low) & (arr < high)] = np.nan

    return arr


def make_plot(my_title, xarr, yarr, colorarr, legarr, limits_arr):
        s = figure(
             width = 340, 
             height = 350, 
             title = my_title,
             x_axis_type = "datetime",
             tools = "",
             #y_range = [y_min, y_max],
             #tools = "pan,wheel_zoom,box_zoom,reset",
             #active_scroll="wheel_zoom"
             )

        for k in range(len(xarr)):
            s.line(xarr[k], yarr[k], color = colorarr[k], legend = legarr[k])

            if len(limits_arr[k])==2:
                s.renderers.extend([Span(location=limits_arr[k][0], dimension='width', line_dash = 'dashdot', line_color=colorarr[k], line_width=1)])
                s.renderers.extend([Span(location=limits_arr[k][1], dimension='width', line_dash = 'dashed', line_color=colorarr[k], line_width=1)])

        s.legend.location = 'top_left'
              
        return s


def plot_fig(
        data,
        my_title = '',
        colorarr = [],
        sensorarr = [],
        limit_lines = False
        ):

    xarr = []
    yarr = []
    legendarr = []
    limit_lines_arr = []
    for key in sensorarr:
        
        if key in data.keys():
            x = data[key]['x']

            # conversion from raw data to plot value
            conversion = lambda x : eval(sensors[key]['conversion'])
            label_conversion = lambda x : eval(sensors[key]['label_conversion'])

            # if there is an issue, try to transform each element individually
            y = []
            for n in range(len(data[key]['y'])):
                try:
                    y.append(conversion(np.float64(data[key]['y'][n])))
                except:
                    y.append(np.nan)

            y = np.array(y)

            xd = np.array(x, dtype = np.datetime64)

            # sort x, y data
            ind = np.argsort(xd)
            xd = xd[ind]
            y = y[ind]

            # replace invalid values
            y = replace_invalid_values(y, sensors[key])


            # moving average
            # not build in yet

            last_value = " ({1:{0}} {2})".format(sensors[key]['format'], label_conversion(y[-1]), sensors[key]['unit'])
        else:
            xd = []
            y = []
            last_value = " (nan)"

        xarr.append(xd)
        yarr.append(y)
        legendarr.append(sensors[key]['label'] + last_value)
        if limit_lines:
            limit_lines_arr.append([np.float(sensors[key]['low']), np.float(sensors[key]['high'])])
        else:
            limit_lines_arr.append([])

    return make_plot(my_title, xarr, yarr, colorarr, legendarr, limit_lines_arr)


def get_plots(data, date):
    s1 = plot_fig(
            data,
            my_title = date + '- PulseTube',
            colorarr = ['blue', 'red', 'orange', 'green'],
            sensorarr = ['cool_in', 'cool_out', 'oil_temp', 'he_temp'],
            limit_lines = True
            )
    
    s2 = plot_fig(
            data,
            my_title = date + '- PulseTube',
            colorarr = ['red','blue'],
            sensorarr = ['he_high_pressure', 'he_low_pressure'],
            limit_lines = True
            )
    
    s3 = plot_fig(
            data,
            my_title = date + '- PulseTube',
            colorarr = ['black'],
            sensorarr = ['motor_current']
            )
    
    s4 = plot_fig(
            data,
            my_title = date + '- Chilled Water',
            colorarr = ['red', 'orange', 'green'],
            sensorarr = ['temp', 'UCR_in', 'UCR_out']
            )
    
    s5 = plot_fig(
            data,
            my_title = date + '- Pressures',
            colorarr = ['red', 'black', 'blue'],
            sensorarr = ['pressure', 'hornet_pressure', 'uhv']
            )
    
    s6 = plot_fig(
            data,
            my_title = date + '- Dewar Temperature',
            colorarr = ['blue', 'red', 'black'],
            sensorarr = ['5', '6', '0']
            )
    
    s6_b = plot_fig(
            data,
            my_title = date + '- Dewar Temperature',
            colorarr = ['yellow', 'blue', 'red', 'black', 'green'],
            sensorarr = ['1', '4', '7', '3', '2']
            )
    
    s7 = plot_fig(
            data,
            my_title = date + '- Chilled Water',
            colorarr = ['blue'],
            sensorarr = ['flow']
            )
    
    return gridplot([[s1, s2, s3, s7], [s4, s5, s6, s6_b]])




####################################
# main
####################################

sensors = read_config()

# get today's date
my_today = datetime.datetime.today()
today = str(my_today.strftime('%Y-%m-%d'))
yesterday = str((my_today - timedelta(1)).strftime('%Y-%m-%d'))

date = today

# get all data
data = get_data(main_path = '/home/lab-user/Lab/Group/Logs/', my_date = today)
data_yesterday = get_data(main_path = '/home/lab-user/Lab/Group/Logs/', my_date = yesterday)

p = get_plots(data, today)
p_yesterday = get_plots(data_yesterday, yesterday)

## export as png
##output_file('k0.html')
#export_png(p, filename='fig0.png')
#
##os.system('cat k0.html > index.html')
#os.system('echo "<img src="fig0.png"></img><hr>" > index.html')

# export as actual plot
output_file('k0.html')
save(p)

output_file('k1.html')
save(p_yesterday)


os.system('cat k0.html > index.html')
os.system('echo "<hr>" >> index.html')
os.system('cat k1.html >> index.html')
os.system('echo "<hr>" >> index.html')


# check errors

status_all = check_errors(sensors, data)

errtable = make_error_table(status_all)

send_email(status_all)

os.system('cat html_base.html > ../status/index.html')
f = open('../status/index.html', 'a')
f.write(errtable)
f.close()

