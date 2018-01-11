__author__ = "mfreer, ohenry"
__date__ = "2017-01-11 11:12"
__version__ = "1.4"
__all__ = ['SolarVectorBlanco']

import numpy
import dateutil.parser as dateparser
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class SolarVectorBlanco(egads_core.EgadsAlgorithm):
    
    """
    FILE        solar_vector_blanco.py

    VERSION     1.4

    CATEGORY    Radiation

    PURPOSE     Calculation of solar vector based on current time, latitude
                and longitude

    DESCRIPTION Calculation of solar vector using the Blanco-Muriel et al. algorithm.
                This algorithm is optimized for the period between 1999 and 2005, however
                it has been shown to compute the solar vector with an error of less
                than 0.5 minutes of arc out to 2015.                

    INPUT       date-time    vector    yyyymmddThhmmss    ISO8601 string of current
                                                          date/time
                lat          vector    degrees            latitude
                lon          vector    degrees            longitude

    OUTPUT      ra           vector    radians            right ascension
                delta        vector    radians            declination
                theta_z      vector    radians            solar zenith
                gamma        vector    radians            solar azimuth

    SOURCE      

    REFERENCES  Manuel Blanco-Muriel, et al., "Computing the Solar Vector," 
                Solar Energy, 70 (2001): 436-38.
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'radians',
                                                               'long_name':'right ascension',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'radians',
                                                               'long_name':'declination',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'radians',
                                                               'long_name':'solar zenith',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'radians',
                                                               'long_name':'solar azimuth',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['date-time', 'lat', 'lon'],
                                                          'InputUnits':['', 'degrees', 'degrees'],
                                                          'InputTypes':['time','vector','vector'],
                                                          'InputDescription':['ISO8601 string of current date/time','Latitude','Longitude'],
                                                          'Outputs':['ra', 'delta', 'theta_z', 'gamma'],
                                                          'OutputUnits':['radians','radians','radians','radians'],
                                                          'OutputTypes':['vector','vector','vector','vector'],
                                                          'OutputDescription':['Right ascension','Declination','Solar zenith','Solar azimuth'],
                                                          'Purpose':'Calculation of solar vector based on current time, latitude and longitude',
                                                          'Description':'Calculation of solar vector using the Blanco-Muriel et al. algorithm. This algorithm is optimized for the period between 1999 and 2005, however it has been shown to compute the solar vector with an error of less than 0.5 minutes of arc out to 2015',
                                                          'Category':'Radiation',
                                                          'Source':'',
                                                          'References':'Manuel Blanco-Muriel, et al., "Computing the Solar Vector," Solar Energy, 70 (2001): 436-38.',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, date_time, lat, lon):
        return egads_core.EgadsAlgorithm.run(self, date_time, lat, lon)


    def _algorithm(self, date_time, lat, lon):
        year = numpy.array([], 'i')
        month = numpy.array([], 'i')
        day = numpy.array([], 'i')
        hour = numpy.array([])
        idx = numpy.array([], 'i')
        for element in date_time.flat:
            date_time_sep = dateparser.parse(str(element))
            year = numpy.append(year, date_time_sep.year)
            month = numpy.append(month, date_time_sep.month)
            day = numpy.append(day, date_time_sep.day)
            if (date_time_sep.month <= 2):
                idx = numpy.append(idx, -1)
            else:
                idx = numpy.append(idx, 0)
            hour = numpy.append(hour,
                                date_time_sep.hour +
                                date_time_sep.minute / 60.0 +
                                date_time_sep.second / 3600.0)
        EARTH_MEAN_RADIUS = 6371.01  # km
        AU = 149597890.0  # km

        # Calculate Julian Day
        jd = ((1461 * (year + 4800 + idx)) / 4 +
              (367 * (month - 2 - 12 * idx)) / 12 -
              (3 * ((year + 4900 + idx) / 100)) / 4 +
              day - 32075)

        n = jd - 0.5 + hour / 24.0 - 2451545.0

        # Calculate ecliptic coordinates of the sun
        Omega = 2.1429 - 0.0010394594 * n
        L = 4.8950630 + 0.017202791698 * n
        g = 6.2400600 + 0.0172019699 * n
        l = (L + 0.03341607 * numpy.sin(g) + 0.00034894 * numpy.sin(2 * g) -
             0.0001134 - 0.0000203 * numpy.sin(Omega))
        ep = 0.4090928 - 6.2140e-9 * n + 0.0000396 * numpy.cos(Omega)

        # Convert ecliptic coordinates to celestial coordinates
        ra = numpy.arctan2(numpy.cos(ep) * numpy.sin(l), numpy.cos(l))
        delta = numpy.arcsin(numpy.sin(ep) * numpy.sin(l))
        ra = ra % (2 * numpy.pi)  # @UndefinedVariable

        # Convert from celestial coordinates to horizontal coordinates
        gmst = 6.6974243242 + 0.0657098283 * n + hour
        lmst = (gmst * 15 + lon) * numpy.pi / 180.0
        hour_angle = lmst - ra
        theta_z = numpy.arccos(numpy.cos(lat * numpy.pi / 180.0) *
                               numpy.cos(hour_angle) * numpy.cos(delta) +
                               numpy.sin(delta) * numpy.sin(lat * numpy.pi / 180.0))
        gamma = numpy.arctan2(-numpy.sin(hour_angle), (numpy.tan(delta) *
                                                       numpy.cos(lat * numpy.pi / 180) -
                                                       numpy.sin(lat * numpy.pi / 180) *
                                                       numpy.cos(hour_angle))
                              )
        Parallax = EARTH_MEAN_RADIUS / AU * numpy.sin(theta_z)
        theta_z = theta_z + Parallax
        return [ra, delta, theta_z, gamma]

