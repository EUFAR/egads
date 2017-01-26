#!/usr/bin/env python

# import egads package
import egads			
# import thermodynamic module and rename to simplify usage
import egads.algorithms.thermodynamics as thermo

# get list of all NetCDF files in 'data' directory
filenames = egads.get_file_list('data/*.nc')

f = egads.input.EgadsNetCdf()   # create EgadsNetCdf instance

for name in filenames:          # loop through files

    f.open(name, 'a')            # open NetCdf file with append permissions

    T_s = f.read_variable('T_t') # read in static temperature
    P_s = f.read_variable('P_s') # read in static pressure from file

    rho = thermo.DensityDryAirCnrm().run(P_s, T_s)  # calculate density

    f.write_variable(rho, 'rho', ('Time',))      # output variable

    f.close()                                    # close file

