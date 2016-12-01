/* Applies the PML IOP model to an input HDF file, writing the output back
   to the input HDF or to a different HDF file. */
 
#include "apply_pml_iop_model.h"

/* Input options. */
char *inhdf_opt = "--inhdf";
char *outhdf_opt = "--outhdf";
char *out2in_opt = "--out2in";
char *outdir_opt = "--outdir";
char *saveram_opt = "--saveram";
char *config_opt = "--saveram";
char *help_opt = "--help";

/* Input paramaters. */
char *inhdf;
char *outhdf;
char *outdir;
char *config = DEFAULT_CFG;
int saveram = 0;
int out2in = 0;
int help = 0;

int main(int argc, char *argv[]){
   int i;
   int inerr_flag = 0;
   char *exename = "apply_pml_iop_model";
   time_t start_time;
   time_t end_time;
   double total_time;
   
   start_time = time(NULL);
   
   if(argc <= 1) help = 1;
   
   /* Parse options. */
   for (i=1; i<argc; i++){
      if(strcmp(argv[i], inhdf_opt) == 0) {
         if(++i < argc && !is_opt(argv[i])){
            inhdf = argv[i];
            continue;
         }else{
            printf("Input error: option '%s' requires an argument.\n",inhdf_opt);
            inerr_flag = 1;
         }
      }
      else if(strcmp(argv[i], outhdf_opt) == 0) {
         if(++i < argc && !is_opt(argv[i])){
            outhdf = argv[i];
            continue;
         }else{
            printf("Input error: option '%s' requires an argument.\n",outhdf_opt);
            inerr_flag = 1;
         }
      }
      else if(strcmp(argv[i], outdir_opt) == 0) {
         if(++i < argc && !is_opt(argv[i])){
            outdir = argv[i];
            continue;
         }else{
            printf("Input error: option '%s' requires an argument.\n",outdir_opt);
            inerr_flag = 1;
         }
      }
      else if(strcmp(argv[i], config_opt) == 0) {
         if(++i < argc && !is_opt(argv[i])){
            config = argv[i];
            continue;
         }else{
            printf("Input error: option '%s' requires an argument.\n",config_opt);
            inerr_flag = 1;
         }
      }
      else if(strcmp(argv[i], saveram_opt) == 0) {
         saveram = 1;
      }
      else if(strcmp(argv[i], out2in_opt) == 0) {
         out2in = 1;
      }
      else if(strcmp(argv[i], help_opt) == 0) {
         help = 1;
      }
   }
   
   /* Validate the inputs. */
   if( (outdir && out2in) || (outhdf && out2in) ){
      printf("Warning: if --out2in is given then the output is written to the\n");
      printf("  input HDF, --outhdf and --outdir will be ignored.\n");
      inerr_flag = 1;
   }
   
   /* Tell user how to get usage if there was an input error. */
   if(inerr_flag){
      printf("Give the --help option in order to see a usage message.\n");
      exit(0);
   }
   
   /* Give usage message. */
   if(help){
      printf("Usage: %s <options> \n",exename);
      printf("   --inhdf      The HDF file from which the Rrs, solz, sola, senz and sena\n");
      printf("                products are read.\n");
      printf("   --out2in     Write the outputs to the input HDF.\n");
      printf("   --outhdf     Name of the file to write output to (unless --out2in).\n");
      printf("   --outdir     Directory in which the output HDF will be written (unless --out2in).\n");
      //printf("   --saveram    Tries not to use so much RAM in one go (this results in more computations).\n");
      printf("   --config     The file from which to load various settings.\n");
      printf("   --help       Display this usage message.\n");
      exit(0);
   }
   
   /* Run the thing on the HDF. */
   apply_pml_iop_model();
   
   end_time = time(NULL);
   total_time = difftime(end_time, start_time);
   printf("Total running time of program: %f seconds\n",total_time);
}

int is_opt(char *text){
        if(strcmp(text,inhdf_opt) == 0) return 1;
   else if(strcmp(text,out2in_opt) == 0) return 1;
   else if(strcmp(text,outhdf_opt) == 0) return 1;
   else if(strcmp(text,outdir_opt) == 0) return 1;
   else if(strcmp(text,saveram_opt) == 0) return 1;
   else if(strcmp(text,config_opt) == 0) return 1;
   else if(strcmp(text,help_opt) == 0) return 1;
   return 0;
}





/* Do the processing. */
int apply_pml_iop_model(){

   int bufsize = 0;
   float *Rrs[NB];              /* Array to hold data loaded from the HDF file. */
   float *rho_w[NB];
   float *solz;
   float *sola;
   float *senz;
   float *sena;
   float *out_a[NB];
   float *out_bbp[NB];
   float *out_ady[NB];
   float *out_ap[NB];
   char outhdf[1000];
   
   int width;                       /* Width of the datasets from input HDF file. */
   int height;                      /* Height of the datasets from input HDF file. */
   
   void *buffer;                    /* All data loaded should be type float. */
   int32 *dims;                     /* There should only be 2D images loaded. */
   int i;
   int outermost_limit;
   int pix;
   int result = 0;                  /* Flag for successful iterations. */
   int32 natts;
   float slope;
   float intercept;
   attribute **atts;
   int append = 1;
   char *group;
   float min_a;
   float min_bbp;
   float min_ady;
   float min_ap;

   /* Variables related to writing attributes. */
   attribute **a_atts;
   attribute **bbp_atts;
   attribute **ady_atts;
   attribute **ap_atts;
   
   char *a_lname = "?";
   char *bbp_lname = "?";
   char *ady_lname = "?";
   char *ap_lname = "?";
   
   char *a_units = "m^-1";
   char *bbp_units = "m^-1";
   char *ady_units = "m^-1";
   char *ap_units = "m^-1";
   
   float a_slope = 1.0;
   float bbp_slope = 1.0;
   float ady_slope = 1.0;
   float ap_slope = 1.0;
   
   float a_intercept = 0.0;
   float bbp_intercept = 0.0;
   float ady_intercept = 0.0;
   float ap_intercept = 0.0;
   
   float a_range[] = {0.0, 100.0};
   float bbp_range[] = {0.0, 100.0};
   float ady_range[] = {0.0, 100.0};
   float ap_range[] = {0.0, 100.0};
   
   
   int out_natts = 0;

   int wavelengths[6] = {412, 443, 490, 510, 555, 670};
   char a_names[NB][7];
   char bbp_names[NB][9];
   char ady_names[NB][9];
   char ap_names[NB][8];
   char Rrs_names[NB][9];
   
   /* Make the names for the output products. */
   for(i=0; i<NB; i++){
      int wavelen = wavelengths[i];
      sprintf(a_names[i],"a_%d",wavelen);
      sprintf(bbp_names[i],"bbp_%d",wavelen);
      sprintf(ady_names[i],"ady_%d",wavelen);
      sprintf(ap_names[i],"ap_%d",wavelen);
      sprintf(Rrs_names[i],"Rrs_%d",wavelen);
   }
   
   /*char *a_names[NB] = {"a_412", "a_443", "a_490", "a_510", "a_555", "a_670"};
   char *bbp_names[NB] = {"bbp_412", "bbp_443", "bbp_490", "bbp_510", "bbp_555", "bbp_670"};
   char *ady_names[NB] = {"ady_412", "ady_443", "ady_490", "ady_510", "ady_555", "ady_670"};
   char *ap_names[NB] = {"ap_412", "ap_443", "ap_490", "ap_510", "ap_555", "ap_670"};*/
   
   
   
   /* Load the various LUTs into memory */
   load_work_tab(config);
   
   /* Load the various parameters into memory */
   load_config(config);
   
   
   printf("About to load the data from the HDF file.\n");
   
   /* Load Rrs (which will be of type float) and convert to rho_w. */
   for(i=0; i<NB; i++){
      printf("loading '%s' from '%s'\n",Rrs_names[i],inhdf);
      read_dataset_from_hdf_file(inhdf, Rrs_names[i], &buffer, 0, 0, &dims, 0);
      
      if(!bufsize){
         width = dims[1];
         height = dims[0];
         bufsize = width * height;
      }
      
      Rrs[i] = buffer;
      
      rho_w[i] = (float*)calloc(bufsize, sizeof(float));
      for(pix=0; pix<bufsize; pix++)
         if(Rrs[i][pix] != 0.0)
            rho_w[i][pix] = Rrs[i][pix] * M_PI;
      
      free(Rrs[i]);  /* Rrs are no longer needed, but RAM is. */
   }
   
   
   printf("Read the Rrs data from the HDF file and converted to rho_w.\n");
   printf("Each image has %d pixels.\n",bufsize);
   
   if(bufsize <= 0) exit(0);

   /* Load and scale solar and sensor zenith and azimuth. */
   /*solz = (float*)calloc(bufsize, sizeof(float));
   sola = (float*)calloc(bufsize, sizeof(float));
   senz = (float*)calloc(bufsize, sizeof(float));
   sena = (float*)calloc(bufsize, sizeof(float));*/
   
   
   read_and_scale_int16_dataset_from_hdf_file(inhdf, "solz", &solz);
   read_and_scale_int16_dataset_from_hdf_file(inhdf, "sola", &sola);
   read_and_scale_int16_dataset_from_hdf_file(inhdf, "senz", &senz);
   read_and_scale_int16_dataset_from_hdf_file(inhdf, "sena", &sena);
   
   
   /* Append output to the input file. */
   if(out2in){
      sprintf(outhdf, "%s", inhdf);
      group = "Geophysical Data";
   }else{
      char *name = make_outname(inhdf, outdir);
      sprintf(outhdf, "%s", name);
      write_empty_hdf_file(outhdf);
      group = 0;
   }
   printf("Will output to %s\n",outhdf);
   
   /*out_a[i] = (float*)calloc(bufsize, sizeof(float));
   out_bbp[i] = (float*)calloc(bufsize, sizeof(float));
   out_ady[i] = (float*)calloc(bufsize, sizeof(float));
   out_ap[i] = (float*)calloc(bufsize, sizeof(float));*/
   
   a_atts = make_product_atts(a_lname, a_slope, a_intercept, a_units, a_range);
   bbp_atts = make_product_atts(bbp_lname, bbp_slope, bbp_intercept, bbp_units, bbp_range);
   ady_atts = make_product_atts(ady_lname, ady_slope, ady_intercept, ady_units, ady_range);
   ap_atts = make_product_atts(ap_lname, ap_slope, ap_intercept, ap_units, ap_range);
   
   
   
   
   /* Run iop_model for each pixel. */
   printf("Calculating and writing products.\n");
   
   
   /* For calculation of the new products it would be most efficient to loop over each
      pixel, and then each band.
      However, that can use too much RAM, so the bands are looped and then the pixels
      if the --saveram option is given. */
   
   /* Decide whether or not there'll be an outer loop over the bands. */
   if(saveram){
      outermost_limit = NB;
   }else{
      outermost_limit = 1;
   }
   
   /* If saving RAM then the bands must be looped over before the pixels.
      If not then this outer loop should only be run once. */
   for(i=0; i<outermost_limit; i++){
      int j;
      int lastband;
      
      /* These variable declarations are here in order to avoid the overhead of
         run-time reallocation for each pixel. */
      double tmp_rho_w[NB];
      float sen_theta;
      float sol_theta;
      float dphi;
      double a[NB];
      double bbp[NB];
      double ady[NB];
      double ap[NB];
      int there_is_rho;
      
      if(saveram){
         lastband = i+1;
      }else{
         lastband = NB;
      }
      
      /* Allocate memory.
         If saving RAM then use the outermost loop (i) to reference bands. If not saving
         RAM then loop over all of the bands (note: i will be 0 in this case). */
      for(j=i; j<lastband; j++){
         out_a[j] = (float*)calloc(bufsize, sizeof(float));
         out_bbp[j] = (float*)calloc(bufsize, sizeof(float));
         out_ady[j] = (float*)calloc(bufsize, sizeof(float));
         out_ap[j] = (float*)calloc(bufsize, sizeof(float));
      }
   
      printf("looping over pixels\n");
      for(pix=0; pix<bufsize; pix++){
         /*double tmp_rho_w[NB];
         float sen_theta;
         float sol_theta;
         float dphi;
         double a[NB];
         double bbp[NB];
         double ady[NB];
         double ap[NB];
         int no_rho;*/
         
         there_is_rho = 0;
         for(j=0; j<NB; j++){
            tmp_rho_w[j] = (double)(rho_w[j][pix]);
            if(rho_w[j][pix] != 0.0) there_is_rho = 1;
         }
         if(!there_is_rho) continue;  /* Don't do any calculations if there's no data. */

         sen_theta = radians(senz[pix]);
         sol_theta = radians(solz[pix]);
         dphi = radians(sena[pix]) - radians(sola[pix]);
         
         result = iop_model(tmp_rho_w, sol_theta, sen_theta, dphi, a, bbp, ady, ap);
         
         if(saveram){
            lastband = i+1;
         }else{
            lastband = NB;
         }
         
         /* If saving RAM then use the outermost loop (i) to reference bands. If not saving
            RAM then loop over all of the bands (note: i will be 0 in this case). */
         for(j=i; j<lastband; j++){
         

            /* Make sure that the values are in the valid range. */
            if(a[j] >= a_range[0] && a[j] <= a_range[1])
               out_a[j][pix] = (float)(a[j]);
               
            if(bbp[j] >= bbp_range[0] && bbp[j] <= bbp_range[1])
               out_bbp[j][pix] = (float)(bbp[j]);
               
            if(ady[j] >= ady_range[0] && ady[j] <= ady_range[1])
               out_ady[j][pix] = (float)(ady[j]);
               
            if(ap[j] >= ap_range[0] && ap[j] <= ap_range[1])
               out_ap[j][pix] = (float)(ap[j]);
               
            #if 0
            out_a[j][pix] = (float)(a[j]);
            out_bbp[j][pix] = (float)(bbp[j]);
            out_ady[j][pix] = (float)(ady[j]);
            out_ap[j][pix] = (float)(ap[j]);


            /* Make sure that the values are in the valid range. */
            if(out_a[j][pix] < a_range[0] || out_a[j][pix] > a_range[1])
               out_a[j][pix] = 0.0;

            if(out_bbp[j][pix] < bbp_range[0] || out_bbp[j][pix] > bbp_range[1])
               out_bbp[j][pix] = 0.0;

            if(out_ady[j][pix] < ady_range[0] || out_ady[j][pix] > ady_range[1])
               out_ady[j][pix] = 0.0;

            if(out_ap[j][pix] < ap_range[0] || out_ap[j][pix] > ap_range[1])
               out_ap[j][pix] = 0.0;
            
            #endif

            #if DEBUG
            if(j==0 && pix==0){
               min_a = out_a[j][pix];
               min_bbp = out_bbp[j][pix];
               min_ady = out_ady[j][pix];
               min_ap = out_ap[j][pix];
            }else{
               if(out_a  [j][pix] < min_a  ) min_a   = out_a  [j][pix];
               if(out_bbp[j][pix] < min_bbp) min_bbp = out_bbp[j][pix];
               if(out_ady[j][pix] < min_ady) min_ady = out_ady[j][pix];
               if(out_ap [j][pix] < min_ap ) min_ap  = out_ap [j][pix];
            }
            #endif

         }
      }
      
      if(saveram){
         lastband = i+1;
      }else{
         lastband = NB;
      }
      
      for(j=i; j<lastband; j++){
         printf("about to write some products.\n");

         /* Saving RAM: Write out the products at this wavelength. */
         /* Not saving RAM: Write out all of the products. */
         out_natts = 5;

         write_image_to_hdf_file(outhdf, group, a_names[j], DFNT_FLOAT32, (void*)(out_a[j]), width, height,
            a_atts, out_natts, append);

         write_image_to_hdf_file(outhdf, group, bbp_names[j], DFNT_FLOAT32, (void*)(out_bbp[j]), width, height,
            bbp_atts, out_natts, append);

         write_image_to_hdf_file(outhdf, group, ady_names[j], DFNT_FLOAT32, (void*)(out_ady[j]), width, height,
            ady_atts, out_natts, append);

         write_image_to_hdf_file(outhdf, group, ap_names[j], DFNT_FLOAT32, (void*)(out_ap[j]), width, height,
            ap_atts, out_natts, append);

         /* Free the products that have just been written. */
         free(out_a[j]);
         free(out_bbp[j]);
         free(out_ady[j]);
         free(out_ap[j]);
      }
   }
   
   #if 0
   
   #if DEBUG
   printf("minimum values written\n");
   printf("   a: %f\n",min_a);
   printf("   bbp: %f\n",min_bbp);
   printf("   ady: %f\n",min_ady);
   printf("   ap: %f\n",min_ap);
   #endif

   
   
   
   
   /* Write the outputs to an HDF. */
   for(i=0; i<NB; i++){
      write_image_to_hdf_file(outhdf, group, a_names[i], DFNT_FLOAT32, (void*)(out_a[i]), width, height,
         a_atts, out_natts, append
      );
      write_image_to_hdf_file(outhdf, group, bbp_names[i], DFNT_FLOAT32, (void*)(out_bbp[i]), width, height,
         bbp_atts, out_natts, append
      );
      write_image_to_hdf_file(outhdf, group, ady_names[i], DFNT_FLOAT32, (void*)(out_ady[i]), width, height,
         ady_atts, out_natts, append
      );
      write_image_to_hdf_file(outhdf, group, ap_names[i], DFNT_FLOAT32, (void*)(out_ap[i]), width, height,
         ap_atts, out_natts, append
      );
   }

   for(i=0; i<N_ATTS; i++){
      free(common_atts[i]);
   }
   free(a_atts[0]);
   free(bbp_atts[0]);
   free(ady_atts[0]);
   free(ap_atts[0]);
   #endif
   
   for(i=0; i<NB; i++){
      free(rho_w[i]);
   }
   
   return 1;
}


/* A function to make attributes for the output products.
   Any variables local to this function won't be written to to the HDF. */
attribute **make_product_atts(
   char *desc, float slope, float intercept, char *units, float *valid_range){
   
   int n_atts = 5;
   int i;
   attribute **atts = (attribute**)calloc(n_atts, sizeof(attribute*));
   float *out_slope = calloc(1,sizeof(float));
   float *out_intercept = calloc(1,sizeof(float));
   
   *out_slope = slope;
   *out_intercept = intercept;
   
   for(i=0; i<n_atts; i++) atts[i] = mkatt(0,0);
   
   i=0;
   set_att( atts[i++], "long_name", desc, DFNT_CHAR, strlen(desc)+1);
   set_att( atts[i++], "slope", out_slope, DFNT_FLOAT32, 1);
   set_att( atts[i++], "intercept", out_intercept, DFNT_FLOAT32, 1);
   set_att( atts[i++], "units", units, DFNT_CHAR, strlen(units)+1);
   set_att( atts[i++], "valid_range", valid_range, DFNT_FLOAT32, 2);
   
   return atts;
}

/* A small wrapper for read_dataset_from_hdf_file that applies the slope and intercept
   if either are found. Data is stored as a one-dimensional array, the return value
   is the size of the array.
   Note: this is not a generic function, it's quite specific to the sola, solz, suna
   and sunz products. */
int read_and_scale_int16_dataset_from_hdf_file(
      char *file,                /* Name of the HDF file. */
      char *product,             /* Name of the dataset to look for. */
      float **data               /* Pointer to a pointer of a data buffer. Set to 0 to ignore. */
      ){
   
   int i;
   int bufsize = 1;
   void *buffer;
   int32 rank;
   int32 *dims;
   float slope = 1.0;
   float intercept = 0.0;
   attribute **atts;
   int32 natts;
      
   read_dataset_from_hdf_file(file, product, &buffer, &atts, &rank, &dims, &natts);
   
   for(i=0; i<rank; i++) bufsize *= dims[i];
   *data = (float*)calloc(bufsize, sizeof(float));
   
   for(i=0; i<natts; i++){
      attribute *att = atts[i];
      if(strcmp("slope", att->name) == 0) slope = *((float*)(att->value));
      if(strcmp("intercept", att->name) == 0) intercept = *((float*)(att->value));
   }
   for(i=0; i<bufsize; i++)
      if( ((int16*)buffer)[i] != 0 )
         (*data)[i] = (((int16*)buffer)[i] * slope) + intercept;
   
   free(buffer);
   
   return bufsize;
}


/* Returns an output filename from the one provided.
*/
char *make_outname(char *filename, char *outdir){
   char *f_basename;
   char *f_dirname;
   char *f_extension;
   char *output_filename = (char*)calloc(2000, sizeof(char));
   
   printf("got outdir as '%s'\n",outdir);
   if(outdir == NULL) outdir = ".";
   
   f_basename = file_basename(filename);
   f_dirname = file_dirname(filename);
   f_extension = filename + file_extension(filename);
   
   if(strcmp(f_extension,".hdf") != 0) *f_extension = '\0'; /* Get rid of the extension. */
   
   printf("using outdir as '%s'\n",outdir);
   sprintf(output_filename,"%s/%s.pml_iop.hdf",outdir,f_basename);
   
   return output_filename;
}

/* Returns the position of the rightmost '.' in filename.
   Returns the start position of the filename if there is no extension. 
   Note: this does not inclue the path if there is one. */
int file_extension(char *filename){
   int i = strlen(filename);
   while(filename[--i] != '/' && filename[i] != '.' && i > 0);
   
   if(filename[i] == '/') i++;
   return i;
}

/* Wrapper functions for basename and filename.
   These versions don't modify their argument. */
char *file_basename(char *filename){
   char *bname;
   int len = strlen(filename) + 1;
   
   bname = (char*)calloc(len, sizeof(char));
   strcpy(bname, filename);
   
   bname = basename(bname);
   
   return bname;
}
char *file_dirname(char *filename){
   char *dname;
   int len = strlen(filename) + 1;
   
   dname = (char*)calloc(len, sizeof(char));
   strcpy(dname, filename);
   
   dname = dirname(dname);
   
   return dname;
}
