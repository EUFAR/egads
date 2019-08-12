__author__ = "ohenry"
__date__ = "2019-06-11 15:30"
__version__ = "1.1"

import logging
import os
import datetime
import configparser


def _create_option_dictionary(main_path):
    config_dict = configparser.ConfigParser()
    if not os.path.exists(os.path.join(main_path, 'egads.ini')):
        ini_file = open(os.path.join(main_path, 'egads.ini'), 'w')
        config_dict.add_section('LOG')
        config_dict.add_section('OPTIONS')
        config_dict.set('LOG', 'level', 'INFO')
        config_dict.set('LOG', 'path', main_path)
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


def _create_user_algorithms_structure(main_path):
    logging.debug('egads - egads_utils.py - create_user_algorithms_structure - main_path ' + str(main_path))
    user_path = os.path.join(main_path, 'algorithms/user/')
    if not os.path.isdir(user_path):
        logging.debug('egads - egads_utils.py - create_user_algorithms_structure - no user folder detected, '
                      'creating user structure')
        os.makedirs(user_path)
        init_string = ('__author__ = "Olivier Henry"\n'
                       + '__date__ = "2019/05/06 11:45"\n'
                       + '__version__ = "1.0"\n\n'
                       + 'import egads.algorithms.user.comparisons\n'
                       + 'import egads.algorithms.user.corrections\n'
                       + 'import egads.algorithms.user.mathematics\n'
                       + 'import egads.algorithms.user.microphysics\n'
                       + 'import egads.algorithms.user.thermodynamics\n'
                       + 'import egads.algorithms.user.transforms\n'
                       + 'import egads.algorithms.user.radiation\n')
        init_file = open(user_path + '__init__.py', 'w')
        init_file.write(init_string)
        init_file.close()
        user_folder = ['comparisons', 'corrections', 'mathematics', 'microphysics', 'thermodynamics', 'transforms',
                       'radiation']
        for folder in user_folder:
            logging.debug('egads - egads_utils.py - create_user_algorithms_structure - creating [user/' + folder + '] '
                          + 'folder')
            os.makedirs(os.path.join(user_path, folder))
            init_string = ('__author__ = "Olivier Henry"\n'
                           + '__date__ = "2019/05/06 11:45"\n'
                           + '__version__ = "1.0"\n\n'
                           + 'import logging\n\n'
                           + 'try:\n'
                           + "    logging.info('egads [user/" + folder + "] algorithms have been loaded')\n"
                           + 'except Exception as e:\n'
                           + "    logging.error('an error occured during the loading of a [user/" + folder
                           + "] algorithm: ' + str(e)\n")
            init_file = open(os.path.join(user_path, folder) + '/__init__.py', 'w')
            init_file.write(init_string)
            init_file.close()
    else:
        logging.debug('egads - egads_utils.py - create_user_algorithms_structure - user folder detected, no need to '
                      'create user structure')
