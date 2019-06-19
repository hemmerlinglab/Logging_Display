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
from time import mktime
from scipy.interpolate import interp1d
import fileinput

from read_in_config import read_config
from helper_functions import *
from get_data import *
from check_errors import *


def make_plot(my_title, xarr, yarr, colorarr, legarr):
        s = figure(
             width = 450, 
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

        s.legend.location = 'top_left'
              
        return s


def plot_fig(
        my_title = '',
        colorarr = [],
        sensorarr = []
        ):

    xarr = []
    yarr = []
    legendarr = []
    for key in sensorarr:
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

        ind = np.argsort(xd)
        xd = xd[ind]
        y = y[ind]

        last_value = " ({1:{0}} {2})".format(sensors[key]['format'], label_conversion(y[-1]), sensors[key]['unit'])

        xarr.append(xd)
        yarr.append(y)
        legendarr.append(sensors[key]['label'] + last_value)

    return make_plot(my_title, xarr, yarr, colorarr, legendarr)




####################################
# main
####################################

sensors = read_config()

# get today's date
my_today = datetime.datetime.today()
today = str(my_today.strftime('%Y-%m-%d'))

date = today
# get all data
data = get_data(main_path = '/home/lab-user/Lab/Group/Logs/')

s1 = plot_fig(
        my_title = date + '- PulseTube',
        colorarr = ['blue', 'red', 'orange', 'green'],
        sensorarr = ['cool_in', 'cool_out', 'oil_temp', 'he_temp']
        )

s2 = plot_fig(
        my_title = date + '- PulseTube',
        colorarr = ['red','blue'],
        sensorarr = ['he_high_pressure', 'he_low_pressure']
        )

s3 = plot_fig(
        my_title = date + '- PulseTube',
        colorarr = ['black'],
        sensorarr = ['motor_current']
        )

s4 = plot_fig(
        my_title = date + '- Chilled Water',
        colorarr = ['red', 'blue', 'orange', 'green'],
        sensorarr = ['temp', 'flow', 'UCR_in', 'UCR_out']
        )

s5 = plot_fig(
        my_title = date + '- Pressures',
        colorarr = ['red', 'black'],
        sensorarr = ['pressure', 'hornet_pressure']
        )

s6 = plot_fig(
        my_title = date + '- Dewar Temperature',
        colorarr = ['blue', 'red', 'black', 'green'],
        sensorarr = ['0', '1', '2', '3']
        )



p = gridplot([[s1, s2, s3], [s4, s5, s6]])


## export as png
##output_file('k0.html')
#export_png(p, filename='fig0.png')
#
##os.system('cat k0.html > index.html')
#os.system('echo "<img src="fig0.png"></img><hr>" > index.html')



# export as actual plot
output_file('k0.html')
save(p)

os.system('cat k0.html > index.html')
os.system('echo "<hr>" >> index.html')


# check errors

status_all = check_errors(sensors, data)

errtable = make_error_table(status_all)

send_email(status_all)

f = open('../status/index.html', 'w')
f.write(errtable)
f.close()

