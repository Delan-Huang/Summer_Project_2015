"""
Author: Delan Huang
Date: 07/01/2015
Version: 1.0

Purpose: Displays multiple textures onto a cube, each with a different color
"""

# Imports
from PySide import QtCore, QtOpenGL
from OpenGL.GL import *
from OpenGL import GLU
import numpy as np

class CubeGraphic(QtOpenGL.QGLWidget):
    sharedObject = 0

    coords = (
        ((+1, +1, +1), (-1, +1, +1), (-1, -1, +1), (+1, -1, +1)),  # first image
        ((+1, +1, -1), (+1, +1, +1), (+1, -1, +1), (+1, -1, -1)),  # second image
        ((-1, +1, -1), (+1, +1, -1), (+1, -1, -1), (-1, -1, -1)),  # third image
        ((-1, +1, +1), (-1, +1, -1), (-1, -1, -1), (-1, -1, +1)),  # fourth image
        ((-1, +1, +1), (+1, +1, +1), (+1, +1, -1), (-1, +1, -1)),  # fifth image
        ((-1, -1, -1), (+1, -1, -1), (+1, -1, +1), (-1, -1, +1)),  # sixth image
    )

    color = [
        (255, 0, 0),     # Red
        (0, 255, 0),     # Blue
        (0, 0, 255),     # Green
        (255, 255, 0),   # Yellow
        (255, 0, 255),   # Pink
        (0, 255, 255)    # Cyan
    ]

    def __init__(self, list1, list2, list3, list4, list5, list6, xDim, yDim, zDim):
        QtOpenGL.QGLWidget.__init__(self)
        # Commandline Variables
        self.list1 = list1
        self.list2 = list2
        self.list3 = list3
        self.list4 = list4
        self.list5 = list5
        self.list6 = list6
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim

        # User Controlled Variables
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.zoom = 5.0

        # Hard coded Variables
        self.imgHeight = 100
        self.imgWidth = 100
        self.imgByte = np.zeros((self.imgWidth, self.imgHeight, 4))  # creates an imgHeight x imgWidth x 4 array
        self.alpha = 255 # 0 is transparent, 255 is opaque
        self.lastPos = QtCore.QPoint()

    # Widget Based Getter and Setter Functions
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

    def minimumSizeHint(self):
        return QtCore.QSize(100, 100)

    # Cube Graphic Texture Functions and Overloads
    def makeTexture(self, r, g, b):
        for i in range(self.imgWidth):
            for j in range(self.imgHeight):
                self.imgByte[i][j][0] = r
                self.imgByte[i][j][1] = g
                self.imgByte[i][j][2] = b
                self.imgByte[i][j][3] = self.alpha

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslated(0.0, 0.0, -75.0)
        # Functions with variables update upon movement from sliders
        glScaled(self.zoom, self.zoom, self.zoom)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glTranslate(0.0, 0.0, 0.0)
        glTranslated(self.xPos / 20.0, self.yPos / 20.0, self.zPos / 20.0)
        glCallList(CubeGraphic.sharedObject)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        GLU.gluPerspective(10.0, width / height, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        self.textures = []
        for i in range(6):
            # Create a new texture for each face
            texture = glGenTextures(1)
            self.textures.append(texture)
            glBindTexture(GL_TEXTURE_2D, self.textures[i])
            # Edit values in imgByte 3d array and assign rgb value
            self.makeTexture(CubeGraphic.color[i][0],
                             CubeGraphic.color[i][1],
                             CubeGraphic.color[i][2])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                            GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.imgWidth,
                         self.imgHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                         self.imgByte)
        # Initialize
        CubeGraphic.sharedObject = self.makeObject()

        # Allow access to alpha value
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Change alpha dependent on variable (future = slider?)
        glBlendColor(0.0, 0.0, 0.0, self.alpha)
        glDisable(GL_CULL_FACE)

    def makeObject(self):
        dlist = glGenLists(1)
        glNewList(dlist, GL_COMPILE)

        for i in range(6):
            glBindTexture(GL_TEXTURE_2D, self.textures[i])

            glBegin(GL_QUADS)
            for j in range(4):
                tx = {False: 0, True: 1}[j == 0 or j == 3]
                ty = {False: 0, True: 1}[j == 0 or j == 1]
                glTexCoord2d(tx, ty)
                glVertex3d(0.2 * CubeGraphic.coords[i][j][0],
                           0.2 * CubeGraphic.coords[i][j][1],
                           0.2 * CubeGraphic.coords[i][j][2])

            glEnd()

        glEndList()
        return dlist