import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QTabWidget, QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPalette, QPolygon, QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, pyqtSignal, QPoint
import numpy as np

class DewarTempWidget(QWidget):

	valueChanged = pyqtSignal(int)

	def __init__(self,parent = None,scl = 1.5,opts = []):
		super(DewarTempWidget,self).__init__(parent)

		min1 = 6.0
		max1 = 11.0
		min2 = 50.0
		max2 = 77.2

		if len(opts) > 0:
			self.mins=[]
			self.maxs=[]
			self.vals=[]
			for i,oi in enumerate(opts):
				self.mins.append(oi['plot_min'])
				self.maxs.append(oi['plot_max'])
				self.vals.append(oi['plot_min'])

			self.mins = [min2,min1,min1,min1,min1,min2,min2,min1]
			self.maxs = [max2,max1,max1,max1,max1,max2,max2,max1]

		else:
			foot40_val = 39.0
			bot40_val = 45.0
			top40_val = 60.0
			top4_val = 4.3
			bot4_val = 4.5
			foot4_val = 4.4
			cell_val = 10.0
			sorb_val = 8.0
			self.vals = [bot40_val,foot4_val,cell_val,bot4_val,sorb_val,foot40_val,top40_val,top4_val]
			self.mins = [min2,min1,min1,min1,min1,min2,min2,min1]
			self.maxs = [max2,max1,max1,max1,max1,max2,max2,max1]


		self.scl = scl
	def update_value(self,vals,mouse_controlled=False):
		self.vals=vals
		self.valueChanged.emit(vals)
		self.update()

	def paintEvent(self,event):
		self.top = 50
		self.left = 100
		width = int(self.scl*50)
		space = int(self.scl*10)
		self.bottom = self.top+10*width+5*space
		split = self.top+5*width+3*space
		self.right = self.left+7*space + 6*width
		top = self.top
		bottom = self.bottom
		left = self.left
		right = self.right
		foot40 = QPolygon([QPoint(left+width+space,top),QPoint(right-space-width,top),QPoint(right-space-width,top+width),QPoint(left+width+space,top+width)])
		bot40 = QPolygon([QPoint(left,top+split+space),QPoint(left+width,top+split+space),QPoint(left+width,bottom-width),QPoint(right-width,bottom-width),QPoint(right-width,top+split+space),QPoint(right,top+split+space),QPoint(right,bottom),QPoint(left,bottom)])
		top40 = QPolygon([QPoint(left,top+width+space),QPoint(right,top+width+space),QPoint(right,top+split),QPoint(right-width,top+split),QPoint(right-width,top+2*width+space),QPoint(left+width,top+2*width+space),QPoint(left+width,top+split),QPoint(left,top+split)])
		top4 = QPolygon([QPoint(left+width+space,top+3*width+3*space),QPoint(right-width-space,top+3*width+3*space),QPoint(right-width-space,top+split),QPoint(right-2*width-space,top+split),QPoint(right-2*width-space,top+4*width+3*space),QPoint(left+2*width+space,top+4*width+3*space),QPoint(left+2*width+space,top+split),QPoint(left+width+space,top+split)])
		bot4 = QPolygon([QPoint(left+width+space,top+split+space),QPoint(left+2*width+space,top+split+space),QPoint(left+2*width+space,bottom-2*width-space),QPoint(right-2*width-space,bottom-2*width-space),QPoint(right-2*width-space,top+split+space),QPoint(right-width-space,top+split+space),QPoint(right-width-space,bottom-width-space),QPoint(left+width+space,bottom-width-space)])
		foot4 = QPolygon([QPoint(left+2*width+space,top+2*width+2*space),QPoint(right-2*width-space,top+2*width+2*space),QPoint(right-2*width-space,top+3*width+2*space),QPoint(left+2*width+space,top+3*width+2*space)])
		cell = QPolygon([QPoint(left+2*width+2*space,top+split-width+space),QPoint(right-2*width-4*space,top+split-width+space),QPoint(right-2*width-4*space,top+split+width),QPoint(left+2*width+2*space,top+split+width)])
		sorb = QPolygon([QPoint(right-2*width-3*space,top+4*width+4*space),QPoint(right-2*width-2*space,top+4*width+4*space),QPoint(right-2*width-2*space,bottom-2*width-2*space),QPoint(right-2*width-3*space,bottom-2*width-2*space)])

		text_center = int((right+left)/2)
		half_width = top+int(width/2)
		text_vertical = [9*width+5*space+half_width,2*width+2*space+half_width,5*width+3*space+half_width,8*width+4*space+half_width,7*width+3*space+half_width,half_width,width+space+half_width,3*width+3*space+half_width]
		w = 200
		h = 50

		polys = [bot40,foot4,cell,bot4,sorb,foot40,top40,top4]

		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(QPen(Qt.white,1,Qt.SolidLine))
		for i,pi in enumerate(polys):
			# print(self.vals)
			if self.vals[i] <= self.mins[i]:
				painter.setBrush(QBrush(QColor(0,68,204,200),Qt.SolidPattern))
			elif self.vals[i] > self.maxs[i]:
				painter.setBrush(QBrush(QColor(204,0,34,200),Qt.SolidPattern))
			else:
				painter.setBrush(QBrush(QColor(255,187,51,200),Qt.SolidPattern))

			painter.drawPolygon(pi)
			painter.setFont(QFont('Decorative',20))
			painter.drawText(text_center-int(w/2),text_vertical[i]-int(h/2),w,h,Qt.AlignCenter,'{:.2f}K'.format(self.vals[i]))
		painter.end()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_gauge = DewarTempWidget()
	my_gauge.show()
	sys.exit(app.exec_())