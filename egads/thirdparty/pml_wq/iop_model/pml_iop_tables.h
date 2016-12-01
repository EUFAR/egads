#ifndef tjsm_pml_iop_tables 
#define tjsm_pml_iop_tables
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 180

/* These are declared here as an extern so they will be useable */
/* by the rest of the code (static was previously used incorrectly)*/
extern float *lambda,*a_w,*b_w;

/* Geophysical (GOP) variables */
extern long nband, ch_n, sp_n, od_n;
extern float *ch_lev, *ac[MAX_BANDS], *bc[MAX_BANDS];
extern float *sp_lev, *as[MAX_BANDS], *bs[MAX_BANDS];
extern float *od_lev, *od[MAX_BANDS];

/* IOP variables */
extern long th_s_n, th_v_n, dphi_n;
extern float *th_s_lev, *th_v_lev, *dphi_lev;
extern long ap_n, bp_n;
extern float *ap_lev, *bp_lev;

extern float *refen;    /* The pointer for refen.*/

/* Case I / Case II switch - default is Case I (0) */
extern int CASEII;

/* 490:510 ratio - step 1 of the model */
extern int bp[2], maxit;
extern float eps_a_init, init_chl, tol;
extern float b_tilde_w, b_tilde_p;
extern float scat_a, scat_b, scat_c, scat_n, scat_l;

/* Gelbstoff and pigment parameters */
extern float eps_y_412_443, eps_p_412_443; 
extern float ysbpa_0, ysbpa_s;

/* TC and PFT parameters */
extern float a_ap_star_443, a_ap_star_490, a_ap_star_510;
extern float a_chl_star_443, a_chl_ratio; 

/* Function declarations */
int load_work_tab(char *configname, int sensorID);
void load_config(char *configname);
float geo2iop(float *levels,float *iopv[MAX_BANDS],int band,float value,int size);
float interp_l(float *x, float u, int n);
float interp(float *x, float u, int n);
int setgeom(float sun_theta,float sen_theta,float dphi);
double f_ab(double a,double b,int band);
double fint(double a,double b,int band);

#endif
