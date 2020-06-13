#! /usr/bin/env python

#This code will get the Oabcgatat Banes
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

#######################
# Global Declarations
#######################

url="http://www.hostedivr.in"
browser="Firefox"

#############
# Functions
#############

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='Jobcard script for crawling, downloading & parsing')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-t', '--timeout', help='Time to wait before a page loads', required=False)
  parser.add_argument('-b', '--browser', help='Specify the browser to test with', required=False)
  parser.add_argument('-u', '--url', help='Specify the url to crawl', required=False)
  parser.add_argument('-f', '--filename', help='Specify the wave file to upload', required=True)
  parser.add_argument('-d', '--directory', help='Specify directory to download html file to', required=False)

  args = vars(parser.parse_args())
  return args

def parserFinalize(parser):
  parser.close()


def displayInitialize(isVisible=0):
  from pyvirtualdisplay import Display
  
  display = Display(visible=isVisible, size=(600, 400))
  display.start()
  return display

def displayFinalize(display):
  display.stop()

def driverInitialize(browser="Firefox"):
  if browser == "Firefox":
    fp = webdriver.FirefoxProfile()
    fp.native_events_enabled = False
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", os.getcwd())
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")

    driver = webdriver.Firefox(fp)
  elif browser == "PhantomJS":
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
  else:
    driver = webdriver.Chrome()

  driver.implicitly_wait(10)

  return driver

def driverFinalize(driver):
  driver.close()


def wdTest(driver):
  driver.get("http://www.google.com")
  print driver.page_source.encode('utf-8')



def waveUpload(url, driver, wave_file):
  '''
  Fetch the html for the jobcard
  '''
  driver.get(url)
  driver.find_element_by_name("uname").clear()
  driver.find_element_by_name("uname").send_keys("togoli@gmail.com")
  driver.find_element_by_name("upass").clear()
  driver.find_element_by_name("upass").send_keys("golani123")
  driver.find_element_by_css_selector("button.button-yellow").click()
  driver.find_element_by_xpath("(//a[contains(text(),'Upload Wave')])[3]").click()
  driver.find_element_by_name("uploaded_file").send_keys(wave_file)
  #driver.find_element_by_name("uploaded_file").send_keys("/home/mayankr/libtech/scripts/test.wav")
  driver.find_element_by_css_selector("button.button-yellow").click()


def main():
  args = argsFetch()

  display = displayInitialize(args['visible'])
  driver = driverInitialize(browser)

  # wdTest(driver)
  waveUpload(url, driver, args['filename'])

  driverFinalize(driver)
  displayFinalize(display)
  exit(0)

if __name__ == '__main__':
  main()
