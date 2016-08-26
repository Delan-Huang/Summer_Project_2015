$CubeModel
==========

$CubeModel creates a cube onto the screen with random projections
uploaded onto its faces.

To import CubeModel:

    import CubeModel
    CubeModel.MainWindow()

Table of Contents (Methods):

CubeModel.py
------------

     Class MainWindow:
        - __init__(self)

CubeGraphic.py
--------------

    Class CubeGraphic:
        - __init__(self)

        Widget based Functions (PySide / PyQt4)
        ---------------------------------------
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
        - setLists(self)
        - make2dScaledArray(self, a_list)
        - makeTextures(self)
        - setTexture(self, a_list)
        - replaceTextures(self)
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

Required Dependencies/Packages:

    Python 2.6
    Microsoft Visual C++ 2008 Express Edition
    pip_7.1.0
    Numpy 1.9.2
    PyOpenGL_3.1.0
    PySide4
    OpenGLContext_2.2.0
    pydispatcher_2.0.5
    PyVRML297_.3.0
    pywin32_2.1.9 (Not sure about this one)


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

    None

Description:

    Creates and sets the main layout for the GUI, and includes signal/slots to allow widgets
        to 'communicate' with one another.

Last Edited:

    July 2, 2015

Associated Functions:

    - __init__(self)
    ----------------------
    Description:

        Constructor function

    Parameters:

        None

    Return:

        None

    Last Edited:
        June 18, 2015

Class Name:

    class CubeGraphic(QtOpenGL.QGLWidget):

Parameters:

    None

Description:

    Contains all methods and variables necessary for the creation of a CubeGraphic Object,
    which is visually projected to the screen as a OpenGLWidget in the MainWindow.

Last Edited:

    June 7, 2015

Associated Functions:

    - __init__(self)
    ----------------
    Description:

        Constructor

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 2, 2015

    Widget Based Functions (PySide4 / PyQt4)
    ======================================

    - getXRot(self)
    ---------------
    Return:
        Returns self.xRot (x rotation value)

    Last Edited:
        June 18, 2015

    - getYRot(self)
    ---------------
    Return:
        Returns self.yRot (y rotation value)

    Last Edited:
        June 18, 2015

    - getZRot(self)
    ---------------
    Return:
        Returns self.zRot (z rotation value)

    Last Edited:
        June 18, 2015

    - getXPos(self)
    ---------------
    Return:
        Returns self.xPos (x position value)

    Last Edited:
        June 18, 2015

    - getYPos(self)
    ---------------
    Return:

        Returns self.yPos (y position value)

    Last Edited:
        June 18, 2015

    - mousePressEvent(self, event)
    ------------------------------
    Description:

        Overloaded mousePressEvent. Sets last click point (x1, y1) on Clicked (left or right) event.

    Parameters:

        Clicked event.

    Return:

        None

    Last Edited:
        June 18, 2015

    - mouseMoveEvent(self, event)
    -----------------------------
    Description:

        Overloaded mouseMoveEvent. Finds difference between last clicked point (x1, y1) and
        new mouse position (x2, y2). Uses the difference to calculate angle rotation of graphic.
        Sets graphic rotation, updates graphic on screen, and sets lastPos to event position.

    Parameters:

        Requires a Left Click or Right Click event.

    Return:

        None

    Last Edited:
        June 18, 2015

    - setXRotation(self, angle)
    ---------------------------
    Description:

        Sets xRot value to angle value, after angle has been normalized (0 < angle < 360)
        and updates graphic.

    Parameters:

        - angle (integer): ranges from 0 to 5760 (360 * 16)

    Return:

        None

    Last Edited:
        June 18, 2015

    - setYRotation(self, angle)
    ---------------------------
    Description:

        Sets yRot value to angle value, after angle has been normalized (0 < angle < 360)
        and updates graphic.

    Parameters:

        - angle (integer): ranges from 0 to 5760 (360 * 16)

    Return:

        None

    Last Edited:
        June 18, 2015

    - setZRotation(self, angle)
    ---------------------------
    Description:

        Sets zRot value to angle, after angle has been normalized (0 < angle < 360)
        and updates graphic.

    Parameters:

        - angle (integer): ranges from 0 to 5760 (360 * 16)

    Return:

        None

    Last Edited:
        June 18, 2015

    - setXPosition(self, distance)
    ------------------------------
    Description:

        Sets xPos value to distance and updates graphic.

    Parameters:

        - distance (integer): ranges from 0 to 30

    Return:

        None

    Last Edited:
        June 18, 2015

    - setYPosition(self, distance)
    ------------------------------
    Description:

        Sets yPos value to distance and updates graphic.

    Parameters:

        - distance (integer): ranges from 0 to 30

    Return:

        None

    Last Edited:
        June 18, 2015

    - setZoom(self, new_zoom)
    -------------------------
    Description:

        Sets zoom value to new_zoom and updates graphic.

    Parameters:

        new_zoom (double): ranges from 0.1 - 20.0

    Return:

        None

    Last Edited:
        June 18, 2015

    - normalizeAngle(self, angle)
    -----------------------------
    Description:

        Checks if angle value is outside of bounds, and then puts it back into bounds.
        If angle is over 360, subtract 360 * 16 from it.
        If angle is under 0, add 360 * 16 to it.

    Parameters:

        - angle (integer)

    Return:

        - angle (integer)

    Last Edited:
        June 18, 2015

    Cube Graphic Texture Functions and OpenGL Overloads (PyOpenGL)
    ==============================================================

    - setLists(self)
    ----------------
    Description:

        Puts all lists (list1, ..., list6) into initialized lists array.
        This is here for the sake of reducing copy/paste code.

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - make2dScaledArray(self, a_list)
    ---------------------------------
    Description:

        Takes a 1-d array from a projection (produced from a .mrc file) and creates a 2-d array.
        Linearly scales the values in the produced 2-d array on a 0 - 255 (RGB) scale.

    Parameters:

        - a_list (list of doubles): 1-d array

    Return:

        - scaledArray (list of integers): 2-d array

    Last Edited:
        July 6, 2015

    - setTexture(self, a_list)
    --------------------------
    Description:

        Sets the RGBA value of public img variable using scaledArray element values.
        img variable looks like this:

            [[[R, G, B, A],
              ...
              [R, G, B, A]],

              ...

             [[R, G, B, A],
              ...
              [R, G, B, A]]]

            Where it simulates a 2-d array (like a picture) and each point has a RGBA value.

    Parameters:

        - a_list (list of integers): 2-d array

    Return:

        None

    Last Edited:
        July 6, 2015


    - makeTextures(self)
    --------------------
    Description:

        Creates 6 textures, one at a time, each iteration re-writing the img variable
        and calling glTexImage2D.

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - replaceTextures(self)
    -----------------------
    Description:

        Creates new projections from same .mrc file and replace textures on graphic with new ones.
        Calls makeTextures().

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - paintGL(self)
    ---------------
    Description:

        Overloaded function. Sets canvas size and 'camera' settings.
        Gets called each time graphic updates.

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - resizeGL(self, width, height)
    -------------------------------
    Description:

        Overloaded function. Specifies how to re-set 'camera' perspective when window is re-sized.

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - initializeGL(self)
    --------------------
    Description:

        Overloaded function. Graphic Object is created and drawing settings enabled.

    Parameters:

        None

    Return:

        None

    Last Edited:
        July 6, 2015

    - makeObject(self)
    ------------------
    Description:

        Creates the vertices for the 3-d cube object and the vertices for the 2-d texture on the cube.
        Binds the texture to x number faces of the cube, where x = faces - iterator (n).

        For example:
        At 0 in range(6):
        Texture 1 is bound to all textures (6 - 0)

        ...

        At 5 in range(6): (range is exclusive)
        Texture 6 is bound to one texture (and overwrites previous texture) (6 - 5)

    Parameters:

        None

    Return:

        - dlist (list of integers): Each integer is actually a GLuint. Each integer corresponds to a list of commands,
        which callList calls the instructions in order. This is useful for possible future implementation if there
        were to be more than one graphic drawn on the screen.

    Last Edited:
        July 6, 2015