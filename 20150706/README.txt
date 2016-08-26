$CubeModel
==========

$CubeModel creates a cube onto the screen with random projections
uploaded onto its faces.

To import CubeModel:

    import CubeModel
    CubeModel.MainWindow(args)
    # args passed into CubeModel.py through a c++ extension

Table of Contents:

CubeModel.py
------------

     Class MainWindow:
        - __init__(self, args)

CubeGraphic.py
--------------

    Class CubeGraphic:
        - __init__(self, args)

        Getter and Setter Functions
        ---------------------------
        - getXRot(self)
        - getYRot(self)
        - getZRot(self)
        - getXPos(self)
        - getYPos(self)
        - mousePressEvent(self, event)
        - mouseMoveEvent(self, event)
        - setXRotation(self, angle)
        - setYRotation(self, angle)
        - setZRotation(self, angle)
        - setXPosition(self, distance)
        - setYPosition(self, distance)
        - setZoom(self, new_zoom)
        - normalizeAngle(self, angle)

        Cube Graphic Texture Functions and OpenGL Overloads
        ---------------------------------------------------
        - make2dScaledArray(self, a_list)
        - makeTexture(self, a_list)
        - paintGL(self)
        - resizeGL(self, width, height)
        - initializeGL(self)
        - makeObject(self)

Features
--------

- Projects a 3d Cube with a random projection on each face
- Rotate along X and Y axis
- Translate along X and Y axis
- Scale up to 20x Cube size

Installation
------------

Install $CubeModel by running:

    # Coming Soon
    pip install CubeModel

Contribute
----------

# Standard is to use github for this
- Issue Tracker:
- Source Code:

Support
-------

If you are having issues, please let us know.
We have a mailing list located at:

License
-------

# I am not too sure about this one, but it looks good
The project is licensed under the BSD license.

Methods
-------

Class Name:

    class MainWindow(QtGui.QWidget):

Parameters:

    args: This is a single tuple containing 6 lists (list1, list2 ...) and 3 integers (xDim, yDim, zDim).
          It gets passed into MainWindow by a C++ extension.

Description:

    Creates and sets the main layout for the GUI, and includes signal/slots to allow widgets
        to 'communicate' with one another

Last Edited:

    2 July 2015

Associated Functions:

    - __init__(self, args)
    Description:
        Constructor function

    Parameters:
        args: A tuple containg 6 Python lists and 3 integers.

        Within args is (list1, list2, list3, list4, list5, list6, xDim, yDim, zDim).
        args is passed into CubeGraphic by a C++ extension.

    Return:
        None

    Last Edited:
        June 18 2015

    - getXRot(self)
    Return:
        Returns self.xRot (x rotation value)

    - getYRot(self)
    Return:
        Returns self.yRot (y rotation value)

    Last Edited:
        June 18 2015

    - getZRot(self)
    Return:
        Returns self.zRot (z rotation value)

    Last Edited:
        June 18 2015

    - getXPos(self)
    Return:
        Returns self.xPos (x position value)
    Last Edited:
        June 18 2015

    - getYPos(self)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - mousePressEvent(self, event)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - mouseMoveEvent(self, event)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setXRotation(self, angle)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setYRotation(self, angle)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setZRotation(self, angle)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setXPosition(self, distance)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setYPosition(self, distance)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - setZoom(self, new_zoom)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015

    - normalizeAngle(self, angle)
    Description:

    Parameters:

    Return:

    Last Edited:
        June 18 2015