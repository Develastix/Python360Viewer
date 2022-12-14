from PyQt5.QtWidgets import QApplication,QWidget, QMainWindow,QHBoxLayout
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
import sys

from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap, QTransform
from os.path import expanduser, dirname
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QMenu, QLabel

class MyPlotWidget(pg.PlotWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def wheelEvent(self,event):
    #     #this works
    #     print("wheel event")
    
    # def mouseReleaseEvent(self, event):
    #     #this works
    #     print("mouse released")

    # def mousePressEvent(self, event):
    #     #this works
    #     print("mousepressed")

class MainWidget(QMainWindow):


    def __init__(self, parent=None):
        super(MainWidget, self).__init__()
        self.resize(400,200)
        self.setMouseTracking(True)

        self.graphWidget = MyPlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        data = np.random.randn(10)
        self.graphWidget.plot(data)

        myLayout = QHBoxLayout()
        myLayout.addWidget(self.graphWidget)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(myLayout)

    # def mouseReleaseEvent(self, event):
    #     #this is not working
    #     print("mouse released")

    # def mousePressEvent(self, event):
    #     #this is working
    #     print("mousepressed")

    # def wheelEvent(self,event):
    #     #this is not working
    #     print("wheelevent?")      
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_Equal or event.key() == QtCore.Qt.Key_E:
            self.zoomIn()
        elif event.key() == QtCore.Qt.Key_Minus or event.key() == QtCore.Qt.Key_D:
            self.zoomOut()
        elif event.key() == QtCore.Qt.Key_1:
            self.zoomReset()   
        
    def zoomIn(self):
        self.zoom *= 1.05
        self.updateView()

    def zoomOut(self):
        self.zoom /= 1.05
        self.updateView()

    def zoomReset(self):
        self.zoom = 1
        self.updateView()   
        
        def fitView(self):
            self.view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
            if self.rotate == 0:
                self.zoom = self.view.transform().m11()
            elif self.rotate == -90:
                self.zoom = (self.view.transform().m12()) * -1
            elif self.rotate == -180:
                self.zoom = (self.view.transform().m11()) * -1
            else:
                self.zoom = self.view.transform().m12()

    def updateView(self):
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))

def window():
    app = QApplication(sys.argv)
    win = MainWidget()

    win.show()
    sys.exit(app.exec_())

window()