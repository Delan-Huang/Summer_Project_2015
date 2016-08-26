"""
Author: Delan Huang
Date: 06/17/2015
Plan: Draw a Cube. Code will be added to existing Cube_Model_PySide
program.
"""

import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU


class CubeGraphic(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.yRotDeg = 0.0

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslate(0.0, 0.0, -50.0)
        GL.glScale(20.0, 20.0, 20.0)
        GL.glRotate(self.yRotDeg, 0.2, 1.0, 0.3)
        GL.glTranslate(-0.5, -0.5, -0.5)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        # GL.glEnableClientState(GL.GL_COLOR_ARRAY)
        GL.glVertexPointerf(self.cubeVtxArray)
        # GL.glColorPointerf(self.cubeClrArray)
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
        # self.cubeClrArray = [
        #     [0.0, 0.0, 0.0],
        #     [1.0, 0.0, 0.0],
        #     [1.0, 1.0, 0.0],
        #     [0.0, 1.0, 0.0],
        #     [0.0, 0.0, 1.0],
        #     [1.0, 0.0, 1.0],
        #     [1.0, 1.0, 1.0],
        #     [0.0, 1.0, 1.0]]

    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        aspect = w / float(h)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.initGeometry()

        GL.glEnable(GL.GL_DEPTH_TEST)


def main():
    app = QtGui.QApplication(sys.argv)
    window = CubeGraphic()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
