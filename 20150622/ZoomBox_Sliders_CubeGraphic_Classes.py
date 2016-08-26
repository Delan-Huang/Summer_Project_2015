"""
Author: Delan Huang
Date: 06/22/2015
Purpose: Holds all of the Classes needed for CubeModel_FrontEnd.py
Version: 1.0, PySide

Notes:
- Slider Classes not fully functioning.
    - To fix this: make class accept defaults, but still create a function
    createSlider()
- CubeGraphic Class not universal, may be taken out and moved
  into Cube_Model_PySide.py
"""

# imports
import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

class LabelledLineEdit(QtGui.QWidget):
    def __init__(self, labelText="TestLabel"):
        super(LabelledLineEdit, self).__init__()

        self.label = QtGui.QLabel(labelText)
        self.lineEdit = QtGui.QLineEdit()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

class RotSlider(QtGui.QWidget):
    def __init__(self, minRange=0, maxRange=360,
                 singleStep=16, pageStep=16, tickInterval=16):
        super(RotSlider, self).__init__()

        self.slider = QtGui.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(minRange, maxRange * 16)
        self.slider.setSingleStep(singleStep)
        self.slider.setPageStep(pageStep * 16)
        self.slider.setTickInterval(tickInterval * 16)
        self.slider.setTickPosition(QtGui.QSlider.TicksAbove)

        self.rotation = 0

class Slider(QtGui.QWidget):
    def __init__(self):
        super(Slider, self).__init__()

        self.minRange = 0
        self.maxRange = 360
        self.singleStep = 16
        self.pageStep = 16
        self. tickInterval = 16

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(self.minRange, self.maxRange * 16)
        self.slider.setSingleStep(self.singleStep)
        self.slider.setPageStep(self.pageStep * 16)
        self.slider.setTickInterval(self.tickInterval * 16)
        self.slider.setTickPosition(QtGui.QSlider.TicksAbove)


class CubeGraphic(QtOpenGL.QGLWidget):
    def __init__(self):
        super(CubeGraphic, self).__init__()

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.zoom = 5.0

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

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -50.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glTranslate(-0.5, -0.5, -0.5)
        GL.glTranslated(self.xPos / 5.0, self.yPos / 5.0, self.zPos / 5.0)
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
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]]

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

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged"), self.xRot)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged"), self.yRot)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

    def setXPosition(self, distance):
        if distance != self.xPos:
            self.xPos = distance
            self.emit(QtCore.SIGNAL("xPositionChanged"), self.xPos)
            self.updateGL()

    def setYPosition(self, distance):
        if distance != self.yPos:
            self.yPos = distance
            self.emit(QtCore.SIGNAL("yPositionChanged"), self.yPos)
            self.updateGL()

    # Unsupported Code(no Widget uses this function)
    # def setZPosition(self, distance):
    #     self.updateGL()

    def setZoom(self, new_zoom):
        if new_zoom != self.zoom:
            self.zoom = new_zoom
            self.emit(QtCore.SIGNAL("scaleChanged"), self.zoom)
            self.updateGL()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

