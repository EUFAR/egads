__author__ = "ohenry"
__date__ = "2019-06-11 15:30"
__version__ = "1.2"

import logging
import os
import datetime
import configparser
import pathlib


def _create_option_dictionary(user_path):
    config_dict = configparser.ConfigParser()
    if not pathlib.Path(pathlib.Path(user_path).joinpath('egads.ini')).is_file():
        if not pathlib.Path(user_path).is_dir():
            pathlib.Path(user_path).mkdir()
        ini_file = open(os.path.join(user_path, 'egads.ini'), 'w')
        config_dict.add_section('LOG')
        config_dict.add_section('OPTIONS')
        config_dict.set('LOG', 'level', 'WARNING')
        config_dict.set('LOG', 'path', user_path)
        config_dict.set('OPTIONS', 'check_update', 'False')
        config_dict.write(ini_file)
        ini_file.close()


def _create_log_system(config_dict, default_path):
    using_default_path = False
    if pathlib.Path(config_dict.get('LOG', 'path')).exists():
        log_filename = os.path.join(config_dict.get('LOG', 'path'), 'egads.log')
    else:
        using_default_path = True
        log_filename = os.path.join(default_path, 'egads.log')
    logging.getLogger('').handlers = []
    logging.basicConfig(filename=log_filename,
                        level=getattr(logging, config_dict.get('LOG', 'level')),
                        filemode='w',
                        format='%(asctime)s : %(levelname)s : %(message)s')
    formatter = logging.Formatter('%(levelname)s : %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    if using_default_path:
        logging.error('egads - logging system - path from ini file not found, using default path')


def _create_user_algorithms_structure(user_path):
    logging.debug('egads - egads_utils.py - create_user_algorithms_structure - user_path ' + str(user_path))
    algo_path = str(pathlib.Path(user_path).joinpath('user_algorithms'))
    if not pathlib.Path(algo_path).is_dir():
        logging.debug('egads - egads_utils.py - create_user_algorithms_structure - no user folder detected, '
                      'creating user structure')
        pathlib.Path(algo_path).mkdir()
        init_string = ('__author__ = "Olivier Henry"\n'
                       + '__date__ = "2019/05/06 11:45"\n'
                       + '__version__ = "1.0"\n\n'
                       + 'import user_algorithms.comparisons\n'
                       + 'import user_algorithms.corrections\n'
                       + 'import user_algorithms.mathematics\n'
                       + 'import user_algorithms.microphysics\n'
                       + 'import user_algorithms.thermodynamics\n'
                       + 'import user_algorithms.transforms\n'
                       + 'import user_algorithms.radiation\n')
        init_file = open(algo_path + '/__init__.py', 'w')
        init_file.write(init_string)
        init_file.close()
        user_folder = ['comparisons', 'corrections', 'mathematics', 'microphysics', 'thermodynamics', 'transforms',
                       'radiation']
        for folder in user_folder:
            logging.debug('egads - egads_utils.py - create_user_algorithms_structure - creating [user_algorithms/'
                          + folder + '] folder')
            pathlib.Path(pathlib.Path(algo_path).joinpath(folder)).mkdir()
            init_string = ('__author__ = "Olivier Henry"\n'
                           + '__date__ = "2019/05/06 11:45"\n'
                           + '__version__ = "1.0"\n\n'
                           + 'import logging\n\n'
                           + 'try:\n'
                           + "    logging.info('egads [user_algorithms/" + folder + "] algorithms have been loaded')\n"
                           + 'except Exception as e:\n'
                           + "    logging.error('an error occured during the loading of a [user_algorithms/" + folder
                           + "] algorithm: ' + str(e))\n")
            init_file = open(str(pathlib.Path(algo_path).joinpath(folder)) + '/__init__.py', 'w')
            init_file.write(init_string)
            init_file.close()
    else:
        logging.debug('egads - egads_utils.py - create_user_algorithms_structure - user folder detected, no need to '
                      'create user structure')
