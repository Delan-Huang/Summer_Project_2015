#ifndef _MAPS_H
#define _MAPS_H 1

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// disk I/O buffer size (256 MB)
#define EMX_DIO_BUFFER	268435456

// sampling frames in particle contrast detection
#define EMX_IMG_CONTRAST	1024

// periodicity in MRC encryption
#define EMX_ENCRYPT_LEN		37
#define EMX_MRC_PLAIN		0
#define EMX_MRC_CRYPT		1

#define EMS_ZERO   0.00001

struct 	MRC_Header {
	int   nXYZ[3]; //nxyz[3];
	int   mode;
	int   nXYZstart[3];
	int   mXYZ[3];
	float cell[6];
	int	  mapCRS[3];
	float mapMin, mapMax, mapAve;
	int	  spaceGroup;
	int	  symmetry;
	int	  extra[25];
	float oXYZ[3];
	char  mapID[4];
	int   machine;
	float mapStd;
	int	  nLabel;
	char  label[800];
};

class MRC_MAP {
private:
	char encrypted;

public:
	char  exist;					// flag indicating existance
	char  endian;					// flag for endian property (FALSE for no-swap)
	char  modify;					// EMS_TRUE for modified, unsaved image
	int   dimX, dimY, dimZ;			// image dimension
	int   samX, samY, samZ;			// image resampling
	int   mode, dataBytes;			// MRC format mode
	long  mapSize;					// number of pi(vo)xels
	float maxInt, minInt;			// intensity range
	float aveInt, stdInt;			// intensity statistics
	float pixelX, pixelY, pixelZ;	// pixel size
	int   binBox;					// image element binning

	// electron density data, normalized to N(0,1), always mode 2
	float *density;

	MRC_MAP();
	~MRC_MAP();

	// set up an MRC map
	char setup(int x, int y, int z, float px, float py, float pz, float *data);

	// read MRC map header
	FILE* header(char *map_file);
	char headerOnly(char *map_file);

	// write MRC map header, must call setup() first
	char writeHeader(FILE *fp);

	// loading map data to density_original[]
	char input(char *map_file);

	// writing map data to file
	char output(char *map_file);

	// clear all map entries
	void clear(void);

	// MIN, MAX, AVE, STD statistics
	void statistics(void);

	// normalize 3D map to N(0.0, 1.0)
	void normalize(void);

	// normalize 2D frames to N(0.0, 1.0)
	void normalFrame(void);

	// detect STACK image contrast (radius in pixel)
	int imgContrast(double radius);

	// scaling pixel/voxel intensity
	void scaling(double k, double b);

	// invert intensity contrast
	void invert(void);

	// element binning
	void bin2D(void);
	void bin3D(void);

	// image resampling
	char resample2D(void);
	char resample3D(void);
	char resample3D(double pix_size, double pix_ratio);
};


#endif
