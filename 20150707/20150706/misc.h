#ifndef __MISC_H
#define __MISC_H 1

#include <stdio.h>
#include <stdlib.h>

// parameters for random number generator
#define IM1 2147483563
#define IM2 2147483399
#define AM (1.0/IM1)
#define IMM1 (IM1-1)
#define IA1 40014
#define IA2 40692
#define IQ1 53668
#define IQ2 52774
#define IR1 12211
#define IR2 3791
#define NTAB 32
#define NDIV (1+IMM1/NTAB)
#define RNMX 0.99999988
#define RanDB 4096

extern long randSeed;

// random number generator
// flagReset=0  to reset with "-1"
// flagReset=-1 to reset with given SEED (<0)

inline double RandomNumb(long &idum, char flagReset=1)
{
	int i, j;
	long k;
	static long idum2 = 123456789;
	static long iy = 0;
	static long iv[NTAB];
	double randVal;
	static int rnext = RanDB;
	static double RanVal[RanDB];

	// full reset with "-1"
	if ( flagReset == 0 ) {
		idum = -1;
		rnext = 0;
	}

	// reset with given SEED
	else if ( flagReset == -1 ) {
		rnext = 0;
	}

	// get a random number
	else if ( rnext < RanDB ) {
		randVal = RanVal[rnext];
		rnext ++;
		return(randVal);
	}
	
	for ( i=0; i<RanDB; i++ ) {
		
		if ( idum <= 0 ) {
			
			if ( -idum < 1 )
				idum = 1;
			else
				idum *= - 1;
			
			idum2 = idum;
			
			for ( j=(NTAB+7); j>=0; j-- ) {
				k = idum / IQ1;
				idum = IA1 * (idum - k*IQ1) - k * IR1;
				
				if ( idum < 0 )
					idum += IM1;
				
				if (j < NTAB )
					iv[j] = idum;
			}
			
			iy = iv[0];
		}
		
		k = idum / IQ1;
		idum = IA1 * (idum - k*IQ1) - k * IR1;
		if ( idum < 0 ) idum += IM1;
		
		k = idum2 / IQ2;
		idum2 = IA2 * (idum2 - k*IQ2) - k * IR2;
		if ( idum2 < 0 ) idum2 += IM2;
		
		j = iy / NDIV;
		iy = iv[j] - idum2;
		iv[j] = idum;
		if ( iy < 1 ) iy += IMM1;
		
		randVal = AM * iy;
		if ( randVal > RNMX)
			RanVal[i] = RNMX;
		else
			RanVal[i] = randVal;
	}
	
	if ( flagReset <= 0 )
		return(0.0);

	rnext = 1;
	return(RanVal[0]);
}


inline void msgReport(char *msg)
{
  printf(">>> %s\n", msg);
  return;
}


inline void errReport(char *msg)
{
  printf("ERROR: %s\n", msg);
  return;
}


inline void wrnReport(char *msg)
{
  printf("Warning: %s\n", msg);
  return;
}

#endif
