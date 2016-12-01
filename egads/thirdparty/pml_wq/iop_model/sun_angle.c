#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define M_PI 3.1415926536
#define radians(degrees) ((degrees) * M_PI / 180)
#define degrees(radians) ((radians) * 180 / M_PI)

#define USAGE "sun_angle <lat> <lon> <year> <julian> <gmt>"

/*==============================================================================
Calculates solar zenith and azimuth angles
	lat, lon	Coordinates in decimal degrees
	julian		Julian day
	gmt			Time GMT in format HH.MMSS
Outputs:
	zenith, azimuth
------------------------------------------------------------------------------*/
void sun_angle(double lat, double lon, int year, int julian, double gmt, double *zenith, double *azimuth);

int main (int argc, char *argv[])
{
	float	lat, lon, gmt;
	double	zenith, azimuth;
	int	year, julian;

        if(argc != 6){
           printf("%s\n", USAGE);
           exit(1);
        }

        sscanf(argv[1],"%f",&lat);
        sscanf(argv[2],"%f",&lon);
        sscanf(argv[3],"%d",&year);
        sscanf(argv[4],"%d",&julian);
        sscanf(argv[5],"%f",&gmt);

	sun_angle (lat, lon, year, julian, gmt, &zenith, &azimuth);
	printf ("%f\n", radians(zenith));
	
	return EXIT_SUCCESS;
}
/*==============================================================================
Calculates solar zenith and azimuth angles
Inputs:
   lat, lon	Coordinates in decimal degrees
   year         year
   julian	Julian day
   gmt		Time GMT in format HH.MMSS
Outputs:
   zenith, azimuth

Change history:
TJS: 25/1/2005 put in the correct formulation for the sun (azimuth) angle
------------------------------------------------------------------------------*/
void sun_angle(double lat, double lon, int year, int julian, double gmt,
                double *zenith, double *azimuth)
{
   double	time = gmt;
   int          yr, mo, A;
   double       JD, B, T, M, sinM, sin2M, sin3M, Cdeg, C, V, e;
   double       earthRadVec, seconds, e0deg, omega, epsilon, L0deg;
   double       L0, Odeg, lambda, sinSolarDec, solarDec, y, eqTime,
                solarTimeFix;
   double       trueSolarTime, hourAngle, mu0, theta0;
   double       azDenom, azRad, phi0;
   double       exoatmElevation, exoatmElevationdeg, exoatmElevationsub,
                exoatmElevationsubsub;
   double       refractionCorrection, te, tesub, tesub2;

   yr = year - 1;
   mo = 13;
   A = (int) floor(yr/100.);
   B = 2.0 - A + A/4;
   
/* The Julian day corresponding to the date
   Fractional days should be added later. */
   JD = floor(365.25*(yr+4716.))+floor(30.6001*(mo+1))+julian+B-1524.5;
/* centuries since J2000.0 */
   T=(JD+time/24.-2451545.)/36525.;   
/* The Geometric Mean Anomaly of the Sun in radians */
   M=radians(357.52911+T*(35999.05029-.0001537*T));
   sinM=sin(M);
   sin2M=sin(2.*M);
   sin3M=sin(3.*M);
   
/* Equation of sun centre in degrees */
   Cdeg=sinM*(1.914602-T*(.004817+.000014*T))+
        sin2M*(.019993-.000101*T)+
        sin3M*.000289;
	
/* Convert this to radians */
   C=radians(Cdeg);
/* Sun's true anamoly in radians */
   V=M+C;
/* The unitless eccentricity of Earth's orbit */
   e=.016708634-T*(.000042037+.0000001267*T);
/* Sun radius vector in AUs */
   earthRadVec=(1.000001018*(1.-e*e))/(1.+e*cos(V));
   seconds=21.448-T*(46.815+T*(.00059-T*.001813));
/* Mean obliquity of the ecliptic in degrees */
   e0deg=23.+(26.+seconds/60.)/60.;
   omega=radians(125.04-1934.136*T);
/* Corrected obliquity of the ecliptic in radians */
   epsilon=radians(e0deg+.00256*cos(omega));
/* Geometric Mean Longitude of the Sun in degrees/radians */
   L0deg=280.46646+T*(36000.76983+.0003032*T);
   
/* Remove multiples of 360 if L0deg >= 360 */
   if (L0deg >= 360.) {
      while (L0deg >= 360.) L0deg-=360.;
   }
   
/* Add multiples of 360 while L0deg < 0 */
   if (L0deg < 0.){ 
      while (L0deg < 0.) L0deg+=360;
   }
   
   L0 = radians(L0deg);
/* Sun's true longitude in degrees */
   Odeg=L0deg+Cdeg;
/* Sun's apparent longitude in radians */
   lambda=radians(Odeg-.00569-.00478*sin(omega));
   sinSolarDec=sin(epsilon)*sin(lambda);
/* Sun's declination in radians */
   solarDec=asin(sinSolarDec);
   y=(tan(epsilon/2.))*(tan(epsilon/2.));
/* equation of time in minutes of time */
   eqTime = 4.*degrees(y*sin(2.*L0)-2.0*e*sinM+
               4.*e*y*sinM*cos(2.*L0)-.5*y*y*sin(4.*L0)-1.25*e*e*sin2M);
   solarTimeFix=eqTime+4.*lon;
   trueSolarTime=time*60.+solarTimeFix;
   
/* reduce to be less than minutes of a day (1440) if needed*/  
   while (trueSolarTime > 1440.)
      trueSolarTime-=1440.;
   
   hourAngle=trueSolarTime/4.-180.;
   if (hourAngle < -180.) hourAngle+=360.;
   hourAngle = radians(hourAngle);
   mu0 = sin(radians(lat))*sinSolarDec+
           cos(radians(lat))*cos(solarDec)*cos(hourAngle);
   theta0=acos(mu0);
/* Sorting out the azimuth angle */
   azDenom=cos(radians(lat))*sin(acos(mu0)); 
   azRad=azDenom;
   phi0=azDenom;
   
   if(fabs(azDenom) > 0.01){
      azRad=(sin(radians(lat))*mu0-sinSolarDec)/azDenom;
      phi0=M_PI-acos(azRad);
      if (hourAngle > 0.)
         phi0*=-1.;
   } 
   else {
      if (lat > 0.){
         phi0=M_PI;
      } 
      else {
         phi0=0.;
      }
   }
   if (phi0 < 0.)
      phi0+=2.*M_PI;

/* Now do the second order effect calculations of refraction */
   exoatmElevation=M_PI/2.-theta0;
   exoatmElevationdeg=degrees(exoatmElevation);
   
   if (exoatmElevationdeg <= 85.){
      exoatmElevationsub=exoatmElevationdeg;
      te=tan(exoatmElevation);
      refractionCorrection=te;
      
      if (exoatmElevationsub > 5.){
         tesub=te;
         tesub2=tesub*tesub;
         refractionCorrection=(58.1-(.07+.000086/tesub2)/tesub2)/tesub;
      }
      if (exoatmElevationsub <= 5. && exoatmElevationsub > -0.575){
         exoatmElevationsubsub=exoatmElevationsub;
         refractionCorrection = 1735.+       
            exoatmElevationsubsub*(-518.2+exoatmElevationsubsub*(103.4+ 
            exoatmElevationsubsub*(-12.79+exoatmElevationsubsub*.711)));
      }
      if (exoatmElevationsub <= -0.575)
         refractionCorrection=-20.774/te;
	 
      refractionCorrection/=3600.;
      theta0-=radians(refractionCorrection); 
   }

/* Return the resultant zenith and azimuth angles in degrees */
   *zenith=degrees(theta0);
   *azimuth=degrees(phi0);
}
