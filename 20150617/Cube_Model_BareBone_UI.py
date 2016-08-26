"""
Author: Delan Huang
Date: 06/17/2015
Plan: Create MainWindow with UI elements (no functionality)

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
        self.zoomBoxLabel = QtGui.QLabel('Zoom Value', self)
        self.zoomBox = QtGui.QLineEdit(self)
        self.cubeGraphic = CubeGraphic(self)

        self.xRotator = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.xSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        self.yRotator = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.ySlider = QtGui.QSlider(QtCore.Qt.Vertical, self)

        #Set up layout
        self.mainCanvas = QtGui.QHBoxLayout(self)
        self.rightCanvas = QtGui.QVBoxLayout(self)
        self.zoomCanvas = QtGui.QHBoxLayout(self)

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
        # #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

        self.setGeometry(150, 150, 640, 480)
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

