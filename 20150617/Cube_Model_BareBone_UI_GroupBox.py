"""
Author: Delan Huang
Date: 06/17/2015
Plan: Create MainWindow with UI elements (no functionality)
Experiment Failed. Did not find any difference between Splitter and GroupBox in current UI
"""

#imports
import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GL

class MainWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        #Initialize main Window Widgets
        zoomBoxLabel = QtGui.QLabel('Zoom Value', self)
        zoomBox = QtGui.QLineEdit(self)
        cubeGraphic = CubeGraphic(self)

        xRotator = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        xSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        yRotator = QtGui.QSlider(QtCore.Qt.Vertical, self)
        ySlider = QtGui.QSlider(QtCore.Qt.Vertical, self)

        #Set up layout
        hbox = QtGui.QHBoxLayout(self)

        zoomCanvas = QtGui.QGroupBox(self) #Top of Right Canvas
        zoomCanvas.addWidget(zoomBoxLabel)
        zoomCanvas.addWidget(zoomBox)

        xFunctionCanvas = QtGui.QGroupBox(self) #Bottom of Right Canvas
        xFunctionCanvas.addWidget(xRotator)
        xFunctionCanvas.addWidget(xSlider)

        yFunctionCanvas = QtGui.QGroupBox(self) #Left Canvas
        yFunctionCanvas.addWidget(yRotator)
        yFunctionCanvas.addWidget(ySlider)

        rightCanvas = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        rightCanvas.addWidget(zoomCanvas)
        rightCanvas.addWidget(cubeGraphic)
        rightCanvas.addWidget(xFunctionCanvas)

        hbox.addWidget(yFunctionCanvas)
        hbox.addWidget(rightCanvas)
        self.setLayout(hbox)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

        self.setGeometry(150, 150, 900, 600)
        self.setWindowTitle("Cube Model")
        self.show()

class CubeGraphic(QtOpenGL.QGLWidget):
     def __init__(self, parent =None):
        QtOpenGL.QGLWidget.__init__(self, parent)


def main():

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

__author__ = 'Delan'
