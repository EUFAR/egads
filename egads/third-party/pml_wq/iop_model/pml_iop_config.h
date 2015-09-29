#ifndef tjsm_pml_iop_config
#define tjsm_pml_iop_config
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

#define DEFAULT_CFG "pml.cfg"
#define MAX_LINE 180
#define MAX_TOK 20
#define MAX_ENTRY 80
#define MAX_TAB 100
#define MAX_ARR 20

extern int tab_size;

/* Structures for holding the configuration data */
struct tab_atom{
     char token[MAX_TOK];
     char entry[MAX_ENTRY];
     };
extern struct tab_atom cfg_tab[MAX_TAB];

/* Function declarations */
void loadconfig(char *fname);
char *get_cfg_s(char *tok, char *fname);
int get_cfg_i(char *tok, char *fname);
float get_cfg_f(char *tok, char *fname);
float *get_cfg_array(char *tok, char *fname);
#endif
