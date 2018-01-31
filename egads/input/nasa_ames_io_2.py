__author__ = "ohenry"
__date__ = "2017-1-11 14:52"
__version__ = "0.1"
__all__ = ["NasaAmes"]

import logging
import datetime
import egads
import copy
import re
import os
from egads.input import FileCore
try:
    import nappy
    logging.info('egads - nasa_ames_io.py - nappy has been imported')
    if 'egads' not in nappy.__path__[0]:
        logging.warning('egads - nasa_ames_io.py - EGADS has imported an already installed version of Nappy. If issues occure,'
                        + ' please check the version number of Nappy.')
        print ('EGADS has imported an already installed version of Nappy. If issues occure,'
               + ' please check the version number of Nappy.')
except ImportError:
    logging.exception('egads - nasa_ames_io.py - EGADS couldn''t find Nappy. Please check for a valid installation of Nappy'
                 + ' or the presence of Nappy in third-party software directory.')
    raise ImportError('EGADS couldn''t find Nappy. Please check for a valid installation of Nappy'
                 + ' or the presence of Nappy in third-party software directory.')


class NasaAmes(FileCore):
    """
    EGADS module for interfacing with NASA Ames files. This module adapts the NAPpy 
    library to the file access methods used in EGADS. To keep compatibility with
    Windows, all functions calling CDMS or CDMS2 have been revoked. The user still
    can use egads.thirdparty.nappy functions to have access to CDMS possibilities
    under Linux and Unix.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes NASA Ames instance.

        :param string filename:
            Optional - Name of NetCDF file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data), ``a`` and ``r+`` for append, 
            and ``r`` for read. ``r`` is the default value.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_filename - filename ' + str(filename) + ', perms' + str(perms))
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def _open_file(self, filename, perms):
        """
        Private method for opening NASA Ames file using Nappy API.

        :parm string filename:
            Name of NASA Ames file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - open_file - filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            
            self.f = open(filename, mode=perms)
            header_dict = self._get_header()
            '''self.f = nappy.openNAFile(filename, mode=perms)
            self.f.readData()
            self.filename = filename
            self.perms = perms
            self.na_dict = self.f.getNADict()
            attr_dict = {}
            attr_dict['Comments'] = self.f.getNormalComments()
            attr_dict['SpecialComments'] = self.f.getSpecialComments()
            attr_dict['Organisation'] = self.f.getOrganisation()
            dates = self.f.getFileDates()
            attr_dict['CreationDate'] = dates[0]
            attr_dict['RevisionDate'] = dates[1]
            attr_dict['Originator'] = self.f.getOriginator()
            attr_dict['Mission'] = self.f.getMission()
            attr_dict['Source'] = self.f.getSource()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename,
                                                                  conventions="NASAAmes")'''
        except RuntimeError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))



    def _get_header(self):
        tmp = {}
        tmp['NLHEAD'], tmp['FFI'] = self.f.readline().split()
        tmp['ONAME'] = self.f.readline().rstrip('\n')
        tmp['ORG'] = self.f.readline().rstrip('\n')
        tmp['SNAME'] = self.f.readline().rstrip('\n')
        tmp['MNAME'] = self.f.readline().rstrip('\n')
        tmp['IVOL'], tmp['NVOL'] = self.f.readline().split()
        yy1, mm1, dd1, yy2, mm2, dd2 = self.f.readline().split()
        tmp['DATE'] = [int(yy1), int(mm1), int(dd1)]
        tmp['RDATE'] = [int(yy2), int(mm2), int(dd2)]
        tmp['DX'] = self.f.readline().rstrip('\n')
        tmp['XNAME'] = self.f.readline().rstrip('\n')
        tmp['NV'] = int(self.f.readline().rstrip('\n'))
        vscal = self.f.readline().split()
        tmp['VSCAL'] = [float(factor) for factor in vscal]
        vmiss = self.f.readline().split()
        tmp['VMISS'] = [float(miss) for miss in vmiss]
        name_list = []
        for _ in range(tmp['NV']):
            name_list.append(self.f.readline().rstrip('\n'))
        tmp['VNAME'] = name_list
        tmp['NSCOML'] = int(self.f.readline().rstrip('\n'))
        scom_list = []
        for _ in range(tmp['NSCOML']):
            scom_list.append(self.f.readline().rstrip('\n'))
        tmp['SCOM'] = scom_list
        tmp['NNCOML'] = int(self.f.readline().rstrip('\n'))
        ncom_list = []
        for _ in range(tmp['NNCOML']):
            scom_list.append(self.f.readline().rstrip('\n'))
        tmp['NCOM'] = ncom_list
        
        
        
        
        
        return tmp
        



   








    def na_format_information(self):
        string = ("The goal of the 'na_format_information' function is to give few information\n"
                  + "about the file structure. Please see the following link for details:\n"
                  + "    http://badc.nerc.ac.uk/help/formats/NASA-Ames/\n"
                  + "\n"
                  + "A NASA/Ames file is composed of different elements:\n"
                  + "    NLHEAD  FFI\n"
                  + "    ONAME\n"
                  + "    ORG\n"
                  + "    SNAME\n"
                  + "    MNAME\n"
                  + "    IVOL  NVOL\n"
                  + "    DATE  RDATE\n"
                  + "    DX\n"
                  + "    NIV (not written in NASA/Ames file)\n"
                  + "    XNAME\n"
                  + "    NV\n"
                  + "    VSCAL(1) ... VSCAL(NV)\n"
                  + "    VMISS(1) ... VMISS(NV)\n"
                  + "    VNAME(1)\n"
                  + "    ...\n"
                  + "    VNAME(NV)\n"
                  + "    NSCOML\n"
                  + "    SCOM\n"
                  + "    NNCOML\n"
                  + "    NCOM\n"
                  + "    --- Here start the data ---\n"
                  + "\n"
                  + "with NLHEAD: number of lines in the header (above the first line of data\n"
                  + "     FFI: number of the File Format Index used in the file\n"
                  + "     ONAME: list of authors in the format Lastname, Firstname separated by\n"
                  + "        an arbitrary character\n"
                  + "     ORG: Organisation name (your university, institute or lab). May include\n"
                  + "        address and phone number\n"
                  + "     SNAME: Source of data (i.e. instrument, set of instruments, observation\n"
                  + "        station, platform, model name,...)\n"
                  + "     MNAME: Name of mission, campaign, programme, project,...\n"
                  + "     IVOL: Total number of files in the current dataset.\n"
                  + "     NVOL: Number of this file in your dataset (1 <= IVOL <=  NVOL)\n"
                  + "     DATE: Date at which the data recorded in this file begin (YYYY MM DD)\n"
                  + "     RDATE: Date at which the data were last revised (YYYY MM DD)\n"
                  + "     DX: Independent variable interval identifier\n"
                  + "     NIV: Number of independent variables\n"
                  + "     XNAME: Name and unit of the independent variable. E.g.: time (s)\n"
                  + "     NV: Number of dependent variables\n"
                  + "     VSCAL: Scaling factors of the NV dependent variables, in the same order\n"
                  + "        as the dependent variables\n"
                  + "     VMISS: Missing value identifiers for the dependent variables\n"
                  + "     VNAME: Names and units of the NV dependent variables. E.g.: V(n) = temperature (K)\n"
                  + "     NSCOML: Number of Special Comment lines including blank lines (= 0\n"
                  + "        if no Special Comment is given).\n"
                  + "     SCOM: Special Comments. Can expand over any number of lines (equal to NSCOML).\n"
                  + "        If the data are collected at a given site, these should include the \n"
                  + "        following lines: site name, country, longitude, latitude, height above\n"
                  + "        sea level\n"
                  + "     NNCOML: Number of Normal Comment lines including blank lines (= 0 if no\n"
                  + "        Normal Comment is given)\n"
                  + "     NCOM: Normal comments. Can expand on any number of lines (equal to NNCOML)\n"
                  + "        The last line(s) are often used for column headers or to indicate how\n"
                  + "        the data are displayed (but this is not mandatory). The Normal Comments\n"
                  + "        may include some Conditions of Use. They should also include a reference\n"
                  + "        to Gaines and Hipskind, 1998 (see the Instructions worksheet)."
                  )
        print string
    
    def _attemptVarAndUnitsMatch(self, item):
        """
        If it can match variable name and units from the name it does and returns
        (var_name, units). Otherwise returns (item, None).
        """
        
        match = re.compile("^\s*(.*)\((.+?)\)(.*)\s*$").match(item)
        if match:
            (v1, units, v2) = match.groups()
            var_name = v1 + " " + v2
        else:
            (var_name, units) = (item, None)   
        return (var_name.strip(), units)
    
    
    logging.info('egads - nasa_ames_io.py - NasaAmes has been loaded')
        
        