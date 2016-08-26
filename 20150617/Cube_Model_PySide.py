"""
Author: Delan Huang
Date: 06/17/2015
Plan: Finish Program
- Add in Translation functionality
    - Look at glTranslate + update setXPosition etc
- Add in Zooming functionality
    - Look at glPixelZoom + update zoom EntryBox
"""

# imports
import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        # NOTE: UI is built, but widgets do NOT have functionality

        # Initialize main Window Widgets
        self.zoomBoxLabel = QtGui.QLabel('Zoom Value', self)
        self.zoomBox = QtGui.QLineEdit()  # Need to add int only / validator, and to restrict size
        self.cubeGraphic = CubeGraphic()

        self.xRotator = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.xRotator.setRange(0, 360 * 16)
        self.xRotator.setSingleStep(16)
        self.xRotator.setPageStep(16 * 16)
        self.xRotator.setTickInterval(16 * 16)
        self.xRotator.setTickPosition(QtGui.QSlider.TicksAbove)
        self.cubeGraphic.connect(self.xRotator, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setXRotation)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("xRotationChanged(int)"), self.xRotator,
                     QtCore.SLOT("setValue(int)"))

        self.xSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.xSlider.setRange(0, 360 * 16)
        self.xSlider.setSingleStep(15)
        self.xSlider.setPageStep(16 * 16)
        self.xSlider.setTickInterval(16 * 16)
        self.xSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.cubeGraphic.connect(self.xSlider, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setXPosition)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("xPositionChanged(int)"), self.xSlider,
                     QtCore.SLOT("setValue(int)"))

        self.yRotator = QtGui.QSlider(QtCore.Qt.Vertical)
        self.yRotator.setRange(0, 360 * 16)
        self.yRotator.setSingleStep(15)
        self.yRotator.setPageStep(16 * 16)
        self.yRotator.setTickInterval(16 * 16)
        self.yRotator.setTickPosition(QtGui.QSlider.TicksRight)
        self.cubeGraphic.connect(self.yRotator, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setYRotation)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("yRotationChanged(int)"), self.yRotator,
                     QtCore.SLOT("setValue(int)"))

        self.ySlider = QtGui.QSlider(QtCore.Qt.Vertical)
        self.ySlider.setRange(0, 360 * 16)
        self.ySlider.setSingleStep(16)
        self.ySlider.setPageStep(16 * 16)
        self.ySlider.setTickInterval(16 * 16)
        self.ySlider.setTickPosition(QtGui.QSlider.TicksRight)
        self.cubeGraphic.connect(self.ySlider, QtCore.SIGNAL("valueChanged(int)"),
                                 self.cubeGraphic.setYPosition)
        self.connect(self.cubeGraphic, QtCore.SIGNAL("yPositionChanged(int)"), self.ySlider,
                     QtCore.SLOT("setValue(int)"))

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
        self.xRotator.setValue(120 * 16)
        self.yRotator.setValue(120 * 16)

        self.setGeometry(150, 150, 640, 480)
        self.setWindowTitle("Cube Model")


class CubeGraphic(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0

        self.lastPos = QtCore.QPoint()

    def getXRot(self):
        return self.xRot

    def getYRot(self):
        return self.yRot

    def getZRot(self):
        return self.zRot

    def getXPos(self):
        return self.xPos

    def getYPos(self):
        return self.yPos

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

    # def setZRotation(self, angle):
    #     angle = self.normalizeAngle(angle)
    #     if angle != self.zRot:
    #         self.zRot = angle
    #         self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
    #         self.updateGL()

    def setXPosition(self, distance):
        if distance != self.xPos:
            self.xPos = distance
            self.emit(QtCore.SIGNAL("xPositionChanged(int)"), distance)
            self.updateGL()

    def setYPosition(self, distance):
        if distance != self.yPos:
            self.emit(QtCore.SIGNAL("yPositionChanged(int)"), distance)
            self.updateGL()

    # Unsupported Code(no Widget uses this function)
    # def setZPosition(self, distance):
    #     self.updateGL()

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -50.0)
        GL.glScale(20.0, 20.0, 20.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glTranslate(-0.5, -0.5, -0.5)
        # GL.glTranslated(self.xPos, 0.0, 0.0)
        # GL.glTranslated(0.0, self.yPos, 0.0)
        # GL.glTranslated(0.0, 0.0, self.zPos)

        # GL.glCallList(self.object)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)
        GL.glVertexPointerf(self.cubeVtxArray)
        GL.glColorPointerf(self.cubeClrArray)
        GL.glDrawElementsui(GL.GL_QUADS, self.cubeIdxArray)

    def initGeometry(self):
        self.cubeVtxArray = (
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.cubeIdxArray = [
            0, 1, 2, 3,
            3, 2, 6, 7,
            1, 0, 4, 5,
            2, 1, 5, 6,
            0, 3, 7, 4,
            7, 6, 5, 4]
        self.cubeClrArray = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0]]

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # GL.glOrtho(-1.5, +1.5, -1.5, +1.5, 4.0, 15.0)
        GLU.gluPerspective(50.0, width / height, 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.initGeometry()

        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)

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
