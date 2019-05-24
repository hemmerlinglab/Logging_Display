##################################
# Imports
##################################

import sys
from PyQt5.QtWidgets import QLineEdit, QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
import numpy as np
import scipy
import datetime
import fileinput
from scipy.interpolate import interp1d




#from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
#if is_pyqt5():
#    from matplotlib.backends.backend_qt5agg import (
#        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
#else:
#    from matplotlib.backends.backend_qt4agg import (
#        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
#from matplotlib.figure import Figure

from get_temperatures import *

from read_in_config import read_config

from analoggaugewidget import *

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Logging Plots'
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 500
        self.no_of_rows = 20

        self.update_interval = 1000 # ms
        self.no_of_points = 100

        self.sensors = read_config()        

        self.initUI()        

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.update_interval)

    def tick(self):

        data = get_temperatures()

        self.no_of_points = int(self.no_of_points_to_plot_box.text())

        self.pt_he_temp.update_value(np.float(data['he_temp']['y'][-1]))
        self.pt_oil_temp.update_value(np.float(data['oil_temp']['y'][-1]))
        self.pt_cool_in.update_value(np.float(data['cool_in']['y'][-1]))
        self.pt_cool_out.update_value(np.float(data['cool_out']['y'][-1]))
        self.pt_motor_current.update_value(np.float(data['motor_current']['y'][-1]))
        self.pt_he_high_p.update_value(np.float(data['he_high_pressure']['y'][-1]))
        self.pt_he_low_p.update_value(np.float(data['he_low_pressure']['y'][-1]))
        
        self.pt_he_low_p.update_value(np.float(data['he_low_pressure']['y'][-1]))
        self.pt_he_low_p.update_value(np.float(data['he_low_pressure']['y'][-1]))


            
        conversion = lambda x : eval(self.sensors['temp']['conversion'])
        self.chilled_temp.update_value(conversion(np.float(data['temp']['y'][-1])))
        
        self.dewar_0.update_value(np.float(data['0']['y'][-1]))
        self.dewar_1.update_value(np.float(data['1']['y'][-1]))
        self.dewar_2.update_value(np.float(data['2']['y'][-1]))
        self.dewar_3.update_value(np.float(data['3']['y'][-1]))
        self.dewar_4.update_value(np.float(data['4']['y'][-1]))
        self.dewar_5.update_value(np.float(data['5']['y'][-1]))
        self.dewar_6.update_value(np.float(data['6']['y'][-1]))
        self.dewar_7.update_value(np.float(data['7']['y'][-1]))

    def get_settings(self, sensor):

        opts = {}

        opts['plot_min'] = np.float(self.sensors[sensor]['plot_min'])
        opts['plot_max'] = np.float(self.sensors[sensor]['plot_max'])
        opts['alert_low'] = np.float(self.sensors[sensor]['low'])
        opts['alert_high'] = np.float(self.sensors[sensor]['high'])
        opts['unit'] = self.sensors[sensor]['unit']
        opts['name'] = sensor
        opts['label'] = self.sensors[sensor]['label']

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

        self.pt_ucr_in = AnalogGaugeWidget(opts = self.get_settings('ucr_in'))
        self.pt_ucr_out = AnalogGaugeWidget(opts = self.get_settings('ucr_out'))

        
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

        # settings widgets
        self.update_interval_box = QLineEdit(str(self.update_interval))
        self.no_of_points_to_plot_box = QLineEdit(str(self.no_of_points))

        self.tab_main.layout = QGridLayout()
        self.tab_main.layout.addWidget(self.pt_cool_in, 0,0)
        self.tab_main.layout.addWidget(self.pt_cool_out, 0,1)
        self.tab_main.layout.addWidget(self.pt_oil_temp, 0,2)
        self.tab_main.layout.addWidget(self.pt_he_temp, 0,3)
        self.tab_main.layout.addWidget(self.chilled_temp, 0,4)
        
        self.tab_main.layout.addWidget(self.pt_he_high_p, 1,0)
        self.tab_main.layout.addWidget(self.pt_he_low_p, 1,1)

        self.tab_main.layout.addWidget(self.pt_motor_current, 1,2)

        self.tab_main.layout.addWidget(self.pt_ucr_in,1,3)
        self.tab_main.layout.addWidget(self.pt_ucr_out,1,4)
        
        self.tab_main.layout.addWidget(self.dewar_0, 2,0)
        self.tab_main.layout.addWidget(self.dewar_1, 2,1)
        self.tab_main.layout.addWidget(self.dewar_2, 2,2)
        self.tab_main.layout.addWidget(self.dewar_3, 2,3)
        self.tab_main.layout.addWidget(self.dewar_4, 3,0)
        self.tab_main.layout.addWidget(self.dewar_5, 3,1)
        self.tab_main.layout.addWidget(self.dewar_6, 3,2)
        self.tab_main.layout.addWidget(self.dewar_7, 3,3)

        for k in range(4):
            self.tab_main.layout.setRowMinimumHeight(k, 200)
        for k in range(5):
            self.tab_main.layout.setColumnMinimumWidth(k, 200)

        self.tab_main.setLayout(self.tab_main.layout)

        self.tab_pulse.layout = QHBoxLayout()
        self.tab_pulse.setLayout(self.tab_pulse.layout)

        self.tab_settings.layout = QVBoxLayout()
        self.tab_settings.layout.addWidget(self.update_interval_box)
        self.tab_settings.layout.addWidget(self.no_of_points_to_plot_box)
        self.tab_settings.setLayout(self.tab_settings.layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout) 
 
        # Show widget
      
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

