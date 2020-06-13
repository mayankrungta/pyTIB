#! /usr/bin/env python

#This code will get the Oabcgatat Banes
import os
import csv
from bs4 import BeautifulSoup, Tag

import logging
import MySQLdb
import time
import re


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
  #  parser.add_argument('-j', '--jobcard-number', help='Specify the jobcard no to fetch', required=True)
  #  parser.add_argument('-m', '--mobile-number', help='Specify the mobile number', required=True)
  #  parser.add_argument('-i', '--missed-call-id', help='Specify the ID of missed call', required=True)
  parser.add_argument('-d', '--directory', help='Specify directory to write xml file to', required=False)
  parser.add_argument('-c', '--csv', help='Specify the CSV file to convert', required=True)
  parser.add_argument('-x', '--xml', help='Specify the XML file to convert to', required=False)

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

  

def preText():
  '''
  Prefixing to the XML file
  '''
  text = '''<?xml version="1.0"?>
<chaupal>
'''
  return text


def addressBookEntry(ab_entry):
  '''
  For adding the Address Book Entry
  '''
  entry ='''
  <addressbookEntry>
    <formType>addressbookEntry</formType>
    <block>block_name</block>
    <panchayat>panchayat_name</panchayat>
    <jobcard>jobcard_number</jobcard>
    <phone>phone_number</phone>
    <pdsno>pds_number</pdsno>
  </addressbookEntry>
'''
  return xmlUpdate(entry, ab_entry)


def postText():
  '''
  Suffixing to the html file script
  '''
  text = '''
</chaupal>
'''
  return text

def xmlUpdate(entry, ab_entry):
  '''
  Returns the ASCII decoded version of the given HTML string. This does
  NOT remove normal HTML tags like <p>.
  '''

  (block, panchayat, jobcard, phone) = ab_entry

  entry = entry.replace("block_name", str(block))
  entry = entry.replace("panchayat_name", str(panchayat))
  entry = entry.replace("jobcard_number", str(jobcard))
  entry = entry.replace("phone_number", str(phone))
  
  return entry

def list2xml(logger, addressbook, dir=None, xml_file=None):
  '''
  Convert the list to xml
  '''
  logger.info("Directory[%s] XML[%s]" % (dir, xml_file))

  if dir == None:
    dir = "."
    
  filename = dir + '/' + xml_file

  xml_text = preText()

  for ab_entry in addressbook:
    (block, panchayat, jobcard, phone) = ab_entry
    logger.info("block[%s], panchayat[%s], jobcard[%s], phone[%s]" % (block, panchayat, jobcard, phone))

    xml_entry = addressBookEntry(ab_entry)
    xml_text += xml_entry

    
  xml_text += postText()


  with open(filename, 'w') as xml_file:
    xml_file.write(xml_text)
    logger.info("Written file [%s]" % filename)
    logger.debug("File content [%s]" % xml_text)


def csv2xml(logger, dir=None, csv_file=None, xml_file=None):
  '''
  Convert the CSV file to XML file
  '''

  logger.info("BEGIN PROCESSING...")

  if xml_file == None:
    xml_file = csv_file.replace("csv", "xml")

  logger.info("dir[%s]" % dir)
  logger.info("csv[%s]" % csv_file)
  logger.info("xml[%s]" % xml_file)

  with open(csv_file, "r") as csv_handle:
    addressbook = list(csv.reader(csv_handle))

  logger.debug("addressbook[%s]" % str(addressbook))
  list2xml(logger, addressbook, dir, xml_file)

  logger.info("...END PROCESSING")
  

def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))

  outdir = args['directory']
  csv_file = args['csv']
  
  csv2xml(logger, outdir, csv_file, args['xml'])

  exit(0)

if __name__ == '__main__':
  main()
