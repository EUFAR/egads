#ifndef tjsm_pml_iop_calculate
#define tjsm_pml_iop_calculate
#include<stdio.h>
#include <stdlib.h>
#include <string.h>

int iop_model(double rho_w[],float sun_theta, float sen_theta, float dphi, double a[], double bbp[], double ady[], double ap[]);
int mod_iter(double rho_w[],float sun_theta, float sen_theta, float dphi, float eps_a, double a[], double bb[]); 
int iter_ab(double rho_w[],double aw[],double bbw[],double F[],double epsb,double epsa, double ab[]);
int iter_ab2(double rho_w[],double aw[],double bbw[],double F[],double epsb,double epsa, double ab[]);
double iter_a(double rho_w,double aw,double bbw,double F,double bb);
double iter_a2(double rho_w,double aw,double bbw,double F,double bb);
int biogeochem_mod(float a443, float ady443, float *a412_m, float *ady412, float *aph412);
int biogeochem_iter(float a412, float a443, float *ady443, float *ady412, float *aph412);
#endif
