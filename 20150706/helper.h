#ifndef _HELPER_H
#define _HELPER_H 1

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

// Constants
#define IMG_NAME_IN    "./S4150_SR001.map"
#define IMG_NAME_OUT   "./stack.mrc"
#define PI 3.14159265

typedef float matrix[3][3];

void mult_matrix(matrix Fst_Mat, matrix Sec_Mat, matrix Result_Mat);
void Concatenate_Matrices(matrix First_Mat, matrix Second_Mat, matrix Third_Mat, matrix Fin_Mat);
void rotateImg(matrix A, float *in,  float* rotate, int xDim, int yDim, int zDim);
void invertMatrix(matrix A, matrix AInv);
float interpolate(float * in, float x, float y, float z, int xDim, int yDim, int zDim);
void projection(float *source, float *destination, int xDim, int yDim, int zDim);
void createProjection(float *project, float *rotate, float *in, int xDim, int yDim, int zDim);



#endif
