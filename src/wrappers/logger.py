import logging

#######################
# Global Declarations
#######################

logFile = __file__+'.log'
logLevel = "info" # logging.ERROR
logFormat = '%(asctime)s:[%(name)s|%(module)s|%(funcName)s|%(lineno)s|%(levelname)s]: %(message)s' #  %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s"

#############
# Functions
#############

'''
def logInitialize():
  logging.basicConfig(filename=logFile, level=logLevel, format=logFormat) # Mynk
  logging.basicConfig(
    filename = fileName,
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)

def logFinalize():
  logging.shutdown()
  
'''

def loggerSetLevel(logger, level):
  numeric_level = getattr(logging, level.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % level)
  else:
    logger.setLevel(numeric_level)

def logger_fetch(level=None):
  return loggerFetch(level)
    
def loggerFetch(level=None):
  logger = logging.getLogger(__name__)

  if not level:
    level = logLevel

  if level:
    loggerSetLevel(logger=logger, level=level)

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

def runTestSuite():
  logger = loggerFetch(logLevel) # Test Info
  loggerTest(logger)
    
def main():
  runTestSuite()
  exit(0)

if __name__ == '__main__':
  main()
