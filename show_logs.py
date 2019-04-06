##################################
# Imports
##################################

import sys
from PyQt5.QtWidgets import QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
import numpy as np
import scipy
import datetime
import fileinput
from scipy.interpolate import interp1d


from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from get_temperatures import *

from read_in_config import read_config


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

        self.sensors = read_config()        

        self.initUI()        

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        
        self.timer.start(self.update_interval)

    def tick(self):
        #print("hallo")
        data = get_temperatures()

        #print(data.keys())

        # update all plots
        self.main_plot.plot(data, ['0', '1', '2', '3'], self.sensors, colors = ['g-', 'k-', 'r-', 'b-']) 
        
        self.pulsetube_plot.plot(data, ['he_temp', 'oil_temp', 'cool_in', 'cool_out'], self.sensors, ymin = 50.0, ymax = 100.0, colors = ['g-', 'y-', 'r-', 'b-']) 
        
        self.pulsetube_press_plot.plot(data, ['he_high_pressure', 'he_low_pressure'], self.sensors, ymin = 150.0, ymax = 250.0, colors = ['r-', 'b-']) 
        
        self.pulsetube_curr_plot.plot(data, ['motor_current'], self.sensors, ymin = 0.0, ymax = 12.0, colors = ['k-']) 
        
        self.chilled_water_plot.plot(data, ['temp'], self.sensors, ymin = 0.0, ymax = 100.0, colors = ['k-']) 

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.tabs = QTabWidget()

        self.tab_main = QWidget()
        self.tab_pulse = QWidget()
        self.tab_pulse_press = QWidget()
        self.tab_log = QWidget()

        self.tabs.addTab(self.tab_main, "Dewar")
        self.tabs.addTab(self.tab_pulse, "Pulse Tube")
        self.tabs.addTab(self.tab_log, "Log")
        
        self.main_plot = PlotCanvas(self, width=5, height=4)
        self.pulsetube_plot = PlotCanvas(self, width=5, height=4)
        self.room_plot = PlotCanvas(self, width=5, height=4)
        self.pulsetube_press_plot = PlotCanvas(self, width=5, height=4)
        self.pulsetube_curr_plot = PlotCanvas(self, width=5, height=4)
        self.chilled_water_plot = PlotCanvas(self, width=5, height=4)
        
        self.tab_main.layout = QVBoxLayout()
        self.tab_main.layout.addWidget(self.main_plot)
        self.tab_main.setLayout(self.tab_main.layout)

        self.tab_pulse.layout = QHBoxLayout()
        self.tab_pulse.layout.addWidget(self.pulsetube_plot)
        self.tab_pulse.layout.addWidget(self.pulsetube_press_plot)
        self.tab_pulse.layout.addWidget(self.pulsetube_curr_plot)
        self.tab_pulse.layout.addWidget(self.chilled_water_plot)
        self.tab_pulse.setLayout(self.tab_pulse.layout)



        ##self.createTable()
 
        #self.button = QPushButton('Fit', self)
        #self.button.setToolTip('This is an example button')
        #self.button.move(100,70)
        ##self.button.clicked.connect(self.button_click)


        #self.canvas.move(0,0)

        #self.textbox = QTextEdit()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QHBoxLayout()
        #self.layout.addWidget(self.tableWidget) 
        #self.layout.addWidget(self.canvas) 
        self.layout.addWidget(self.tabs) 
        #self.layout.addWidget(self.textbox) 
        self.setLayout(self.layout) 
 
        # Show widget
      
        self.show()



class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        self.axes = self.fig.add_subplot(111)
 
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        #self.fig.draw()
        #self.plot(0,0)
 
 
    def plot(self, data, sensors, sensor_config, ymin = 0, ymax = 300, colors = [], fit_plot = None):
        
        self.axes.clear()
        legs = []
        for n, s in enumerate(sensors):
            x = np.array(data[s]['x'], dtype = np.datetime64)
            y = np.array(data[s]['y'], dtype = np.float)

            ind = np.argsort(x)
            x = x[ind]
            y = y[ind]

            x = x[-100:]
            y = y[-100:]

            legs.append(data[s]['title'])

            #print(len(x))

            self.axes.plot(x, y, colors[n], label = sensor_config[s]['location'])

            #line = 
            #line.set_ydata(y)
            #self.axes.draw_artist(line)
          
        self.axes.set_ylim([ymin, ymax])

        self.axes.legend()
        #self.axes.set_yticks([298.0])
        #self.axes.set_yticklabels(['298.0'])

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

