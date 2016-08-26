#include "Python.h"
#include "maps.h"
#include "misc.h"

#define MRCH_OLD	1024	// header size of OLD MRC
#define MRCH_NEW	1104	// header size of NEW MRC
#define OLD2NEW		80		// 80 extra chars in NEW MRC header
#define RGB_CHANNEL	2		// 32-bit TIFF pixel: ABGR

#define EMS_TRUE   1
#define EMS_FALSE  0

#define EMS_PIXEL_SIZE 1.0f

MRC_MAP::MRC_MAP()
{
	mode = -1;
	dimX = dimY = dimZ = 0;
	samX = samY = samZ = 0;
	mapSize = 0;
	binBox = 1;
	dataBytes = 0;
	endian = EMS_FALSE;
	pixelX = pixelY = pixelZ = 0.0;
	maxInt = aveInt = minInt = stdInt = 0.0;
	density = NULL;
	exist = EMS_FALSE;
	modify = EMS_FALSE;
	encrypted = EMX_MRC_PLAIN;
}


MRC_MAP::~MRC_MAP()
{
	if ( density != NULL ) {
		delete [] density;
		density = NULL;
	}
}


// read MRC map header
FILE* MRC_MAP::header(char *map_file)
{
	long data_size;
	struct MRC_Header mapHeader;
	unsigned char symstr[OLD2NEW];
	static FILE *fp;

	// open map file to read
	fp = fopen(map_file, "rb");
	
	if ( fp == NULL ) {
//		wrnReport("Cannot open this MRC image file!", 0);
		return(NULL);
	}

	// read map parameters from the header
	fread(&mapHeader, sizeof(struct MRC_Header), 1, fp);

	// byteswap header if necessary (normal modes take small ID#)
	endian = EMS_FALSE;

	if ( (mapHeader.mode<0) || (mapHeader.mode>255) ) {
		endian = EMS_TRUE;
	}
	else if ( mapHeader.mode == 0 ) {
		if ( (mapHeader.nXYZ[0]<0) || (mapHeader.nXYZ[0]>65535) )
			endian = EMS_TRUE;
		else if ( (mapHeader.nXYZ[1]<0) || (mapHeader.nXYZ[1]>65535) )
			endian = EMS_TRUE;
		else if ( (mapHeader.nXYZ[2]<0) || (mapHeader.nXYZ[2]>65535) )
			endian = EMS_TRUE;
	}

	// 3D data array SHOULD be in X-Y-Z order
	if ( mapHeader.mapCRS[0] != 1 ) {
		msgReport("Density map is not in X-Y-Z order. Proceed anyway ...");
	}

	mode = mapHeader.mode;
	dimX = mapHeader.nXYZ[0];
	dimY = mapHeader.nXYZ[1];
	dimZ = mapHeader.nXYZ[2];

	// pixel size (A) has to be physically meaningful
	pixelX = pixelY = pixelZ = EMS_PIXEL_SIZE;

	if ( (mapHeader.cell[0]>EMS_ZERO) && (mapHeader.mXYZ[0]>EMS_ZERO) ) {
		pixelX = mapHeader.cell[0] / mapHeader.mXYZ[0];
		if ( pixelX < 0.1 ) pixelX = EMS_PIXEL_SIZE;
	}

	if ( (mapHeader.cell[1]>EMS_ZERO) && (mapHeader.mXYZ[1]>EMS_ZERO) ) {
		pixelY = mapHeader.cell[1] / mapHeader.mXYZ[1];
		if ( pixelY < 0.1 ) pixelY = EMS_PIXEL_SIZE;
	}

	if ( (mapHeader.cell[2]>EMS_ZERO) && (mapHeader.mXYZ[2]>EMS_ZERO) ) {
		pixelZ = mapHeader.cell[2] / mapHeader.mXYZ[2];
		if ( pixelZ < 0.1 ) pixelZ = EMS_PIXEL_SIZE;
	}

	// calculate number of bytes to read
	if ( mode == 0 )		// signed char
		dataBytes = sizeof(char);
	else if ( mode == 1 )	// short int (2-bytes)
		dataBytes = sizeof(short);
	else if ( mode == 2 )	// float (4-bytes)
		dataBytes = sizeof(float);
	else if ( mode == 6 )	// short int (2-bytes)
		dataBytes = sizeof(short);
	else {
		errReport("Unrecognized image format!");
		fclose(fp);
		return(NULL);
	}

	mapSize = (long)dimX * dimY * dimZ;

	// determine data encryption status
	encrypted = EMX_MRC_PLAIN;

	// safe-guard data format
	data_size = mapSize * dataBytes;
	  // fread(symstr, OLD2NEW, 1, fp);

	return(fp);
}


char MRC_MAP::headerOnly(char *map_file)
{
	FILE *fp;

	if ( (fp=header(map_file)) != NULL ) {
		fclose(fp);
		return(EMS_TRUE);
	}
	else {
		return(EMS_FALSE);
	}

	return(EMS_TRUE);
}


// load MRC image
char MRC_MAP::input(char *map_file)
{
	long index, index2, bp, rdata, ndata;
	unsigned char *buffer;
	FILE *fp;

	clear();

	// open map header
	if ( (fp=header(map_file)) == NULL ) {
		return(EMS_FALSE);
	}

	density = new float[mapSize];
	buffer = new unsigned char[EMX_DIO_BUFFER];

	if ( (density==NULL) || (buffer==NULL) ) {
		errReport("Cannot allocate enough memory for this density map!");
		fclose(fp);
		return(EMS_FALSE);
	}

	bp = mapSize * dataBytes;
	index2 = 0;

	do {
		if ( bp > EMX_DIO_BUFFER )
			rdata = EMX_DIO_BUFFER;
		else
			rdata = bp;

		fread(buffer, rdata, 1, fp);
		ndata = rdata / dataBytes;

		for ( index=0; index<ndata; index++ ) {
			switch ( mode ) {
			case 0:
				density[index2] = buffer[index];
				break;
			case 1:
				density[index2] = ((short *)buffer)[index];
				break;
			case 2:
				density[index2] = ((float *)buffer)[index];
				break;
			case 6:
				density[index2] = ((short *)buffer)[index];
				break;
			}

			index2 ++;
		}

		bp -= rdata;

	} while ( bp > 0 );

	fclose(fp);
	delete [] buffer;

	mode = 2;
	dataBytes = sizeof(float);
	endian = EMS_FALSE;
	exist = EMS_TRUE;

	// evaluate intensity range (cannot trust the original header)
	statistics();

	return(EMS_TRUE);
}




// write out MRC map header, X/Y/Z known, data may be unknown
char MRC_MAP::writeHeader(FILE *fp)
{
	int index;
	char encFlag;
	struct MRC_Header mapHeader;

	// forced decryption
	encFlag = EMX_MRC_PLAIN;

	// must call setUp() beforehand
	mapHeader.mode = mode;

	mapHeader.nXYZ[0] = dimX;
	mapHeader.nXYZ[1] = dimY;
	mapHeader.nXYZ[2] = dimZ;

	mapHeader.nXYZstart[0] = 0;
	mapHeader.nXYZstart[1] = 0;
	mapHeader.nXYZstart[2] = 0;

	mapHeader.mXYZ[0] = dimX;
	mapHeader.mXYZ[1] = dimY;
	mapHeader.mXYZ[2] = dimZ;

	mapHeader.oXYZ[0] = 0;
	mapHeader.oXYZ[1] = 0;
	mapHeader.oXYZ[2] = 0;

	mapHeader.mapCRS[0] = 1;
	mapHeader.mapCRS[1] = 2;
	mapHeader.mapCRS[2] = 3;

	mapHeader.cell[0] = pixelX * dimX;
	mapHeader.cell[1] = pixelY * dimY;
	mapHeader.cell[2] = pixelZ * dimZ;
	mapHeader.cell[3] = 90.0;
	mapHeader.cell[4] = 90.0;
	mapHeader.cell[5] = 90.0;

	mapHeader.mapMin = minInt;
	mapHeader.mapMax = maxInt;
	mapHeader.mapAve = aveInt;
	mapHeader.mapStd = stdInt;

	mapHeader.symmetry = 0;
	mapHeader.spaceGroup = 0;
	// enforced little-endian
	mapHeader.machine = 68;
	strncpy(mapHeader.mapID, "MAP ", 4);

	for ( index=0; index<25; index++ ) mapHeader.extra[index] = 0;
	for ( index=0; index<800; index++ ) mapHeader.label[index] = ' ';

	mapHeader.nLabel = 1;
	// label indicates encryption status
	strcpy(mapHeader.label, "PARTICLE data processing");

	// write the header
	fwrite(&mapHeader, sizeof(struct MRC_Header), 1, fp);

	return(EMS_TRUE);
}


// write out an MRC map without symmetry record
char MRC_MAP::output(char *map_file)
{
	FILE *fp;
	char encFlag;
	  char message[1024];

	// must call setup() first
	if ( density == NULL ) {
		errReport("There is no data to save!");
		return(EMS_FALSE);
	}

	if ( (fp=fopen(map_file, "wb")) == NULL ) {
		sprintf(message, "Cannot write to file %s!", map_file);
		errReport(message);
		return(EMS_FALSE);
	}

	// forced decryption
	encFlag = EMX_MRC_PLAIN;

	// write MRC header (1024 bytes)
	statistics();
	writeHeader(fp);

	// set number of bytes to write
	if ( mode == 0 ) {       // 1-byte data
		dataBytes = sizeof(char);
	}
	else if ( mode == 2 ) {  // 4-byte reals
		dataBytes = sizeof(float);
	}
	else {
		fclose(fp);
		errReport("Incorrect MRC map mode!");
		return(EMS_FALSE);
	}

	// export plain data
	fwrite(density, mapSize, dataBytes, fp);
	fclose(fp);

	return(EMS_TRUE);
}


void MRC_MAP::clear(void)
{
	int index;

	if ( density != NULL ) {
		delete [] density;
		density = NULL;
	}

	mode = -1;
	dimX = dimY = dimZ = 0;
	mapSize = 0;
	dataBytes = 0;
	endian = EMS_FALSE;
	pixelX = pixelY = pixelZ = 0.0;
	maxInt = aveInt = minInt = stdInt = 0.0;
	exist = EMS_FALSE;
	modify = EMS_FALSE;
}


void MRC_MAP::statistics(void)
{
	long index;
	double std_t, ave_t;

	maxInt = -1.0E9;
	minInt = +1.0E9;
	ave_t = std_t = 0.0;

	for ( index=0; index<mapSize; index++ ) {
		ave_t += density[index];
		std_t += density[index] * density[index];

		if ( density[index] > maxInt )
			maxInt = density[index];

		if ( density[index] < minInt )
			minInt = density[index];
	}

	aveInt = (float)(ave_t / mapSize);
	stdInt = (float)(std_t / mapSize - aveInt * aveInt);

	if ( stdInt < EMS_ZERO ) stdInt = EMS_ZERO;
	stdInt = (float)(sqrt(stdInt));
}


void MRC_MAP::normalize(void)
{
	long index;

	if ( exist == EMS_FALSE ) return;

	statistics();

	for ( index=0; index<mapSize; index++ )
		density[index] = (float)((density[index] - aveInt) / stdInt);

	maxInt = (float)((maxInt - aveInt) / stdInt);
	minInt = (float)((minInt - aveInt) / stdInt);
	aveInt = 0.0; stdInt = 1.0;

	modify = EMS_TRUE;
}


void MRC_MAP::bin2D(void)
{
	int xx, yy, binX, binY, binBox2;
	long x, y, z, index, binMapSize;
	float *binMap, binSum;

	binX = dimX / binBox;
	binY = dimY / binBox;
	binBox2 = binBox * binBox;

	binMapSize = (long)binX * binY * dimZ;
	binMap = new float[binMapSize];

	for ( z=0; z<dimZ; z++ ) {
		for ( y=0; y<binY; y++ ) {
			for ( x=0; x<binX; x++ ) {
				binSum = 0.0;

				for ( yy=0; yy<binBox; yy++ ) {
					for ( xx=0; xx<binBox; xx++ ) {
						index = (z*dimY+y*binBox+yy)*dimX + x*binBox + xx;
						binSum += density[index];
					}
				}

				binMap[(z*binY+y)*binX+x] = binSum / binBox2;
			}
		}
	}

	delete [] density;

	dimX = binX; pixelX *= binBox;
	dimY = binY; pixelY *= binBox;
	mapSize = binMapSize;

	density = new float[mapSize];
	memcpy(density, binMap, sizeof(float)*mapSize);
	statistics();

	delete [] binMap;
	modify = EMS_TRUE;
}


void MRC_MAP::bin3D(void)
{
	int xx, yy, zz, binX, binY, binZ, binBox3;
	long x, y, z, index, binMapSize;
	float *binMap, binSum;

	binX = dimX / binBox;
	binY = dimY / binBox;
	binZ = dimZ / binBox;
	binBox3 = binBox * binBox * binBox;

	binMapSize = (long)binX * binY * binZ;
	binMap = new float[binMapSize];

	for ( z=0; z<binZ; z++ ) {
		for ( y=0; y<binY; y++ ) {
			for ( x=0; x<binX; x++ ) {
				binSum = 0.0;

				for ( zz=0; zz<binBox; zz++ ) {
					for ( yy=0; yy<binBox; yy++ ) {
						for ( xx=0; xx<binBox; xx++ ) {
							index = ((z*binBox+zz)*dimY+y*binBox+yy)*dimX + x*binBox + xx;
							binSum += density[index];
						}
					}
				}

				binMap[(z*binY+y)*binX+x] = binSum / binBox3;
			}
		}
	}

	delete [] density;

	dimX = binX; pixelX *= binBox;
	dimY = binY; pixelY *= binBox;
	dimZ = binZ; pixelZ *= binBox;
	mapSize = binMapSize;

	density = new float[mapSize];
	memcpy(density, binMap, sizeof(float)*mapSize);
	statistics();

	delete [] binMap;
	modify = EMS_TRUE;
}
char MRC_MAP::resample2D(void)
{
	long x, y, z, x0, y0, x1, y1;
	long samMapSize, page;
	float rateX, rateY, xf, yf;
	float dA, dB, dC, dD, dE, dF, *samMap;

	if ( (samX<3) || (samY<3) ) {
		errReport("Resampling rate is too low!");
		return(EMS_FALSE);
	}

	rateX = 1.0f * dimX / samX;
	rateY = 1.0f * dimY / samY;
	samMapSize = (long)samX * samY * dimZ;
	samMap = new float[samMapSize];

	for ( z=0; z<dimZ; z++ ) {
		page = z * dimX * dimY;
		for ( y=0; y<samY; y++ ) {
			yf = rateY * y;
			y0 = (long)(floor(yf)); y1 = y0 + 1;
			if ( y1 == dimY ) { y0--; y1--; yf=(float)y1; }

			for ( x=0; x<samX; x++ ) {
				xf = rateX * x;
				x0 = (long)(floor(xf)); x1 = x0 + 1;
				if ( x1 == dimX ) { x0--; x1--; xf=(float)x1; }

				dA = density[page + y0 * dimX + x0];
				dB = density[page + y0 * dimX + x1];
				dC = density[page + y1 * dimX + x0];
				dD = density[page + y1 * dimX + x1];
				dE = (x1-xf) * dA + (xf-x0) * dB;
				dF = (x1-xf) * dC + (xf-x0) * dD;

				samMap[(z*samY+y)*samX+x] = (y1-yf) * dE + (yf-y0) * dF;
			}
		}
	
	}

	delete [] density;

	dimX = samX; pixelX *= rateX;
	dimY = samY; pixelY *= rateY;
	mapSize = samMapSize;

	density = new float[mapSize];
	memcpy(density, samMap, sizeof(float)*mapSize);
	statistics();

	delete [] samMap;
	modify = EMS_TRUE;

	return(EMS_TRUE);
}


char MRC_MAP::resample3D(void)
{
	long x, y, z, x0, y0, z0, x1, y1, z1;
	long samMapSize;
	float rateX, rateY, rateZ, xf, yf, zf;
	float dA, dB, dC, dD, dE, dF, *samMap;

	if ( (samX<3) || (samY<3) || (samZ<3) ) {
		errReport("Resampling rate is too low!");
		return(EMS_FALSE);
	}

	rateX = 1.0f * dimX / samX;
	rateY = 1.0f * dimY / samY;
	rateZ = 1.0f * dimZ / samZ;

	samMapSize = (long)samX * samY * samZ;
	samMap = new float[samMapSize];

	for ( z=0; z<samZ; z++ ) {
		zf = rateZ * z;
		z0 = (long)(floor(zf)); z1 = z0 + 1;
		if ( z1 == dimZ ) { z0--; z1--; zf=(float)z1; }

		for ( y=0; y<samY; y++ ) {
			yf = rateY * y;
			y0 = (long)(floor(yf)); y1 = y0 + 1;
			if ( y1 == dimY ) { y0--; y1--; yf=(float)y1; }

			for ( x=0; x<samX; x++ ) {
				xf = rateX * x;
				x0 = (long)(floor(xf)); x1 = x0 + 1;
				if ( x1 == dimX ) { x0--; x1--; xf=(float)x1; }

				dA = (x1-xf)*density[(z0*dimY+y0)*dimX+x0]+(xf-x0)*density[(z0*dimY+y0)*dimX+x1];
				dB = (x1-xf)*density[(z0*dimY+y1)*dimX+x0]+(xf-x0)*density[(z0*dimY+y1)*dimX+x1];
				dE = (y1-yf) * dA + (yf-y0) * dB;

				dC = (x1-xf)*density[(z1*dimY+y0)*dimX+x0]+(xf-x0)*density[(z1*dimY+y0)*dimX+x1];
				dD = (x1-xf)*density[(z1*dimY+y1)*dimX+x0]+(xf-x0)*density[(z1*dimY+y1)*dimX+x1];
				dF = (y1-yf) * dC + (yf-y0) * dD;

				samMap[(z*samY+y)*samX+x] = (z1-zf) * dE + (zf-z0) * dF;
			}
		}
	}

	delete [] density;

	dimX = samX; pixelX *= rateX;
	dimY = samY; pixelY *= rateY;
	dimZ = samZ; pixelZ *= rateZ;
	mapSize = samMapSize;

	density = new float[mapSize];
	memcpy(density, samMap, sizeof(float)*mapSize);
	statistics();

	delete [] samMap;
	modify = EMS_TRUE;

	return(EMS_TRUE);
}


char MRC_MAP::resample3D(double pix_size, double pix_ratio)
{
	long x, y, z, x0, y0, z0, x1, y1, z1;
	long samMapSize;
	int x_c, y_c, z_c, samXc, samYc, samZc;
	float rateX, rateY, rateZ, xf, yf, zf;
	float dA, dB, dC, dD, dE, dF, *samMap;

	if ( pix_ratio > EMS_ZERO ) {
		rateX = rateY = rateZ = (float)pix_ratio;
	}
	else if ( pix_size > EMS_ZERO ) {
		rateX = rateY = rateZ = (float)(pix_size/pixelX);
	}

	samX = (int)(floor(dimX/rateX + EMS_ZERO));
	samY = (int)(floor(dimY/rateY + EMS_ZERO));
	samZ = (int)(floor(dimZ/rateZ + EMS_ZERO));
	x_c = dimX/2; samXc = samX/2;
	y_c = dimY/2; samYc = samY/2;
	z_c = dimZ/2; samZc = samZ/2;

	samMapSize = (long)samX * samY * samZ;
	samMap = new float[samMapSize];

	// resampling from the map center
	for ( z=0; z<samZ; z++ ) {
		zf = rateZ * (z - samZc) + z_c;
		z0 = (long)(floor(zf)); z1 = z0 + 1;
		if ( z1 >= dimZ ) { z0=dimZ-2; z1=dimZ-1; zf=(float)z1; }

		for ( y=0; y<samY; y++ ) {
			yf = rateY * (y - samYc) + y_c;
			y0 = (long)(floor(yf)); y1 = y0 + 1;
			if ( y1 >= dimY ) { y0=dimY-2; y1=dimY-1; yf=(float)y1; }

			for ( x=0; x<samX; x++ ) {
				xf = rateX * (x - samXc) + x_c;
				x0 = (long)(floor(xf)); x1 = x0 + 1;
				if ( x1 >= dimX ) { x0=dimX-2; x1=dimX-1; xf=(float)x1; }

				dA = (x1-xf)*density[(z0*dimY+y0)*dimX+x0]+(xf-x0)*density[(z0*dimY+y0)*dimX+x1];
				dB = (x1-xf)*density[(z0*dimY+y1)*dimX+x0]+(xf-x0)*density[(z0*dimY+y1)*dimX+x1];
				dE = (y1-yf) * dA + (yf-y0) * dB;

				dC = (x1-xf)*density[(z1*dimY+y0)*dimX+x0]+(xf-x0)*density[(z1*dimY+y0)*dimX+x1];
				dD = (x1-xf)*density[(z1*dimY+y1)*dimX+x0]+(xf-x0)*density[(z1*dimY+y1)*dimX+x1];
				dF = (y1-yf) * dC + (yf-y0) * dD;

				samMap[(z*samY+y)*samX+x] = (z1-zf) * dE + (zf-z0) * dF;
			}
		}
	}

	delete [] density;

	dimX = samX; pixelX *= rateX;
	dimY = samY; pixelY *= rateY;
	dimZ = samZ; pixelZ *= rateZ;
	mapSize = samMapSize;

	density = new float[mapSize];
	memcpy(density, samMap, sizeof(float)*mapSize);
	statistics();

	delete [] samMap;
	modify = EMS_TRUE;

	return(EMS_TRUE);
}


char MRC_MAP::setup(int x, int y, int z, float px, float py, float pz, float *data)
{
	clear();

	dimX = x;
	dimY = y;
	dimZ = z;

	pixelX = px;
	pixelY = py;
	pixelZ = pz;

	mapSize = (long)dimX * dimY * dimZ;
	maxInt = aveInt = minInt = stdInt = 0.0;

	// MODE-2 MRC MAP ONLY
	mode = 2;

	if ( mapSize == 0 ) {
		errReport("Map dimension is undefined!");
		return(EMS_FALSE);
	}

	// when data is ready
	if ( data != NULL ) {

		density = new float[mapSize];

		if ( density == NULL ) {
			errReport("Cannot allocate enough memory!");
			return(EMS_FALSE);
		}

		memcpy(density, data, mapSize * sizeof(float));
		statistics();
	}

	exist = EMS_TRUE;
	encrypted = EMX_MRC_PLAIN;

	return(EMS_TRUE);
}
