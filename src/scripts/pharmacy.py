from bs4 import BeautifulSoup

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from os import errno

import requests
import time
import unittest

from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize, driverFinalize, displayInitialize, displayFinalize

#######################
# Global Declarations
#######################

timeout = 10
dirname = 'pharmacies'

def fetch_state(logger, driver, state=None):
    '''
    if not state:
        # default value?
    
    vendor_id = 'ctl00_cphMain_dlVendors_ctl00_lbVendor'
    '''

    url = 'http://www.ecompoundingpharmacy.com/local-compounding-pharmacy/%s' % state
    driver.get(url)
    logger.info("Fetching...[%s]" % url)

    html_source = driver.page_source.replace('<head>',
                                         '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
    logger.debug("HTML Fetched [%s]" % html_source)

    bs = BeautifulSoup(html_source, 'html.parser')

    table = bs.find(id='ctl00_cphMain_dlVendors')
    logger.debug('table[%s]' % str(table))

    tr_list = table.select('tr')
    logger.debug(str(tr_list))

    for tr in tr_list:
        td = tr.findChild('td')
        a = td.findChild('a')
        shop_name = a.text.strip()
        vendor_id = a.get('id').strip()
        logger.info('Fetching the HTML for [%s, %s]' % (shop_name, vendor_id))
    
        filename = '%s/%s_%s_%s.html' % (dirname, state, shop_name, vendor_id)
        if os.path.exists(filename):
            logger.info('File already donwnloaded. Skipping [%s]' % filename)
            continue
        
        try:
            elem = driver.find_element_by_id(vendor_id)   # Selenium IDE gave - id=ctl00_cphMain_dlVendors_ctl00_lbVendor
            elem.click()
            logger.info('Entering vendor_id[%s]' % vendor_id)
        except Exception as e:
            logger.error('Ouch! Caught Exception[%s]' % e)
        #time.sleep(timeout)
        
        html_source = driver.page_source.replace('<head>',
                                                 '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
        logger.debug("HTML Fetched [%s]" % html_source)
        with open(filename, 'w') as html_file:
            logger.info('Writing [%s]' % filename)
            html_file.write(html_source)
            
        driver.back()  # can do forward back for the rest of the IDs obtained from the html
            
    return 'SUCCESS'

def fetch_pharmacies(logger, driver):
    logger.info('Fetch the jobcards')

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise        

    state_list = ['Alabama', ]  # or hard code here    
    
    for state in state_list:
        '''
        Use post to get the list of IDs??

        filename = '%s/%s.html' % (dirname, state)
        # If already downloaded before the state file just re-read
        if os.path.exists(filename):
            with open(filename, 'rb') as html_file:
                logger.info('File already donwnloaded. Reading [%s]' % filename)
                state_html = html_file.read()
        else:
            url = 'http://www.ecompoundingpharmacy.com/local-compounding-pharmacy/%s' % state
            
            try:
                logger.info('Requesting URL[%s]' % url)
                response = requests.get(url, timeout=timeout) # , cookies=cookies)
            except Exception as e:
                logger.error('Caught Exception[%s]' % e) 
            
            state_html = response.content
            with open(filename, 'wb') as html_file:
                logger.info('Writing [%s]' % filename)
                html_file.write(state_html)   # Writing this just for debuging and reuse

        logger.debug('List of IDs under state[%s]' % state_html)
        '''
        
        fetch_state(logger, driver, state=state)
    
    return 'SUCCESS'

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = loggerFetch('info')
        self.logger.info('BEGIN PROCESSING...')
        self.display = displayInitialize(1)
        self.driver = driverInitialize(path='/opt/firefox/', timeout=3)

    def tearDown(self):
        #FIXME driverFinalize(self.driver) 
        displayFinalize(self.display)
        self.logger.info('...END PROCESSING')

    def test_rn6_report(self):
        result = fetch_pharmacies(self.logger, self.driver)
        self.assertEqual(result, 'SUCCESS')

if __name__ == '__main__':
    unittest.main()
