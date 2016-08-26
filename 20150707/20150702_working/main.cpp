#include <Python.h>
#include <stdlib.h>
#include "maps.h"
#include "helper.h"

static PyObject* test(PyObject* self, PyObject* args) {
	// Create variables to hold the map and the stack
	MRC_MAP myImg;
	
	// The Python Object that we will be returning.
	PyObject *pReturn;
	// The PyObjects that will hold our projections.
	PyObject *p1, *p2, *p3, *p4, *p5, *p6;
	PyObject *pItem1, *pItem2, *pItem3, *pItem4, *pItem5, *pItem6;

	//Create other c++ variables that will be needed.
	float *in; // Hold the density of the map.
	float *stack; // Final array
	int xDim, yDim, zDim; // the dim. of the image
	float *rotate1, *rotate2, *rotate3;
	float *rotate4, *rotate5, *rotate6; // Hold the densities after rotation.
	float *project1, *project2, *project3; // Densities for the 2D projections.
	float *project4, *project5, *project6;
	// Load the map.
	myImg.input("./S4150_SR001.map");
	myImg.normalize();
	// Get the density
	in = myImg.density;
	// Get the dim of the image.
	xDim = myImg.dimX;
	yDim = myImg.dimY;
	zDim = myImg.dimZ;
printf("%d %d %d\n", xDim, yDim, zDim);
	// Allocate memory.	
	int size3D = ((zDim-1)*yDim+(yDim-1))*xDim+(xDim-1);	
	rotate1 = new float[size3D];
	rotate2 = new float[size3D];
	rotate3 = new float[size3D];
	rotate4 = new float[size3D];
	rotate5 = new float[size3D];
	rotate6 = new float[size3D];
	int size2D = (yDim-1)*xDim+(xDim-1);
	project1 = new float[size2D];
	project2 = new float[size2D];
	project3 = new float[size2D];
	project4 = new float[size2D];
	project5 = new float[size2D];
	project6 = new float[size2D];
	
	// Create the 6 sides of the cubes.
	// By creating a projection for each side.
	// See notes on June 30, 2015 for side names.
	
	// Side 1- No rotation.
	createProjection(project1, rotate1, in, xDim, yDim, zDim, 0, 0, 0);
	// Side 2- 180 degrees along Z
	createProjection(project2, rotate2, in, xDim, yDim, zDim, 0, 0, 180);
	// Side 3- 90 degrees along Z
	createProjection(project3, rotate3, in, xDim, yDim, zDim, 0, 0, 90);
	// Side 4- 270 degrees along Z
	createProjection(project4, rotate4, in, xDim, yDim, zDim, 0, 0, 270);
	// Top- 90 degrees along Y
	createProjection(project5, rotate5, in, xDim, yDim, zDim, 0, 90, 0);
	// Bottom- 270 degrees along Y
// IS NOT CORRECT!
	createProjection(project6, rotate6, in, xDim, yDim, zDim, 0, 270, 0);

	// Create the Python lists of that size.
	p1 = PyList_New(size2D);
	p2 = PyList_New(size2D);
	p3 = PyList_New(size2D);
	p4 = PyList_New(size2D);
	p5 = PyList_New(size2D);
	p6 = PyList_New(size2D);
	// You guessed it...Error check.	
	if(p1 == NULL || p2 == NULL || p3 == NULL || p4 == NULL || p5 == NULL || p6 == NULL) { 
		printf("ERROR: Could not create list. Line %d.\n", __LINE__);
		delete [] rotate1;
		delete [] rotate2;
		delete [] rotate3;
		delete [] rotate4;
		delete [] rotate5;
		delete [] rotate6;
		delete [] project1;
		delete [] project2;
		delete [] project3;
		delete [] project4;
		delete [] project5;
		delete [] project6;	
		myImg.clear();
		Py_RETURN_NONE;	
	}
	// Copy the projections array to the python list.
	for(int i = 0; i < size2D; i++) {		
		pItem1 = PyFloat_FromDouble((double)project1[i]);
		pItem2 = PyFloat_FromDouble((double)project2[i]);
		pItem3 = PyFloat_FromDouble((double)project3[i]);
		pItem4 = PyFloat_FromDouble((double)project4[i]);
		pItem5 = PyFloat_FromDouble((double)project5[i]);
		pItem6 = PyFloat_FromDouble((double)project6[i]);
		
		PyList_SET_ITEM(p1, i, pItem1);
		PyList_SET_ITEM(p2, i, pItem2);
		PyList_SET_ITEM(p3, i, pItem3);
		PyList_SET_ITEM(p4, i, pItem4);
		PyList_SET_ITEM(p5, i, pItem5);
		PyList_SET_ITEM(p6, i, pItem6);
	}
	

	// Build the arguments that will be passed to the Python function.
	// We will be passing in the Python List and the three dim.
	// So as a tuple, the six objects and three integers
	pReturn = Py_BuildValue("(O,O,O,O,O,O,i,i,i)", p1, p2, p3, p4, p5, p6, xDim, yDim, zDim);
	// We almost didn't error check... but we did.	
	if(pReturn == NULL) {
		printf("ERROR: Could not build values. Line %d.\n", __LINE__);
		myImg.clear();
		delete [] rotate1;
		delete [] rotate2;
		delete [] rotate3;
		delete [] rotate4;
		delete [] rotate5;
		delete [] rotate6;
		delete [] project1;
		delete [] project2;
		delete [] project3;
		delete [] project4;
		delete [] project5;
		delete [] project6;
		Py_DECREF(p1);
		Py_DECREF(p2);
		Py_DECREF(p3);
		Py_DECREF(p4);
		Py_DECREF(p5);
		Py_DECREF(p6);
		Py_RETURN_NONE;
	}		

	// Clean Up the C++ stuff.
	myImg.clear();
	delete [] rotate1;
	delete [] rotate2;
	delete [] rotate3;
	delete [] rotate4;
	delete [] rotate5;
	delete [] rotate6;
	delete [] project1;
	delete [] project2;
	delete [] project3;
	delete [] project4;
	delete [] project5;
	delete [] project6;
	
	// Clean up the Python Objects.
	Py_DECREF(p1);
	Py_DECREF(p2);
	Py_DECREF(p3);
	Py_DECREF(p4);
	Py_DECREF(p5);
	Py_DECREF(p6);	
	
	// Return the Python Value that we created.
	return pReturn;
}


static PyMethodDef test_methods[] = {
	{"test", test, METH_NOARGS, "Greet somebody."},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initproject(void) {
	(void) Py_InitModule("project", test_methods);
}	
