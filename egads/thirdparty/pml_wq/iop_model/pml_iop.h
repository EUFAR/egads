#ifndef tjsm_pml_iop
#define tjsm_pml_iop
/* Switch on/off iteration flag */
#define NFLAG 1
/* Switch on/off VERBose mode for error checking */
#define VERB 0
/* Switch on/off VERBose mode for LUT access */
#define TAB_VERB 0
/* Switch on/off full VERBose mode */
#define FULL_VERB 0
/* Switch on/off only the first estimate */
#define FIRST_EST 0
/* Switch on/off VERBose mode for model */
#define VERB_MOD 0
/* Switch on/off VERBose mode for Matt Pinkerton */
#define VERB_MATT 0
/* Switch on/off VERBose mode for BP effect */
#define VERB_BP 0
/* Switch on/off VERBose mode to print out LUT reflectance in NIR*/
#define VERB_RLUT 0
/* Switch on/off VERBose mode for IOP model*/
#define VERB_IOP 0

/* Define maximum bands for other processors */
#define MAX_BANDS 16

/* Sensor */
#define BANDS 8
/* 11 as MERIS, accounted for in geo2iop and r_ab */
#define TBANDS 11
#define B_THR 5
#define B_HIGH 6
#define B_NIR1 6
#define B_NIR2 7
#define  NB 6
#define NPB 4
/* Newton-Raphson */
#define NR_EPSILON 1.e-14 /*used to check for degenerate Jacobian - can be v.small. Changed from 1.e-6 M.Pinkerton */
#define NR_STATS 0
#define NR_OK 0
#define NR_LIN_NULL 2
#define NR_LIN_DEGENERATE 3
#define NR_FUNC_VOID 4
#define NR_NOT_CONVERGED 5
#define TurbMinDelta 0.01	/*Changed from 1.0e-4 M. Pinkerton. Now scales error by range*/
#define TurbMinVal 1.e-5	/*Changed from 1.0e-4 M. Pinkerton */

/* Constants */
#define p0 1013.25 /* Standard atmospheric pressure */
#define ang_max 1.5 /* Minimum angstrom exponent from 2.0 */
#define ang_min -0.5 /* Maximun angstrom exponent from -1.0 */
#define M_PI 3.14159265358979323846

/* Functions */
#define radians(degrees)	((degrees) * M_PI / 180.0)
#define degrees(radians)	((radians) * 180.0 / M_PI)

#endif
