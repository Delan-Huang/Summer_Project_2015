#include <Python.h>
#include <stdlib.h>
#include "maps.h"
#include "misc.h"
#include "helper.h"



/*
 * Helper file created to store functions.
 * Purpose is to clean up the main.cpp file.
 * Created June 15 2015.
 * Author: Taylor Spooner.
 * Advised by Dr. James Chen
*/


/* mult_matrix()
 * Created June 15, 2015
 * Author: Taylor Spooner. Advised by Dr. James Chen
 * 
 * Purpose: Multiply two 3x3 matrices together and store them in a resulting matrix.
 *
 * Input: Two 3x3 matrices in which the user would like to multiply together.
 *	A resulting matrix.
 *
 * Output: Void. Matrix "Result_Mat" is modified in running of function.
 */
void mult_matrix(matrix Fst_Mat, matrix Sec_Mat, matrix Result_Mat) {
	float temp = 0.0f;
	int a, b, c;

	for(a = 0; a < 3; a++)
	{
		for(b = 0; b < 3; b++)
		{
			for(c = 0; c < 3; c++)
			{
			temp += Fst_Mat[b][c] * Sec_Mat[c][a];
			}
		Result_Mat[b][a] = temp;
		temp = 0.0f;
		}
	}
}

/* Concatenate_Matrices()
 * Created June 15, 2015
 * Author: Taylor Spooner. Advised by Dr. James Chen
 * 
 * Purpose: Compute the final rotation matrix.
 *		First multiply B and C. Store in a temp. matrix.
 *		Second multiply the temp matrix by D store in the rotation matrix.
 *
 * Input: Three 3x3 matries in the order in which user would like to multipy.
 *	An array to store the final result of the multiplication.
 *
 * Output: Void. The 3x3 matrix "Fin_Mat" is modified in function.
 */
void Concatenate_Matrices(matrix First_Mat, matrix Second_Mat, matrix Third_Mat, matrix Fin_Mat)
{	
	matrix Concat_Mat;

	mult_matrix(First_Mat, Second_Mat, Concat_Mat);
	mult_matrix(Concat_Mat, Third_Mat, Fin_Mat);
}


/* rotateImg()
 * Created June 15, 2015
 * Author: Taylor Spooner. Advised by Dr. James Chen
 * 
 * Purpose: Rotate the density map by the rotation matrix.
 *			Put the densities from their current position to the rotated position.
 *
 * Input: A 3x3 rotation matrix.
 *	An array of floats representing the densities of the original image.
 *	An array of floats that will represent the densities of the rotated image.
 *	The dimensions of the image.
 *
 * Output: Void. Array "rotate" is modified in the function.
*/
void rotateImg(matrix A, float *in, float* rotate, int xDim, int yDim, int zDim) {
	int b[3];
	float c[3];
	int idx = 0;
	matrix AI; //The Inverse Rotation Matrix.
	invertMatrix(A, AI);
	
	// Assume the center of mass is at the center of geometry.
	double centerX = xDim/2;
	double centerY = yDim/2;
	double centerZ = zDim/2;

	// Iterate over every voxel in the image.
	for(int x = 0; x < xDim; x++) {
		for(int y = 0; y < yDim; y++) {
			for(int z =0; z < zDim; z++) {
				// The current position in the rotated image relative to center of mass
				b = {x-centerX,y-centerY,z-centerZ}; 	
				// Calculate the corresponding original position.
				c[0] = AI[0][0]*b[0] + AI[0][1]*b[1] + AI[0][2]*b[2]; //x
				c[1] = AI[1][0]*b[0] + AI[1][1]*b[1] + AI[1][2]*b[2]; //y
				c[2] = AI[2][0]*b[0] + AI[2][1]*b[1] + AI[2][2]*b[2]; //z
				// Convert coordinates back to absolute.
				c[0] = c[0]+centerX;
				c[1] = c[1]+centerY;
				c[2] = c[2]+centerZ;
				// Do interpulation and store in a new array.
				idx = (z*yDim+y)*xDim+x;
				rotate[idx] = interpolate(in, c[0], c[1], c[2], xDim, yDim, zDim);
			} //inside for loop
		} //middle for loop
	}//outside for loop.
} //rotateImg()


/* invertMatrix()
 * Created: June 15, 2015
 * Author: Taylor Spooner. Advised by Dr. James Chen
 * 
 * Purpose: Invert a 3x3 matrix.
 * Input: A 3x3 matrix.
 * Output: void. The inverse matrix is modified in the function.
 *	Because C++ does not support returning arrays/functions.
 *
 */
void invertMatrix(matrix A, matrix AInv) {
	// Scalars.
	float a,b,c,d,e,f,g,h,i;	
	a = A[1][1]*A[2][2] - A[1][2]*A[2][1];
	b = -(A[1][0]*A[2][2] - A[1][2]*A[2][0]);
	c = A[1][0]*A[2][1] - A[1][1]*A[2][0];
	d = -(A[0][1]*A[2][2] - A[0][2]*A[2][1]);
	e = A[0][0]*A[2][2] - A[0][2]*A[2][0];
	f = -(A[0][0]*A[2][1] - A[0][1]*A[2][0]);
	g = A[0][1]*A[1][2] - A[0][2]*A[1][1];
	h = -(A[0][0]*A[1][2] - A[0][2]*A[1][0]);
	i = A[0][0]*A[1][1] - A[0][1]*A[1][0];
	
	// Calculate the determinant of the inputed matrix.
	// Appling the "rule of Sarrus"
	float det = A[0][0]*a + A[0][1]*b + A[0][2]*c;
	
	// Multiply 1/det by all the scalars.
	a = (1/det)*a;
	b = (1/det)*b;
	c = (1/det)*c;
	d = (1/det)*d;
	e = (1/det)*e;
	f = (1/det)*f;
	g = (1/det)*g;
	h = (1/det)*h;
	i = (1/det)*i;
	
	// Calculate inverse.
	AInv[0][0] = a;
	AInv[0][1] = d;
	AInv[0][2] = g;
	AInv[1][0] = b;
	AInv[1][1] = e;
	AInv[1][2] = h;
	AInv[2][0] = c;
	AInv[2][1] = f; 
	AInv[2][2] = i;
}

/* interpolate()
 *
 * Author: Taylor Spooner. Advised by Dr. James Chen
 *
 * Purpose: Find the density in the original image using trilinear interpolation.
 * 		Trilinear Interpolation equation taken from https://en.wikipedia.org/wiki/Trilinear_interpolation
 * 
 * Input: An array of floats representing the densities of the original image.
 * 	A (x, y, z) coordinate point that we wish to interpolate.
 *	The dimensions of the image.
 * Output: The density at the new location, represented as a float. 
 */
float interpolate(float * in, float x, float y, float z, int xDim, int yDim, int zDim){
	
	// Error checking conditions.
	// If one of the positions is outside the original image,
	// there is not information to be had, return 0.
	if(x >= xDim || y >= yDim || z >= zDim) { return 0; }	
	if( x < 0 || y < 0 || z < 0 ) { return 0; }	

	// First create the cube of values surrounding the inputed point.
	int x0 = floor(x);
	int x1 = ceil(x);
	int y0 = floor(y);
	int y1 = ceil(y);
	int z0 = floor(z);
	int z1 = ceil(z);
			
	// Create the differences between inputed values and smaller coordinate	
	double xd = (x-x0);
	double yd = (y-y0);
	double zd = (z-z0);

//NEED TO TEST THIS.
//FOR THE EDGES, IF THE NEXT LARGEST INTEGER IS OUT OF BOUNDS
// USE THE NEXT SMALLEST INTEGER AGAIN OR RETURN 0 OR JUST RETURN THE DENSITY?
	if (x1 >= xDim ) { return 0; }
	if (y1 >= yDim ) { return 0; }
	if (z1 >= zDim ) { return 0; }

	// Interpolate along x.
	// Will find the density at each point by indexing the in array.
	// Index = (z*yDim+y)*xDim + x
	float cX[2][2];
	cX[0][0] = in[(z0*yDim+y0)*xDim+x0]*(1-xd)+in[(z0*yDim+y0)*xDim+x1]*xd;
	cX[1][0] = in[(z0*yDim+y1)*xDim+x0]*(1-xd)+in[(z0*yDim+y1)*xDim+x1]*xd;
	cX[0][1] = in[(z1*yDim+y0)*xDim+x0]*(1-xd)+in[(z1*yDim+y0)*xDim+x1]*xd;
	cX[1][1] = in[(z1*yDim+y1)*xDim+x0]*(1-xd)+in[(z1*yDim+y1)*xDim+x1]*xd;	

	// Interpolate along y.
	float cY[2];
	cY[0] = cX[0][0]*(1-yd)+cX[1][0]*yd;
	cY[1] = cX[0][1]*(1-yd)+cX[1][1]*yd;	

	// Interpolate along z.
	float c;
	c = cY[0]*(1-zd)+cY[1]*zd;
	return c;
}

/* projection()
 *
 * Author: Taylor Spooner. Advised by Dr. James Chen
 *
 * Purpose: Given a 3D image, "flatten" the image into a 2D projection.
 *		Accumulate the z-values.
 * Input: 
 * 	source: An array holding the intensities of the 3D image.
 *	destination: An array that will hold the accumlated z-values.
 *	xDim, yDim, zDim: Dimensions of the 3D image
 * Output: Void. The destination array is modified in the function.
 */
void projection(float *source, float *destination, int xDim, int yDim, int zDim){
	// Iterate over every voxel in the 3D image.
	// For each (x,y) coordinate, accumulate the z-value intensities.
	// Store that value to the destination array.	
	int idx3D, idx2D;
	float z_count = 0.0; // Store the z intensities
	for(int x=0; x < xDim; x++) {
		for(int y=0; y < yDim; y++) {
			idx2D = y*xDim+x;
			for(int z=0; z < zDim; z++) {
				idx3D = (z*yDim+y)*xDim+x;			
				// Accumulate z-values.
				z_count += source[idx3D];
			} //z for loop
			destination[idx2D]=z_count;
			z_count = 0.0;			
		} // y for loop
	}//x for loop
}

/* createProjection()
 *
 * Created: June 30, 2015
 * Author: Taylor Spooner. Advised by Dr. James Chen
 *
 * Inputs: A float array that will be the final projection, the thing that will be changed.
 *		A float array to hold the 3D map of the rotated image.
 *		A float array that is the original 3D map.
 *		The dim. of the map.
 *		The three Euler angles (in degrees).
 *
 * Purpose: Save code! Creates a 2D projection
 * Output: Void. The project array will be modified.
 */
void createProjection(float *project, float *rotate, float *in, int xDim, int yDim, int zDim) {
	long randSeed = time(0); // The seed for the random number generator.	
	// Convert the Euler angles from degrees to radians.	
	double phi = RandomNumb(randSeed)*PI;	
	double psi = RandomNumb(randSeed)*PI;
	double theta = RandomNumb(randSeed)*PI;

	matrix B, C, D; // Create matrices B, C, D for single rotations.
	matrix A; //The Rotation Matrix.
	// Create the single rotation matrices.
	//Initialize D. For rotations around the Z-Axis
	D = { {cos(psi),-sin(psi),0},
		{sin(psi),cos(psi),0},
		{0,0,1} };
	//Initialize C. For rotations around the Y-Axis
	C = { {cos(theta),0,sin(theta)},
		{0,1,0},
		{-sin(theta),0,cos(theta)} };
	//Initialize B. For rotations around the X-axis
	B = { {1,0,0},
		{0,cos(phi),-sin(phi)},
		{0,sin(phi),cos(phi)} };

	// Multiply B, C and D to create the rotation matrix, A.
	// A = BCD
	Concatenate_Matrices(B, C, D, A);

	// Rotate the Image.
	rotateImg(A, in, rotate, xDim, yDim, zDim);
  	
	// Project a 2D image.
	projection(rotate, project, xDim, yDim, zDim);			
	
}
