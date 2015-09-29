#include <math.h>
#include "pml_iop.h"
#include "pml_iop_config.h"
#include "pml_iop_tables.h"
#include "pml_iop_calculate.h"

/* Module: pml_iop_tables.c */
/* Authors: Gerald Moore and Tim Smyth */
/* Date: 07/03/05 */
/* Version: 1.7 */
/* Description: Module containing functions to read in the various */
/* tables defined in the config file and to perform interpolations */

#define MAX_LINE 180

float *lambda,*a_w,*b_w;
/* Geophysical (GOP) variables */
long nband, ch_n, sp_n, od_n;
float *ch_lev, *ac[MAX_BANDS], *bc[MAX_BANDS];
float *sp_lev, *as[MAX_BANDS], *bs[MAX_BANDS];
float *od_lev, *od[MAX_BANDS];

/* IOP variables */
long th_s_n, th_v_n, dphi_n;
float *th_s_lev, *th_v_lev, *dphi_lev;
long ap_n, bp_n;
float *ap_lev, *bp_lev;

float *refen;    /* The pointer for refen.*/
static long refind=0l; /* current index */
static long refind_max=0l;

/* Constants for interior conversions */
/* loaded by config routine */
int bp[2], maxit;
int CASEII;
float b_tilde_w, b_tilde_p, init_chl, eps_a_init, eps_bb_init;
float scat_a, scat_b, scat_c, scat_n, scat_l;
float tol;

/* Gelbstoff and pigment parameters */
float eps_y_412_443, eps_p_412_443; 
float ysbpa_0, ysbpa_s;

/* TC and PFT parameters */
float a_ap_star_443, a_ap_star_490, a_ap_star_510;
float a_chl_star_443, a_chl_ratio; 

/* Function: load_work_tab */
/* Loads the sensor Look-Up Tables into memory  */
int load_work_tab(char *configfname, int sensorID)
{
   int i,j;
   long t_nbands,v_len;
   float *t_lambda;
   char fname[MAX_LINE],created[MAX_LINE];

   FILE *table;

   /* Geophysical LUT */
   sprintf(fname,"%s",get_cfg_s("gop_table",configfname));
   if (TAB_VERB)
      fprintf(stderr,"Using Geophysical Look-up Table: %s\n", fname);
   if((table = fopen(fname,"r")) == NULL){
      printf("Error opening %s\n", fname);
      exit(1);
   }
   
   /* start by reading bands and alocating variables */
   t_nbands=(long)get_cfg_i("n_bands",configfname);
   fread(&nband,sizeof(long),1,table);
   /* verify correct size of table */
   if (nband != t_nbands) {
       printf("Table band mismatch expected %ld read %ld\n",t_nbands,nband);
       printf("Using Geophysical Look-up Table: %s \n",fname);
       exit(1);
   }
   /* Allocate the arrays according to the number of wavelengths */
   lambda=calloc(nband,sizeof(float));
   a_w=calloc(nband,sizeof(float));
   b_w=calloc(nband,sizeof(float));
   /* Read in the wavelengths and aw,bw (in that order) */
   fread(lambda,sizeof(float),nband,table);
   fread(a_w,sizeof(float),nband,table);
   fread(b_w,sizeof(float),nband,table);
   if (TAB_VERB) {
      fprintf(stderr,"nband %ld lambda %f %f\n",nband,lambda[0],lambda[1]);
      fprintf(stderr,"nband %ld a_w %f %f\n",nband,a_w[0],a_w[1]);
      fprintf(stderr,"nband %ld b_w %f %f\n",nband,b_w[0],b_w[1]);
   }
   
   /* Chlorophyll */
   fread(&ch_n,sizeof(long),1,table);
   ch_lev=calloc(ch_n,sizeof(float));
   fread(ch_lev,sizeof(float),ch_n,table);
   if (TAB_VERB) 
      fprintf(stderr,"ch_n %ld ch_lev %f %f\n",ch_n,ch_lev[0],ch_lev[1]);
   
   for (i=0;i<nband;i++){
      ac[i]=calloc(ch_n,sizeof(float));
      bc[i]=calloc(ch_n,sizeof(float));
   }
   for (i=0;i<ch_n;i++){
      for (j=0;j<nband; j++){
         fread(&ac[j][i],sizeof(float),1,table);
      }        
   }
   for (i=0;i<ch_n;i++){
      for (j=0;j<nband; j++){
         fread(&bc[j][i],sizeof(float),1,table);
      }        
   }
   
   /* SPM */
   fread(&sp_n,sizeof(long),1,table);
   sp_lev=calloc(sp_n,sizeof(float));
   fread(sp_lev,sizeof(float),sp_n,table);
   if (TAB_VERB) 
      fprintf(stderr,"sp_n %ld sp_lev %f %f\n",sp_n,sp_lev[0],sp_lev[1]);

   for (i=0;i<nband;i++){
      as[i]=calloc(sp_n,sizeof(float));
      bs[i]=calloc(sp_n,sizeof(float));
   }
   for (i=0;i<sp_n;i++){
      for (j=0;j<nband; j++){
         fread(&as[j][i],sizeof(float),1,table);
      }        
   }
   for (i=0;i<sp_n;i++){
       for (j=0;j<nband; j++){
            fread(&bs[j][i],sizeof(float),1,table);
       }        
   }

   if (TAB_VERB){
      fprintf(stderr,"sp_n %ld sp_lev %f %f\n",sp_n,sp_lev[0],sp_lev[1]);
      fprintf(stderr,"as[1]: band6 %f band7 %f band8 %f\n",as[5][1],as[6][1],as[7][1]);
      fprintf(stderr,"as[40]: band6 %f band7 %f band8 %f\n",as[5][40],as[6][40],as[7][40]);
      fprintf(stderr,"bs[1]: band6 %f band7 %f band8 %f\n",bs[5][1],bs[6][1],bs[7][1]);
      fprintf(stderr,"bs[40]: band6 %f band7 %f band8 %f\n",bs[5][40],bs[6][40],bs[7][40]);
   }

   /* Gelbstoff */
   fread(&od_n,sizeof(long),1,table);
   od_lev=calloc(od_n,sizeof(float));
   fread(od_lev,sizeof(float),od_n,table);
   if (TAB_VERB) 
      fprintf(stderr,"od_n %ld od_lev %f %f\n",od_n,od_lev[0],od_lev[1]);

   for (i=0;i<nband;i++){
      od[i]=calloc(od_n,sizeof(float));
   }
   for (i=0;i<od_n;i++){
      for (j=0;j<nband; j++){
         fread(&od[j][i],sizeof(float),1,table);
      }        
   }

   if (TAB_VERB) 
      fprintf(stderr,"od_n %ld od_lev %f %f\n",od_n,od_lev[0],od_lev[1]);
   fread(&v_len,sizeof(long),1,table);
   fread(created,sizeof(char),v_len,table);
   created[v_len]='\0';
   if (TAB_VERB)
      fprintf(stderr,"Table created %s\n",created);
   
   fclose(table);
   
   /* IOP tables */
   /* IOP header file */
   sprintf(fname,"%s",get_cfg_s("iop_F_head",configfname));
   if (TAB_VERB)
      fprintf(stderr,"IOP tables - using header: %s\n", fname);
   if((table = fopen(fname,"r")) == NULL){
      printf("Error opening %s\n", fname);
      exit(1);
   }
   
   /* start by reading bands and alocating variables */
   t_nbands=(long)get_cfg_i("n_bands",configfname);
   fread(&nband,sizeof(long),1,table);
   /* verify correct size of table */
   if (nband != t_nbands){
      printf("Table band mismatch expected %ld read %ld\n",t_nbands,nband);
      printf("Using IOP  header Table: %s \n",fname);
      exit(1);
   }
   /* First wavelengths */
   t_lambda=calloc(nband,sizeof(float));
   fread(t_lambda,sizeof(float),nband,table);
   if (TAB_VERB) fprintf(stderr,"nband %ld lambda %f %f\n",nband,lambda[0],lambda[1]);

   /* verify that these match */
   for (i=0;i<nband;i++) {
      if (abs(t_lambda[i] - lambda[i]) >15.0) {
         printf("Error IOP table wavelength mismatch expected %f got %f\n",lambda[i],t_lambda[i]);
         exit(1);
      }
   }   
   free(t_lambda);      
   /* Solar zenith angle */
   fread(&th_s_n,sizeof(long),1,table);
   th_s_lev=calloc(th_s_n,sizeof(float));
   fread(th_s_lev,sizeof(float),th_s_n,table);
   /* view zenith angle */
   fread(&th_v_n,sizeof(long),1,table);
   th_v_lev=calloc(th_v_n,sizeof(float));
   fread(th_v_lev,sizeof(float),th_v_n,table);
   /* azimuth angle difference (view and satellite)*/
   fread(&dphi_n,sizeof(long),1,table);
   dphi_lev=calloc(dphi_n,sizeof(float));
   fread(dphi_lev,sizeof(float),dphi_n,table);
   /* absorption (a) */
   fread(&ap_n,sizeof(long),1,table);
   ap_lev=calloc(ap_n,sizeof(float));
   fread(ap_lev,sizeof(float),ap_n,table);
   /* scatter (b) */
   fread(&bp_n,sizeof(long),1,table);
   bp_lev=calloc(bp_n,sizeof(float));
   fread(bp_lev,sizeof(float),bp_n,table);

   if(TAB_VERB){
      fprintf(stderr,"th_s_n %ld th_s_lev %f %f\n",th_s_n,th_s_lev[0],th_s_lev[1]);
      fprintf(stderr,"th_v_n %ld th_v_lev %f %f\n",th_v_n,th_v_lev[0],th_v_lev[1]);
      fprintf(stderr,"dphi_n %ld dphi_lev %f %f\n",dphi_n,dphi_lev[0],dphi_lev[1]);
      fprintf(stderr,"ap_n %ld ap_lev %f %f\n",ap_n,ap_lev[0],ap_lev[1]);
      fprintf(stderr,"bp_n %ld bp_lev %f %f\n",bp_n,bp_lev[0],bp_lev[1]);
   }
   
   fclose(table);
   
   /* Master IOP table for the geometry */
   sprintf(fname,"%s",get_cfg_s("iop_F_table",configfname));
   if (TAB_VERB)
      fprintf(stderr,"IOP tables - main table: %s\n", fname);
   if((table = fopen(fname,"r")) == NULL){
      printf("Error opening %s\n", fname);
      exit(1);
   }
   
   /* Allocate memory for refen array */
   refind=th_s_n*th_v_n*dphi_n*ap_n*bp_n*nband;
   refind_max=refind-(ap_n*bp_n*nband);
   refen = (float *)calloc((refind),sizeof(float));
   if(refen == NULL){
      fprintf(stderr,"load_work_tab: memory allocation failure for refen\n");
      exit(1);
   }

   fread(refen,sizeof(float),refind,table); 
   if (TAB_VERB){
      fprintf(stderr,"refind_ns %ld ap_ns %ld bp_ns %ld bands %ld \n",refind,ap_n,bp_n,nband);
      fprintf(stderr,"refen first %f %f %f %f %f %f %f %f\n",refen[0],refen[1],refen[2],refen[3],refen[4],refen[5],refen[6],refen[7]);
      fprintf(stderr,"refen last %f %f %f %f %f %f %f %f\n",
              refen[refind-8],refen[refind-7],refen[refind-6],refen[refind-5],
	      refen[refind-4],refen[refind-3],refen[refind-2],refen[refind-1]);
   }
   /* Check that table limits are not exceeded */
   if (feof(table)) {
      printf("IOP master table error: table too short!\n");
      exit(1);
   }
   /* Try next byte as constitancy check */
   i=fgetc(table);
   if (!feof(table)) {
      printf("IOP master table error: table too long!\n");
      exit(1);
   }  

   fclose(table);
   refind=0l;
   return refind;
}

/* Function: load_config */
/* Stores the config table values such that they are available to */
/* the main calling routine */
void load_config(char *configfname)
{
   CASEII = get_cfg_i("CASEII",configfname);
   bp[0] = get_cfg_i("low_band",configfname);
   bp[1] = get_cfg_i("high_band",configfname);   
   b_tilde_p=get_cfg_f("b_tilde_p",configfname);
   b_tilde_w=get_cfg_f("b_tilde_w",configfname);

   /* Step 1: 490:510 ratio absorption and backscatter */
   eps_a_init=get_cfg_f("eps_a_init",configfname);
   eps_bb_init=get_cfg_f("eps_bb_init",configfname);
   scat_a=get_cfg_f("scat_a",configfname);
   scat_b=get_cfg_f("scat_b",configfname);
   scat_c=get_cfg_f("scat_c",configfname);
   scat_n=get_cfg_f("scat_n",configfname);
   scat_l=get_cfg_f("scat_l",configfname);
   
   /* Iterations to get the F parameter correctly */
   init_chl=get_cfg_f("init_chl",configfname);
   tol=get_cfg_f("iop_tol",configfname);
   maxit=get_cfg_i("iop_maxit",configfname);

   /* Step 2: 412:443 ratios to get the gelbstoff and pigment */
   eps_y_412_443=get_cfg_f("eps_y_412_443",configfname);
   eps_p_412_443=get_cfg_f("eps_p_412_443",configfname);
   
   ysbpa_0=get_cfg_f("YSBPA_0",configfname);
   ysbpa_s=get_cfg_f("YSBPA_S",configfname);
   
   /* Step 3: get the TC and PFT information */
   a_ap_star_443=get_cfg_f("a_ap_star_443",configfname);
   a_ap_star_490=get_cfg_f("a_ap_star_490",configfname);
   a_ap_star_510=get_cfg_f("a_ap_star_510",configfname);
   a_chl_star_443=get_cfg_f("a_chl_star_443",configfname);
   a_chl_ratio=get_cfg_f("a_chl_ratio",configfname); 

}

/* Function: geo2iop */
/* Returns the IOP values for a given geophysical input */
float geo2iop(float *levels,float *iopv[MAX_BANDS],int band,float value,int size){

   float res,ind;
   /* Conversion of band number to account for an 11 band IOP table */
   ind=interp_l(levels,value,size);
   res=iopv[band][(int)ind]*(floor(ind)+1.0-ind)+iopv[band][(int)ind+1]*(ind-floor(ind));
   if (TAB_VERB) {
      fprintf(stderr,"geo2iop: iop value %f [conc] value %f \n",res,value);
   }

   return res;
}

/* Function: interp */
/* Returns an interpolated value */
float interp(float *x, float u, int n){
   int s,i;
   s=0;
   if (u > x[n-1]) return n-1;
   for (i=0;i<n;i++) {
      if (x[i] >= u) {
         s=i-1;
         break;
      }
   }  
   if (s < 0) s=0;
   return ((u-x[s])/(x[s+1]-x[s])+s);
}

/* Function: interp_l */
/* Returns the log interpolated value */
/* Fast version for geophysical variables */
float interp_l(float *x, float u, int n){
   int s,i;
   s=0;
   if (u > x[n-1]) return n-1;
   for (i=0;i<n;i++){
      if (x[i] >= u){
         s=i-1;
         break;
      }
   }  
   if (s < 0) s=0;
   if (s == 0) return ((u-x[s])/(x[s+1]-x[s])+s);
   return ((log(u)-log(x[s]))/(log(x[s+1])-log(x[s]))+s);
}

/* Function: setgeom */
/* Interpolates from the LUT to get correct value for geometry */
int setgeom(float sun_theta,float sen_theta,float dphi){
   int status=0;
   long th_s_ent, th_v_ent, dphi_ent; 
   if (TAB_VERB) fprintf(stderr,"SOLZA %f SATZA %f DPHI %f\n",degrees(sun_theta),degrees(sen_theta),degrees(dphi));
     
   /* Page in IOP table */
   /* check that the angle matches index */
   th_s_ent=(long)floor(interp(th_s_lev,sun_theta,th_s_n)+0.5);
   th_v_ent=(long)floor(interp(th_v_lev,sen_theta,th_v_n)+0.5);
   if (dphi < 0.0) dphi=dphi+M_PI*2.0;
   if (dphi > M_PI*2.0) dphi=dphi-M_PI*2.0;
   dphi_ent=(long)floor(interp(dphi_lev,dphi,dphi_n)+0.5);
   /* IOP data */
   refind=(int)(th_s_ent*th_v_n*dphi_n*nband*bp_n*ap_n)
              +(th_v_ent*dphi_n*nband*bp_n*ap_n)
	      +(dphi_ent*nband*bp_n*ap_n);
   if (TAB_VERB) fprintf(stderr,"th_s_ent %ld th_v_ent %ld dphi_ent %ld refind %ld\n",
                 th_s_ent,th_v_ent,dphi_ent,refind);
   /* Geometry beyond table limits */
   if (refind > refind_max) {
      if (TAB_VERB) fprintf(stderr,"Table limits exceeded \n");
      status=1;
      return status;
   }
   return status;
}

/* Function: f_ab */
/* Interpolates to get a value f/Q */
/* for a pair of a and b */
double f_ab(double a,double b,int band)
{
   double ain,bin;
   double res;
   ain = interp_l(ap_lev,a,ap_n);
   bin = interp_l(bp_lev,b,bp_n);
   res = fint(ain,bin,band);
   if (FULL_VERB) printf("\nres = %f",res);
   return res;
}

/* Function: fint */
/* Interpolates for a pair of doubles and a given waveband */
double fint(double a,double b,int band)
{
   double ral,rah,res;
   int al,bl,bh,ah;
   if (a>0) al=(int)floor(a);
   else al=0;
   if (b>0) bl=(int)floor(b);
   else bl=0;
   bh=bl+1;
   ah=al+1;


   if ((bh>15)||(ah>15)) return 0.0;
   ral=refen[refind+band*bp_n*ap_n+bl*ap_n+ah]*(a-(double)al)
      +refen[refind+band*bp_n*ap_n+bl*ap_n+al]*((double)ah-a);
   rah=refen[refind+band*bp_n*ap_n+bh*ap_n+ah]*(a-(double)al)
      +refen[refind+band*bp_n*ap_n+bh*ap_n+al]*((double)ah-a);
   res=rah*(b-(double)bl)+ral*((double)bh-b);
   if (FULL_VERB) printf("\nral=%f,rah=%f,res=%f\n",ral,rah,res);
   return res;
}
