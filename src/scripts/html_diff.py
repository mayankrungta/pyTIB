from bs4 import BeautifulSoup

import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch

import unittest


#######################
# Global Declarations
#######################



#############
# Functions
#############

def diff_html(logger,):
    filename1 = './60.html'
    filename2 = './61.html'
    if os.path.exists(filename1):
        with open(filename1, 'r+') as html_file1:
            cur_source1 = html_file1.read()
            bs1 = BeautifulSoup(cur_source1, "html.parser")
      
    if os.path.exists(filename2):
        with open(filename2, 'r+') as html_file2:
            cur_source2 = html_file2.read()
            bs2 = BeautifulSoup(cur_source2, "html.parser")

    # If body is same just return
    if(bs1.find('body') == bs2.find('body')):
        return 'SUCCESS'

    # Can do a more specific compare of the table alone
    if(bs1.find(id='basic') == bs2.find(id='basic')):
        return 'SUCCESS'

    tr_list1 = bs1.findAll('tr')
    tr_list2 = bs2.findAll('tr')
    for i in range(len(tr_list1)):        
        logger.debug('ROW:[%s]' % tr_list1[i])

        tr1 = tr_list1[i]
        tr2 = tr_list2[i]
        if (tr1 != tr2):
            logger.info("NOT SAME row[%d] [%s vs %s]" %(i, tr1,tr2))
        else:
            logger.debug("same [%s vs %s]" %(tr1,tr2))

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
    
  def test_diff(self):
    result = diff_html(self.logger)
    
    self.assertEqual('SUCCESS', result)


if __name__ == '__main__':
  unittest.main()

