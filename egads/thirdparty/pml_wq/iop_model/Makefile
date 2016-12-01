CC=gcc
CFLAGS=	-g -O0 -pedantic -Wall --std=c99
LDFLAGS= -L/usr/lib64/hdf -lmfhdf -ldf -ljpeg -lz -lm

EXE=	pml_iop_model sun_angle
SRCS=	pml_iop_model.c pml_iop_config.c pml_iop_tables.c pml_iop_calculate.c sun_angle.c

all:	$(EXE)

install: $(EXE)

PML_IOP_MODEL_DEPEND = pml_iop_model.o pml_iop_config.o pml_iop_tables.o pml_iop_calculate.o
SUN_ANGLE_DEPEND = sun_angle.o

pml_iop_model: $(PML_IOP_MODEL_DEPEND)
	$(CC) -o $@ $(CFLAGS) pml_iop_model.o pml_iop_config.o pml_iop_tables.o pml_iop_calculate.o -lm $(LDFLAGS) #-lefence

sun_angle: $(SUN_ANGLE_DEPEND)
	$(CC) -o $@ $(CFLAGS) sun_angle.o -lm     

clean:
	@rm -f core
	rm -f $(EXE)
	rm -f *.o
