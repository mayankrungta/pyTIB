#! /usr/bin/env python

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

import time
import unittest

from includes.settings import user, password
from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize,waitUntilID

from selenium.webdriver.common.action_chains import ActionChains


#######################
# Global Declarations
#######################

delay = 2
base_url = 'https://www.udemy.com/'
filename = './cmd.txt'
url = 'https://www.udemy.com/python-regular-expressions/learn/v4/t/lecture/5407736?start=0'
url = 'https://www.udemy.com/the-complete-guide-to-angular-2/learn/v4/t/lecture/6655594?start=0'


#############
# Functions
#############

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='Script for fetching Udemy lessons')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-b', '--browser', help='Specify the browser to test with', required=False)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-u', '--url', help='the URL to the first lecture', required=False, action='store_const', const=1)

  args = vars(parser.parse_args())
  return args



##########
# Tests
##########

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.args = argsFetch()
        self.logger = loggerFetch('info')
        self.logger.info('BEGIN PROCESSING')
        self.display = displayInitialize(self.args['visible'])
        self.driver = driverInitialize(browser=self.args['browser'] , path='/home/mayank/.mozilla/firefox/4s3bttuq.default/')
        self.cmd = 'nohup youtube-dl --username %s --password %s -o %s ' % (user, password, '"%(title)s.%(ext)s"')
        self.url = self.args['url']


    def tearDown(self):
        driverFinalize(self.driver)
        displayFinalize(self.display)
        self.logger.info('...END PROCESSING')

    @unittest.skip('Skipping direct command approach')
    def test_direct_cmd(self):
        cmd = 'curl -L -O %s' % url
        os.system(cmd)

    def test_fetch_lessons(self):
        result = 'SUCCESS'

        self.driver.get(base_url)
        self.logger.info('Fetching URL[%s]' % base_url)
        try:
            self.driver.find_element_by_link_text("Log In").click()
            self.driver.find_element_by_id("id_email").clear()
            self.driver.find_element_by_id("id_email").send_keys(user)
            self.driver.find_element_by_id("id_password").clear()
            self.driver.find_element_by_id("id_password").send_keys(password)
            self.driver.find_element_by_id("submit-id-submit").click()
            
            #time.sleep(100) # If you want to manually log in
        except Exception as e:
            self.logger.info('Already signed in [%s]', e)
        time.sleep(delay)

        self.driver.get(url)
        time.sleep(delay)

        current_url = url
        
        while True:
            try:
                if 'quiz' in current_url:
                    elem = self.driver.find_element_by_class_name("continue-button--btn__label--3H0BR")
                else:
                    elem = self.driver.find_element_by_class_name("continue-button--responsive--3c3TI")
                    hover = ActionChains(self.driver).move_to_element(elem)
                    hover.perform()
                elem.click()
                current_url = self.driver.current_url
                self.logger.info('Current URL[%s]' % current_url)                
                if 'quiz' not in current_url:
                    self.cmd += ' ' + current_url
                    self.logger.debug('Command so far [%s]' % self.cmd)
                time.sleep(delay)
                    
            except Exception as e:
                self.logger.info('Oops there was a problem![%s]' % str(e))
                result = 'FAILED'
                break

        self.logger.info('From URL[%s] to URL[%s]' % (url, current_url))
        self.logger.info('Command[%s]' % self.cmd)

        with open(filename, 'w') as cmdfile:
            self.logger.info('Writing to file[%s]' % filename)
            cmdfile.write(self.cmd)
        
        self.assertEqual('SUCCESS', result)

if __name__ == '__main__':
    unittest.main()
