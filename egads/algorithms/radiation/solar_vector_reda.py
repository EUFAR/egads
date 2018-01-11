__author__ = "mfreer, ohenry"
__date__ = "2017-01-11 11:16"
__version__ = "1.5"
__all__ = ['SolarVectorReda']

import numpy
import dateutil.parser as dateparser
import egads  # @UnusedImport
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import egads.algorithms.mathematics


class SolarVectorReda(egads_core.EgadsAlgorithm):

    """
    FILE        solar_vector_reda.py

    VERSION     1.5

    CATEGORY    Radiation

    PURPOSE     Calculates the solar vector based on current date/time, elevation,
                latitude and longitude.

    DESCRIPTION Calculates the solar vector based on current date/time, elevation,
                latitude and longitude. Takes additional optional arguments of pressure
                and temperature to correct for atmospheric refraction effects. The zenith
                and azimuth angle calculated by this algorithm have uncertainties equal
                to +/- 0.0003 degrees in the period from year -2000 to 6000.

    INPUT       date_time    vector    yyyymmddThhmmss    ISO string of current date time
                                                          in UTC
                lat          vector    degrees            latitude
                lon          vector    degrees            longitude
                elevation    vector    m                  elevation
                pressure     vector    hPa                local pressure
                temperature  vector    degC               local temperature

    OUTPUT      Theta        vector    degree            solar zenith angle
                Phi          vector    degree            solar azimuth angle

    SOURCE

    REFERENCES  Reda and Andreas, "Solar Position Algorithm for Solar Radiation
                Applications," National Renewable Energy Laboratory, Revised 2008,
                accessed February 14, 2012, http://www.nrel.gov/docs/fy08osti/34302.pdf
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'degree',
                                                               'long_name':'Solar Zenith Angle',
                                                               'standard_name':'solar_zenith_angle',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'degree',
                                                               'long_name':'Solar Azimuth Angle',
                                                               'standard_name':'solar_azimuth_angle',
                                                               'Category':['Radiation']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['date_time', 'lat', 'lon', 'elevation', 'pressure', 'temperature'],
                                                          'InputUnits':['', 'degrees', 'degrees', 'm', 'hPa', 'degC'],
                                                          'InputTypes':['time','vector','vector','vector','vector','vector'],
                                                          'InputDescription':['ISO string of current date time in UTC', 'Latitude', 'Longitude', 'Elevation','Local pressure','Local temperature'],
                                                          'Outputs':['Theta', 'Phi'],
                                                          'OutputUnits':['degree','degree'],
                                                          'OutputTypes':['vector','vector'],
                                                          'OutputDescription':['Solar zenith angle','Solar azimuth angle'],
                                                          'Purpose':'Calculates the solar vector based on current date/time, elevation, latitude and longitude',
                                                          'Description':'Calculates the solar vector based on current date/time, elevation, latitude and longitude. Takes additional optional arguments of pressure and temperature to correct for atmospheric refraction effects. The zenith and azimuth angle calculated by this algorithm have uncertainties equal to +/- 0.0003 degrees in the period from year -2000 to 6000',
                                                          'Category':'Radiation',
                                                          'Source':'',
                                                          'References':'Reda and Andreas, "Solar Position Algorithm for Solar Radiation Applications," National Renewable Energy Laboratory, Revised 2008,accessed February 14, 2012, http://www.nrel.gov/docs/fy08osti/34302.pdf',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, date_time, lat, lon, elevation, pressure=None, temperature=None):
        return egads_core.EgadsAlgorithm.run(self, date_time, lat, lon, elevation, pressure, temperature)

    def _algorithm(self, date_time, lat, lon, elevation, pressure, temperature):
        RAD_TO_DEG = 180 / numpy.pi
        DEG_TO_RAD = numpy.pi / 180.0

        # A, B, C terms of L0
        L0 = numpy.array([[175347046.0, 0, 0],
                          [3341656.0, 4.6692568, 6283.07585],
                          [34894.0, 4.6261, 12566.1517],
                          [3497.0, 2.7441, 5753.3849],
                          [3418.0, 2.8289, 3.5231],
                          [3136.0, 3.6277, 77713.7715],
                          [2676.0, 4.4181, 7860.4194],
                          [2343.0, 6.1352, 3930.2097],
                          [1324.0, 0.7425, 11506.7698],
                          [1273.0, 2.0371, 529.691],
                          [1199.0, 1.1096, 1577.3435],
                          [990, 5.233, 5884.927],
                          [902, 2.045, 26.298],
                          [857, 3.508, 398.149],
                          [780, 1.179, 5223.694],
                          [753, 2.533, 5507.553],
                          [505, 4.583, 18849.228],
                          [492, 4.205, 775.523],
                          [357, 2.92, 0.067],
                          [317, 5.849, 11790.629],
                          [284, 1.899, 796.298],
                          [271, 0.315, 10977.079],
                          [243, 0.345, 5486.778],
                          [206, 4.806, 2544.314],
                          [205, 1.869, 5573.143],
                          [202, 2.458, 6069.777],
                          [156, 0.833, 213.299],
                          [132, 3.411, 2942.463],
                          [126, 1.083, 20.775],
                          [115, 0.645, 0.98],
                          [103, 0.636, 4694.003],
                          [102, 0.976, 15720.839],
                          [102, 4.267, 7.114],
                          [99, 6.21, 2146.17],
                          [98, 0.68, 155.42],
                          [86, 5.98, 161000.69],
                          [85, 1.3, 6275.96],
                          [85, 3.67, 71430.7],
                          [80, 1.81, 17260.15],
                          [79, 3.04, 12036.46],
                          [75, 1.76, 5088.63],
                          [74, 3.5, 3154.69],
                          [74, 4.68, 801.82],
                          [70, 0.83, 9437.76],
                          [62, 3.98, 8827.39],
                          [61, 1.82, 7084.9],
                          [57, 2.78, 6286.6],
                          [56, 4.39, 14143.5],
                          [56, 3.47, 6279.55],
                          [52, 0.19, 12139.55],
                          [52, 1.33, 1748.02],
                          [51, 0.28, 5856.48],
                          [49, 0.49, 1194.45],
                          [41, 5.37, 8429.24],
                          [41, 2.4, 19651.05],
                          [39, 6.17, 10447.39],
                          [37, 6.04, 10213.29],
                          [37, 2.57, 1059.38],
                          [36, 1.71, 2352.87],
                          [36, 1.78, 6812.77],
                          [33, 0.59, 17789.85],
                          [30, 0.44, 83996.85],
                          [30, 2.74, 1349.87],
                          [25, 3.16, 4690.48]])

        L1 = numpy.array([[628331966747.0, 0, 0],
                          [206059.0, 2.678235, 6283.07585],
                          [4303.0, 2.6351, 12566.1517],
                          [425.0, 1.59, 3.523],
                          [119.0, 5.796, 26.298],
                          [109.0, 2.966, 1577.344],
                          [93, 2.59, 18849.23],
                          [72, 1.14, 529.69],
                          [68, 1.87, 398.15],
                          [67, 4.41, 5507.55],
                          [59, 2.89, 5223.69],
                          [56, 2.17, 155.42],
                          [45, 0.4, 796.3],
                          [36, 0.47, 775.52],
                          [29, 2.65, 7.11],
                          [21, 5.34, 0.98],
                          [19, 1.85, 5486.78],
                          [19, 4.97, 213.3],
                          [17, 2.99, 6275.96],
                          [16, 0.03, 2544.31],
                          [16, 1.43, 2146.17],
                          [15, 1.21, 10977.08],
                          [12, 2.83, 1748.02],
                          [12, 3.26, 5088.63],
                          [12, 5.27, 1194.45],
                          [12, 2.08, 4694],
                          [11, 0.77, 553.57],
                          [10, 1.3, 6286.6],
                          [10, 4.24, 1349.87],
                          [9, 2.7, 242.73],
                          [9, 5.64, 951.72],
                          [8, 5.3, 2352.87],
                          [6, 2.65, 9437.76],
                          [6, 4.67, 4690.48]])

        L2 = numpy.array([[52919.0, 0, 0],
                          [8720.0, 1.0721, 6283.0758],
                          [309.0, 0.867, 12566.152],
                          [27, 0.05, 3.52],
                          [16, 5.19, 26.3],
                          [16, 3.68, 155.42],
                          [10, 0.76, 18849.23],
                          [9, 2.06, 77713.77],
                          [7, 0.83, 775.52],
                          [5, 4.66, 1577.34],
                          [4, 1.03, 7.11],
                          [4, 3.44, 5573.14],
                          [3, 5.14, 796.3],
                          [3, 6.05, 5507.55],
                          [3, 1.19, 242.73],
                          [3, 6.12, 529.69],
                          [3, 0.31, 398.15],
                          [3, 2.28, 553.57],
                          [2, 4.38, 5223.69],
                          [2, 3.75, 0.98]
                          ])

        L3 = numpy.array([[289.0, 5.844, 6283.076],
                          [35, 0, 0],
                          [17, 5.49, 12566.15],
                          [3, 5.2, 155.42],
                          [1, 4.72, 3.52],
                          [1, 5.3, 18849.23],
                          [1, 5.97, 242.73]
                          ])

        L4 = numpy.array([[114.0, 3.142, 0],
                          [8, 4.13, 6283.08],
                          [1, 3.84, 12566.15]
                          ])

        L5 = numpy.array([[1, 3.14, 0]])

        B0 = numpy.array([[280.0, 3.199, 84334.662],
                          [102.0, 5.422, 5507.553],
                          [80, 3.88, 5223.69],
                          [44, 3.7, 2352.87],
                          [32, 4, 1577.34]
                          ])

        B1 = numpy.array([[9, 3.9, 5507.55],
                          [6, 1.73, 5223.69]
                          ])

        R0 = numpy.array([[100013989.0, 0, 0],
                          [1670700.0, 3.0984635, 6283.07585],
                          [13956.0, 3.05525, 12566.1517],
                          [3084.0, 5.1985, 77713.7715],
                          [1628.0, 1.1739, 5753.3849],
                          [1576.0, 2.8469, 7860.4194],
                          [925.0, 5.453, 11506.77],
                          [542.0, 4.564, 3930.21],
                          [472.0, 3.661, 5884.927],
                          [346.0, 0.964, 5507.553],
                          [329.0, 5.9, 5223.694],
                          [307.0, 0.299, 5573.143],
                          [243.0, 4.273, 11790.629],
                          [212.0, 5.847, 1577.344],
                          [186.0, 5.022, 10977.079],
                          [175.0, 3.012, 18849.228],
                          [110.0, 5.055, 5486.778],
                          [98, 0.89, 6069.78],
                          [86, 5.69, 15720.84],
                          [86, 1.27, 161000.69],
                          [65, 0.27, 17260.15],
                          [63, 0.92, 529.69],
                          [57, 2.01, 86996.85],
                          [56, 5.24, 71430.7],
                          [49, 3.25, 2544.31],
                          [47, 2.58, 775.52],
                          [45, 5.54, 9437.76],
                          [43, 6.01, 6275.96],
                          [39, 5.36, 4694],
                          [38, 2.39, 8827.39],
                          [37, 0.83, 19651.05],
                          [37, 4.9, 12139.55],
                          [36, 1.67, 12036.46],
                          [35, 1.84, 2942.46],
                          [33, 0.24, 7084.9],
                          [32, 0.18, 5088.63],
                          [32, 1.78, 398.15],
                          [28, 1.21, 6286.6],
                          [28, 1.9, 6279.55],
                          [26, 4.59, 10447.39]
                          ])

        R1 = numpy.array([[103019.0, 1.10749, 6283.07585],
                          [1721.0, 1.0644, 12566.1517],
                          [702.0, 3.142, 0],
                          [32, 1.02, 18849.23],
                          [31, 2.84, 55073.55],
                          [25, 1.32, 5223.69],
                          [18, 1.42, 1577.34],
                          [10, 5.91, 10977.08],
                          [9, 1.42, 6275.96],
                          [9, 0.27, 5486.78]
                          ])

        R2 = numpy.array([[4359.0, 5.7846, 6283.0758],
                          [124.0, 5.579, 12566.152],
                          [12, 3.14, 0],
                          [9, 3.63, 77713.77],
                          [6, 1.87, 5573.14],
                          [3, 5.47, 18849.23]
                          ])

        R3 = numpy.array([[145.0, 4.273, 6283.076],
                          [7, 3.92, 12566.15]
                          ])

        R4 = numpy.array([[4, 2.56, 6283.08]])

        Y = numpy.array([[0, 0, 0, 0, 1],
                         [-2, 0, 0, 2, 2],
                         [0, 0, 0, 2, 2],
                         [0, 0, 0, 0, 2],
                         [0, 1, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [-2, 1, 0, 2, 2],
                         [0, 0, 0, 2, 1],
                         [0, 0, 1, 2, 2],
                         [-2, -1, 0, 2, 2],
                         [-2, 0, 1, 0, 0],
                         [-2, 0, 0, 2, 1],
                         [0, 0, -1, 2, 2],
                         [2, 0, 0, 0, 0],
                         [0, 0, 1, 0, 1],
                         [2, 0, -1, 2, 2],
                         [0, 0, -1, 0, 1],
                         [0, 0, 1, 2, 1],
                         [-2, 0, 2, 0, 0],
                         [0, 0, -2, 2, 1],
                         [2, 0, 0, 2, 2],
                         [0, 0, 2, 2, 2],
                         [0, 0, 2, 0, 0],
                         [-2, 0, 1, 2, 2],
                         [0, 0, 0, 2, 0],
                         [-2, 0, 0, 2, 0],
                         [0, 0, -1, 2, 1],
                         [0, 2, 0, 0, 0],
                         [2, 0, -1, 0, 1],
                         [-2, 2, 0, 2, 2],
                         [0, 1, 0, 0, 1],
                         [-2, 0, 1, 0, 1],
                         [0, -1, 0, 0, 1],
                         [0, 0, 2, -2, 0],
                         [2, 0, -1, 2, 1],
                         [2, 0, 1, 2, 2],
                         [0, 1, 0, 2, 2],
                         [-2, 1, 1, 0, 0],
                         [0, -1, 0, 2, 2],
                         [2, 0, 0, 2, 1],
                         [2, 0, 1, 0, 0],
                         [-2, 0, 2, 2, 2],
                         [-2, 0, 1, 2, 1],
                         [2, 0, -2, 0, 1],
                         [2, 0, 0, 0, 1],
                         [0, -1, 1, 0, 0],
                         [-2, -1, 0, 2, 1],
                         [-2, 0, 0, 0, 1],
                         [0, 0, 2, 2, 1],
                         [-2, 0, 2, 0, 1],
                         [-2, 1, 0, 2, 1],
                         [0, 0, 1, -2, 0],
                         [-1, 0, 1, 0, 0],
                         [-2, 1, 0, 0, 0],
                         [1, 0, 0, 0, 0],
                         [0, 0, 1, 2, 0],
                         [0, 0, -2, 2, 2],
                         [-1, -1, 1, 0, 0],
                         [0, 1, 1, 0, 0],
                         [0, -1, 1, 2, 2],
                         [2, -1, -1, 2, 2],
                         [0, 0, 3, 2, 2],
                         [2, -1, 0, 2, 2]
                         ])

        delta_psi_coeff = numpy.array([[-171996, -174.2],
                                       [-13187, -1.6],
                                       [-2274, -0.2],
                                       [2062, 0.2],
                                       [1426, -3.4],
                                       [712, 0.1],
                                       [-517, 1.2],
                                       [-386, -0.4],
                                       [-301, 0.0],
                                       [217, -0.5],
                                       [-158, 0.0],
                                       [129, 0.1],
                                       [123, 0.0],
                                       [63, 0.0],
                                       [63, 0.1],
                                       [-59, 0.0],
                                       [-58, -0.1],
                                       [-51, 0.0],
                                       [48, 0.0],
                                       [46, 0.0],
                                       [-38, 0.0],
                                       [-31, 0.0],
                                       [29, 0.0],
                                       [29, 0.0],
                                       [26, 0.0],
                                       [-22, 0.0],
                                       [21, 0.0],
                                       [17, -0.1],
                                       [16, 0.0],
                                       [-16, 0.1],
                                       [-15, 0.0],
                                       [-13, 0.0],
                                       [-12, 0.0],
                                       [11, 0.0],
                                       [-10, 0.0],
                                       [-8, 0.0],
                                       [7, 0.0],
                                       [-7, 0.0],
                                       [-7, 0.0],
                                       [-7, 0.0],
                                       [6, 0.0],
                                       [6, 0.0],
                                       [6, 0.0],
                                       [-6, 0.0],
                                       [-6, 0.0],
                                       [5, 0.0],
                                       [-5, 0.0],
                                       [-5, 0.0],
                                       [-5, 0.0],
                                       [4, 0.0],
                                       [4, 0.0],
                                       [4, 0.0],
                                       [-4, 0.0],
                                       [-4, 0.0],
                                       [-4, 0.0],
                                       [3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0],
                                       [-3, 0.0]
                                       ])

        delta_epsilon_coeff = numpy.array([[92025, 8.9],
                                           [5736, -3.1],
                                           [977, -0.5],
                                           [-895, 0.5],
                                           [54, -0.1],
                                           [-7, 0.0],
                                           [224, -0.6],
                                           [200, 0.0],
                                           [129, -0.1],
                                           [-95, 0.3],
                                           [0.0, 0.0],
                                           [-70, 0.0],
                                           [-53, 0.0],
                                           [0.0, 0.0],
                                           [-33, 0.0],
                                           [26, 0.0],
                                           [32, 0.0],
                                           [27, 0.0],
                                           [0.0, 0.0],
                                           [-24, 0.0],
                                           [16, 0.0],
                                           [13, 0.0],
                                           [0.0, 0.0],
                                           [-12, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [-10, 0.0],
                                           [0.0, 0.0],
                                           [-8, 0.0],
                                           [7, 0.0],
                                           [9, 0.0],
                                           [7, 0.0],
                                           [6, 0.0],
                                           [0.0, 0.0],
                                           [5, 0.0],
                                           [3, 0.0],
                                           [-3, 0.0],
                                           [0.0, 0.0],
                                           [3, 0.0],
                                           [3, 0.0],
                                           [0.0, 0.0],
                                           [-3, 0.0],
                                           [-3, 0.0],
                                           [3, 0.0],
                                           [3, 0.0],
                                           [0.0, 0.0],
                                           [3, 0.0],
                                           [3, 0.0],
                                           [3, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0],
                                           [0.0, 0.0]
                                           ])

        year = numpy.array([], 'i')
        month = numpy.array([], 'i')
        day = numpy.array([])
        for element in date_time.flat:
            date_time_sep = dateparser.parse(str(element))
            year = numpy.append(year, date_time_sep.year)
            month = numpy.append(month, date_time_sep.month)
            frac_day = (date_time_sep.hour / 24.0 +
                        date_time_sep.minute / (24 * 60.0) +
                        date_time_sep.second / (24 * 60.0 * 60.0))
            day = numpy.append(day, date_time_sep.day + frac_day)
        for i, _ in enumerate(year):
            if month[i] <= 2:
                year[i] -= 1
                month[i] += 12
        A = numpy.int0(year / 100)
        B = 2 - A + numpy.int0(A / 4)

        # Calcluate Julian Day, Ephemeris Day, Century and Millenium
        JD = numpy.int0(365.25 * (year + 4716)) + numpy.int0(30.6001 * (month + 1)) + day - 1524.5
        if isinstance(B, numpy.int64):
            JD[JD > 2299160.0] += B
        else:
            JD[JD > 2299160.0] += B[JD > 2299160.0]
        JDE = JD + self.__compute_delta_T(year) / 86400.0
        JC = (JD - 2451545) / 36525.0
        JCE = (JDE - 2451545) / 36525.0
        JME = JCE / 10.0

        # Calculate the Earth heliocentric longitude, latitude and radius vector
        L0a = numpy.tile(L0, (len(JME), 1, 1))
        L1a = numpy.tile(L1, (len(JME), 1, 1))
        L2a = numpy.tile(L2, (len(JME), 1, 1))
        L3a = numpy.tile(L3, (len(JME), 1, 1))
        L4a = numpy.tile(L4, (len(JME), 1, 1))
        L5a = numpy.tile(L5, (len(JME), 1, 1))
        L0i = L0a[:, :, 0].T * numpy.cos(L0a[:, :, 1].T + numpy.outer(L0[:, 2], JME))
        L1i = L1a[:, :, 0].T * numpy.cos(L1a[:, :, 1].T + numpy.outer(L1[:, 2], JME))
        L2i = L2a[:, :, 0].T * numpy.cos(L2a[:, :, 1].T + numpy.outer(L2[:, 2], JME))
        L3i = L3a[:, :, 0].T * numpy.cos(L3a[:, :, 1].T + numpy.outer(L3[:, 2], JME))
        L4i = L4a[:, :, 0].T * numpy.cos(L4a[:, :, 1].T + numpy.outer(L4[:, 2], JME))
        L5i = L5a[:, :, 0].T * numpy.cos(L5a[:, :, 1].T + numpy.outer(L5[:, 2], JME))
        L0_sum = L0i.sum(axis=0)
        L1_sum = L1i.sum(axis=0)
        L2_sum = L2i.sum(axis=0)
        L3_sum = L3i.sum(axis=0)
        L4_sum = L4i.sum(axis=0)
        L5_sum = L5i.sum(axis=0)
        L = (L0_sum + L1_sum * JME + L2_sum * JME ** 2 + L3_sum * JME ** 3 +
             L4_sum * JME ** 4 + L5_sum * JME ** 5) / (1.0e8) * RAD_TO_DEG
        B1a = numpy.tile(B1, (len(JME), 1, 1))
        B0a = numpy.tile(B0, (len(JME), 1, 1))
        B0i = B0a[:, :, 0].T * numpy.cos(B0a[:, :, 1].T + numpy.outer(B0[:, 2], JME))
        B1i = B1a[:, :, 0].T * numpy.cos(B1a[:, :, 1].T + numpy.outer(B1[:, 2], JME))
        B0_sum = B0i.sum(axis=0)
        B1_sum = B1i.sum(axis=0)
        B = (B0_sum + B1_sum * JME) / (1.0e8) * RAD_TO_DEG
        R0a = numpy.tile(R0, (len(JME), 1, 1))
        R1a = numpy.tile(R1, (len(JME), 1, 1))
        R2a = numpy.tile(R2, (len(JME), 1, 1))
        R3a = numpy.tile(R3, (len(JME), 1, 1))
        R4a = numpy.tile(R4, (len(JME), 1, 1))
        R0i = R0a[:, :, 0].T * numpy.cos(R0a[:, :, 1].T + numpy.outer(R0[:, 2], JME))
        R1i = R1a[:, :, 0].T * numpy.cos(R1a[:, :, 1].T + numpy.outer(R1[:, 2], JME))
        R2i = R2a[:, :, 0].T * numpy.cos(R2a[:, :, 1].T + numpy.outer(R2[:, 2], JME))
        R3i = R3a[:, :, 0].T * numpy.cos(R3a[:, :, 1].T + numpy.outer(R3[:, 2], JME))
        R4i = R4a[:, :, 0].T * numpy.cos(R4a[:, :, 1].T + numpy.outer(R4[:, 2], JME))
        R0_sum = R0i.sum(axis=0)
        R1_sum = R1i.sum(axis=0)
        R2_sum = R2i.sum(axis=0)
        R3_sum = R3i.sum(axis=0)
        R4_sum = R4i.sum(axis=0)
        R = (R0_sum + R1_sum * JME + R2_sum * JME ** 2 + R3_sum * JME ** 3 +
             R4_sum * JME ** 4) / (1.0e8)
             
        # Calculate the geocentric longitude and latitude
        Theta = egads.algorithms.mathematics.LimitAngleRange().run(L + 180).value
        beta = -B

        # Calculate the nutation in longitude and obliquity
        X = numpy.zeros([len(JCE), 5])
        X[:, 0] = 297.85036 + 445267.111480 * JCE - 0.0019142 * JCE ** 2 + JCE ** 3 / 189474.0
        X[:, 1] = 357.52772 + 35999.050340 * JCE - 0.0001603 * JCE ** 2 + JCE ** 3 / 300000.0
        X[:, 2] = 134.96298 + 477198.867398 * JCE + 0.0086972 * JCE ** 2 + JCE ** 3 / 56250.0
        X[:, 3] = 93.27191 + 483202.017538 * JCE + 0.0036825 * JCE ** 2 + JCE ** 3 / 327270.0
        X[:, 4] = 125.04452 - 1934.136261 * JCE + 0.0020708 * JCE ** 2 + JCE ** 3 / 450000.0
        delta_psi_coeff_ext = numpy.tile(delta_psi_coeff, (len(JCE), 1, 1))
        delta_epsilon_coeff_ext = numpy.tile(delta_epsilon_coeff, (len(JCE), 1, 1))
        X_Y_sum = numpy.dot(X, Y.T) * DEG_TO_RAD
        delta_psi_i = (delta_psi_coeff_ext[:, :, 0].T +
                       numpy.outer(delta_psi_coeff[:, 1], JCE)) * numpy.sin(X_Y_sum.T)
        delta_epsilon_i = (delta_epsilon_coeff_ext[:, :, 0].T +
                           numpy.outer(delta_epsilon_coeff[:, 1], JCE)) * numpy.cos(X_Y_sum.T)
        delta_psi = delta_psi_i.sum(axis=0) / 36000000.0
        delta_epsilon = delta_epsilon_i.sum(axis=0) / 36000000.0
        
        # Calculate the true obliquity of the ecliptic
        U = JME / 10.0
        epsilon_0 = (84381.448 - 4680.93 * U - 1.55 * U ** 2 + 1999.25 * U ** 3 -
                     51.38 * U ** 4 - 249.67 * U ** 5 - 39.05 * U ** 6 + 7.12 * U ** 7 +
                     27.87 * U ** 8 + 5.79 * U ** 9 + 2.45 * U ** 10)
        epsilon = epsilon_0 / 3600.0 + delta_epsilon

        # Calculate the aberration correction
        delta_tau = -20.4898 / (3600.0 * R)

        # Calculate the apparent sun longitude
        lambda_sun = Theta + delta_psi + delta_tau

        # Calculate apparent sidereal time at Greenwich
        nu_0 = (280.46061837 + 360.98564736629 * (JD - 2451545) + 0.000387933 * JC ** 2 - JC ** 3 / 38710000.0)
        nu_0 = egads.algorithms.mathematics.LimitAngleRange().run(nu_0).value
        nu = nu_0 + delta_psi * numpy.cos(epsilon * DEG_TO_RAD)

        # Calculate geocentric sun right ascension
        alpha = numpy.arctan2(numpy.sin(lambda_sun * DEG_TO_RAD) * numpy.cos(epsilon * DEG_TO_RAD) -
                              numpy.tan(beta * DEG_TO_RAD) * numpy.sin(epsilon * DEG_TO_RAD),
                              numpy.cos(lambda_sun * DEG_TO_RAD)) * RAD_TO_DEG
        alpha = egads.algorithms.mathematics.LimitAngleRange().run(alpha).value

        # Calculate geocentric sun declination
        delta = numpy.arcsin(numpy.sin(beta * DEG_TO_RAD) * numpy.cos(epsilon * DEG_TO_RAD) +
                             numpy.cos(beta * DEG_TO_RAD) * numpy.sin(epsilon * DEG_TO_RAD) *
                             numpy.sin(lambda_sun * DEG_TO_RAD)) * RAD_TO_DEG

        # Calculate the observer local hour angle
        H = nu + lon - alpha
        H = egads.algorithms.mathematics.LimitAngleRange().run(H).value

        # Calculate the topocentric sun right ascension
        xi = 8.794 / (3600.0 * R)
        u = numpy.arctan(0.99664719 * numpy.tan(lat * DEG_TO_RAD))
        x = numpy.cos(u) + elevation / 6378140.0 * numpy.cos(lat * DEG_TO_RAD)
        y = 0.99664719 * numpy.sin(u) + elevation / 6378140.0 * numpy.sin(lat * DEG_TO_RAD)
        delta_alpha = numpy.arctan2(-x * numpy.sin(xi * DEG_TO_RAD) * numpy.sin(H * DEG_TO_RAD),
                                    numpy.cos(delta * DEG_TO_RAD) - x * numpy.sin(xi * DEG_TO_RAD) *
                                    numpy.cos(H * DEG_TO_RAD)) * RAD_TO_DEG
        delta_prime = numpy.arctan2((numpy.sin(delta * DEG_TO_RAD) - y * numpy.sin(xi * DEG_TO_RAD)) *
                                     numpy.cos(delta_alpha * DEG_TO_RAD),
                                     numpy.cos(delta * DEG_TO_RAD) -
                                     x * numpy.sin(xi * DEG_TO_RAD) * numpy.cos(H * DEG_TO_RAD)) * RAD_TO_DEG

        # Calculate topocentric hour angle
        H_prime = H - delta_alpha

        # Calculate the topographic zenith angle
        e_0 = numpy.arcsin(numpy.sin(lat * DEG_TO_RAD) * numpy.sin(delta_prime * DEG_TO_RAD) +
                           numpy.cos(lat * DEG_TO_RAD) * numpy.cos(delta_prime * DEG_TO_RAD) *
                           numpy.cos(H_prime * DEG_TO_RAD)) * RAD_TO_DEG
        if pressure.any() and temperature.any():
            tan_arg = e_0 + 10.3 / (e_0 + 5.11)
            delta_e = pressure / 1010.0 * 283 / (273.0 + temperature) * 1.02 / (60 *
                                                                              numpy.tan(tan_arg * DEG_TO_RAD))
        else:
            delta_e = 0
        e = e_0 + delta_e
        theta = 90 - e

        # Calculate the topocentric azimuth angle
        Gamma = numpy.arctan2(numpy.sin(H_prime * DEG_TO_RAD),
                              numpy.cos(H_prime * DEG_TO_RAD) * numpy.sin(lat * DEG_TO_RAD) -
                              numpy.tan(delta_prime * DEG_TO_RAD) * numpy.cos(lat * DEG_TO_RAD)) * RAD_TO_DEG
        Gamma = egads.algorithms.mathematics.LimitAngleRange().run(Gamma).value
        Phi = Gamma + 180
        Phi = egads.algorithms.mathematics.LimitAngleRange().run(Phi).value
        return [theta, Phi]
    
    def __compute_delta_T(self, year):
        """
        Compute delta_T, the difference between Earth rotation time and the Terrestrial time, based
        on NASA GSFC "Polynomial expressions for delta T" (cf. https://eclipse.gsfc.nasa.gov/LEcat5/deltatpoly.html)
        """
        
        delta_T = 67. # default value used by Matt Freer at algorithm creation time
        
        if year < -500:
            t = (year - 1820.) / 100.
            delta_T = -20. + 32. * t ** 2.
        elif year >= -500 and year < 500:
            t = year / 100.
            delta_T = 10583.6 - 1014.41 * t + 33.78311 * t ** 2 - 5.952053 * t ** 3 
            - 0.1798452 * t ** 4 + 0.022174192 * t ** 5 + 0.0090316521 * t ** 6 
        elif year >= 500 and year < 1600:
            t = (year - 1000.) / 100.
            delta_T = 1574.2 - 556.01 * t + 71.23472 * t ** 2 + 0.319781 * t ** 3 - 0.8503463 * t ** 4 
            - 0.005050998 * t ** 5 + 0.0083572073 * t ** 6
        elif year >= 1600 and year < 1700:
            t = year - 1600.
            delta_T = 120 - 0.9808 * t - 0.01532 * t ** 2 + (t ** 3) / 7129. 
        elif year >= 1700 and year < 1800:
            t = year - 1700.
            delta_T = 8.83 + 0.1603 * t - 0.0059285 * t ** 2 + 0.00013336 * t ** 3 - (t ** 4) / 1174000.
        elif year >= 1800 and year < 1860:
            t = year - 1800.
            delta_T = 13.72 - 0.332447 * t + 0.0068612 * t ** 2 + 0.0041116 * t ** 3 - 0.00037436 * t ** 4 
            + 0.0000121272 * t ** 5 - 0.0000001699 * t ** 6 + 0.000000000875 * t ** 7
        elif year >= 1860 and year < 1900:
            t = year - 1860.
            delta_T = 7.62 + 0.5737 * t - 0.251754 * t ** 2 + 0.01680668 * t ** 3 -0.0004473624 * t ** 4 
            + (t ** 5) / 233174.
        elif year >= 1900 and year < 1920:
            t = year - 1900.
            delta_T = -2.79 + 1.494119 * t - 0.0598939 * t ** 2 + 0.0061966 * t ** 3 - 0.000197 * t ** 4 
        elif year >= 1920 and year < 1941:
            t = year - 1920.
            delta_T = 21.20 + 0.84493 * t - 0.076100 * t ** 2 + 0.0020936 * t ** 3
        elif year >= 1941 and year < 1960:
            t = year - 1950.
            delta_T = 29.07 + 0.407 * t - (t ** 2) / 233. + (t ** 3) / 2547.
        elif year >= 1961 and year < 1986:
            t = year - 1975.
            delta_T = 45.45 + 1.067 * t - t ** 2 / 260. - t ** 3 / 718.
        elif year >= 1986 and year < 2005:
            t = year - 2000.
            delta_T = 63.86 + 0.3345 * t - 0.060374 * t ** 2 + 0.0017275 * t ** 3 + 0.000651814 * t ** 4 
            + 0.00002373599 * t ** 5
        elif year >= 2005 and year < 2050:
            t = year - 2000.
            delta_T = 62.92 + 0.32217 * t + 0.005589 * t ** 2
        elif year >= 2050 and year < 2150:
            delta_T = -20. + 32. * ((year - 1820.) / 100.) ** 2 - 0.5628 * (2150. - year)
        elif year >= 2150:
            t = (year - 1820.) / 100.
            delta_T = -20. + 32. * t ** 2
  
        return delta_T
        
