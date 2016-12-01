#ifndef HDF_UTILS_HEADER
#define HDF_UTILS_HEADER

#define APPEND_HDF 1
#define OVERWRITE_HDF 0

#include <hdf.h>
#include <ctype.h>
#include <string.h>

/* The type constants from hdf.h can be used for the data_type parameter.
   See hdfi.h for details on the types.
   
   Constant name     Type
   DFNT_INT8         int8
   DFNT_UINT8        uint8
   DFNT_INT16        int16
   DFNT_UINT16       uint16
   DFNT_INT32        int32
   DFNT_UINT32       uint32
   DFNT_INT64        int64
   DFNT_UINT64       uint64
   DFNT_FLOAT32      float32
   DFNT_FLOAT64      float64
   DFNT_UCHAR8       uchar8
   DFNT_CHAR8        char8
   DFNT_UCHAR16      uchar16
   DFNT_CHAR16       char16
*/

typedef struct _attribute{
   char *   name;
   void *   value;
   int32    type;
   int32    array_size;
} attribute;

int DFNT_typesize(int32 datatype);

int read_dataset_from_hdf_file(
   char * filename,
   char * product,
   void ** data,
   attribute ***attributes,
   int32 *rank,
   int32 **dims,
   int32 *num_attributes
   );
   
int read_dataset_from_hdf(
   int32 sd_id,
   char * product,
   void ** data,
   attribute ***attributes,
   int32 *rank,
   int32 **dims,
   int32 *num_attributes
   );

int write_empty_hdf_file(char *filename);

int write_dataset_to_hdf(
   int32 sd_id,
   char * dataset_name,
   int32 datatype,
   int32 rank,
   int32 *dims,
   void * data_buffer,
   attribute ** atts,
   int num_atts
   );
      
int write_image_to_hdf_file(
   char * filename,
   char * group,
   char * name,
   int32 data_type,
   void * image_data,
   int width,
   int height,
   attribute ** attributes,
   int num_attributes,
   int append
   );

int32 write_image_to_hdf (
   int32 file_id,
   int32 sd_id,
   char * group,
   char * name,
   int32 data_type,
   void * image_data,
   int width,
   int height,
   attribute ** attributes,
   int num_atts
   );
   
   
attribute * mkatt(
   int name_len,
   int value_len
   );

attribute ** get_object_attributes(
   int32 obj_id,
   int32 natts
   );
   
int write_attributes_to_object(
   int32 obj_id,
   attribute **atts,
   int32 natts
   );
   
void free_attribute_array(
   attribute **atts,
   int natts
   );
   
void free_attribute(attribute *att);


char * get_attname (attribute *att);
void * get_attvalue(attribute *att);
int32  get_atttype (attribute *att);
int    get_attsize (attribute *att);

void set_attname (attribute *att, char *name);
void set_attvalue(attribute *att, void *value);
void set_atttype (attribute *att, int32 type);
void set_attsize (attribute *att, int array_size);

void set_att(
   attribute *att,
   char *name,
   void *val,
   int32 type,
   int size
   );
 
#endif

