__author__ = "ohenry"
__date__ = "2019-06-05 13:45"
__version__ = "1.0"
__all__ = ["CheckEgadsUpdate"]

import logging
try:
    import requests
except ImportError:
    print('requests is not available')
from distutils.version import LooseVersion
from threading import Thread


class CheckEgadsUpdate(Thread):
    """
    This class is designed to check the availability of an update for egads on GitHub.
    """
    
    def __init__(self, egads_version):
        logging.debug('egads - egads_thread.py - CheckEgadsUpdate - __init__')
        Thread.__init__(self)
        self.egads_version = egads_version
    
    def run(self):
        logging.debug('egads - egads_thread.py - CheckEgadsUpdate - run')
        url = 'https://api.github.com/repos/eufarn7sp/egads/releases'
        try:
            json_object = requests.get(url=url, timeout=5).json()
            lineage_list = []
            for egads_package in json_object:
                if 'Lineage' in egads_package['name']:
                    lineage_list.append([egads_package['tag_name'], egads_package['assets'][2]['browser_download_url']])

            lineage_list = sorted(lineage_list)
            if LooseVersion(self.egads_version) < LooseVersion(lineage_list[-1][0]):
                logging.info('EGADS v' + lineage_list[-1][0] + ' is available on GitHub. You can updateccEGADS '
                             + 'by using pip (pip install egads-lineage --upgrade) or by using the following  link: '
                             + str(lineage_list[-1][1]))
                print('EGADS v' + lineage_list[-1][0] + ' is available on GitHub. You can update EGADS by using pip '
                      + '(pip install egads-lineage --upgrade) or by using the following link: '
                      + str(lineage_list[-1][1]))
            else:
                print('No update available.')
                logging.info('No update available.')
        except Exception:
            logging.exception('egads - egads_thread.py - CheckEgadsUpdate - run - internet connection error - url ' +
                              url)
        
    def stop(self):
        self.terminate()
