__author__ = "ohenry"
__date__ = "2018-01-02 14:32"
__version__ = "1.0"
__all__ = ["CheckEgadsUpdate"]

import logging
import requests
from distutils.version import LooseVersion
from egads._version import __version__
from threading import Thread


class CheckEgadsUpdate(Thread):
    """
    This class is designed to check the availability of an update for egads on GitHub.
    """
    
    def __init__(self):
        logging.debug('egads - egads_thread.py - CheckEgadsUpdate - __init__')
        Thread.__init__(self)
    
    def run(self):
        logging.debug('egads - egads_thread.py - CheckEgadsUpdate - run')
        url = 'https://api.github.com/repos/eufarn7sp/egads/releases/latest'
        try:
            json_object = requests.get(url=url, timeout=5).json()
            if LooseVersion(__version__) < LooseVersion(json_object['tag_name']):
                logging.info('EGADS v' + json_object['tag_name'] + ' is available on GitHub. You can update'
                       + ' EGADS by using pip (pip install egads --upgrade) or by using the following'
                       + ' link: ' + str(json_object['assets'][0]['browser_download_url']))
                print ('EGADS v' + json_object['tag_name'] + ' is available on GitHub. You can update'
                       + ' EGADS by using pip (pip install egads --upgrade) or by using the following'
                       + ' link: ' + str(json_object['assets'][0]['browser_download_url']))
        except Exception:
            logging.exception('egads - egads_thread.py - CheckEgadsUpdate - run - internet connection error - url ' + url)
        
    def stop(self):
        self.terminate()
        