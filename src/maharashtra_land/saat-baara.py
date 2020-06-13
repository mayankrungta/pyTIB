from bs4 import BeautifulSoup

import time
import csv
import json
import ast

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
from wrappers.sn import driverInitialize,driverFinalize,displayInitialize,displayFinalize

from selenium.webdriver.support.ui import Select

#######################
# Global Declarations
#######################

timeout = 10

url = "https://mahabhulekh.maharashtra.gov.in/"
filename = 'z.html'

dc = "32"
did = "32"
dn = "रत्नागिरी"
surveyno = "21"
gat = "100"
sno = gat + "/" + surveyno
tc = "3"
tid = "3"
tn = "खेड"
vid = "273200030399810000"
vn = "वावे तर्फे खेड"
vn = "सार्पिली"

cmd = '''curl 'https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx/getSnos' -X POST -H 'Accept: application/json, text/plain, */*' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Content-Length: 60' -H 'Content-Type: application/json;charset=utf-8' -H 'Cookie: ASP.NET_SessionId=xgahrcwef0hoicteddbwrxxo' -H 'Host: mahabhulekh.maharashtra.gov.in' -H 'Referer: https://mahabhulekh.maharashtra.gov.in/Konkan/Home.aspx' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' -d "{'ptxt':'%s','vid':'273200030399810000','did':'32','tid':'3'}" -o %s.json ''' % (gat, gat)

gat_list = [ 1, 2, 3, 4, 5, 6, 7, 13, 21, 23, 25, 26, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 72, 86, 91, 92, 93, 94, 95, 96, 97, 98, 105, 128, 129, 143, 149, 150, 151, 152, 153, 154, 155, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 175, 176, 177, 178, 179, 180, 182, 186, 188, 191, 192, 193, 194, 196, 197, 198, ]

gat_list = range(1, 911)
gat_list = [44, 124, 125, 220]
gat_list.extend(range(396, 419))
print('#### %s #####' % gat_list)

#############
# Functions
#############

def runTestSuite():
  logger = loggerFetch("info")
  logger.info("BEGIN PROCESSING...")
  
  display = displayInitialize(1)
  driver = driverInitialize()

  '''
  content = csv.reader(open('./gats.csv', 'r'), delimiter=',', quotechar='"')
  for (gat, d) in content:
  '''
  
  for gat in gat_list:
    logger.info('Fetching gat[%s]...' % gat)

    driver.get(url)
    try:
      driver.find_element_by_xpath("//form[@id='aspnetForm']/div[3]/div/div/div[3]/a[3]/p").click()
    except:
      logger.error('Cant find element for [%s]' % gat)
      continue

    Select(driver.find_element_by_id("distSelect")).select_by_visible_text(dn)
    Select(driver.find_element_by_id("talSelect")).select_by_visible_text(tn)
    Select(driver.find_element_by_id("vilSelect")).select_by_visible_text(vn)
    # Select(driver.find_element_by_id("vilSelect")).select_by_visible_text(u"सार्पिली")
    # driver.find_element_by_css_selector("option[value=\"string:273200030399810000\"]").click()
    driver.find_element_by_id("rbsryno").click()
    driver.find_element_by_xpath("//input[@type='number']").clear()
    driver.find_element_by_xpath("//input[@type='number']").send_keys(gat)
    driver.find_element_by_css_selector("input[type=\"button\"]").click()

    '''
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    
    try:
      WebDriverWait(driver, 5).until(EC.alert_is_present(), 'Waiting for alert timed out')

      alert = driver.switch_to_alert()
      alert.accept()
      logger.warning("alert accepted")

    except:
      logger.info("Yippie!")    
    '''
    if len(driver.window_handles) > 1:
      logger.info("Dialog Box Window [" + str(driver.window_handles) + "]")
      # self.assertEqual(u"सर्वे नंबर / गट नंबर तपासुन पहा.", self.close_alert_and_get_its_text())
      # driver.find_element_by_xpath("//div[@id='block-desktop']/div[3]/div[2]/div").click()
      driver.switch_to_alert().accept()
      continue
    
    html_source = driver.page_source.replace('<head>',
                                             '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')

    logger.debug("HTML Fetched [%s]" % html_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #dict_from_json = soup.find(attribute).text
    sno_select = soup.find("select", {"ng-model" : "selectedSno"}) # ng-model="selectedSno"
    sno_options = sno_select.findAll("option")
    snos = [ sno_option.text for sno_option in sno_options ]
    logger.debug("Found [%s]" % str(snos))
    snos = snos[1:]
    logger.info("SNO List [%s]" % str(snos))

    #time.sleep(5)
    for sno in snos:
      logger.info('Processing [%s]' % sno)
      filename = '/home/mayank/wd/SaatBaara/remaining/%s.html' % sno.replace('/','_')
      if os.path.exists(filename):
        #time.sleep(1)
        continue
      Select(driver.find_element_by_xpath("//form[@id='aspnetForm']/div[3]/div/div/div[3]/div/div[3]/table/tbody/tr[3]/td/select")).select_by_visible_text(sno)
      #logger.info(driver.find_element_by_link_text(sno))
      driver.find_element_by_css_selector("td.last-rows > input[type=\"button\"]").click()
      time.sleep(5)
      
      parent_handle = driver.current_window_handle
      logger.info("Handles : %s Number : %s" % (driver.window_handles, len(driver.window_handles)))
  
      if len(driver.window_handles) == 2:
        driver.switch_to_window(driver.window_handles[-1])
      else:
        logger.error("Handlers gone wrong [" + str(driver.window_handles) + "]")
        driver.save_screenshot('z.png')

      html_source = driver.page_source.replace('<head>',
                                               '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>').encode('utf-8')

      logger.debug("HTML Fetched [%s]" % html_source)
      if(driver.title != '७/१२'):
        logger.error(driver.title)
        driver.close()
        driver.switch_to_window(parent_handle)
        continue
        
      bs = BeautifulSoup(html_source, "html.parser")
      body = bs.find('tbody')
      try:
        body = body.findNext('tbody')
      except:
        logger.error('Empty body for [%s]' % sno)
        driver.close()
        driver.switch_to_window(parent_handle)
        continue
      body = body.findNext('tbody')
      logger.debug(body)
      td = body.find('td')
      td = td.findAll('td')
  
      logger.info("Checking [%s]" % td[2].text)
      if(sno != td[2].text):
        logger.error('sno[%s] != td.text[%s]' % (sno, td[2].text))
        driver.close()
        driver.switch_to_window(parent_handle)
        continue
  
      with open(filename, 'wb') as html_file:
        logger.info('Writing [%s]' % filename)
        html_file.write(html_source)
    
      driver.close()
      driver.switch_to_window(parent_handle)
      time.sleep(1)
    time.sleep(1)

  driverFinalize(driver)
  displayFinalize(display)


  logger.info("...END PROCESSING")     


def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
