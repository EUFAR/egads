#ifndef APPLY_PML_IOP_MODEL_HEADER
#define APPLY_PML_IOP_MODEL_HEADER

#include "pml_iop.h"
#include "pml_iop_config.h"
#include "pml_iop_tables.h"
#include "pml_iop_calculate.h"

#include "hdf_utils.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <libgen.h>
#include <time.h>

int is_opt(char *text);

int apply_pml_iop_model(void);

attribute **make_product_atts(char *desc, float slope, float intercept, char *units, float *valid_range);

int read_and_scale_int16_dataset_from_hdf_file(char *file,char *product,float **data);

char *make_outname(char *filename, char *outdir);

int file_extension(char *filename);

char *file_basename(char *filename);

char *file_dirname(char *filename);

#endif
