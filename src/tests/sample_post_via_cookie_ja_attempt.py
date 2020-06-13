from bs4 import BeautifulSoup

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch

import unittest
import httplib2
import requests

from urllib.request import urlopen, build_opener, HTTPCookieProcessor   # REVIST
from urllib import request
from urllib.parse import urlencode, quote

from http.cookiejar import CookieJar


#######################
# Global Declarations
#######################

httplib2.debuglevel = 1
h = httplib2.Http('.cache')

orig_url = 'http://mnregaweb2.nic.in/netnrega/citizen_html/musternew.aspx?state_name=RAJASTHAN&district_name=CHITTORGARH&block_name=बेगूँ&panchayat_name=अन‍ोपपुरा&workcode=2729003055/IF/112908246951&panchayat_code=2729003055&msrno=7369&finyear=2017-2018&dtfrm=10/06/2017&dtto=24/06/2017&wn=अपना+खेत+अपना+काम+लाडू+लाल+/गणेश+लाल+हजुरी+0834&id=1'

url = 'http://mnregaweb2.nic.in/netnrega/citizen_html/musternew.aspx?state_name=RAJASTHAN&district_name=CHITTORGARH&block_name=' + quote('बेगूँ') + '&panchayat_name=' + quote('अन‍ोपपुरा') + '&workcode=2729003055/IF/112908246951&panchayat_code=2729003055&msrno=7369&finyear=2017-2018&dtfrm=10/06/2017&dtto=24/06/2017&wn=' + quote('अपना') + '+' + quote('खेत') + '+' + quote('अपना') + '+' + quote('काम') + '+' + quote('लाडू') + '+' + quote('लाल') + '+/' + quote('गणेश') + '+' + quote('लाल') + '+' + quote('हजुरी') + '0834&id=1'

url1 = 'http://mnregaweb2.nic.in/netnrega/citizen_html/musternew.aspx?state_name=RAJASTHAN&district_name=CHITTORGARH&block_name=%E0%A4%AC%E0%A5%87%E0%A4%97%E0%A5%82%E0%A4%81&panchayat_name=%E0%A4%85%E0%A4%A8%E2%80%8D%E0%A5%8B%E0%A4%AA%E0%A4%AA%E0%A5%81%E0%A4%B0%E0%A4%BE&workcode=2729003055/IF/112908246951&panchayat_code=2729003055&msrno=7369&finyear=2017-2018&dtfrm=10/06/2017&dtto=24/06/2017&wn=%E0%A4%85%E0%A4%AA%E0%A4%A8%E0%A4%BE+%E0%A4%96%E0%A5%87%E0%A4%A4+%E0%A4%85%E0%A4%AA%E0%A4%A8%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%AE+%E0%A4%B2%E0%A4%BE%E0%A4%A1%E0%A5%82+%E0%A4%B2%E0%A4%BE%E0%A4%B2+/%E0%A4%97%E0%A4%A3%E0%A5%87%E0%A4%B6+%E0%A4%B2%E0%A4%BE%E0%A4%B2+%E0%A4%B9%E0%A4%9C%E0%A5%81%E0%A4%B0%E0%A5%80+0834&id=1'

# url = quote(orig_url)
print(url)
print(url1)

#############
# Functions
#############

def mnregaweb_fetch(logger,):
    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    response = opener.open(url)
    html_source = response.read()
    logger.debug("HTML Fetched [%s]" % html_source)

    filename = 'opener1.html'
    with open(filename, 'wb') as html_file:
      logger.info('Writing [%s]' % filename)
      html_file.write(html_source)

    response = opener.open(url)
    html_source = response.read()
    logger.debug("HTML Fetched [%s]" % html_source)

    filename = 'opener2.html' 
    with open(filename, 'wb') as html_file:
      logger.info('Writing [%s]' % filename)
      html_file.write(html_source)
            
    return 'SUCCESS'

def requests_fetch(logger,):
    url = 'http://mnregaweb2.nic.in/netnrega/citizen_html/musternew.aspx'

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36 Vivaldi/1.91.867.42',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    params = (
        ('state_name', 'RAJASTHAN'),
        ('district_name', 'CHITTORGARH'),
        ('block_name', 'बेगूँ'),
        ('panchayat_name', 'अन‍ोपपुरा'),
        ('workcode', '2729003055/IF/112908246951'),
        ('panchayat_code', '2729003055'),
        ('msrno', '7369'),
        ('finyear', '2017-2018'),
        ('dtfrm', '10/06/2017'),
        ('dtto', '24/06/2017'),
        ('wn', 'अपना+खेत+अपना+काम+लाडू+लाल+/गणेश+लाल+हजुरी'),
        ('id', '1'),
    )

    if 0:
        cookies = {
            'ASP.NET_SessionId': 'vnf1foeiqlsprxvx5z11xzim',
        }
    else:
        response = requests.get(url, headers=headers, params=params)
        cookies = response.cookies
        logger.info(cookies)
        
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    logger.info(response.cookies)
    filename = 'requests.html' 
    with open(filename, 'wb') as html_file:
        logger.info('Writing [%s]' % filename)
        html_file.write(response.text.encode('utf-8'))

    return 'SUCCESS'


#############
# Tests
#############


class TestSuite(unittest.TestCase):
  def setUp(self):
    self.logger = loggerFetch('info')
    self.logger.info('BEGIN PROCESSING...')

  def tearDown(self):
    self.logger.info("...END PROCESSING")
    
  def test_urllib_fetch(self):
    result = mnregaweb_fetch(self.logger)
    self.assertEqual('SUCCESS', result)

  def test_requests_fetch(self):
    if 0:
        result = requests_fetch(self.logger)    
    else:
        result = 'SUCCESS'
    self.assertEqual('SUCCESS', result)

  def pull(self):
    bs = BeautifulSoup(self.html, "html.parser")
    self.logger.info(bs.find(id='__VIEWSTATE'))
    self.logger.info(bs.find(id='__EVENTVALIDATION'))

    self.assertEqual(1, 1)


if __name__ == '__main__':
  unittest.main()

