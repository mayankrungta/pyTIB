import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
#from includes.settings import dbhost,dbuser,dbpasswd
from wrappers.db import dbInitialize, dbFinalize

import unittest
import json

#######################
# Global Declarations
#######################
filename = 'z.json'

#############
# Functions
#############

def fetchindict(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

def sql2json(logger,):
  db = dbInitialize(db="surguja", charset="utf8")

  query = 'select id, panchayatName, name, jobcard, musterNo, workCode, accountNo, bankNameOrPOName, musterStatus from workDetails limit 10'
  cur = db.cursor()
  cur.execute(query)
  res = fetchindict(cur)
  logger.info("Converting query[%s]" % query)
  #data = str(res[0]).encode('utf-8')
  data = res
  logger.info("Data[%s]" % data)

  '''
  with open(filename, 'wb') as outfile:
      logger.info('Writing to file[%s]' % filename)
      outfile.write(res)
  '''

  with open(filename, 'w') as outfile:
    logger.info('Writing to file[%s]' % filename)
    json.dump(data, outfile, ensure_ascii=False, indent=4)
      
  dbFinalize(db)

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
    
  def test_sql2json(self):
    result = sql2json(self.logger)
    
    self.assertEqual('SUCCESS', result)


if __name__ == '__main__':
  unittest.main()

