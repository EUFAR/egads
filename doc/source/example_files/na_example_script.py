#!/usr/bin/env python
# -*- coding: utf-8 -*-

import egads

data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0],
                        units='mm',
                        name='sea level',
                        scale_factor=1,
                        _FillValue=-9999)

data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0],
                        units='mm',
                        name='corr sea level',
                        scale_factor=1,
                        _FillValue=-9999)

time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0],
                        units='seconds since 19700101T00:00:00',
                        name='time')

filename = "na_example_file.na"
f = egads.input.NasaAmes()

na_dict = f.create_na_dict()

scom = ['========SPECIAL COMMENTS===========','this file has been created with egads','=========END=========']
ncom = ['========NORMAL COMMENTS===========','headers:','time    sea level   corrected sea level','=========END=========']
f.write_attribute_value('ONAME', 'John Doe', na_dict = na_dict)
f.write_attribute_value('ORG', 'An institution', na_dict = na_dict)
f.write_attribute_value('SNAME', 'tide gauge', na_dict = na_dict)
f.write_attribute_value('MNAME', 'ATESTPROJECT', na_dict = na_dict)
f.write_attribute_value('DATE', [2017, 1, 30], na_dict = na_dict)
f.write_attribute_value('NIV', 1, na_dict = na_dict)
f.write_attribute_value('NSCOML', 3, na_dict = na_dict)
f.write_attribute_value('NNCOML', 4, na_dict = na_dict)
f.write_attribute_value('SCOM', scom, na_dict = na_dict)
f.write_attribute_value('NCOM', ncom, na_dict = na_dict)

f.write_variable(data1, vartype="main", na_dict = na_dict)
f.write_variable(data2, vartype="main", na_dict = na_dict)
f.write_variable(time, vartype="independant", na_dict = na_dict)

f.save_na_file(filename, na_dict)
