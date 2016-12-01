#include "pml_iop.h"
#include "pml_iop_config.h" 
#include "pml_iop_tables.h"
#include "pml_iop_calculate.h"

/* Module: pml_iop_calculate */
/* Author: Tim Smyth and Gerald Moore */
/* Date: 13/2/2006 */
/* Version: 1.0 */
/* Description */

/* Function: iop_model */
int iop_model(double rho_w[],float sun_theta, float sen_theta, float dphi, double a[],
              double bbp[], double ady[], double ap[])
{

   int i,result;
   float eps_a, denominator, ady_0;
   float ady443, ady412, ap412;
   float ysbpa_sc, x1, x2;

   eps_a = eps_a_init;

   /* calculate the total absorption and backscatter */
   result = mod_iter(rho_w,sun_theta,sen_theta,dphi,eps_a,a,bbp);
   if (result != 0){
     /* fprintf(stderr,"Model iterations not converged\n");*/
     return result;      
   }

   /* using the spectral slopes between 412 and 443 work out ady */
   denominator = eps_y_412_443 - eps_p_412_443;

   if (a[0] > 0. && a[1] > 0. && a[2] > 0.){
      /* ady[0] = a[0]*eps_y_412_443/denominator - a[1]*eps_p_412_443*eps_y_412_443/denominator;
      ady[1] = ady[0]/eps_y_412_443;
      ady_440 = ady[1]; */

      /* new formulation to account for non-linear behavior of spectral slope in ady */
      result = biogeochem_iter(a[0], a[1], &ady443, &ady412, &ap412); 
      if (result != 0){
         fprintf(stderr,"Biogeochemical model iterations not converged\n");
         x1 = 0.1; /* set to a fake value of x1 so that empirical fix used */
      }
      else {
         ady[0] = ady412;
         ady[1] = ady443;
         ap[0] = ap412;

         /* calculate the spectral slope of CDOM from info at two shorter wavelengths */
         ysbpa_0 = lambda[1];
         ysbpa_sc = log(ady[0]/ady[1])/(lambda[0] - lambda[1]); 

         for(i=0;i<NB;i++){
            /* Apply gelbstoff slope and intercept (at 443) to give entire spectra */
            ady[i] = ady443*exp(ysbpa_sc*(lambda[i] - ysbpa_0));
            /* Calculate spectral ap (absorption due to pigments) using the remainder */   
            ap[i] = a[i] - ady[i];
         }
      
         /* check aph443 range (this sanity check is an empirical fix from the Lee model */
         x1 = ap[1] / a[1];
      }
      if ( x1 < 0.15 || x1 > 0.6 ) {
         /* ratio is between 443 and 412 */
         x2 = -0.8 + 1.4 * (a[1]/a[0]);
         if ( x2 < 0.15 ) 
            x2 = 0.15;
         if ( x2 > 0.6 ) 
            x2 = 0.6;
         ap[1] = a[1] * x2;
         ady_0 = a[1] - ap[1];

         for (i=0;i<NB;i++) {
            /* Use the preset slope for gelbstoff */
            ady[i] = ady_0 * exp( ysbpa_s * (lambda[i] - ysbpa_0));
            ap[i] = a[i] - ady[i];
         }
         
         result = 0; /* Perhaps need to put more sophisticated error handling here */
      }
   }         
   /* End of the empirical fix */

   return result;
}

/* Function: mod_iter */
int mod_iter(double rho_w[],float sun_theta, float sen_theta, float dphi, float eps_a, double a[], double bb[])
{
   int    i,j,k,result, loop_counter, al, bl; 
   double b[NB], FC[NB];
   double rho_wT[2],awT[2],bbwT[2],FT[2];
   double ab[2];
   double temp, eps_bb;
   double a_i, bb_i;
   float bbw[NB]; /* backscatter due to pure water */
   float bn[NB]; 
   float temp_a[NB],temp_bb[NB]; 
   float eps_a_m[5] = {1.402,1.641,1.268,1.536,1.834}; /* slopes between successive wavelengths move this to the config file*/
   float minimise;
   float rho_w_mod[NB];
   float previous_min;
   int fail = 2;
      
   /* Set the relevant geometry */
   setgeom(sun_theta, sen_theta, dphi);

   temp=pow(lambda[bp[1]]/scat_l,scat_n);
   for (i=0;i<NB;i++){
      bbw[i]=b_w[i]*b_tilde_w;
      bn[i]=pow(lambda[i]/scat_l,scat_n);
      bn[i]=bn[i]/temp;
   }
   
   /* The result of this is eps_b of 1.0202 - as in paper */
   eps_bb=bn[bp[0]];
   previous_min = 1.0; /* set this to the minimum convergence criterion */

   rho_wT[0]=rho_w[bp[0]];
   rho_wT[1]=rho_w[bp[1]];
   awT[0]=a_w[bp[0]];
   awT[1]=a_w[bp[1]];
   bbwT[0]=bbw[bp[0]];
   bbwT[1]=bbw[bp[1]];

   loop_counter = 0;
   for (j=-2;j<2;j++){
      for (al=0;al<90;al++){
         a_i = pow(10,1.0*j)+al*pow(10,1.0*j-1);
         for (i=-3;i<1;i++){
            for (bl=0;bl<90;bl++){
               bb_i = pow(10,1.0*i)+bl*pow(10,1.0*i-1);
               loop_counter+=1;
               /* Solving for 510 nm - everything at 490 nm in terms of 510 */
               /* implement the caseII formulation as well */
               if (CASEII){
               /* possibly need to add in pure water term as well */
                  FT[0] = f_ab(a_i*eps_a,(bb_i/b_tilde_p)*eps_bb,bp[0])*(1. + (bb_i*eps_bb+bbw[bp[0]])/(a_i*eps_a + a_w[bp[0]]));
                  FT[1] = f_ab(a_i,bb_i/b_tilde_p,bp[1])*(1. + (bb_i+bbw[bp[1]])/(a_i+a_w[bp[1]]));
               }
               else {
                  FT[0] = f_ab(a_i*eps_a,(bb_i/b_tilde_p)*eps_bb,bp[0]);
                  FT[1] = f_ab(a_i,bb_i/b_tilde_p,bp[1]);
               }
               temp_a[bp[1]] = a_i; /* a(510) nm */
               temp_a[bp[0]] = a_i*eps_a; /* a(490) nm */
               for (k=0;k<NB;k++){
                  temp_bb[k]=bb_i*bn[k]; /* spectral bb assuming slope */
                  b[k]=temp_bb[k]/b_tilde_p;
               }
               /* now calculate the values of a using spectral slopes */
               /* this needs improving in terms of the coding */
               /* a443 */
               temp_a[1] = temp_a[bp[0]]*eps_a_m[1];
               /* a412 */
               temp_a[0] = temp_a[1]*eps_a_m[0];
               /* a555 */
               temp_a[4] = temp_a[bp[1]]/eps_a_m[3];
               /* a670 */
               temp_a[5] = temp_a[4]/eps_a_m[4];
               /* printf("a[412]: %f; a[443]: %f; a[490]: %f; a[510]: %f; a[555]: %f\n", a[0], a[1], a[2], a[3], a[4]);
               printf("bb[412]: %f; bb[443]: %f; bb[490]: %f; bb[510]: %f; bb[555]: %f\n", bb[0], bb[1], bb[2], bb[3], bb[4]); */
         
               minimise = 0;
               for (k=0;k<5;k++){
                  if (CASEII){
                     /* need to put the correction to the surface interface term here */
                     FC[k] = f_ab(temp_a[k],temp_bb[k]/b_tilde_p,k)*(1. + (temp_bb[k]+bbw[k])/(temp_a[k]+a_w[k]));
                     rho_w_mod[k] = FC[k]*(temp_bb[k]+bbw[k])/(temp_a[k]+a_w[k]+temp_bb[k]+bbw[k]);
                  }
                  else {
                     FC[k] = f_ab(temp_a[k],temp_bb[k]/b_tilde_p,k);
                     rho_w_mod[k] = FC[k]*(temp_bb[k]+bbw[k])/(temp_a[k]+a_w[k]);
                  }
                  minimise += fabs((rho_w_mod[k] - rho_w[k])/rho_w[k]);
               }
            
               /* minimise differences in rho */
               /* possible improvements:
                  1) % difference in rho_w
                  2) idea of the quality of the retrieval of bb and a (possibly the percentage difference in rho 
                  3) could minimise on individual wavelengths rather than a complete spectrum */
               if (minimise < previous_min){
                  previous_min = minimise;
                  /* printf("Modelled - rho[412]: %f; rho[443]: %f; rho[490]: %f; rho[510]: %f; rho[555]: %f\n", rho_w_mod[0], rho_w_mod[1], rho_w_mod[2], rho_w_mod[3], rho_w_mod[4]);
                  printf("Measured - rho[412]: %f; rho[443]: %f; rho[490]: %f; rho[510]: %f; rho[555]: %f\n", rho_w[0], rho_w[1], rho_w[2], rho_w[3], rho_w[4]);
                  printf("Modelled - a[412]: %f; a[443]: %f; a[490]: %f; a[510]: %f; a[555]: %f\n", a[0], a[1], a[2], a[3], a[4]);
                  printf("Measured - bb[412]: %f; bb[443]: %f; bb[490]: %f; bb[510]: %f; bb[555]: %f\n", bb[0], bb[1], bb[2], bb[3], bb[4]);
                  printf("rho_w differences: %f\n", minimise); */
                  for (k=0; k<NB;k++){
                     a[k] = temp_a[k];
                     bb[k] = temp_bb[k];
                  }
                  fail=0;
               }                
            }
         }
      }
   }
   /* printf("Number of loops: %d\n", loop_counter); */
   /* printf("surface_term: %f\n", surface_term); */ 
   return fail;
}   

/* Function: iter_ab */
/* Returns the new a and b values for CASEI formulation */
int iter_ab(double rho_w[],double aw[],double bbw[],double F[],double epsb,double epsa, double ab[])
{
   int result=0;
   double x,y,z,n;
   double scale;

   x=F[0]*rho_w[1];
   y=epsb*x;
   z=epsa*F[1]*rho_w[0];
   n=z-y;
   scale=y-z;
   if (scale == 0.0) {
     if(VERB_MOD){ 
        printf("iter_ab: scale == 0\n");
        printf("iter_ab: epsa %f epsb %f F[0] %f F[1] %f \n",epsa,epsb,F[0],F[1]);
     }
     ab[0]=-1.0;
     ab[1]=-1.0;
     result = 1;
     return result;   
   }
   if(VERB_MOD)  
      printf("iter_ab: x=%f, y=%f, z=%f, n=%f\n",x,y,z,n);
   /* a510 */
   ab[0]=(F[0]*F[1]*(bbw[1]*epsb-bbw[0])+aw[0]*F[1]*rho_w[0]-aw[1]*y)/scale; 
   /* bb510 */
   ab[1]=(rho_w[0]*rho_w[1]*(aw[0]-aw[1]*epsa)-bbw[0]*x+bbw[1]*z)/scale;
   
   if (ab[0] < 0. || ab[1] < 0.) {
      ab[0]=-1.0;
      ab[1]=-1.0;
      result  = 1;
      return result;
   }
   
   if (VERB_MOD) printf("iter_ab: a=%f, b=%f\n",ab[0],ab[1]);
   return result;
}

/* Function: iter_ab2 */
/* Returns the new a and b values for CASEII formulation */
int iter_ab2(double rho_w[],double aw[],double bbw[],double F[],double epsb,double epsa, double ab[])
{
   int result=0;
   double y,z;
   double scale_bb, scale_a;

   z=epsa*(rho_w[0]*rho_w[1] - rho_w[0]*F[1]);
   y=epsb*(rho_w[0]*rho_w[1] - rho_w[1]*F[0]);
   scale_a=z-y;
   
   z=-epsa*(rho_w[0]*rho_w[1] - rho_w[0]*F[1]);
   y= epsb*(rho_w[0]*rho_w[1] - rho_w[1]*F[0]);
   scale_bb=z+y; 
   

   if (scale_a == 0.0 || scale_bb == 0.0) {
     if(VERB_MOD){ 
        printf("iter_ab2: scale == 0\n");
        printf("iter_ab2: epsa %f epsb %f F[0] %f F[1] %f \n",epsa,epsb,F[0],F[1]);
     }
     ab[0]=-1.0;
     ab[1]=-1.0;
     result = 1;
     return result;   
   }
   if(VERB_MOD)  
      printf("iter_ab2: scale_a=%f, scale_bb=%f\n",scale_a,scale_bb);
   /* a510 */
   ab[0]=( epsb*(rho_w[0]-F[0])*(rho_w[1]*(aw[1]+bbw[1])-F[1]*bbw[1]) + (rho_w[1]-F[1])*(F[0]*bbw[0]-rho_w[0]*(aw[0]+bbw[0])) ) / scale_a; 
 
   /* bb510 */
   ab[1]=( -rho_w[0]*(epsa*(F[1]*bbw[1]-rho_w[1]*(aw[1]+bbw[1])) + rho_w[1]*(aw[0]+bbw[0])) + rho_w[1]*F[0]*bbw[0] ) / scale_bb;


   if (ab[0] < 0. || ab[1] < 0.) {
      ab[0]=-1.0;
      ab[1]=-1.0;
      result  = 1;
      return result;
   }

   if (VERB_MOD) printf("iter_ab2: a=%f, b=%f\n",ab[0],ab[1]);
   return result;
}


/* Function: iter_a */
/* Solve the absorption coefficient given the backscatter */
double iter_a(double rho_w,double aw,double bbw,double F,double bb) 
{
   double a;
   a=F*(bb+bbw)/rho_w-aw;
   if (VERB_MOD) printf("iter_a output: %f\n",a);
   return a;
}

/* Function: iter_a */
/* Solve the absorption coefficient given the backscatter */
/* Case II waters */
double iter_a2(double rho_w,double aw,double bbw,double F,double bb) 
{
   double a;
   a=F*(bb+bbw)/rho_w-(aw+bb+bbw);
   if (VERB_MOD) printf("iter_a2 output: %f\n",a);
   return a;
}

/* Function: biogeochem_iter */
/* Iterates until convergence on the "measured" value of a412 */
int biogeochem_iter(float a412, float a443, float *ady443, float *ady412, float *aph412)
{    
   float ady443_upper, ady443_lower, ady443_next;
   float a412_m, df;
   float aph412_m, ady412_m;
   float TOL=0.001;
   float MAXIT=20;
   int result, iter=0;

   /* Lower first guess for ady443 = 0.01*a443 */
   /* Upper first guess for ady443 = a443 - biogeochem tolerance */
   ady443_lower = 0.01*a443;
   ady443_upper = a443 - TOL;

   /* first pass of the functions to get initial guesses */
   result = biogeochem_mod(a443, ady443_lower, &a412_m, &ady412_m, &aph412_m);
   result = biogeochem_mod(a443, ady443_upper, &a412_m, &ady412_m, &aph412_m);

   do {
      /* bisect the interval */
      ady443_next = 0.5*(ady443_lower+ady443_upper);
      result = biogeochem_mod(a443,ady443_next, &a412_m, &ady412_m, &aph412_m);
      /* test to see if overestimate or underestimate */
      if ((a412_m - a412) > 0.)
	     ady443_upper = ady443_next;
      if ((a412_m - a412) < 0.)
         ady443_lower = ady443_next;
      /* absolute difference to see if convergence met */
      df = fabs(a412_m - a412);
      iter ++;

   } while ((iter <= MAXIT) && (df >= TOL));

   /* Return error if maximum number of iterations exceeded */
   if (iter > maxit)
      return 1;

   *ady443 = ady443_next;
   *ady412 = ady412_m;
   *aph412 = aph412_m;

   return 0;
}


/* Function: biogeochem_mod */
/* This function was created because of the failure of the */
/* analytical expression, which contained in effect a first order */
/* polynomial for the spectral slope */
/* Function returns the value of a412 which can be compared with the value of a412 */
/* obtained from the primary IOP part of the PML IOP model */
int biogeochem_mod(float a443, float ady443, float *a412_m, float *ady412_m, float *aph412_m)
{
   float ady_part, aph_part;

   float A=0.059;
   float B=1.099;
   float C=0.229;
   float D=0.004;
   float E=1.033;
   float F=-0.059;

   ady_part = A*pow(log10(ady443),2) + B*log10(ady443) + C;
   aph_part = D*pow(log10(a443 - ady443),2) + E*log10(a443-ady443) + F;

   *a412_m = pow(10,ady_part) + pow(10,aph_part);
   *ady412_m = pow(10,ady_part);
   *aph412_m = pow(10,aph_part);

   return 0;
}
