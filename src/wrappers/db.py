import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

if sys.version_info[0] > 2:
  import pymysql
  pymysql.install_as_MySQLdb()
import MySQLdb

from wrappers.logger import loggerFetch
from includes.settings import dbhost,dbuser,dbpasswd


#######################
# Global Declarations
#######################


#############
# Functions
#############

def dbInitialize(host=dbhost, user=dbuser, passwd=dbpasswd, db="libtech", charset=None):
  '''
  Connect to MySQL Database
  '''
  db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)
  db.autocommit(True)
  return db;

def dbFinalize(db):
  db.close()


def runTestSuite():
  logger = loggerFetch("info")
  logger.info("BEGIN PROCESSING...")

  db = dbInitialize(db="surguja", charset="utf8")

  cur = db.cursor()
  cur.execute("SET NAMES utf8")

  jobcard = 'CH-05-005-015-001/187'
  query = 'select headOfFamily from jobcardRegister where jobcard="' + jobcard + '"'
  logger.info("query[%s]" % query)
  cur.execute(query)
  head = cur.fetchall()[0][0]
  logger.info("HeadOfFamily[%s]" % head)
  
  query = 'select applicantName, accountNo from jobcardDetails where jobcard="' + jobcard + '"'
  logger.info("query[%s]" % query)
  cur.execute(query)
  names = cur.fetchall()
  #print names.encode('UTF-8')
  logger.info("Names[%s]" % str(names).encode('UTF-8'))
  
  dbFinalize(db)
  logger.info("...END PROCESSING")     
  
    
def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
