import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import sys
sys.path.insert(0, '../')
from wrappers.logger import loggerFetch


#######################
# Global Declarations
#######################

browser = "Firefox"
visible = 0
logfile = "/tmp/%s_firefox_console.log"%os.environ.get('USER')
size = (width, height) = (1920, 1080)
chromedriver = '/usr/lib/chromium-browser/chromedriver'


#############
# Functions
#############

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='Script for crawling, downloading & parsing musters')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-t', '--timeout', help='Time to wait before a page loads', required=False)
  parser.add_argument('-b', '--browser', help='Specify the browser to test with', required=False)
  parser.add_argument('-u', '--url', help='Specify the url to crawl', required=False)
  parser.add_argument('-c', '--cookie-dump', help='Cookie Dump', required=False, action='store_const', const=True)

  args = vars(parser.parse_args())
  return args

def displayInitialize(isVisible=0, isDisabled=False):
  if isDisabled:
    return None
  
  if not isVisible:
    isVisible = visible
    
  from pyvirtualdisplay import Display
  
  display = Display(visible=isVisible, size=size) # size=(600, 400))
  display.start()
  return display

def displayFinalize(display):
  if not display:
    return
  
  display.stop()

def vDisplayInitialize(isVisible=0):
  from xvfbwrapper import Xvfb
  vdisplay = Xvfb()
  vdisplay.start()

  return vdisplay

def vDisplayFinalize(vdisplay):
  vdisplay.stop()

# This is not working  :( Mynk - Source: http://stackoverflow.com/questions/18182653/xvfb-browser-window-does-not-fit-display
def xDisplayInitialize(isVisible=0):
  import Xlib
  import Xlib.display

  ### Create virtual display and open the browser here ###

  dpy = Xlib.display.Display()
  root = dpy.screen().root
  geometry = root.get_geometry()
  for win in root.query_tree().children:
        win.configure(x = 0, y = 0,
                              width = geometry.width, height = geometry.height)
  dpy.sync()

  return dpy

def xDisplayFinalize(display):
  display.stop()

def driverInitialize(browser=None, path=None, timeout=None, options=None):
  if not browser:
    browser="Firefox"
  if not timeout:
    timeout=30
  if browser == "Firefox":
    if path:
      fp = webdriver.FirefoxProfile(path)
      # If you want to log into a site with save passwords DO NOT start in private mode which is default
      fp.set_preference("browser.privatebrowsing.autostart", False)
      fp.set_preference("media.autoplay.enabled", False) # If you do not want videos playing
    else:
      fp = webdriver.FirefoxProfile()
      fp.set_preference("webdriver.log.file", logfile)
      fp.native_events_enabled = False
      fp.set_preference("browser.download.folderList",2)
      fp.set_preference("browser.download.manager.showWhenStarting",False)
      fp.set_preference("browser.download.dir", os.getcwd())
      fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
      fp.set_preference("browser.privatebrowsing.autostart", False)

    # To use when downloading using a profile excel/csv, etc - e.g. googlesheets-downlaod.py  
    if False:
      fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
      fp.set_preference("browser.helperApps.alwaysAsk.force", False)
      fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
      fp.set_preference("browser.download.manager.focusWhenStarting", False)
      fp.set_preference("browser.download.manager.useWindow", False)
      fp.set_preference("browser.download.manager.showAlertOnComplete", False)
      fp.set_preference("browser.download.manager.closeWhenDone", False)
      
    # Got this working by fixing the size in xulstore.json search 'main-window' (src - https://support.mozilla.org/t5/Firefox/How-to-open-maximized/td-p/1327140)
    fp.set_preference('browser.window.width', width)
    fp.set_preference('browser.window.height', height)

    if options:
      opts = webdriver.FirefoxOptions()
      opts.add_argument(options)
      driver = webdriver.Firefox(firefox_profile=fp, options=opts)
    else:
      driver = webdriver.Firefox(firefox_profile=fp)
      
  elif browser == "PhantomJS":
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
  else:
    driver = webdriver.Chrome(chromedriver)

  driver.implicitly_wait(timeout)
  # driver.maximize_window() # Mynk is this really needed anymore? Why is FF55 causing problem still?
  driver.set_window_size(width, height)
  # print(driver.get_window_size())
    

  return driver

def driverFinalize(driver):
  driver.close()
  driver.quit()

def waitUntilID(logger, driver, id, timeout):
  '''
  A function that waits until the ID is available else times out.
  Return: The element if found by ID
  '''
  try:
    logger.info("Waiting for the page to load...")
    elem = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, id))
    )
    logger.info("...done looking")
    return elem

  except (NoSuchElementException, TimeoutException):
    logger.error("Failed to fetch the page")
    return None
  

def wdTest(driver, url=None):
  if not url:
    url = "http://www.google.com"
  driver.get(url)
  return driver.page_source

import pickle
def cookieDump(driver, filename=None):
    # login code
    cookies = driver.get_cookies()
    print("[[[%s]]]" % cookies)
    pickle.dump(cookies, open("QuoraCookies.pkl","wb"))

def cookieLoad(driver, filename=None):
    for cookie in pickle.load(open("QuoraCookies.pkl", "rb")):
        driver.add_cookie(cookie)

def runTestSuite():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))

  logger.info("BEGIN PROCESSING...")

  display = displayInitialize(args['visible'])
  driver = driverInitialize(args['browser'])
  # Mynk to use personal profile driver = driverInitialize(browser=args['browser'] , path='/home/mayank/.mozilla/firefox/4s3bttuq.default/')

  if args['cookie_dump']:
    cookieDump(driver)

  logger.info("Fetching [%s]" % driver.current_url)
  logger.info(wdTest(driver, args['url']))
  logger.info("Fetched [%s]" % driver.current_url)

  if args['cookie_dump']:
    cookieDump(driver)

  driverFinalize(driver)
  displayFinalize(display)

  '''
  display = vDisplayInitialize(visible)
  driver = driverInitialize(browser)

  logger.info(wdTest(driver))

  driverFinalize(driver)
  vDisplayFinalize(display)
  '''	

  logger.info("...END PROCESSING")     


def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
