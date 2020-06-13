import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

#from os import errno

#import time
import unittest

import pandas as pd
#import xlsxwriter

from wrappers.logger import loggerFetch

###


#######################
# Global Declarations
#######################

#timeout = 10


#############
# Functions
#############


def appify(logger, dirname=None):
    if not dirname:
        dirname = 'jcs'

    logger.info('Concat CSVs in [%s]' % dirname)
    
    count = 0
    for basename in os.listdir(dirname):
        filename=os.path.join(dirname,basename)
        logger.info('Reading [%s]' % filename)
        if 'sample' not in filename:
            logger.info('Skipping [%s]' % filename)
            continue
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig')
        except Exception as e:
            logger.error('Exception when reading filename[%s] - EXCEPT[%s:%s]' % (filename, type(e), e))

        df_array = []
        sorted = df.sort_values(by='WorkerID')
        sorted['WorkerID'].to_csv(filename.replace('list', 'workers'), index=False)
        df_array.append(sorted['WorkerID'])
        
        sorted = df.sort_values(by='जॉब कार्ड')
        sorted['जॉब कार्ड'].drop_duplicates().to_csv(filename.replace('list', 'jobcards'), index=False)
        df_array.append(sorted['जॉब कार्ड'].drop_duplicates())

        sorted = df.sort_values(by='गांव')                               
        sorted['गांव'].drop_duplicates().to_csv(filename.replace('list', 'villages'), index=False)
        df_array.append(sorted['गांव'].drop_duplicates())
        
        concat = pd.concat(df_array)
        logger.info('Concatenated: \n%s' % concat.head())
        concat.to_csv(filename.replace('list', 'all'), index=False)
    
    return 'SUCCESS'
    

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = loggerFetch('info')
        self.logger.info('BEGIN PROCESSING...')

    def tearDown(self):
        self.logger.info('...END PROCESSING')

    def test_appify(self):
        dirname = '/Users/mayank/Downloads/Dewata'
        result = appify(self.logger, dirname=dirname)
        self.assertEqual(result, 'SUCCESS')
        
if __name__ == '__main__':
    unittest.main()
