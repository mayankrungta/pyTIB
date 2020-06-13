from bs4 import BeautifulSoup
import multiprocessing, time
import csv
import requests
import os
import os.path
import time
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
fileDir=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, fileDir+'/../includes/')
print(fileDir+'/../includes/')
sys.path.insert(0, fileDir+'/../')
print(fileDir+'/../')
#sys.path.insert(0, rootdir)
import datetime
from wrappers.logger import loggerFetch
from wrappers.db import dbInitialize,dbFinalize
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize,waitUntilID

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='Script for crawling, downloading & parsing Jobcards')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-b', '--browser', help='Specify the browser to test with', required=False)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)

  args = vars(parser.parse_args())
  return args

def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))
  logger.info("BEGIN PROCESSING...")

  display = displayInitialize(args['visible'])
  driver = driverInitialize(browser=args['browser'] , path='/home/mayank/.mozilla/firefox/4s3bttuq.default/')
  base_url="https://www.skillshare.com/login"
  driver.get(base_url)
  logger.info('Fetching URL[%s]' % base_url)
  # driver.find_element_by_link_text("Sign In").click()
  try:
    driver.find_element_by_name("LoginForm[email]").clear()
    driver.find_element_by_name("LoginForm[email]").send_keys("anupreet@anupreet.com")
    driver.find_element_by_name("LoginForm[password]").clear()
    # driver.find_element_by_name("LoginForm[password]").send_keys("#######")
    # driver.find_element_by_xpath("//input[@value='Sign In']").click()
    time.sleep(100) # If you want to manually log in
  except Exception as e:
    logger.info('Already signed in [%s]', e)
  time.sleep(10)

  filename = "./z.csv"
  content = csv.reader(open(filename, 'r'), delimiter=',', quotechar='"')
  for (title, url) in content:    
    # driver.get('https://www.skillshare.com/classes/Sketchbook-Practice-Bring-watercolour-to-Life-with-Line-Drawing/1053382271/classroom/discuss')
    logger.info('Fetching URL[%s]' % url)
    driver.get(url)
    time.sleep(10)

    escaped_title = re.sub(r"[^A-Za-z 0-9]+", '', title).replace(' ', '_')
    dirname = 'SkillsShare/' + escaped_title
    cmd = 'mkdir -p ' + dirname
    logger.info(cmd)
    os.system(cmd)    

    els = driver.find_elements_by_class_name("session-item")
    
    for i, el in enumerate(els):
      logger.debug(str(el))
      bs = BeautifulSoup(el.get_attribute('innerHTML'), "html.parser")
      p = bs.find('p')
      name = p.text
      name = "%02d" % (i+1) + '_' + re.sub(r"[^A-Za-z 0-9]+", '', name).replace(' ', '_') + '.mp4'
      
      logger.info(str(p) + name)
      el.click()
      time.sleep(10)
      html_source = driver.page_source

      bs = BeautifulSoup(html_source, "html.parser")
      html = bs.findAll('video', attrs={'class':['vjs-tech']})
      str_html = str(html)
      logger.info(str_html)
      url = str_html[str_html.find("src=")+5:]
      fetch_url = url[:url.find("?pubId")]
      logger.info(fetch_url)

      if os.path.exists(dirname + '/' + name):
        continue
      cmd = 'cd %s && curl -s %s -o %s' % (dirname, fetch_url, name)
      logger.info(cmd)
      # os.system(cmd)

  driverFinalize(driver)
  displayFinalize(display)
  logger.info("...END PROCESSING")     
  exit(0)

if __name__ == '__main__':
  main()
