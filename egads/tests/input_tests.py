"""
Test suite for NetCDF, NASA Ames and text file input and output libraries.
Uses NetCDF4 Python library to test known inputs and outputs against the EGADS
NetCDF library (based on NetCDF4).
"""

__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 09:37"
__version__ = "1.3"

import tempfile
import unittest
import csv
import egads
import egads.input as einput
import netCDF4
from numpy.random.mtrand import uniform
from numpy.testing import assert_array_equal  # @UnresolvedImport

FILE_NAME = tempfile.mktemp('.nc')
FILE_NAME_ALT = tempfile.mktemp('.nc')
VAR_NAME = 'test_var'
VAR_UNITS = 's'
VAR_LONG_NAME = 'test variable'
VAR_STD_NAME = ''
CATEGORY = 'TEST'
VAR_MULT_NAME = 'test_mult_var'
VAR_MULT_UNITS = 'm'
GLOBAL_ATTRIBUTE = 'test_file'
CONVENTIONS = 'EUFAR'
TITLE = 'Test file'
SOURCE = 'Generated for testing purposes'
INSTITUTION = 'EUFAR'
PROJECT = 'EGADS TEST RUN'
DIM1_NAME = 'x'
DIM1_LEN = 10
DIM2_NAME = 'y'
DIM2_LEN = 5

NAFILETEXT = '''20    1001
John Doe; email: john.doe@email.com
ORGANIS
Test NASA Ames File
Test001
1    1
2011 8 23    2011 8 24
0
Time_np (seconds after midnight)
4
1   1    1    1
-9900    -9900    -9900    -9900
GPS LAT (degrees)
GPS LON (degrees)
Height above sea level (m)
Time2 (seconds after midnight)
1
This is a test file for verifying the status of the EGADS NASA Ames functionality.
1
TIME GPS_LAT_NP GPS_LON_NP GPS_ALT_NP TIME2
51143.42    48.0797    11.2809    584.3 51143.42
51144.42    48.0792    11.2800    585.6 51144.42
51145.42    48.0787    11.2793    587.8 51145.42
51146.42    48.0782    11.2786    591.3 51146.42
51147.42    48.0775    11.2778    596.0 51147.42'''


NA_DICT = {
    "NLHEAD":26,
    "FFI":1001,
    "ONAME":"John Doe; email: john.doe@email.com",
    "ORG":"ORGANIS",
    "SNAME":"Test NASA Ames File",
    "MNAME":"Test001",
    "IVOL":1,
    "NVOL":1,
    "DATE":[2011,8,23],
    "RDATE":[2011,8,24],
    "DX":"0",
    "NIV":1,
    "XNAME":["Time_np (seconds after midnight)"],
    "NV":4,
    "VSCAL":[1,1,1,1],
    "VMISS":[-9900,-9900,-9900,-9900],
    "VNAME":["GPS LAT (degrees)","GPS LON (degrees)","Height above sea level (m)","Time2 (seconds after midnight)"],
    "NSCOML":1,
    "SCOM":["This is a test file for verifying the status of the EGADS NASA Ames functionality."],
    "NNCOML":1,
    "NCOM":["TIME GPS_LAT_NP GPS_LON_NP GPS_ALT_NP TIME2"],
    "X":[51143.42,51144.42,51145.42,51146.42,51147.42],
    "V":[[48.0797,48.0792,48.0787,48.0782,48.0775],
         [11.2809,11.2800,11.2793,11.2786,11.2778],
         [584.3,585.6,587.8,591.3,596.0],
         [51143.42,51144.42,51145.42,51146.42,51147.42]]
    }

random_data = uniform(size=(DIM1_LEN))
random_mult_data = uniform(size=(DIM1_LEN, DIM2_LEN))


class NetCdfFileInputTestCase(unittest.TestCase):
    """ Test input from NetCDF file """
    
    def setUp(self):
        self.file = FILE_NAME
        f = netCDF4.Dataset(self.file, 'w')  # @UndefinedVariable
        f.attribute = GLOBAL_ATTRIBUTE
        f.Conventions = CONVENTIONS
        f.title = TITLE
        f.source = SOURCE
        f.institution = INSTITUTION
        f.project = PROJECT
        f.createDimension(DIM1_NAME, DIM1_LEN)
        f.createDimension(DIM2_NAME, DIM2_LEN)
        v1 = f.createVariable(VAR_NAME, 'f8', (DIM1_NAME))
        v2 = f.createVariable(VAR_MULT_NAME, 'f8', (DIM1_NAME, DIM2_NAME))
        v1.units = VAR_UNITS
        v2.units = VAR_MULT_UNITS
        v1.long_name = VAR_LONG_NAME
        v1.standard_name = VAR_STD_NAME
        v1.Category = CATEGORY
        v1[:] = random_data
        v2[:] = random_mult_data
        f.close()

    def test_bad_file_name(self):
        """ Test handling of missing file """
        
        self.assertRaises((RuntimeError, IOError), einput.NetCdf, 'test12345.nc')

    def test_open_file(self):
        """ Test opening of file using open method """

        data = einput.NetCdf()
        data.open(self.file)
        self.assertEqual(data.filename, self.file, 'file opening failed')
        self.assertEqual(data.get_perms(), 'r', 'file permissions do not match')
        data.close()
        data_write = einput.NetCdf()
        data_write.open(self.file, 'w')
        self.assertEqual(data_write.filename, self.file, 'file opening failed for write')
        self.assertEqual(data_write.get_perms(), 'w', 'file permissions do not match')
        data_write.close()

    def test_bad_variable(self):
        """ Test handling of missing variable name"""

        data = einput.NetCdf(self.file)
        self.assertRaises(KeyError, data.read_variable, 'blah')
        data.close()

    def test_bad_attribute(self):
        """ Test handling of bad attribute name"""

        data = einput.NetCdf(self.file)
        self.assertRaises(KeyError, data.get_attribute_value, 'bad_attr')
        self.assertRaises(KeyError, data.get_attribute_value, 'bad_attr', VAR_NAME)
        data.close()

    def test_read_attribute(self):
        """ Test reading attribute from file """

        data = einput.NetCdf(self.file)
        self.assertEqual(data.get_attribute_value('units', VAR_NAME), VAR_UNITS,
                        'Variable attributes do not match')
        self.assertEqual(data.get_attribute_value('attribute'), GLOBAL_ATTRIBUTE,
                         'Global attributes do not match')
        data.close()

    def test_read_dimensions(self):
        """ Test reading dimensions from file """

        data = einput.NetCdf(self.file)
        dimdict = {DIM1_NAME : DIM1_LEN, DIM2_NAME : DIM2_LEN}
        self.assertEqual(data.get_dimension_list(), dimdict,
                        'dimensions dictionary does not match')
        vardimdict = {DIM1_NAME : DIM1_LEN}
        self.assertEqual(data.get_dimension_list(VAR_NAME), vardimdict,
                         'variable dimensions do not match')
        data.close()

    def test_load_data_1d(self):
        """ Test reading 1D netcdf data"""

        data = einput.NetCdf(self.file).read_variable(VAR_NAME)
        self.assertEqual(len(data), DIM1_LEN, "Input dimensions don't match")
        assert_array_equal(data, random_data)

    def test_load_data_2d(self):
        """ Test reading 2D netcdf data"""

        data = einput.NetCdf(self.file).read_variable(VAR_MULT_NAME)
        self.assertEqual(data.shape, (DIM1_LEN, DIM2_LEN), "Input dimensions don't match")
        assert_array_equal(data, random_mult_data)

    def test_read_range_1d(self):
        """ Test reading subset of data"""
        data = einput.NetCdf(self.file).read_variable(VAR_NAME, input_range=(0, DIM1_LEN - 2))
        assert_array_equal(data, random_data[:DIM1_LEN - 2])
        data = einput.NetCdf(self.file).read_variable(VAR_NAME, input_range=(-1, DIM1_LEN))
        assert_array_equal(data, random_data[-1:DIM1_LEN])
        data = einput.NetCdf(self.file).read_variable(VAR_NAME, input_range=(None, DIM1_LEN))
        assert_array_equal(data, random_data[0:DIM1_LEN])
        data = einput.NetCdf(self.file).read_variable(VAR_NAME, input_range=(None, DIM1_LEN + 1))
        assert_array_equal(data, random_data[0:DIM1_LEN])

    def test_read_range_2d(self):
        """ Test reading subset of data in 2d"""

        data = einput.NetCdf(self.file).read_variable(VAR_MULT_NAME, input_range=(0, DIM1_LEN - 2))
        assert_array_equal(data, random_mult_data[:DIM1_LEN - 2, :],)
        data = einput.NetCdf(self.file).read_variable(VAR_MULT_NAME, input_range=(None, None, 0, DIM1_LEN - 2))
        assert_array_equal(data, random_mult_data[:, :DIM1_LEN - 2])

    def test_read_n6sp_data(self):
        """ Test reading in data using N6SP formatted NetCDF """

        infile = einput.EgadsNetCdf(self.file)
        self.assertEqual(infile.file_metadata['title'], TITLE, 'NetCDF title attribute doesnt match')
        data = infile.read_variable(VAR_NAME)
        assert_array_equal(data.value, random_data)
        self.assertEqual(data.units, VAR_UNITS, 'EgadsData units attribute doesnt match')
        self.assertEqual(data.metadata['units'], VAR_UNITS, 'EgadsData units attribute doesnt match')
        self.assertEqual(data.metadata['long_name'], VAR_LONG_NAME, 'EgadsData long name attribute doesnt match')
        self.assertEqual(data.metadata['standard_name'], VAR_STD_NAME, 'EgadsData standard name attribute doesnt match')
        infile.close()


class NetCdfFileOutputTestCase(unittest.TestCase):
    """ Test output to NetCDF file """
    
    def setUp(self):
        self.data1 = egads.EgadsData(value = [0.5,2.3,6.2,8.1,4.],
                        units = 'mm',
                        long_name = 'a common data',
                        scale_factor = 1.,
                        _FillValue = -999)
        self.data2 = egads.EgadsData(value = [0.,1.,2.,3.,4.],
                        units = 'days since 20170101 00:00:00Z',
                        long_name = 'a common time vector',
                        scale_factor = 1.,
                        _FillValue = -999)
        self.file = FILE_NAME_ALT
        f = einput.NetCdf(self.file, 'w')
        f.add_dim(DIM1_NAME, DIM1_LEN)
        f.add_dim(DIM2_NAME, DIM2_LEN)
        f.write_variable(random_data, VAR_NAME, (DIM1_NAME,), 'double')
        f.write_variable(random_mult_data, VAR_MULT_NAME, (DIM1_NAME, DIM2_NAME,), 'double')
        f.add_attribute('units', VAR_UNITS, VAR_NAME)
        f.add_attribute('units', VAR_MULT_UNITS, VAR_MULT_NAME)
        f.close()

    def test_dimension_creation(self):
        """ Test creation of dimensions in file """

        f = netCDF4.Dataset(self.file, 'r')  # @UndefinedVariable
        self.assertTrue(DIM1_NAME in f.dimensions, 'Dim1 missing')
        self.assertTrue(DIM2_NAME in f.dimensions, 'Dim2 missing')
        self.assertEqual(DIM1_LEN, len(f.dimensions[DIM1_NAME]), 'Dim1 length not equal')
        self.assertEqual(DIM2_LEN, len(f.dimensions[DIM2_NAME]), 'Dim2 length not equal')
        f.close()

    def test_1d_variable_creation(self):
        """ Test creation of 1d variable in file """

        f = netCDF4.Dataset(self.file, 'r')  # @UndefinedVariable
        varin = f.variables[VAR_NAME]
        self.assertEqual(varin.shape, (DIM1_LEN,), 'Variable dimensions dont match')
        self.assertEqual(varin.units, VAR_UNITS, 'Variable units dont match')
        assert_array_equal(varin[:], random_data)
        f.close()

    def test_2d_variable_creation(self):
        """ Test creation of 2d variable in file """

        f = netCDF4.Dataset(self.file, 'r')  # @UndefinedVariable
        varin = f.variables[VAR_MULT_NAME]
        self.assertEqual(varin.shape, (DIM1_LEN, DIM2_LEN), 'Variable dimensions dont match')
        self.assertEqual(varin.units, VAR_MULT_UNITS, 'Variable units dont match')
        assert_array_equal(varin[:], random_mult_data)
        f.close()
        
    def test_egadsnetcdf_instance_creation(self):
        """ Test creation of a netcdf file via the EgadsNetCdf class """
        
        filename = tempfile.mktemp('.nc')
        g = einput.EgadsNetCdf(filename, 'w')
        g.add_dim('time', len(self.data2))
        g.write_variable(self.data2, 'time', ('time',), 'double')
        g.write_variable(self.data1, 'data', ('time',), 'double')
        g.close()
        f = netCDF4.Dataset(filename, 'r')  # @UndefinedVariable
        varin = f.variables['data']
        self.assertEqual(varin.shape[0], len(self.data2), 'Variable dimensions dont match')
        self.assertEqual(varin.scale_factor, 1.0, 'Variable scale factor dont match')
        self.assertEqual(varin.long_name, 'a common data', 'Variable long name dont match')
        f.close()


class EgadsFileInputTestCase(unittest.TestCase):
    """ Test input from text file"""
    
    def setUp(self):
        self.filename = tempfile.mktemp('.txt')
        self.strdata1ln = 'testtesttest\n'
        self.strdata2ln = 'testtesttest\n testtesttest\n'
        f = open(self.filename, 'w')
        f.write(self.strdata2ln)
        f.close()

    def test_open_file(self):
        """ Test opening of file """

        f = einput.EgadsFile(self.filename, 'r')
        self.assertEqual(f.filename, self.filename, 'Filenames do not match')
        self.assertRaises(IOError, einput.EgadsFile, 'nofile.txt')
        self.assertEqual(f.pos, 0, 'File position is not correct')
        f.close()

    def test_read_data(self):
        """ Test reading data from file """

        f = einput.EgadsFile(self.filename, 'r')
        data = f.read()
        self.assertEqual(self.strdata2ln, data, 'Data read in does not match')
        f.reset()
        data = f.read(4)
        self.assertEqual(self.strdata2ln[0:4], data, 'Characters read in do not match')
        f.close()

    def test_read_data_one_line(self):
        """ Test reading one line of data from file """

        f = einput.EgadsFile(self.filename, 'r')
        data = f.read_line()
        self.assertEqual(self.strdata1ln, data, 'One line data does not match')
        f.close()

    def test_seek_file(self):
        """ Test file seek function """

        f = einput.EgadsFile(self.filename, 'r')
        f.seek(3)
        data = f.read(1)
        self.assertEqual(4, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[3], data, 'Data from pos 3 does not match')
        f.seek(3, 'c')
        data = f.read(1)
        self.assertEqual(8, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[7], data, 'Data from pos 7 does not match')
        f.seek(4)
        data = f.read(1)
        self.assertEqual(5, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[4], data, 'Data from pos 3 does not match')
        f.close()


class EgadsFileOutputTestCase(unittest.TestCase):
    """ Test output to text file """

    def setUp(self):
        self.filename = tempfile.mktemp('.txt')
        self.f = einput.EgadsFile(self.filename, 'w')
        self.strdata1ln = 'testtesttest\n'
        self.strdata2ln = 'testtesttest\n testtesttest\n'
        self.intdata = [123, 456]

    def tearDown(self):
        self.f.close()

    def test_write_string_oneline(self):
        """ Test writing one line string to file. """

        self.f.write(self.strdata1ln)
        self.f.close()
        g = open(self.filename)
        data = g.read()
        self.assertEqual(data, self.strdata1ln, "Written one line string data does not match.")
        g.close()

    def test_write_string_twoline(self):
        """ Test writing two line string to file. """

        self.f.write(self.strdata2ln)
        self.f.close()
        g = open(self.filename)
        data = g.read()
        self.assertEqual(data, self.strdata2ln, "Written two line string data does not match.")
        g.close()

    def test_write_int(self):
        """ Test writing integers to file. """

        self.f.write(str(self.intdata))
        self.f.close()
        g = open(self.filename)
        data = g.read()
        self.assertEqual(data, str(self.intdata), "Written int data does not match.")


class EgadsCsvInputTestCase(unittest.TestCase):
    """Test input from CSV file."""

    def setUp(self):
        self.filename = tempfile.mktemp('.csv')
        self.titles = ['Time', 'Lat', 'Lon', 'Alt']
        self.data = [['1', 0, 1, 0.3],
                     ['2', 1, 0, 1.5],
                     ['3', 2, -1, 1.7]]
        self.times = ['1', '2', '3']
        self.lats = [0, 1, 2]
        self.lons = [1, 0, -1]
        self.alts = [0.3, 1.5, 1.7]
        self.data_as_str = [['1', '2', '3'],
                            ['0', '1', '2'],
                            ['1', '0', '-1'],
                            ['0.3', '1.5', '1.7']]
        self.format = ['s', 'i', 'i', 'f']
        f = open(self.filename, 'w')
        writer = csv.writer(f)
        writer.writerow(self.titles)
        writer.writerows(self.data)
        f.close()
        self.f = einput.EgadsCsv(self.filename)

    def tearDown(self):
        self.f.close()

    def test_open_file(self):
        """ Test opening of file """

        self.assertEqual(self.f.filename, self.filename, 'Filenames do not match')
        self.assertRaises(IOError, einput.EgadsFile, 'nofile.txt')
        self.assertEqual(self.f.pos, 0, 'File position is not correct')
        self.assertEqual(self.f.delimiter, ',', 'Delimiter value not correct')
        self.assertEqual(self.f.quotechar, '"', 'Quote character not correct')

    def test_read_data(self):
        """ Test reading data from csv file."""

        title = self.f.read(1)
        time, lat, lon, alt = self.f.read(out_format=self.format)
        self.f.reset()
        self.f.skip_line()
        data_str = self.f.read()
        self.assertEqual(title, self.titles, 'Titles do not match')
        assert_array_equal(time, self.times, 'Values do not match')
        assert_array_equal(lat, self.lats, 'Values do not match')
        assert_array_equal(lon, self.lons, 'Values do not match')
        assert_array_equal(alt, self.alts, 'Values do not match')
        assert_array_equal(data_str, self.data_as_str, 'Non-formatted data does not match')


class EgadsCsvOutputTestCase(unittest.TestCase):
    """ Test writing of CSV files. """

    def setUp(self):
        self.filename = tempfile.mktemp('.csv')
        self.titles = ['Time', 'Lat', 'Lon', 'Alt']
        self.data = [['1', '2', '3'],
                [0, 1, 2],
                [1, 0, -1],
                [0.3, 1.5, 1.7]]
        self.times = ['1', '2', '3']
        self.lats = [0, 1, 2]
        self.lons = [1, 0, -1]
        self.alts = [0.3, 1.5, 1.7]
        self.data_as_str = [['1', '2', '3'],
                ['0', '1', '2'],
                ['1', '0', '-1'],
                ['0.3', '1.5', '1.7']]
        self.format = ['s', 'i', 'i', 'f']
        f = einput.EgadsCsv(self.filename, 'w')
        f.write(self.titles)
        f.writerows(self.data)
        f.close()
        self.f = einput.EgadsCsv(self.filename)
        
    def tearDown(self):
        self.f.close()
    
    def test_read_data_from_EGADS_created_csv(self):
        """ Test reading data from csv file."""

        title = self.f.read(1)
        time, lat, lon, alt = self.f.read(out_format=self.format)
        self.f.reset()
        self.f.skip_line()
        data_str = self.f.read()
        self.assertEqual(title, self.titles, 'Titles do not match')
        assert_array_equal(time, self.times, 'Values do not match')
        assert_array_equal(lat, self.lats, 'Values do not match')
        assert_array_equal(lon, self.lons, 'Values do not match')
        assert_array_equal(alt, self.alts, 'Values do not match')
        assert_array_equal(data_str, self.data_as_str, 'Non-formatted data does not match')


class NAInputTestCase(unittest.TestCase):
    """ Test reading of NASA Ames files. """

    def setUp(self):
        self.filename = tempfile.mktemp('.na');
        f = einput.EgadsFile(self.filename, 'w')
        f.write(NAFILETEXT)
        f.close()
        self.originator = 'John Doe; email: john.doe@email.com'
        self.org = 'ORGANIS'
        self.scom = ['This is a test file for verifying the status of the EGADS NASA Ames functionality.']
        self.var_names = ['GPS LAT', 'GPS LON', 'Height above sea level', 'Time2']
        self.units = ['degrees', 'degrees', 'm', 'seconds after midnight']
        self.miss_vals = [-9900.0, -9900.0, -9900.0, -9900.0]
        self.time_max = 51147.42
        self.time_min = 51143.42
        self.GPS_LON_max = 11.2778
        self.GPS_LON_min = 11.2809

    def test_read_file(self):
        " Test reading data from NASA Ames file"
        
        f = einput.NasaAmes(self.filename)
        self.assertEqual(self.org, f.file_metadata['Organisation'], 'Organisation values do not match')
        self.assertEqual(self.originator, f.file_metadata['Originator'], 'Originator values do not match')
        self.assertEqual(self.scom, f.file_metadata['SpecialComments'], 'Special comments do not match')
        var_names = f.get_variable_list()
        self.assertEqual(self.var_names, var_names, 'Variable names do not match')
        var1_intcall = f.read_variable(1)
        self.assertEqual(self.units[1], var1_intcall.metadata['units'], 'Var 1 units do not match; {0} expected, {1} returned'.format(self.units[1], var1_intcall.metadata['units']))
        self.assertEqual(self.miss_vals[1], var1_intcall.metadata['_FillValue'], 'Var 1 missing values do not match')
        self.assertEqual(self.GPS_LON_max, var1_intcall.value[-1], 'Var 1 max values do not match')
        self.assertEqual(self.GPS_LON_min, var1_intcall.value[0], 'Var 1 min values do not match')
        var1_namecall = f.read_variable(var_names[1])
        self.assertEqual(self.units[1], var1_namecall.metadata['units'], 'Var 1 units do not match')
        self.assertEqual(self.miss_vals[1], var1_namecall.metadata['_FillValue'], 'Var 1 missing values do not match')
        self.assertEqual(self.GPS_LON_max, var1_namecall.value[-1], 'Var 1 max values do not match')
        self.assertEqual(self.GPS_LON_min, var1_namecall.value[0], 'Var 1 min values do not match')
        f.close()


class NAOutputTestCase(unittest.TestCase):
    """ Test writing of NASA Ames files. """
    
    def setUp(self):
        self.filename = tempfile.mktemp('.na');
        f = einput.NasaAmes()
        f.save_na_file(self.filename, NA_DICT, float_format='%.4f')
        f.close()
        self.originator = 'John Doe; email: john.doe@email.com'
        self.new_originator = 'Jane Doe; email: jane.doe@email.net'
        self.org = 'ORGANIS'
        self.scom = ['This is a test file for verifying the status of the EGADS NASA Ames functionality.']
        self.var_names = ['GPS LAT', 'GPS LON', 'Height above sea level', 'Time2']
        self.units = ['degrees', 'degrees', 'm', 'seconds after midnight']
        self.miss_vals = [-9900.0, -9900.0, -9900.0, -9900.0]
        self.time_max = 51147.42
        self.time_min = 51143.42
        self.GPS_LON_max = 11.2778
        self.GPS_LON_min = 11.2809
        self.new_data = [61143.42,61144.42,61145.42,61146.42,61147.42]
    
    def test_read_file(self):
        " Test reading data from NASA Ames file"
        
        f = einput.NasaAmes(self.filename)
        self.assertEqual(self.org, f.file_metadata['Organisation'], 'Organisation values do not match')
        self.assertEqual(self.originator, f.file_metadata['Originator'], 'Originator values do not match')
        self.assertEqual(self.scom, f.file_metadata['SpecialComments'], 'Special comments do not match')
        var_names = f.get_variable_list()
        self.assertEqual(self.var_names, var_names, 'Variable names do not match')
        var1_intcall = f.read_variable(1)
        self.assertEqual(self.units[1], var1_intcall.metadata['units'], 'Var 1 units do not match; {0} expected, {1} returned'.format(self.units[1], var1_intcall.metadata['units']))
        self.assertEqual(self.miss_vals[1], var1_intcall.metadata['_FillValue'], 'Var 1 missing values do not match')
        self.assertEqual(self.GPS_LON_max, var1_intcall.value[-1], 'Var 1 max values do not match')
        self.assertEqual(self.GPS_LON_min, var1_intcall.value[0], 'Var 1 min values do not match')
        var1_namecall = f.read_variable(var_names[1])
        self.assertEqual(self.units[1], var1_namecall.metadata['units'], 'Var 1 units do not match')
        self.assertEqual(self.miss_vals[1], var1_namecall.metadata['_FillValue'], 'Var 1 missing values do not match')
        self.assertEqual(self.GPS_LON_max, var1_namecall.value[-1], 'Var 1 max values do not match')
        self.assertEqual(self.GPS_LON_min, var1_namecall.value[0], 'Var 1 min values do not match')
        f.close()
    
    def test_replace_data_in_file(self):
        " Test replacing data in NASA Ames file"
        
        f = einput.NasaAmes(self.filename)
        f.write_attribute_value("ONAME", "Jane Doe; email: jane.doe@email.net")
        f.write_variable(self.new_data, varname="Time2")
        f.save_na_file(self.filename, float_format = '%.4f')
        f.close()
        g = einput.NasaAmes(self.filename)
        self.assertEqual(self.new_originator, g.file_metadata['Originator'], 'Originator values do not match')
        var1_intcall = g.read_variable("Time2")
        self.assertEqual(self.new_data[2], var1_intcall.value.tolist()[2], 'Var do not match')
        g.close()


class NetCdfConvertFormatTestCase(unittest.TestCase):
    """ Test conversion between formats using nappy toolbox """

    def setUp(self):
        self.data1 = egads.EgadsData(value = [0.5,2.3,6.2,8.1,4.],
                        units = 'mm',
                        long_name = 'a common data',
                        scale_factor = 1.,
                        _FillValue = -999)
        self.data2 = egads.EgadsData(value = [0.,1.,2.,3.,4.],
                        units = 'days since 20170101 00:00:00Z',
                        long_name = 'a common time vector',
                        scale_factor = 1.,
                        _FillValue = -999)
        self.ncfilename = tempfile.mktemp('.nc')
        self.nafilename = tempfile.mktemp('.na')
        self.csvfilename = tempfile.mktemp('.csv')
        f = einput.EgadsNetCdf(self.ncfilename, 'w')
        f.add_attribute('Conventions', 'CF-1.0')
        f.add_attribute('history', 'the netcdf file has been created by EGADS')
        f.add_attribute('comments', 'no comments on the netcdf file')
        f.add_attribute('institution', 'EUFAR')
        f.add_attribute('source', 'computer')
        f.add_attribute('title', 'a test file')
        f.add_attribute('authors', 'John Doe (john.doe@email.com)')
        f.add_dim('time', len(self.data2))
        f.write_variable(self.data2, 'time', ('time',), 'double')
        f.write_variable(self.data1, 'data', ('time',), 'double')
        f.add_attribute('long_name', self.data1.metadata['long_name'], 'data')
        f.add_attribute('units', self.data1.metadata['units'], 'data')
        f.add_attribute('scale_factor', self.data1.metadata['scale_factor'], 'data')
        f.add_attribute('units', self.data2.metadata['units'], 'time')
        f.add_attribute('long_name', self.data2.metadata['long_name'], 'time')
        f.add_attribute('scale_factor', self.data2.metadata['scale_factor'], 'time')
        f.close()

    def test_convert_nc_to_na_netcdf(self):
        """ Test conversion of NetCDF to NASA Ames, using the NetCdf class """
        
        f = einput.NetCdf(self.ncfilename)
        f.convert_to_nasa_ames(self.nafilename)
        f.close()
        g = einput.NasaAmes(self.nafilename)
        self.assertEqual('John Doe (john.doe@email.com)', g.file_metadata['Originator'], 'Originator values do not match')
        self.assertEqual('computer', g.file_metadata['Source'], 'Source values do not match')
        data = g.read_variable('data')
        self.assertListEqual(self.data1.value.tolist(), data.value.tolist(), 'data and data1 values do not match')
        g.close()


    def test_convert_nc_to_na_egadsnetcdf(self):
        """ Test conversion of NetCDF to NASA Ames, using the EgadsNetCdf class """
        
        f = einput.EgadsNetCdf(self.ncfilename)
        f.convert_to_nasa_ames(self.nafilename)
        f.close()
        g = einput.NasaAmes(self.nafilename)
        self.assertEqual('John Doe (john.doe@email.com)', g.file_metadata['Originator'], 'Originator values do not match')
        self.assertEqual('computer', g.file_metadata['Source'], 'Source values do not match')
        data = g.read_variable('data')
        self.assertListEqual(self.data1.value.tolist(), data.value.tolist(), 'data and data1 values do not match')
        g.close()
    
    def test_convert_nc_to_csv_netcdf(self):
        """ Test conversion of NetCDF to Nasa/Ames CSV, using the NetCdf class """
        
        f = einput.NetCdf(self.ncfilename)
        f.convert_to_csv(self.csvfilename)
        f.close()
        g = einput.EgadsCsv()
        g.open(self.csvfilename, 'r')
        lines = g.read()
        author = lines[1][0]
        computer = lines[3][0]
        raw = lines[-5:]
        time = []
        data = []
        for i in raw:
            time.append(float(i[0]))
            data.append(float(i[1]))
        self.assertEqual('John Doe (john.doe@email.com)', author, 'Originator values do not match')
        self.assertEqual('computer', computer, 'Source values do not match')
        self.assertListEqual(self.data1.value.tolist(), data, 'data and data1 values do not match')
        self.assertListEqual(self.data2.value.tolist(), time, 'time and data2 values do not match')
    
    def test_convert_nc_to_csv_egadsnetcdf(self):
        """ Test conversion of NetCDF to Nasa/Ames CSV, using the EgadsNetCdf class """
        
        f = einput.EgadsNetCdf(self.ncfilename)
        f.convert_to_csv(self.csvfilename)
        f.close()
        g = einput.EgadsCsv()
        g.open(self.csvfilename, 'r')
        lines = g.read()
        author = lines[1][0]
        computer = lines[3][0]
        raw = lines[-5:]
        time = []
        data = []
        for i in raw:
            time.append(float(i[0]))
            data.append(float(i[1]))
        self.assertEqual('John Doe (john.doe@email.com)', author, 'Originator values do not match')
        self.assertEqual('computer', computer, 'Source values do not match')
        self.assertListEqual(self.data1.value.tolist(), data, 'data and data1 values do not match')
        self.assertListEqual(self.data2.value.tolist(), time, 'time and data2 values do not match') 


class NAConvertFormatTestCase(unittest.TestCase):
    """ Test conversion between formats using nappy toolbox """

    def setUp(self):
        self.na_filename = tempfile.mktemp('.na');
        self.nc_filename = tempfile.mktemp('.nc');
        f = einput.NasaAmes()
        f.save_na_file(self.na_filename, NA_DICT, float_format='%.4f')
        f.close()
        self.authors = 'John Doe; email: john.doe@email.com'
        self.special_com = 'This is a test file for verifying the status of the EGADS NASA Ames functionality.'
        self.time = egads.EgadsData(value=[51143.42, 51144.42, 51145.42, 51146.42, 51147.42],
                                    units='seconds after midnight',
                                    _FillValue=-9900.,
                                    scale_factor=1.,
                                    standard_name='Time_np')
        
    def test_convert_na_to_nc(self):
        """ Test conversion of NASA Ames to NetCDF"""

        f = einput.NasaAmes(self.na_filename)
        f.convert_to_netcdf(self.nc_filename)
        g = einput.EgadsNetCdf(self.nc_filename, 'r')
        author = g.get_attribute_value('authors')
        special_com = g.get_attribute_value('special_comments')
        time = g.read_variable('Time_np')
        self.assertEqual(self.authors, author, 'Originator values do not match')
        self.assertEqual(self.special_com, special_com, 'Special comments do not match')
        self.assertListEqual(time.value.tolist(), time.value.tolist(), 'both time values do not match')
        

def suite():
    netcdf_in_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileInputTestCase)
    netcdf_out_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileOutputTestCase)
    text_in_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsFileInputTestCase)
    text_out_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsFileOutputTestCase)
    csv_in_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsCsvInputTestCase)
    csv_out_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsCsvOutputTestCase)
    na_in_suite = unittest.TestLoader().loadTestsFromTestCase(NAInputTestCase)
    na_out_suite = unittest.TestLoader().loadTestsFromTestCase(NAOutputTestCase)
    netcdf_convert_format_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfConvertFormatTestCase)
    nasa_ames_convert_format_suite = unittest.TestLoader().loadTestsFromTestCase(NAConvertFormatTestCase)
    return unittest.TestSuite([netcdf_in_suite, netcdf_out_suite, text_in_suite, text_out_suite, 
                               csv_in_suite, csv_out_suite, na_in_suite, na_out_suite, 
                               netcdf_convert_format_suite, nasa_ames_convert_format_suite])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())
