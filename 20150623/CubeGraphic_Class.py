"""
Author: Delan Huang
Date: 06/23/2015
Version: 1.0

Note:
"""

# Imports
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL import GLU
from PIL import Image
from PIL.Image import open
import logging
from OpenGL.GL.ARB import texture_non_power_of_two

log = logging.getLogger(__name__)


class CubeGraphic(QtOpenGL.QGLWidget):
    sharedObject = 0

    coords = (
        ((+1, +1, +1), (-1, +1, +1), (-1, -1, +1), (+1, -1, +1)), # first image
        ((+1, +1, -1), (+1, +1, +1), (+1, -1, +1), (+1, -1, -1)), # second image
        ((-1, +1, -1), (+1, +1, -1), (+1, -1, -1), (-1, -1, -1)), # third image
        ((-1, +1, +1), (-1, +1, -1), (-1, -1, -1), (-1, -1, +1)), # fourth image
        ((-1, +1, +1), (+1, +1, +1), (+1, +1, -1), (-1, +1, -1)), # fifth image
        ((-1, -1, -1), (+1, -1, -1), (+1, -1, +1), (-1, -1, +1)), # sixth image



    )

    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.zoom = 5.0
        self.imageID = self.loadImage("icon1.png")
        self.alpha = 1.0
        self.NPOT_SUPPORT = None

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslated(0.0, 0.0, -50.0)
        glScaled(self.zoom, self.zoom, self.zoom)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glTranslate(0.0, 0.0, 0.0)
        glTranslated(self.xPos / 5.0, self.yPos / 5.0, self.zPos / 5.0)
        glCallList(CubeGraphic.sharedObject)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        GLU.gluPerspective(10.0, width / height, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.textures = []
        for i in range(6):
            self.textures.append(self.bindTexture(QtGui.QImage("icon%d.png" % (i + 1))))
        glTexImage2D( GL_TEXTURE_2D, 0, 4, self.imageWidth, self.imageHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image )
        CubeGraphic.sharedObject = self.makeObject()

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glBlendColor(0.0, 0.0, 0.0, self.alpha)

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

    def loadImage(self, imageName):
        im = open(imageName)
        self.imageWidth = im.size[0]
        self.imageHeight = im.size[1]
        self.image = im.tostring("raw", "RGBA", 0, -1)


        # def bestSize(dim):
        #     """Try to figure out the best power-of-2 size for the given dimension
        #
        #     At the moment, this is the next-largest power-of-two
        #     which is also <= glGetInteger( GL_MAX_TEXTURE_SIZE ).
        #     """
        #     boundary = min((glGetInteger(GL_MAX_TEXTURE_SIZE), dim))
        #     test = 1
        #     while test < boundary:
        #         test = test * 2
        #     return test
        #
        #
        #
        # def ensurePow2(self, imageName):
        #     """Ensure that the PIL image is pow2 x pow2 dimensions
        #
        #     Note:
        #         This method will create a _new_ PIL image if
        #         the image is not a valid size (It will use BICUBIC
        #         filtering (from PIL) to do the resizing). Otherwise
        #         just returns the same image object.
        #     """
        #
        #     if self.NPOT_SUPPORT is None:
        #         self.__class__.NPOT_SUPPORT = texture_non_power_of_two.glInitTextureNonPowerOfTwoARB()
        #         if not self.NPOT_SUPPORT:
        #             log.warn("Implementation requires Power-of-Two textures")
        #     if not self.NPOT_SUPPORT:
        #         BICUBIC = Image.BICUBIC
        #         image = open(imageName)
        #         ### Now resize non-power-of-two images...
        #         # should check whether it needs it first!
        #         newSize = self.bestSize(image.size[0]), self.bestSize(image.size[1])
        #         if newSize != image.size:
        #             log.warn(
        #                 "Non-power-of-2 image %s found resizing: %s",
        #                 image.size, image.info,
        #             )
        #             image = image.resize(newSize, BICUBIC)
        #     return image
        #
