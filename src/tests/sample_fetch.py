from bs4 import BeautifulSoup

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize,waitUntilID # ,cookieDump,cookieLoad
from wrappers.db import dbInitialize,dbFinalize


#######################
# Global Declarations
#######################

url = "http://164.100.112.66/netnrega/Citizen_html/Musternew.aspx?id=2&lflag=eng&ExeL=GP&fin_year=2015-2016&state_code=33&district_code=3305&block_code=3305007&panchayat_code=3305007038&State_name=CHHATTISGARH&District_name=SURGUJA&Block_name=BATAULI&panchayat_name=Govindpur"

state_code = '36'
district_code = '14'
block_code = '057'

state_name = ''
disttict_name = ''
block_name = 'Ghattu'


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
  parser.add_argument('-d', '--directory', help='Specify directory to download html file to', required=False)
  parser.add_argument('-q', '--query', help='Query to specify the workset, E.g ... where id=147', required=False)
  parser.add_argument('-j', '--jobcard', help='Specify the jobcard to download/push', required=False)
  parser.add_argument('-c', '--crawl', help='Crawl the Disbursement Data', required=False)
  parser.add_argument('-f', '--fetch', help='Fetch the Jobcard Details', required=False)
  parser.add_argument('-p', '--parse', help='Parse Jobcard HTML for Muster Info', required=False, action='store_const', const=True)
  parser.add_argument('-r', '--process', help='Process downloaded HTML files for Muster Info', required=False, action='store_const', const=True)
  parser.add_argument('-P', '--push', help='Push Muster Info into the DB on the go', required=False, action='store_const', const=True)
  parser.add_argument('-J', '--jobcard-details', help='Fetch the Jobcard Details for DB jobcardDetails table', required=False, action='store_const', const=True)

  args = vars(parser.parse_args())
  return args


def fetchMusterDetails(logger, db, cmd=None, directory=None, url=None, is_parse_info=None, is_push_info=None, is_visible=None):
  '''
  Fetch the Muster Details for specified parameters in the specified directory
  '''
  if not cmd:
    cmd="FETCH MUSTER DETAILS"
  logger.info("BEGIN %s..." % cmd)
    
  if not directory:
    directory = "./Downloads"

  if not url:
    url = 'http://khadya.cg.nic.in/pdsonline/cgfsa/Report/SSRS_Reports/RptMonthWiseDeleteRestoreNew_RC.aspx'
    url = 'http://164.100.112.66/netnrega/Citizen_html/Musternew.aspx?id=2&lflag=eng&ExeL=GP&fin_year=2015-2016&state_code=33&district_code=3305&block_code=3305007&panchayat_code=3305007038&State_name=CHHATTISGARH&District_name=SURGUJA&Block_name=BATAULI&panchayat_name=Govindpur'
    
  if not is_visible:
    is_visible = 0        # Set to 1 for debugging selenium

  if not is_parse_info:
    is_parse_info = False

  if not is_push_info:
    is_push_info = False

  # The part below could be moved to a function downloadMusterDetails() to make it reusable
  filename = directory + '/' + 'test.html' # Use your naming logic + blockName + '_' + panchayat + '_' + shopCode + '.html'
  logger.info('filename[%s]' % filename)
  
  filepath = os.path.dirname(filename)
  if not os.path.exists(filepath):
    logger.info('Creating direcotry [%s] as it does not exist' % filepath)
    os.makedirs(filepath)

  display = displayInitialize(is_visible)
  driver = driverInitialize()

  logger.error("Current URL [%s] Title [%s]" % (driver.current_url, driver.title))
  # cookieDump(driver)
  # driver.delete_all_cookies()
  logger.error("Current URL [%s] Title [%s]" % (driver.current_url, driver.title))
  logger.info("Fetching...[%s]" % url)
  driver.get(url)

  logger.error("Current URL [%s] Title [%s]" % (driver.current_url, driver.title))

  # cookieDump(driver)
  # Use double refresh if need be like in AP sites
  if False:
    logger.info("Refreshing...[%s]" % url)
    driver.get(url)    # A double refresh required for the page to load
  logger.error("Current URL [%s] Title [%s]" % (driver.current_url, driver.title))
    
  # cookieDump(driver)
  el = waitUntilID(logger, driver, 'ctl00_ContentPlaceHolder1_ddlwork', 10) 
  if el:
    #el = driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlwork')
    logger.info("Found El[%s]" % str(el))
    html_source = driver.page_source.replace('<head>',
                                           '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
    logger.debug("HTML Fetched [%s]" % html_source)
    # cookieDump(driver)

    with open(filename, "wb") as html_file:
      logger.info("Writing [%s]" % filename)
      html_file.write(html_source.encode('UTF-8'))
  else:
    logger.error("Failed to fetch the page [%s]" % driver.current_url)
    logger.error("Current URL [%s] Title [%s]" % (driver.current_url, driver.title))    
    # cookieDump(driver)
    html_source = driver.page_source
    logger.info("HTML Fetched [%s]" % html_source)

    with open(filename, "wb") as html_file:
      logger.info("Writing [%s]" % filename)
      html_file.write(html_source.encode('UTF-8'))
    
    driverFinalize(driver)
    displayFinalize(display)
    return # Error condition to be dealt with

    
  '''  
  try:
    logger.info("Waiting for the page to load...")
    elem = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_ddlwork'))
    )
    logger.info("...done looking")

  except (NoSuchElementException, TimeoutException):
    logger.error("Failed to fetch the page")
    driverFinalize(driver)
    displayFinalize(display)
    return # Error condition to be dealt with

  finally:
    html_source = driver.page_source.replace('<head>',
                                           '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
    logger.debug("HTML Fetched [%s]" % html_source)

    with open(filename, "wb") as html_file:
      logger.info("Writing [%s]" % filename)
      html_file.write(html_source.encode('UTF-8'))
  '''
  
  # If you have information to parse using Beautiful Soup
  if is_parse_info:
    bs = BeautifulSoup(html_source, "html.parser")
    tr_list = bs.findAll('tr', attrs={'class':['normalRow', 'alternateRow']})
    logger.debug(str(tr_list))
    for tr in tr_list:
      td = tr.find('td')
      td = td.findNext('td')
      panchayat = td.text.strip()
      logger.info("Panchayat[%s]", panchayat)
      elem = driver.find_element_by_link_text(panchayat)
      elem.click()
      filename="/tmp/%s.html" % panchayat
      with open(filename, 'w') as html_file:
        logger.info("Writing [%s]" % filename)
        html_file.write(driver.page_source)
        driver.back()
  
  driverFinalize(driver)
  displayFinalize(display)


  # If you want to push the information to the Database
  if is_push_info:  
    query = 'select j.jobcard, p.name, p.panchayatCode from jobcardRegister j, panchayats p, blocks b where j.blockCode=p.blockCode and j.panchayatCode=p.panchayatCode  and j.blockCode=b.blockCode and j.jobcard="%s"' % jobcard
    logger.info("Command[%s] Directory[%s] URL[%s] jobcard[%s]" % (cmd, dir, url, jobcard))
    pushInfoIntoDB(logger, db, "POPULATE_DATABASE", dir, url, is_visible, is_push_info, query) # So that function can be shared

  logger.info("...END %s" % cmd)     


def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))

  logger.info("BEGIN PROCESSING...")

  db = dbInitialize(db="surguja", charset="utf8")  # The rest is updated automatically in the function

  if args['fetch']:
    # For fetch where only download push and parse options can be ignored
    fetchMusterDetails(logger, db, "FETCH MUSTER DETAILS", args['directory'], args['url'], args['parse'], args['push'], args['visible'])
  elif args['parse']:
    # parseDownloadedMuster(logger, db, "PARSE JOBCARDS", args['directory'], args['url'], )
    logger.info("Requested Parse")  # If you are splitting download and parse logic
    fetchMusterDetails(logger, db, "PARSE MUSTER DETAILS", args['directory'], args['url'], args['parse'], args['push'], args['visible'])
  else:
    logger.info("Default fetch which includes download, parse & populate")  # Controlled by options
    fetchMusterDetails(logger, db, "FETCH MUSTER DETAILS", args['directory'], args['url'], args['parse'], args['push'], args['visible'])
    
  dbFinalize(db) # Make sure you put this if there are other exit paths or errors

  logger.info("...END PROCESSING")     
  exit(0)

if __name__ == '__main__':
  main()
