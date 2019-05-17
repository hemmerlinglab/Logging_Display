##################################
# Imports
##################################

import sys
from PyQt5.QtWidgets import QLineEdit, QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout
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
        #print("hallo")
        data = get_temperatures()

        self.no_of_points = int(self.no_of_points_to_plot_box.text())


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

        # settings widgets
        self.update_interval_box = QLineEdit(str(self.update_interval))
        self.no_of_points_to_plot_box = QLineEdit(str(self.no_of_points))

        self.tab_main.layout = QVBoxLayout()
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

