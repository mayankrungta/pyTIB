#! /usr/bin/env python

import os
import logging
import MySQLdb

import requests
import xml.etree.ElementTree as ET



#######################
# Global Declarations
#######################

logFile = __file__+'.log'
logLevel = logging.ERROR
logFormat = '%(asctime)s:[%(name)s|%(module)s|%(funcName)s|%(lineno)s|%(levelname)s]: %(message)s' #  %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s"


#############
# Functions
#############

'''
def logInitialize():
  import logging
  logging.basicConfig(filename=logFile, level=logLevel, format=logFormat) # Mynk
  logging.basicConfig(
    filename = fileName,
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)
'''

def loggerFetch(level=None):
  logger = logging.getLogger(__name__)

  if level:
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % level)
    else:
      logger.setLevel(numeric_level)
  else:
    logger.setLevel(logLevel)

  # create console handler and set level to debug
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)    # Mynk ???

  # create formatter e.g - FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
  formatter = logging.Formatter(logFormat)

  # add formatter to ch
  ch.setFormatter(formatter)

  # add ch to logger
  logger.addHandler(ch)

  return logger

def loggerTest(logger):
  logger.debug('debug message')
  logger.info('info message')
  logger.warn('warn message')
  logger.error('error message')
  logger.critical('critical message')
    

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
  parser.add_argument('-d', '--directory', help='Specify directory to download html file to', required=False)
  parser.add_argument('-q', '--query', help='Query to specify the workset, E.g ... where id=147', required=False)

  args = vars(parser.parse_args())
  return args

def parserFinalize(parser):
  parser.close()

def dbInitialize(host="localhost", user="root", passwd="root123", db="libtech"):
  '''
  Connect to MySQL Database
  '''
  db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
  db.autocommit(True)
  return db;

def dbFinalize(db):
  db.close()


def exotelFetch(logger, query=None):
  '''
  Process any missed calls in the libtech DB
  '''
  logger.info("BEGIN PROCESSING...")

  sid = 'ngopost'
  token = 'd6c9d2927b6b06501f53aaf141a9a76604eb4162'

  db = dbInitialize(host="localhost", user="libtech", passwd="lt123", db="libtech")
  cur = db.cursor()

  if query == None:
    addressbook = ('addressbook', 'anekapalli_ab', 'apvvuVG_ab', 'chakri_ab', 'chattis_ab', 'ghattu_ab', 'rscd_ab')
    query = ' union '.join(['select phone from ' + ab for ab in addressbook])
    
  logger.info("query[%s]" % query)
           
  cur.execute(query)
  mobile_numbers = cur.fetchall()
  logger.debug("mobile_numbers[%s]" % str(mobile_numbers))

  # Enable if you want to ignore already fetched numbers
  if False:
    query = 'select PhoneNumber from exotelDetails'
    cur.execute(query)
    stored_numbers = cur.fetchall()

    logger.info("mobile_numbers[%d]" % len(str(mobile_numbers)))
    logger.info("stored_numbers[%d]" % len(str(stored_numbers)))
    logger.info("mobile_numbers[%s]" % set(mobile_numbers))    
    mobile_numbers = list(set(mobile_numbers) - set(stored_numbers))
#    logger.info("mobile_numbers[%s]" % str(stored_numbers))    
    logger.info("mobile_numbers[%s]" % str(mobile_numbers))
  
  for row in mobile_numbers:
    #Put error checks in place and only then update libtech DB

    mobile = row[0]
    logger.info("Mobile[%s]" % mobile)

    # Example url='https://ngopost:d6c9d2927b6b06501f53aaf141a9a76604eb4162@twilix.exotel.in/v1/Accounts/ngopost/Numbers/9916766748'
    url = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Numbers/%s' % (sid, token, sid, mobile)
    logger.info("Fetching URL[%s]" % url)

    r = requests.get(url)
    logger.debug(r.content)

    root = ET.fromstring(r.content)

    logger.debug("Tag[%s] Attribs[%s]" %(root.tag, root.attrib))

    for number in root.findall('Numbers'):
      PhoneNumber = number.find('PhoneNumber').text
      Circle = number.find('Circle').text
      CircleName = number.find('CircleName').text
      Type = number.find('Type').text
      Operator = number.find('Operator').text
      OperatorName = number.find('OperatorName').text
      DND = number.find('DND').text

      # assert(PhoneNumber[1:] == mobile)
      logger.info("PhoneNumber[%s] == Mobile[0%s]" % (PhoneNumber, mobile))
      PhoneNumber = mobile      # Mynk
      
      litExotelDetails = '(PhoneNumber, Circle, CircleName, Type, Operator, OperatorName, DND)'
      ExotelDetails = (PhoneNumber, Circle, CircleName, Type, Operator, OperatorName, DND)
      logger.info('ExotelDetails: \n \t PhoneNumber[%s] \n \t Circle[%s] \n \t CircleName[%s] \n \t Type[%s] \n \t Operator[%s] \n \t OperatorName[%s] \n \t DND[%s]' % ExotelDetails) 

      query = 'insert into exotelDetails %s' % litExotelDetails + ' values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % ExotelDetails
      logger.info("query[%s]" % query)
      try:    
        cur = db.cursor()
        cur.execute(query)
      except Exception as e:
        logger.error("Query failed with exception[%s]" % e)

  dbFinalize(db)
  logger.info("...END PROCESSING")
  

def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))
  
  exotelFetch(logger, args['query'])

  exit(0)

if __name__ == '__main__':
  main()
