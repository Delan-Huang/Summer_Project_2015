"""
Author: Delan Huang
Date: 06/16/2016
Plan:
- Display Cube
- Have an X/Y translation slider
- Have an X/Y rotator slider
- Zoom input entry box
"""

import sys
import math
from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Cube Model",
                            "PyOpenGL must be installed to run this model.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class MainWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #Initialize main Window Widgets
        self.zoomBoxLabel = self.QLabel('Zoom Value', self)
        self.zoomBox = self.QLineEdit()
        self.cubeGraphic = CubeGraphic()

        self.xRotator = self.createXRotator(QtCore.SIGNAL("xRotationChanged(int)"),
                                            self.cubeGraphic.setXRotation)
        self.xSlider = self.QSlider()

        self.yRotator = self.createYRotator(QtCore.SIGNAL("yRotationChanged(int)"),
                                            self.cubeGraphic.setYRotation)
        self.ySlider = self.QSlider()

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(3)
        hbox.addWidget(self.zoomBoxLabel)
        hbox.addWidget(self.zoomBox)
        hbox.addWidget(self.cubeGraphic)
        hbox.addWidget(self.xRotator)
        hbox.addWidget(self.xSlider)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(self.yRotator)
        vbox.addWidget(self.ySlider)

        self.setLayout(vbox)

        self.setGeometry(900, 900, 900, 150)
        self.setWindowTitle("Cube Model")
        self.show()

    def createXRotator(self, changedSignal, setterSlot):
        rotator = QtGui.QSlider(QtCore.Qt.Horizontal)

        rotator.setRange(0, 360 * 16)
        rotator.setSingleStep(16)
        rotator.setPageStep(15 * 16)
        rotator.setTickInterval(15 * 16)
        rotator.setTickPosition(QtGui.QSlider.TicksUp) #Do testing on this parameter

        return rotator

    def createYRotator(self, changedSignal, setterSlot):
        rotator = QtGui.QSlider(QtCore.Qt.Vertical)

        rotator.setRange(0, 360 * 16)
        rotator.setSingleStep(16)
        rotator.setPageStep(15 * 16)
        rotator.setTickInterval(15 * 16)
        rotator.setTickPosition(QtGui.QSlider.TicksLeft) #D

        return rotator
class CubeGraphic(QtOpenGL.QGLWidget):
    def __init__(self, parent =None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        #Borrowed colors from example
        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def getXRot(self):
        return self.xRot

    def getYRot(self):
        return self.yRot

    def getZRot(self):
        return self.zRot

    def minimumSizeHint(self):
        return QtCore.QSize(50,50)

    def sizeHint(self):
        return QtCore.QSize(400,400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

def main():

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


