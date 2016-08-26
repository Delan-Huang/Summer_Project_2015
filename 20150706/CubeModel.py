"""
Author: Delan Huang
Date: 07/02/2015
Purpose: Uses CubeGraphic Class
Version: 1.1, PySide

- Next Objective:
"""

# imports
import sys
import subprocess
from PySide import QtGui

from CubeGraphic import *


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Initialize main Window Widgets
        self.cubeGraphic = CubeGraphic()
        self.zoomBoxLabel = QtGui.QLabel('Zoom Value', self)
        self.zoomBox = QtGui.QDoubleSpinBox()
        self.zoomBox.setRange(1.0, 20.0)
        self.cubeGraphic.connect(self.zoomBox, QtCore.SIGNAL("valueChanged(double)"),
                                 self.cubeGraphic.setZoom)

        self.xRotator = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.xRotator.setRange(0, 360 * 16)
        self.xRotator.setSingleStep(16)
        self.xRotator.setPageStep(16 * 16)
        self.xRotator.setTickInterval(16 * 16)
        self.xRotator.setTickPosition(QtGui.QSlider.TicksAbove)
        self.cubeGraphic.connect(self.xRotator, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setXRotation)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("xRotationChanged(int)"),
                     self.xRotator, QtCore.SLOT("setValue(int)"))

        self.xSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.xSlider.setRange(0, 30)
        self.xSlider.setValue(0)
        self.xSlider.setSingleStep(1)
        self.xSlider.setPageStep(1)
        self.xSlider.setTickInterval(1)
        self.xSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.cubeGraphic.connect(self.xSlider, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setXPosition)
        # self.connect(self.cubeGraphic, QtCore.SIGNAL("xPositionChanged(int)"), self.xSlider,
        #              QtCore.SLOT("setValue(int)"))

        self.yRotator = QtGui.QSlider(QtCore.Qt.Vertical)
        self.yRotator.setRange(0, 360 * 16)
        self.yRotator.setSingleStep(15)
        self.yRotator.setPageStep(16 * 16)
        self.yRotator.setTickInterval(16 * 16)
        self.yRotator.setTickPosition(QtGui.QSlider.TicksRight)
        self.cubeGraphic.connect(self.yRotator, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setYRotation)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("yRotationChanged(int)"),
                     self.yRotator, QtCore.SLOT("setValue(int)"))

        self.ySlider = QtGui.QSlider(QtCore.Qt.Vertical)
        self.ySlider.setRange(0, 20)
        self.ySlider.setValue(0)
        self.ySlider.setSingleStep(1)
        self.ySlider.setPageStep(1)
        self.ySlider.setTickInterval(1)
        self.ySlider.setTickPosition(QtGui.QSlider.TicksRight)
        self.cubeGraphic.connect(self.ySlider, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setYPosition)
        # self.connect(self.cubeGraphic, QtCore.SIGNAL("yPositionChanged(int)"), self.ySlider,
        #              QtCore.SLOT("setValue(int)"))

        # Set up layout
        self.mainCanvas = QtGui.QHBoxLayout()
        self.rightCanvas = QtGui.QVBoxLayout()
        self.zoomCanvas = QtGui.QHBoxLayout()

        self.zoomCanvas.addWidget(self.zoomBoxLabel)
        self.zoomCanvas.addWidget(self.zoomBox)
        self.rightCanvas.addLayout(self.zoomCanvas)
        self.rightCanvas.addWidget(self.cubeGraphic)
        self.rightCanvas.addWidget(self.xRotator)
        self.rightCanvas.addWidget(self.xSlider)

        self.mainCanvas.addWidget(self.ySlider)
        self.mainCanvas.addWidget(self.yRotator)
        self.mainCanvas.addLayout(self.rightCanvas)
        self.setLayout(self.mainCanvas)

        # Set Defaults

        self.setGeometry(150, 150, 500, 500)
        self.setWindowTitle("Cube Model")


def main():
    # Execute program
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
