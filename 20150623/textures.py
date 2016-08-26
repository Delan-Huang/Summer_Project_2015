#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GLU

try:
    from OpenGL.GL import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL textures",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)



class GLWidget(QtOpenGL.QGLWidget):
    sharedObject = 0
    refCount = 0

    coords = (
        ( ( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 ) ),
        ( ( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 ) ),
        ( ( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 ) ),
        ( ( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 ) ),
        ( ( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 ) ),
        ( ( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ) )
    )

    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QtCore.QPoint()


    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(200, 200)



    def initializeGL(self):
        self.textures = []
        for i in range(6):
            self.textures.append(self.bindTexture(QtGui.QPixmap("icon.png")))
        GLWidget.sharedObject = self.makeObject()
        GLWidget.refCount += 1

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -10.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glCallList(GLWidget.sharedObject)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # GL.glOrtho(-1.5, +1.5, -1.5, +1.5, 4.0, 15.0)
        GLU.gluPerspective(5.0, width / height, 1.0, 10.0)
        glMatrixMode(GL_MODELVIEW)


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
                glVertex3d(0.2 * GLWidget.coords[i][j][0],
                           0.2 * GLWidget.coords[i][j][1],
                           0.2 * GLWidget.coords[i][j][2])

            glEnd()

        glEndList()
        return dlist


class Window(QtGui.QWidget):
    NumRows = 1
    NumColumns = 1

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        mainLayout = QtGui.QGridLayout()
        self.glWidgets = []

        for i in range(Window.NumRows):
            self.glWidgets.append([])
            for j in range(Window.NumColumns):
                self.glWidgets[i].append(None)

        for i in range(Window.NumRows):
            for j in range(Window.NumColumns):
                clearColor = QtGui.QColor()
                clearColor.setHsv(((i * Window.NumColumns) + j) * 255
                                  / (Window.NumRows * Window.NumColumns),
                                  255, 63)

                self.glWidgets[i][j] = GLWidget()
                mainLayout.addWidget(self.glWidgets[i][j], i, j)

        self.setLayout(mainLayout)

        self.currentGlWidget = self.glWidgets[0][0]

        self.setWindowTitle(self.tr("Textures"))

    def setCurrentGlWidget(self):
        self.currentGlWidget = self.sender()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
