#include "hdf_utils.h"

/* This is a library that contains some utilities for reading and writing datasets
 * in HDF files.
 * Functions like write_image_to_hdf_file are supposed to be usable without having
 * to deal with the HDF interface at all. Other functions like read_dataset_from_hdf
 * require some things to already have been done using the HDF interface, but vastly
 * reduces the amount of effort required to achieve the goal (in this example the
 * the goal is to read all of a dataset from an HDF file).
 *
 * In the header file an 'attribute' type has been defined, which is for storing the
 * data about an attribute attached to an HDF dataset. There are initialisation,
 * accessor and destruction routines for this struct that make manipulating HDF
 * dataset attributes a bit more convenient.
 */



/* Makes a blank HDF file. */
int write_empty_hdf_file(char *filename){
   int32 sd_id;
   sd_id = SDstart(filename,DFACC_CREATE);
   SDend(sd_id);
   return (sd_id==FAIL);
}

/* Loads a dataset from an HDF file (along with any attributes).
   This essentially just sets things up for load_dataset_from_hdf.
*/
int read_dataset_from_hdf_file(
      char * file,               /* Name of the HDF file. */
      char * product,            /* Name of the dataset to look for. */
      void ** data,              /* Pointer to a pointer of a data buffer. Set to 0 to ignore. */
      attribute ***attributes,   /* Pointer to an array of attributes. Set to 0 to ignore. */
      int32 *rank,               /* Pointer to an int to hold the rank. Set to 0 to ignore. */
      int32 **dims,              /* Pointer to an int array to hold the dimensions. Set to 0 to ignore. */
      int32 *num_attributes      /* Pointer to an int to hold the number of attributes. Set to 0 to ignore. */
      ){
   int32 sd_id;
   int retn;
   
   /* Open the input file for reading. */
   sd_id = SDstart(file, DFACC_RDONLY);
   if(sd_id==FAIL){
      printf("Failed to open %s\n",file);
      return -1;
   }
   retn = read_dataset_from_hdf(sd_id,product,data,attributes,rank,dims,num_attributes);
   SDend(sd_id);
   return retn;
}

/* Reads a dataset's data and attributes. The rank, dimensions and number
   of attributes are also returned.
   Returns -1 if there was a failure.
*/
int read_dataset_from_hdf(
      int32 sd_id,
      char * product,            /* Name of the dataset to look for. */
      void ** data,              /* Pointer to a pointer of a data buffer. Set to 0 to ignore. */
      attribute ***attributes,   /* Pointer to an array of attributes. Set to 0 to ignore. */
      int32 *rank,               /* Pointer to an int to hold the rank. Set to 0 to ignore. */
      int32 **dimensions,        /* Pointer to an int array to hold the dimensions. Set to 0 to ignore. */
      int32 *num_attributes      /* Pointer to an int to hold the number of attributes. Set to 0 to ignore. */
      ){
   int32 sds_id, sds_index;
   char name[300];
   int32 this_rank, datatype, natts;
   int32 start[MAX_VAR_DIMS], stride[MAX_VAR_DIMS], edge[MAX_VAR_DIMS];
   int32 *dims = calloc(MAX_VAR_DIMS, sizeof(int32));
   int datatype_size, data_count, dim;
   attribute **atts = NULL;
   void *data_buffer;
   
   /* Look for the dataset in the file. */
   sds_index = SDnametoindex(sd_id, product);
   if(sds_index==FAIL){
      printf("Couldn't find a dataset named %s\n",product);
      return -1;
   }
   
   /* Get some info about the dataset. */
   sds_id = SDselect(sd_id,sds_index);
   SDgetinfo(sds_id, name, &this_rank, dims, &datatype, &natts);
   
   /* Set variables to tell the SD interface to load all of the dataset's data. */
   data_count = 1;
   for(dim=0; dim<this_rank; dim++){
      start[dim]=0;
      stride[dim]=1;
      edge[dim]=dims[dim];
      data_count *= dims[dim];
   }
   
   datatype_size = DFNT_typesize(datatype);
   data_buffer = malloc(data_count * datatype_size);
   
   /* Load the data. */
   if(natts > 0) atts = get_object_attributes(sds_id, natts);
   if(SDreaddata(sds_id, start, stride, edge, data_buffer)==FAIL){
      printf("Reading %s data from %s in failed.\n",product,name);
      return -1;
   }
   
   SDendaccess(sds_id);
   
   if(!dimensions) free(dims);
   if(!attributes) free(atts);
   
   /* Set the return values. */
   if(data)             *data = data_buffer;
   if(attributes)       *attributes = atts;
   if(rank)             *rank = this_rank;
   if(dimensions)       *dimensions = dims;
   if(num_attributes)   *num_attributes = natts;
   return 1;
}


/* Writes a dataset of any dimensions. */
int write_dataset_to_hdf(
      int32 sd_id,
      char * dataset_name,
      int32 datatype,
      int32 rank,
      int32 *dims,
      void * data_buffer,
      attribute ** atts,
      int num_atts
      ){
   int32 start[MAX_VAR_DIMS], stride[MAX_VAR_DIMS], edge[MAX_VAR_DIMS];
   int32 sds_id, sds_index;
   int dim, data_count, datatype_size;
   
   
   /* Set variables to tell the SD interface to write all of the dataset's data. */
   data_count = 1;
   for(dim=0; dim<rank; dim++){
      start[dim]=0;
      stride[dim]=1;
      edge[dim]=dims[dim];
      data_count *= dims[dim];
   }
   
   datatype_size = DFNT_typesize(datatype);
   
   
   /* Check if the dataset exists already; if it does then select it, if not
      then make it. */
   sds_index = SDnametoindex(sd_id, dataset_name);
   if(sds_index==FAIL){
      sds_id = SDcreate(sd_id, dataset_name, datatype, rank, dims);
   }else{
      sds_id = SDselect(sd_id, sds_index);
   }
   
   if(sds_id==FAIL){
      printf("Couldn't open or make a dataset for %s.\n",dataset_name);
      return -1;
   }
   SDwritedata(sds_id,start,stride,edge,data_buffer);
   
   /* If the user has supplied an array of attribute structs, write them to
      the HDF. */
   if(atts){
      write_attributes_to_object(sds_id, atts, num_atts);
   }
   
   SDendaccess(sds_id);
   return 1;
}

/* Sets up an HDF file for writing an image to. This is supposed to be
   a one function "write this image to this HDF file" with no hassle
   of dealing with the HDF interfaces.
   This function sets things up for, and then calls, write_image_to_hdf.
   */
int write_image_to_hdf_file(
      char * filename,
      char * group,
      char * name,
      int32 data_type,
      void * image_data,
      int width,
      int height,
      attribute ** attributes, /* Can be set to null (0). */
      int num_atts,
      int append
      ){
   int32 sd_id, file_id, sds_ref;
   int create = !append;
   
   /* Open the HDF for writing, but don't delete existing contents. */
   if(append){
      sd_id = SDstart(filename,DFACC_WRITE);
      if(sd_id==FAIL){
         create = 1;
      }
   }
   /* Make (or overwrite) the output HDF file. */
   if(create){
      sd_id = SDstart(filename,DFACC_CREATE);
      if(sd_id==FAIL){
         printf("Couldn't make or open the HDF file %s.\n",filename);
         return 0;
      }
   }
   
   file_id = Hopen(filename, DFACC_WRITE, 0);
   if(file_id==FAIL){
      printf("Couldn't access the HDF file %s.\n",filename);
      return 0;
   }
   
   /* Now that things are set up, call write_image_to_hdf. */
   sds_ref = write_image_to_hdf(
      file_id, sd_id, group, name, data_type, image_data, width, height, attributes, num_atts
   ); 
   
   /* Finish up. */
   SDend(sd_id);        /* Close the dataset interface. */
   Hclose(file_id);     /* Close the HDF file. */
   
   if( sds_ref == FAIL ) return FAIL;
   return 1;
}


/* Writes all of an image to an HDF file. The image is written to
   a dataset and added to a vgroup. Group can be set to null if
   the dataset shouldn't be added to a vgroup.
   If the dataset name is "longitude" or "latitiude" then attributes
   "long_name", "valid_range" and "units" are added.
   If the dataset already exists then it is overwritten. If it
   doesn't already belong to the vgroup then it is added to it.
   */
int32 write_image_to_hdf(
      int32 file_id,       /* As returned by Hopen().                   */
      int32 sd_id,         /* As returned by SDstart().                 */
      char * group,        /* Name of the vgroup to add the image to.   */
      char * name,         /* Name to give the image's dataset.         */
      int32 data_type,     /* Data type of the image.                   */
      void * image_data,   /* The image.                                */
      int width,           /* Image width.                              */
      int height,          /* Image height.                             */
      attribute ** atts,   /* An array of attributes to write.          */
      int num_atts
      ){
   
   int32 vgroup_id, vgroup_ref, sds_id, sds_index, image_sds_ref;
   int32 dims[2], start[2], stride[2], edge[2];
   int rank=2;
   VOIDP att_value;
   
   /* Height comes before width in the SD interface. */
   dims[0] = height;
   dims[1] = width;
   
   edge[0] = height; /* These variables and their settings tell SDwritedata() */
   edge[1] = width;  /* to write every pixel of the image, (as opposed to a   */
   start[0] = 0;     /* subset of the image).                                 */
   start[1] = 0;     /*                                                       */
   stride[0] = 1;    /*                                                       */
   stride[1] = 1;    /*                                                       */
   
   
   /* Check if the dataset exists already; if it does then select it, if not
      then make it. */
   sds_index = SDnametoindex(sd_id, name);
   if(sds_index==FAIL){
      sds_id = SDcreate(sd_id, name, data_type, rank, dims);
   }else{
      sds_id = SDselect(sd_id, sds_index);
   }
   
   if(sds_id==FAIL){
      printf("Couldn't open or make a dataset for %s.\n",name);
      return 0;
   }
   image_sds_ref = SDidtoref(sds_id);
   SDwritedata(sds_id,start,stride,edge,image_data);
   
   /* If the user has supplied an array of attribute structs, write them to
      the HDF. */
   if(atts){
      write_attributes_to_object(sds_id, atts, num_atts);
   }else{

      /* Add the attributes for longitudes or latitudes. */
      if(strcmp(name, "longitude")==0){
         att_value = "Longitudes at control points";
         SDsetattr(sds_id,"long_name",DFNT_CHAR8,strlen(att_value)+1,att_value);

         att_value = (VOIDP)calloc(2,sizeof(float));
         ((float*)att_value)[0] = -180.0;
         ((float*)att_value)[1] = 180.0;
         SDsetattr(sds_id,"valid_range",DFNT_FLOAT32,2,att_value);
         free(att_value);

         att_value = "degrees";
         SDsetattr(sds_id,"units",DFNT_CHAR8,strlen(att_value)+1,att_value);

      }else if(strcmp(name, "latitude")==0){
         att_value = "Latitudes at control points";
         SDsetattr(sds_id,"long_name",DFNT_CHAR8,strlen(att_value)+1,att_value);

         att_value = (VOIDP)calloc(2,sizeof(float));
         ((float*)att_value)[0] = -90.0;
         ((float*)att_value)[1] = 90.0;
         SDsetattr(sds_id,"valid_range",DFNT_FLOAT32,2,att_value);
         free(att_value);

         att_value = "degrees";
         SDsetattr(sds_id,"units",DFNT_CHAR8,strlen(att_value)+1,att_value);
      }
   }
   
   SDendaccess(sds_id);
   
   /* Look for the vgroup with name group. If it can't be found, make it. */
   if(group){
      Vstart(file_id);  /* Start the vgroup interface. */

      vgroup_ref = Vfind(file_id, group);
      if(!vgroup_ref){
         vgroup_ref = -1; /* vgroup reference of -1 in Vattach makes a new group. */
      }

      vgroup_id = Vattach(file_id,vgroup_ref,"w");
      if(vgroup_id==FAIL){
         printf("Couldn't access or create '%s' group.\n",group);
         return 0;
      }
      Vsetname(vgroup_id,group);
      
      /* Add the image dataset to the vgroup, if it's not already there. */
      if(Vinqtagref(vgroup_id,DFTAG_NDG,image_sds_ref)==FALSE){
         if(( Vaddtagref(vgroup_id,DFTAG_NDG,image_sds_ref) )==FAIL){
            printf("Couldn't add dataset '%s' to group '%s'\n",name,group);
         }
      }
      
      Vdetach(vgroup_id);  /* Update all the changes made to the vgroup. */
      Vend(file_id);       /* Close Vgroup interface.                    */
   }
   
   return image_sds_ref;
}

/* Loads the attributes from an HDF dataset and returns them as
   an array of attribute structs. */
attribute ** get_object_attributes(int32 obj_id, int32 natts){
   attribute **atts_arr;
   int i;
   
   atts_arr = (attribute**) malloc(natts * sizeof(attribute*));
   for(i=0; i<natts; i++){
      attribute *atts = mkatt(100,0);
      
      SDattrinfo(obj_id, i, atts->name, &(atts->type), &(atts->array_size));
      atts->value = (void*) malloc(DFNT_typesize(atts->type) * atts->array_size);
      SDreadattr(obj_id, i, atts->value);
      
      atts_arr[i] = atts;
   }
   
   return atts_arr;
}

/* Takes an array of attributes and writes them to the object. */
int write_attributes_to_object(int32 obj_id, attribute **atts, int32 natts){
   int i, retn, error_flag=0;
   for(i=0; i<natts; i++){
      attribute *att = atts[i];
      retn = SDsetattr(obj_id, att->name, att->type, att->array_size, att->value);
      if(retn==FAIL) error_flag = 1;
   }
   return error_flag;
}

/* Initialises an attribute struct, allocating memory for the struct
   and the number of bytes to allocate for the name and value of the
   attribute.
   Returns a pointer to the attribute. */
attribute * mkatt(int name_len, int value_len){
   attribute *att = malloc(sizeof(attribute));
   att->name = NULL;
   att->value = NULL;
   
   if(name_len)   att->name = (char*) calloc(name_len,sizeof(char));
   if(value_len)  att->value = malloc(value_len);
   
   att->type = -1;
   att->array_size = 0;
   return att;
}


/* Some accessor methods for an attribute struct, to provide abstraction.
*/

char * get_attname(attribute *att){
   return att->name;
}

void * get_attvalue(attribute *att){
   return att->value;
}

int32 get_atttype(attribute *att){
   return att->type;
}

int get_attsize(attribute *att){
   return att->array_size;
}

void set_attname(attribute *att, char *name){
   att->name = name;
}

void set_attvalue(attribute *att, void *value){
   att->value = value;
}

void set_atttype(attribute *att, int32 type){
   att->type = type;
}

void set_attsize(attribute *att, int array_size){
   att->array_size = array_size;
}

void set_att(attribute *att, char *name, void *val, int32 type, int size){
   set_attname(att,name);
   set_attvalue(att,val);
   set_atttype(att,type);
   set_attsize(att,size);
}


/* Frees the memory used by an array of attributes. */
void free_attribute_array(attribute **atts, int natts){
   int i;
   for(i=0; i<natts; i++){
      free_attribute(atts[i]);
   }
   free(atts);
}

/* Frees the memory used by an attribute structure and the memory
   that the 'name' and 'value' fields point to. */
void free_attribute(attribute *att){
   free(att->name);
   free(att->value);
   free(att);
}


/* Returns the size (in bytes) of datatypes represented by the typecode DFNT_* */
int DFNT_typesize(int32 datatype){
   int datatype_size;
   switch(datatype){
      case DFNT_INT8:         datatype_size = sizeof(int8);    break;
      case DFNT_UINT8:        datatype_size = sizeof(uint8);   break;
      case DFNT_INT16:        datatype_size = sizeof(int16);   break;
      case DFNT_UINT16:       datatype_size = sizeof(uint16);  break;
      case DFNT_INT32:        datatype_size = sizeof(int32);   break;
      case DFNT_UINT32:       datatype_size = sizeof(uint32);  break;
      case DFNT_FLOAT32:      datatype_size = sizeof(float32); break;
      case DFNT_FLOAT64:      datatype_size = sizeof(float64); break;
      case DFNT_UCHAR8:       datatype_size = sizeof(uchar8);  break;
      case DFNT_CHAR8:        datatype_size = sizeof(char8);   break;
      default:
         printf("Didn't recognise the datatype (type number: %d).\n",(int)datatype);
         exit(0);
   }
   return datatype_size;
}
