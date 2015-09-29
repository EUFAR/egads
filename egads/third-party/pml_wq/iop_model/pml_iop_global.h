#include "zlib.h"
#include "string.h"

#define image_size(width,height) (width*height * sizeof(float))

static float *nLw412, *nLw443, *nLw490, *nLw510, *nLw555, *nLw670;
static float *atot;
static float *aph;
static float *adg;
static float *bb;
static float *TC;
static float *aph_ratio;
static float *zenith_float;

static int width, height; /* width and height of the input imagery */
static int npix;
static int yymm;

char *nLw_image_filename = NULL;
char *zenith_image_filename = NULL;
char OUTDIR[100]; 
char INDIR[100];

static double fwave[NB] = {412.0, 443.0, 490.0, 510.0, 555.0, 670.0};
static double F0[NB] = {173.004, 190.154, 196.473, 188.158, 183.010, 151.143};
/* static void read_global_imagery(float nLw412, float nLw443, float nLw490, float nLw510, float nLw555, float nLw670); */
static void read_global_imagery(void);
static void write_global_imagery(void);
static void read_zenith_byte(void);
