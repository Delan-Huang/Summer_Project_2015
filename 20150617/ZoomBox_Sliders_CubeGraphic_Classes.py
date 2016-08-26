"""
Author: Delan Huang
Date: 06/17/2015
Purpose: Holds all of the Classes needed for CubeModel_FrontEnd.py
"""

# imports
import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

class ZoomBox(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

class RotSlider(QtGui.QWidget):
    moved = QtCore.Signal(int)

    def __init__(self, orientation="QtCore.Qt.Horizontal", min=0, max=360,
                 singleStep=16, pageStep=16, tickInterval=16,
                 tickPosition= "QtGui.QSlider.TicksAbove"):
        QtGui.QWidget.__init__(self)

        self.slider = QtGui.QSlider(orientation)
        self.slider.setRange(min, max * 16)
        self.slider.setSingleStep(singleStep)
        self.slider.setPageStep(pageStep * 16)
        self.slider.setTickInterval(tickInterval * 16)
        self.TickPosition(tickPosition)

        self.rotation = 0

    def setRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.rotation:
            self.rotation = angle
            self.emit(angle)
            self.updateGL()

class YRotSlider(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

class XTranslationSlider(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

class YTranslationSlider(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

class CubeGraphic(QtOpenGL.QGLWidget):
    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)


