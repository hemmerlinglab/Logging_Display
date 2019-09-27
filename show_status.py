#!/usr/bin/python3
##################################
# Imports
##################################

import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
import numpy as np
import scipy
import datetime
import fileinput
from scipy.interpolate import interp1d

import threading as thd
import time
from pygame import mixer


#from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
#if is_pyqt5():
#    from matplotlib.backends.backend_qt5agg import (
#        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
#else:
#    from matplotlib.backends.backend_qt4agg import (
#        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
#from matplotlib.figure import Figure

from get_data import *

from read_in_config import read_config

from analoggaugewidget import *

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Logging Plots'
        self.left = 3870
        self.top = 0
        self.width = 1700
        self.height = 920
        self.no_of_rows = 20

        self.update_interval = 1000 # ms
        self.no_of_points = 100

        self.sensors = read_config()

        # an array with all gauges
        self.all_gauges = []

        self.initUI()        

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.update_interval)

    def tick(self):

        data = get_data('/home/molecules/skynet/Logs/')
        newtime = data['he_temp']['x'][-1].split('T')[1].split('.')[0]

        self.lasttime.setText(str(newtime))
        self.nowtime.setText(time.strftime("%H:%M:%S",time.localtime()))

        self.no_of_points = int(self.no_of_points_to_plot_box.text())

        # toggle through all gauges and update their values
        for gauge in self.all_gauges:
            conversion = lambda x : eval(self.sensors[gauge.sensor_name]['conversion'])
            gauge.update_value(conversion(np.float(data[gauge.sensor_name]['y'][-1])))
        
        self.update()

    def get_settings(self, sensor):

        opts = {}

        opts['plot_min'] = np.float(self.sensors[sensor]['plot_min'])
        opts['plot_max'] = np.float(self.sensors[sensor]['plot_max'])
        opts['alert_low'] = np.float(self.sensors[sensor]['low'])
        opts['alert_high'] = np.float(self.sensors[sensor]['high'])
        opts['unit'] = self.sensors[sensor]['unit']
        opts['name'] = sensor
        opts['format'] = self.sensors[sensor]['format']
        opts['label'] = self.sensors[sensor]['label']
        opts['label_conversion'] = self.sensors[sensor]['label_conversion']

        return opts
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.tabs = QTabWidget()

        self.tab_main = QWidget()
        self.tab_pulse = QWidget()
        self.tab_pulse_press = QWidget()
        self.tab_log = QWidget()
        self.tab_settings = QWidget()

        self.tabs.addTab(self.tab_main, "Dewar")
        self.tabs.addTab(self.tab_pulse, "Pulse Tube")
        self.tabs.addTab(self.tab_settings, "Settings")
        self.tabs.addTab(self.tab_log, "Log")

        # gauge displays
        self.pt_cool_in = AnalogGaugeWidget(opts = self.get_settings('cool_in'))
        self.pt_cool_out = AnalogGaugeWidget(opts = self.get_settings('cool_out'))
        self.pt_oil_temp = AnalogGaugeWidget(opts = self.get_settings('oil_temp'))
        self.pt_he_temp = AnalogGaugeWidget(opts = self.get_settings('he_temp'))

        self.pt_ucr_in = AnalogGaugeWidget(opts = self.get_settings('UCR_in'))
        self.pt_ucr_out = AnalogGaugeWidget(opts = self.get_settings('UCR_out'))

        self.pt_flow = AnalogGaugeWidget(opts=self.get_settings('flow'))

        
        self.pt_he_high_p = AnalogGaugeWidget(opts = self.get_settings('he_high_pressure'))
        self.pt_he_low_p = AnalogGaugeWidget(opts = self.get_settings('he_low_pressure'))

        self.pt_motor_current = AnalogGaugeWidget(opts = self.get_settings('motor_current'))
        
        self.chilled_temp = AnalogGaugeWidget(opts = self.get_settings('temp'))
        
        self.dewar_0 = AnalogGaugeWidget(opts = self.get_settings('0'))
        self.dewar_1 = AnalogGaugeWidget(opts = self.get_settings('1'))
        self.dewar_2 = AnalogGaugeWidget(opts = self.get_settings('2'))
        self.dewar_3 = AnalogGaugeWidget(opts = self.get_settings('3'))
        self.dewar_4 = AnalogGaugeWidget(opts = self.get_settings('4'))
        self.dewar_5 = AnalogGaugeWidget(opts = self.get_settings('5'))
        self.dewar_6 = AnalogGaugeWidget(opts = self.get_settings('6'))
        self.dewar_7 = AnalogGaugeWidget(opts = self.get_settings('7'))

        
        self.rough_pressure = AnalogGaugeWidget(opts = self.get_settings('pressure'))
        self.hornet_pressure = AnalogGaugeWidget(opts = self.get_settings('hornet_pressure'))
        self.uhv_pressure = AnalogGaugeWidget(opts = self.get_settings('uhv'))

        # add all gauges in an array
        self.all_gauges.extend([
            self.pt_cool_in,
            self.pt_cool_out,
            self.pt_oil_temp,
            self.pt_flow,
            self.pt_he_temp,
            self.pt_ucr_in,
            self.pt_ucr_out,
            self.pt_he_high_p,
            self.pt_he_low_p,    
            self.pt_motor_current,
            self.chilled_temp,        
            self.dewar_0,
            self.dewar_1,
            self.dewar_2,
            self.dewar_3,
            self.dewar_4,
            self.dewar_5,
            self.dewar_6,
            self.dewar_7,
            self.rough_pressure,
            self.hornet_pressure,
            self.uhv_pressure
            ])

        # settings widgets
        self.update_interval_box = QLineEdit(str(self.update_interval))
        self.no_of_points_to_plot_box = QLineEdit(str(self.no_of_points))

        self.tab_main.layout = QGridLayout()
        self.tab_main.layout.addWidget(self.pt_cool_in, 0,0)
        self.tab_main.layout.addWidget(self.pt_ucr_in,1,0)
        self.tab_main.layout.addWidget(self.chilled_temp, 2,0)

        self.tab_main.layout.addWidget(self.pt_cool_out, 0,1)
        self.tab_main.layout.addWidget(self.pt_ucr_out,1,1)
        self.tab_main.layout.addWidget(self.pt_flow,2,1)
        self.tab_main.layout.addWidget(self.pt_he_temp, 3,0)
        
        self.tab_main.layout.addWidget(self.pt_he_high_p, 0,2)
        self.tab_main.layout.addWidget(self.pt_he_low_p, 1,2)

        self.tab_main.layout.addWidget(self.dewar_2, 0,3)
        self.tab_main.layout.addWidget(self.dewar_1, 1,3)
        self.tab_main.layout.addWidget(self.dewar_7, 2,3)
        self.tab_main.layout.addWidget(self.dewar_3, 3,3)
        self.tab_main.layout.addWidget(self.dewar_4, 0,4)
        self.tab_main.layout.addWidget(self.dewar_5, 1,4)
        self.tab_main.layout.addWidget(self.dewar_6, 2,4)
        self.tab_main.layout.addWidget(self.dewar_0, 3,4)

        self.tab_main.layout.addWidget(self.rough_pressure,2,2)
        self.tab_main.layout.addWidget(self.hornet_pressure,3,2)
        self.tab_main.layout.addWidget(self.uhv_pressure, 3,1)

        for k in range(4):
            self.tab_main.layout.setRowMinimumHeight(k, 200)
        for k in range(5):
            self.tab_main.layout.setColumnMinimumWidth(k, 200)

        self.tab_main.setLayout(self.tab_main.layout)

        self.tab_pulse.layout = QHBoxLayout()
        self.tab_pulse.setLayout(self.tab_pulse.layout)

        self.tab_pulse.layout.addWidget(self.pt_motor_current)
        self.tab_pulse.layout.addWidget(self.pt_oil_temp)

        self.tab_settings.layout = QGridLayout()
        self.update_interval_label = QLabel('Update Interval')
        self.tab_settings.layout.addWidget(self.update_interval_label,1,1)
        self.tab_settings.layout.addWidget(self.update_interval_box,1,2)
        self.no_points_label = QLabel('Number of Points to Plot')
        self.tab_settings.layout.addWidget(self.no_points_label,2,1)
        self.tab_settings.layout.addWidget(self.no_of_points_to_plot_box,2,2)
        self.tab_settings.setLayout(self.tab_settings.layout)

        self.lasttime_lab = QLabel('Last Read:')
        self.nowtime_lab = QLabel('Current Time:')
        self.lasttime = QLabel('NOW')
        self.nowtime = QLabel(time.strftime("%H:%M:%S",time.localtime()))
        self.blank_lab = QLabel(' '*40)

        self.layout = QVBoxLayout()
        self.times = QWidget()
        self.time_lay = QHBoxLayout()
        self.time_lay.addWidget(self.nowtime_lab)
        self.time_lay.addWidget(self.nowtime)
        self.time_lay.addWidget(self.lasttime_lab)
        self.time_lay.addWidget(self.lasttime)
        self.time_lay.addWidget(self.blank_lab)
        self.times.setLayout(self.time_lay)
        self.layout.addWidget(self.times)
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53,53,53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15,15,15))
        palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53,53,53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
             
        palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
     
        # Show widget
      
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.showMaximized()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main_thread = thd.Thread(target=main)
    main_thread.start()

    while True:
        if not main_thread.is_alive():
            break
        else:
            pass
        time.sleep(5)

    print('ERROR: GUI THREAD HAS CRASHED!!!')
    mixer.init()
    snd_file = '/home/molecules/software/Logging_Display/siren.wav'
    snd = mixer.Sound(snd_file)
    snd.play()
    time.sleep(15)
