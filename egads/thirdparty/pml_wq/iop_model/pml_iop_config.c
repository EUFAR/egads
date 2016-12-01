#include "pml_iop.h"
#include "pml_iop_config.h"

/* Module: pml_iop_config.c */
/* Authors: Tim Smyth and Gerald Moore */
/* Date: 06/03/07 */
/* Version: 1.3 */
/* History: Modified from the original pml_config.c */
/* Description: */
/* Functions to read in and to extract information from the configuration file */
int tab_size = 0;
struct tab_atom cfg_tab[MAX_TAB];

/* Function: loadconfig */
/* Purpose: Reads in the config file and reads in the variables therein */
void loadconfig(char *fname)
{
   int cp,t_p,t_f,e_p,e_f;
   char line[MAX_LINE],token[MAX_TOK],entry[MAX_ENTRY];
   
   FILE *cfg_file;

   if (TAB_VERB)
      fprintf(stderr,"Using config filename: %s\n", fname);

   if ((cfg_file = fopen(fname, "r")) == NULL){
      printf("loadconfig: File %s was not found\n", fname);
      exit(1);
   }
   
   /* Read in the config file one line at a time */
   while(!feof(cfg_file)){
      fgets(line,MAX_LINE,cfg_file);
      /* Remove terminating carriage return <cr> - replace with NULL*/
      cp = strlen(line) - 1;
      if (cp >= 0)  {
         if (line[cp]=='\n') line[cp]='\0';
      }
      /* Ignore white space, comments (#) and blank lines */
      if (!((strlen(line) == 0)||(line[0]=='#')||(isspace(line[0])))) {
         /* sort out the token and entry */
	 t_p=0; t_f=-1;
	 e_p=0; e_f=-1;
	 for (cp=0;cp<strlen(line);cp++) {
	    if (isspace(line[cp])&&(t_f<0)) t_f=1;
	    if ((t_f >0) && !(isspace(line[cp]))) e_f=1;
	    if (t_f <0) token[t_p++]=line[cp];
	    if (e_f >0) entry[e_p++]=line[cp];
	 }
	 token[t_p]=0;
	 entry[e_p]=0;
         /* put the entry into the cfg_tab structure */
	 strcpy(cfg_tab[tab_size].token,token);
	 strcpy(cfg_tab[tab_size].entry,entry);
	 tab_size++;
      }
   }      
   fclose(cfg_file);
}

/* Function: get_cfg_s */
/* Purpose: get a string value from the configuration table */
char *get_cfg_s(char *tok, char *fname)
{
   int i, found;
   if (tab_size <=0 ) loadconfig(fname);
   found=-1;
   for (i=0;i<tab_size;i++) {
      if (strcmp(tok,cfg_tab[i].token) == 0) found=i;
   }
   if (found <0){
      fprintf(stderr,"Entry %s not found in configuration file\n",tok);
      return NULL;
   }
   return (cfg_tab[found].entry); 
}

/* Function: get_cfg_i */
/* Purpose: get an integer value from the configuration table */
int get_cfg_i(char *tok, char *fname)
{
   int i, found;
   if (tab_size <=0 ) loadconfig(fname);
   found=-1;
   for (i=0;i<tab_size;i++) {
      if (strcmp(tok,cfg_tab[i].token) == 0) found=i;
   }
   if (found <0) {
      fprintf(stderr,"Entry %s not found in configuration file\n",tok);
      return -9999;
   }
   return (atoi(cfg_tab[found].entry)); 
}

/* Function: get_cfg_f */
/* Purpose: get a float value from the configuration table */
float get_cfg_f(char *tok, char *fname)
{
   int i, found;
   if (tab_size <=0 ) loadconfig(fname);
   found=-1;
   for (i=0;i<tab_size;i++) {
      if (strcmp(tok,cfg_tab[i].token) == 0) found=i;
   }
   if (found <0) {
      fprintf(stderr,"Entry %s not found in configuration file\n",tok);
      return -9999.999;
   }
   return atof(cfg_tab[found].entry); 
}

/* Function: get_cfg_array */
/* Purpose: get a float array from the configuration table file */
/* Parses up to a max */
float *get_cfg_array(char *tok, char *fname)
{
   int i, found,n_arr;
   float *tmp_arr;
   char tmp_entry[MAX_ENTRY],*p;

   if (tab_size <=0 ) loadconfig(fname);
   found=-1;

   for (i=0;i<tab_size;i++) {
      if (strcmp(tok,cfg_tab[i].token) == 0) found=i;
   }
   if (found <0) {
      fprintf(stderr,"Entry %s not found in configuration file\n",tok);
      return NULL;
   }
   
   /* Now need to disentangle the comma separated floats */
   strcpy(tmp_entry,cfg_tab[found].entry); 
   /* Strtok destroys the string */
   p=strtok(tmp_entry,",");
   n_arr=0;
   tmp_arr=calloc(MAX_ARR,sizeof(float));
   /* Loop over the "array" of numbers to find the number of elements */
   while (p != NULL) {
      tmp_arr[n_arr]=(float)atof(p);
      p=strtok(NULL,",");
      n_arr++;
   }
   for (i=n_arr;i<MAX_ARR;i++) tmp_arr[i]=0;
   return tmp_arr;
}



