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


from get_lab_temperature import *









class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 500
        self.no_of_rows = 20

        self.update_interval = 1000 # ms

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        
        self.timer.start(self.update_interval)

    def tick(self):
        print("hallo")
        get_lab_temperatures()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.tabs = QTabWidget()

        self.tab_main = QWidget()
        self.tab_aux = QWidget()
        self.tab_log = QWidget()

        self.tabs.addTab(self.tab_main, "Main")
        self.tabs.addTab(self.tab_aux, "Aux")
        self.tabs.addTab(self.tab_log, "Log")
        
        self.canvas = PlotCanvas(self, width=5, height=4)
        
        self.tab_main.layout = QVBoxLayout()
        self.tab_main.layout.addWidget(self.canvas)
        self.tab_main.setLayout(self.tab_main.layout)


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
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
      
        self.show()



class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.x = []
        self.y = []
        self.plot()
 
 
    def plot(self, fit_plot = None):
        ax = self.figure.add_subplot(111)
        # data
        ax.plot(self.x, self.y, 'ro')
        # fit
        if not fit_plot is None:
            (fit_x, fit_y) = fcn2min(fit_plot.params, self.x, None, plot_fit = True)
            ax.plot(fit_x, fit_y)
        
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

