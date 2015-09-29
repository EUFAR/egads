#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <zlib.h>
#include "pml_iop.h"
#include "pml_iop_config.h"
#include "pml_iop_tables.h"
#include "pml_iop_calculate.h"
#include "pml_iop_global.h"

int main(int argc, char *argv[])
{
   int i,j,pixel; 
   int configflag = 0; /* Config flag - if not raised set to default pml.cfg */
   int sun_theta_flag = 0, sen_theta_flag = 0, dphi_flag = 0, Rrs_flag = 0; 
   int pure_water_flag = 0;
   int result = 0; /* flag for successful iterations */
   float sun_theta, sen_theta, dphi; /* Geometry in radians */
   double Rrs[NB], rho_w[NB];
   double a[NB],bbp[NB],ady[NB],ap[NB];
   double ap_490, ap_510, AP; /* Accessory pigment calculations */
   static int GLOBAL = 0; /* processing for global nLws */
   int single_point = 0; /* flag for the single point mode (default off) */
   int line = 0; /* line of the global imagery */
   int month; /* month to determine the solar geometry */
   char configfname[200];
   int sensorID = 5; /* To make code in common with the SeaDAS version */
   
   for(i=0;i<argc;i++){
      if(strncmp(argv[i],"-help",5) == 0){
         printf("Usage: pml_iop_model [-help] [-pure_water] [-config <config_file>]\n");
         printf("[-sun_theta <sun_theta_radians>] [-sen_theta <sen_theta_radians>]\n");
         printf("[-dphi <dphi_radians>] [-Rrs <rrs412 rrs443 rrs490 rrs510 rrs555 rrs670>]\n");
         printf("[-rhow <rhow412 rhow443 rhow490 rhow510 rhow555 rhow670>]\n");
         exit(0);
      }
      if(strncmp(argv[i],"-config",7) == 0){
         sprintf(configfname,"%s",argv[i+1]);
         configflag = 1;
      } 
      if(strncmp(argv[i],"-sun_theta",8) == 0){
         sscanf(argv[i+1],"%f",&sun_theta);
         sun_theta_flag = 1;
      }
      if(strncmp(argv[i],"-sen_theta",8) == 0){
         sscanf(argv[i+1],"%f",&sen_theta);
         sen_theta_flag = 1;
      }
      if(strncmp(argv[i],"-dphi",8) == 0){
         sscanf(argv[i+1],"%f",&dphi);
         dphi_flag = 1;
      }
      if(strncmp(argv[i],"-Rrs",4) == 0){
         single_point = 1;
         for(j=0;j<NB;j++){     
            sscanf(argv[i+(j+1)], "%lf", &Rrs[j]);
         }
         Rrs_flag = 1;
      }
      if(strncmp(argv[i],"-rhow",5) == 0){
         single_point = 1;
         for(j=0;j<NB;j++){     
            sscanf(argv[i+(j+1)], "%lf", &rho_w[j]);
         }
      }
      if(strncmp(argv[i],"-s",2) == 0){
         sscanf(argv[i+1], "%d", &width);
         sscanf(argv[i+2], "%d", &height);
         npix = width*height;
      }
      if(strncmp(argv[i],"-global",7) == 0){
         sscanf(argv[i+1],"%04d", &yymm);
         GLOBAL = 1;
      }
      if(strncmp(argv[i],"-month",6) == 0){
         sscanf(argv[i+1],"%02d", &month);
      }
      if(strncmp(argv[i],"-odir",5) == 0){
         sprintf(OUTDIR,"%s",argv[i+1]);
      }
      if(strncmp(argv[i],"-idir",5) == 0){
         sprintf(INDIR,"%s",argv[i+1]);
      }
      if(strncmp(argv[i],"-pure_water",11) == 0){
         pure_water_flag = 1;
      }
   }

   if(configflag == 0){
       sprintf(configfname,"%s",DEFAULT_CFG);
   }
   
   /* If the solar, satellite and azimuth angles not passed in set to default */
   if(sun_theta_flag == 0) sun_theta = 0.785; /* Solar zenith of 45 degrees */
   if(sen_theta_flag == 0) sen_theta = 0.0;
   if(dphi_flag == 0) dphi = 0.0; 

   /* Load the various LUTs into memory */
   load_work_tab(configfname, sensorID);

   /* Load the various parameters into memory */
   load_config(configfname);

   if(single_point == 1){
      for(i=0;i<NB;i++){
         if(Rrs_flag) rho_w[i] = M_PI*Rrs[i];
      }
   
      /* call iop_model - the matrices a, bbp, ady and ap hold spectral info*/
      result = iop_model(rho_w,sun_theta,sen_theta,dphi,a,bbp,ady,ap);
   
      /* printf("a412 a443 a490 a510 a555 a670 ady412 ady443 ady490 ady510 ady555 ady670 ap412 ap443 ap490 ap510 ap555 ap670 bbp412 bbp443 bbp490 bbp510 bbp555 bbp670\n"); */

	if (result != 0){
	
	    for(i=0;i<NB;i++){
              a[i]=-9.9;
              ady[i]=-9.9;
              ap[i]=-9.9;
              bbp[i]=-9.9;
            }
        }
	
        for(i=0;i<NB;i++){
           if (pure_water_flag == 1){
              if (a[i] > 0)		  
                 printf("%f ", a[i]+a_w[i]); 
              else
                 printf("%f ", a[i]);
           }
           else
              printf("%f ", a[i]);		  
        }				  
        for(i=0;i<NB;i++){		  
              printf("%f ", ady[i]);	  
        }				  
        for(i=0;i<NB;i++){		  
              printf("%f ", ap[i]);	  
        }				  
        for(i=0;i<NB;i++){		  
              printf("%f ", bbp[i]);	  
        }				  
         
      printf("\n");
   }
   
   if(GLOBAL == 1){
      /* Read in the zenith angle lookup table */
      read_zenith_byte();
      read_global_imagery();
      /* Allocate the memory - need to think about deallocating it later */
      /* Do band interleaved storage */
      atot = malloc(width*height*NB*sizeof(float));
      adg = malloc(width*height*NB*sizeof(float));
      aph = malloc(width*height*NB*sizeof(float));
      bb = malloc(width*height*NB*sizeof(float));
      TC = malloc(width*height*sizeof(float));
      aph_ratio = malloc(width*height*sizeof(float));
      
      for(pixel=0;pixel<width*height;pixel++){
         if (pixel % width == 0) {
            line ++;
            sun_theta = zenith_float[12*line+(month - 1)];
         }
         if(nLw412[pixel] > 0. && nLw443[pixel] > 0. && nLw490[pixel] > 0. &&
            nLw510[pixel] > 0. && nLw555[pixel] > 0. && nLw670[pixel] > 0.){
            rho_w[0] = M_PI*nLw412[pixel]/F0[0];
            rho_w[1] = M_PI*nLw443[pixel]/F0[1];
            rho_w[2] = M_PI*nLw490[pixel]/F0[2];
            rho_w[3] = M_PI*nLw510[pixel]/F0[3];
            rho_w[4] = M_PI*nLw555[pixel]/F0[4];
            rho_w[5] = M_PI*nLw670[pixel]/F0[5];
            
            /* call iop_model - the matrices a, bbp, ady and ap hold spectral info*/
            result = iop_model(rho_w,sun_theta,sen_theta,dphi,a,bbp,ady,ap);
            for(i=0;i<NB;i++){
               /* change in nomenclature is in line with Lee model output (model first */
               /* to have global data applied */
	       
	       /* atot[(pixel*NB)+i] = a[i]+a_w[i]; */
               atot[(pixel*NB)+i] = a[i];
               
	       adg[(pixel*NB)+i] = ady[i];
               aph[(pixel*NB)+i] = ap[i];
               bb[(pixel*NB)+i] = bbp[i];
            }
         
            /* Work out the total chlorophyll from 443, 490, 510 combination */
            /* Accessory pigments at 490 and 510 - work out mean AP */
            ap_490 = aph[(pixel*NB)+2]/a_ap_star_490;
            ap_510 = aph[(pixel*NB)+3]/a_ap_star_510;
            /* set AP to zero if ap_490 and ap_510 are negative */
            AP = 0.;
            if(ap_490 > 0. && ap_510 > 0.)
               /* AP = (ap_490+ap_510)/2.; */
               AP = ap_490;
         
            /* 443 has contribution for accessories and total chlorophyll */
            /* TC[pixel] = (aph[(pixel*NB)+1] - AP*a_ap_star_443)/a_chl_star_443;*/
            /* This relationship with TC is from Bricaud 1998 */
            TC[pixel] = pow((aph[(pixel*NB)+1]/0.0378),1.595);
            /* TC[pixel] = pow((aph[(pixel*NB)+1]/0.0520),1.575); */

            /* Now to find the species of phytoplankton */
            aph_ratio[pixel] = a_chl_star_443*a_chl_ratio*TC[pixel]/aph[(pixel*NB)+1];

         }
      }
      /* Now write out the band specific atot, aph and bb */
      write_global_imagery();      
   }
   
   return 0;
}

/* function to read in the global imagery
based on the wavelengths provided and a yymm integer
supplied by the user.  The arrays are populated here and
made available to the rest of the code as static floats */
static void read_global_imagery(void){
   int size, i, decimal, negative;
   int strlen=3;
   char nLw_image_filename[100];
   char *lambda;
  
   gzFile file;

   /* initialise the arrays based on the user input of width and height */
   size = width*height*sizeof(float); 
   nLw412 = malloc(size);
   nLw443 = malloc(size);
   nLw490 = malloc(size);
   nLw510 = malloc(size);
   nLw555 = malloc(size);
   nLw670 = malloc(size);

   /* use fwave in here to read in the various bands */
   for (i=0;i<NB;i++){
      /* convert the float (fwave) to a string (lambda) */
      lambda = ecvt(fwave[i],strlen,&decimal,&negative);
      /* nLw image filename based on wavelength and yymm */
      sprintf(nLw_image_filename,"%s/nLw_%s_%04d.flw.gz",INDIR,lambda,yymm);
      if (nLw_image_filename == NULL){
         fprintf(stderr,"Need to enter correct filename\n");
         exit(1);
      }
      printf("Reading in: %s\n", nLw_image_filename);
      if ((file = gzopen(nLw_image_filename, "rb")) == NULL) {
         fprintf(stderr, "Could not open %s\n", nLw_image_filename);
         exit(1);
      }
      /* switch based on wavelength (currently set to SeaWiFS bands) */
      switch((int)fwave[i]){
         case 412:
            if (gzread(file, nLw412, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         case 443:
            if (gzread(file, nLw443, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         case 490:
            if (gzread(file, nLw490, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         case 510:
            if (gzread(file, nLw510, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         case 555:
            if (gzread(file, nLw555, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         case 670:   
            if (gzread(file, nLw670, size) != size) {
               fprintf(stderr, "Could not read image from %s (file too small?)\n", nLw_image_filename);
               gzclose(file);
               exit(1);
            }
            break;
         default:
            printf("No such wavelength\n");
            break;
      }
      /* close the file */
      gzclose(file);
   }
}

/* Need to write out global imagery */
static void write_global_imagery()
{
   int i,size,pixel,decimal,negative;
   int strlen=3;
   char *lambda;
   char atot_image_filename[100];
   char aph_image_filename[100];
   char ady_image_filename[100];
   char bb_image_filename[100];
   char tc_image_filename[100];
   char aph_ratio_image_filename[100];
   
   float *atot_lambda, *aph_lambda, *ady_lambda, *bb_lambda;

   gzFile *atot_file, *aph_file, *ady_file, *bb_file, *tc_file, *aph_ratio_file;

   size = width*height*sizeof(float); 

   for(i=0;i<NB;i++){
      atot_lambda = malloc(width*height*sizeof(float));
      aph_lambda = malloc(width*height*sizeof(float));
      ady_lambda = malloc(width*height*sizeof(float));
      bb_lambda = malloc(width*height*sizeof(float));
      lambda = ecvt(fwave[i],strlen,&decimal,&negative);
      /* IOP image filename based on wavelength and yymm */
      printf("Creating IOP outputs at %s nm ...\n", lambda);
      sprintf(atot_image_filename,"%s/atot_%s_%04d.flw.gz",OUTDIR,lambda,yymm);
      sprintf(aph_image_filename,"%s/aph_%s_%04d.flw.gz",OUTDIR,lambda,yymm);
      sprintf(ady_image_filename,"%s/ady_%s_%04d.flw.gz",OUTDIR,lambda,yymm);
      sprintf(bb_image_filename,"%s/bb_%s_%04d.flw.gz",OUTDIR,lambda,yymm);
      /* printf("%s\n",atot_image_filename);
      printf("%s\n",aph_image_filename);
      printf("%s\n",ady_image_filename);
      printf("%s\n",bb_image_filename);  */
      if ((atot_file = gzopen(atot_image_filename, "wb")) == NULL) {
         fprintf(stderr, "Could not open %s\n", atot_image_filename);
         exit(1);
      }
      if ((aph_file = gzopen(aph_image_filename, "wb")) == NULL) {
         fprintf(stderr, "Could not open %s\n", aph_image_filename);
         exit(1);
      } 
      if ((ady_file = gzopen(ady_image_filename, "wb")) == NULL) {
         fprintf(stderr, "Could not open %s\n", ady_image_filename);
         exit(1);
      }
      if ((bb_file = gzopen(bb_image_filename, "wb")) == NULL) {
         fprintf(stderr, "Could not open %s\n", bb_image_filename);
         exit(1);
      }  
      /* retrieve the individual bands from the BIP created in 
      main function */   
      for(pixel=0;pixel<width*height;pixel++){
         atot_lambda[pixel] = atot[(pixel*NB)+i];
         aph_lambda[pixel] = aph[(pixel*NB)+i];
         ady_lambda[pixel] = adg[(pixel*NB)+i];
         bb_lambda[pixel] = bb[(pixel*NB)+i];
      }
      
      /* now write out to file */
      gzwrite(atot_file, atot_lambda, size);
      gzwrite(aph_file, aph_lambda, size); 
      gzwrite(ady_file, ady_lambda, size);
      gzwrite(bb_file, bb_lambda, size); 
      
      /* close the files */ 
      gzclose(atot_file);
      gzclose(aph_file); 
      gzclose(ady_file);
      gzclose(bb_file); 
      
      /* free up the temporary array memory */
      free(atot_lambda);
      free(aph_lambda); 
      free(ady_lambda);
      free(bb_lambda); 
   }

   /* write out the global total-chlorophyll product and absorption ratio */
   sprintf(tc_image_filename,"%s/tc_%04d.flw.gz",OUTDIR,yymm);   
   sprintf(aph_ratio_image_filename,"%s/aph_ratio_%04d.flw.gz",OUTDIR,yymm);
   if ((tc_file = gzopen(tc_image_filename, "wb")) == NULL) {
      fprintf(stderr, "Could not open %s\n", tc_image_filename);
      exit(1);
   }
   if ((aph_ratio_file = gzopen(aph_ratio_image_filename, "wb")) == NULL) {
      fprintf(stderr, "Could not open %s\n", aph_ratio_image_filename);
      exit(1);
   }
   
   /* now write out to file */
   gzwrite(tc_file,TC,size);
   gzwrite(aph_ratio_file,aph_ratio,size);
   
   /* close the files */
   gzclose(tc_file);
   gzclose(aph_ratio_file);

   /* free up the BIP memory created in the main routine */
   free(atot);
   free(aph);
   free(adg);
   free(bb);
   free(TC);
   free(aph_ratio);
}

static void read_zenith_byte()
{
   int i,j,size;
   int nmonths=12;
   unsigned char *zenith;
   float slope;
   char zenith_image_filename[100];
   
   gzFile *zenith_file;

   size = nmonths*height*sizeof(unsigned char); 
   zenith = malloc(size);
   zenith_float = malloc(nmonths*height*sizeof(float));
   slope = M_PI/2./255.;
   
   sprintf(zenith_image_filename,"data/solar_zenith_monthly.8bit.gz");
   
   if ((zenith_file = gzopen(zenith_image_filename, "rb")) == NULL) {
      fprintf(stderr, "Could not open %s\n", zenith_image_filename);
      exit(1);
   }
   
   if (gzread(zenith_file, zenith, size) != size) {
      fprintf(stderr, "Could not read image from %s (file too small?)\n", zenith_image_filename);
      gzclose(zenith_file);
      exit(1);
   }

   gzclose(zenith_file);
   
   for(i=0;i<nmonths;i++){
     for(j=0;j<height;j++){
        zenith_float[i+nmonths*j] = slope*zenith[i+nmonths*j];
     }
   }

}
