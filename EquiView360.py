import os
import sys
import math
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QDesktopWidget
from PyQt5 import QtCore
import Equirec2Perspec as E2P 
import cv2
import platform 

from PyQt5.QtGui import (
    QPainter,
    QBrush,
    QPen,
    QFont,
    QIcon,
    QTransform,
    QPalette,
    QColor,
)

from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QProgressDialog #cw

# Linux systems need this env var
if platform.system() == 'Linux':
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
else :
    pass

# Main windows
class Window(QDialog):
    def __init__(self):

        # Initialisation of the vars
        super().__init__()
        self.title = "Equirectangular 360° Viewer"
        self.posh = 0
        self.posw = 0
        self.save = QPoint(0,0)
        self.fov = 100
        self.imgPath = cv2.imread('./example.jpg', cv2.IMREAD_COLOR)
        self.equ = E2P.Equirectangular(self.imgPath)
        self.width = 1080
        self.height = 720
        self.setFixedSize(self.width, self.height)
        self.InitWindow()
        self.zoom = 1
        
        # Mouse wheel zooming.
        # self.wheelZoomFactor = 1.25  # Set to None or 1 to disable
        
        # self.graphicsView.viewport().installEventFilter(self)
        # self.graphicsView.viewport().installEventFilter(self)
        # self.graphicsView.installEventFilter(self)

    # Create the windows
    def InitWindow(self):

        # Setting icon title and geometry
        self.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        # Centering the windows
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Setting the image into the windows
        self.labelImage = QLabel(self)
        self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))
        self.show()

    # Image creation photo to get the correct perspective
    def img(self, fov, tet, fi) :
        img = self.equ.GetPerspective(fov, tet, fi, self.height, self.width)
        qimg = QtGui.QImage(img.data, self.width, self.height, self.width * 3, QtGui.QImage.Format_BGR888)
        return qimg

    # Key movement 
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            self.posh -= 30
            self.labelImage.setPixmap(QPixmap(self.img( self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Up:
            self.posh  += 30
            self.labelImage.setPixmap(QPixmap(self.img( self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Left:
            self.posw  -= 30
            self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))
        if event.key() == QtCore.Qt.Key_Right:
            self.posw  += 30
            self.labelImage.setPixmap(QPixmap(self.img(self.fov, self.posw, self.posh)))

    # Mouse press event for the mouse movement function
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    # Mouse movement function - Generate the correct perspective on each mouse moves
    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        self.delta =  (self.mousePos - event.pos()) + self.save
        self.labelImage.setPixmap(QPixmap(self.img(self.fov, (self.delta.x() / 10 + self.posh), (-self.delta.y() / 10 + self.posw))))

    def mousescroll(self, event):
        self.wheelZoomFactor = 1.25
    
    # def on_mouse_scroll(x, y, scroll_x, scroll_y):
    #     # printing some message
    #     print("Mouse scrolled")
        
    # def wheelEvent(self,event):
    #     #this is not working
    #     print("wheelevent?")    
    

    
    # def wheelEvent(self, event):
    #     x = event.angleDelta().y() / 120
    #     if x > 0:
    #         self.zoom *= 1.05
    #         self.updateView()
    #     elif x < 0:
    #         self.zoom /= 1.05
    #         self.updateView()
            
    # def updateView(self):
    #     self.setTransform(QtGui.QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
    
    # def eventFilter(self, source, event):
    #     if source == self.graphicsView.viewport() and event.type() == event.Wheel:
    #         x = event.angleDelta().y() / 120
    #         if x > 0:
    #             self.zoom *= 1.05
    #             self.updateView()
    #         elif x < 0:
    #             self.zoom /= 1.05
    #             self.updateView()
    #         return True
    #     return super().eventFilter(source, event)
    
    # def zoomFactor(self, newZoomFactor):
    #     if newZoomFactor < 1.0:
    #         self._pixmapItem.setTransformationMode(QtCore.Qt.SmoothTransformation)
    #     else:
    #         self._pixmapItem.setTransformationMode(QtCore.Qt.FastTransformation)
    #     self._view.zoomFactor = newZoomFactor
    
    # def wheelEvent ( self, event ) :
    #     self.zoom_step = 1.1 
    #     zoom_in = event.angleDelta ( )     
    #     if zoom_in.y ( ) > 0 :
    #         zoom = self.zoom_step  
    #     else :
    #         zoom = 1 / self.zoom_step
    #         print ( "zoom" ,zoom ) 
    #     self.scale ( zoom,zoom ) 
    #     print ( "view" ,self.scale ( zoom,zoom ) )
        
    # def wheelEvent(self, event):        
    #     '''Zoom In/Out with CTRL + mouse wheel'''
    #     if event.modifiers() == Qt.ControlModifier:
    #         self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))
    #     else:
    #         return QGraphicsView.wheelEvent(self, event)
        
    # def wheelEvent(self,event):
    #     self.x =self.x + event.delta()/120
    #     print (self.x)
    #     self.label.setText("Total Steps: "+QString.number(self.x))
    
    # def eventFilter(self, source, event):
    #     if (source == self.graphicsView.viewport() and 
    #         event.type() == QtCore.QEvent.Wheel):
    #             if event.angleDelta().y() > 0:
    #                 scale = 1.25
    #             else:
    #                 scale = .8
    #             self.graphicsView.scale(scale, scale)
    #             # do not propagate the event to the scroll area scrollbars
    #             return True
    #     elif event.type() == QtCore.QEvent.GraphicsSceneMousePress:
    #     # ...
    #         return super().eventFilter(source,event)
    
    # def wheelEvent(self, event):
    #     if event.angleDelta().y() > 0:
    #         self.zoomIn()
    #     else:
    #         self.zoomOut()
    #     return super(Klassenname, self).wheelEvent(event)
    
    # def eventFilter(self, obj, event):
    #     if obj is self.graphicsView and event.type() == QtCore.QEvent.Wheel:
    #         if event.angleDelta().y() > 0:
    #             self.zoomIn()
    #         else:
    #             self.zoomOut()
    #     return super(Klassenname, self).eventFilter(obj, event)

    # def wheelEvent(self, event):
    #     x = event.angleDelta().y() / 120
    #     if x > 0:
    #         self.zoom *= 1.05
    #         self.updateView()
    #     elif x < 0:
    #         self.zoom /= 1.05
    #         self.updateView()

    # def updateView(self):
    #     self.Transform(QtGui.QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
    
    # def wheelEvent(self, event):
    #     """Zoom in/out"""
    #     self.scaleView(math.pow(2.0, event.angleDelta().y() / 240.0))
        
    # def scaleView(self, scaleFactor):
    #     """Transform function and zoom QrecF is the area visible"""
    #     factor = (
    #         self.transform()
    #         .scale(scaleFactor, scaleFactor)
    #         .mapRect(QRectF(0, 0, 50, 50))
    #         .width()
    #     )
    #     if factor < 0.07 or factor > 100:
    #         return
    #     self.scale(scaleFactor, scaleFactor)
        
    #     # Update the cursor position on mouse release
    #     def mouseReleaseEvent(self, event):
    #         self.save = self.delta
    
    # def wheelEvent(self, event):
    #     """
    #     Zoom in the view with the mouse wheel.
    #     """
    #     self.currentState = 'ZOOM_VIEW'
    #     self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    #     inFactor = 1.15
    #     outFactor = 1 / inFactor

    #     if event.delta() > 0:
    #         zoomFactor = inFactor
    #     else:
    #         zoomFactor = outFactor

    #     self.scale(zoomFactor, zoomFactor)
    #     self.currentState = 'DEFAULT'

# Launch the application
if __name__ =='__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())