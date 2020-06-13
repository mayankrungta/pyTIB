from bs4 import BeautifulSoup

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize


#######################
# Global Declarations
#######################

timeout = 10

url = "http://www.nrega.telangana.gov.in/Nregs/FrontServlet?requestType=SmartCardreport_engRH&actionVal=debitLoagReport&id=1457@DOP$APOL&type=01/04/2015&listType="


#############
# Functions
#############


def runTestSuite():
  logger = loggerFetch("info")
  logger.info("BEGIN PROCESSING...")

  display = displayInitialize(1)
  driver = driverInitialize(path='/opt/firefox/')

  driver.get(url)
  logger.info("Fetching...[%s]" % url)
  
  driver.get(url)    # A double refresh required for the page to load
  logger.info("Refreshing...[%s]" % url)
  
  html_source = driver.page_source.replace('<head>',
                                           '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
  logger.debug("HTML Fetched [%s]" % html_source)

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
    with open(filename, 'wb') as html_file:
      logger.info("Writing [%s]" % filename)
      html_file.write(driver.page_source.encode('utf-8'))

    driver.back()

  driverFinalize(driver)
  displayFinalize(display)


  logger.info("...END PROCESSING")     


def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
