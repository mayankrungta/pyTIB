import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from wrappers.logger import loggerFetch
import unittest
import pandas as pd

#######################
# Global Declarations
#######################


#############
# Functions
#############


def csv2json(logger, filename=None):
    # data = fetchindict(csv.reader(filename))
    df = pd.read_csv(filename)

    # logger.info("Data[%s]" % df.to_json(orient='records'))
    # exit(0)

    filename = filename.replace('.csv', '.json')
    with open(filename, 'w') as outfile:
        logger.info('Writing to file[%s]' % filename)
        #json.dump(df.to_json(orient='records'), outfile, ensure_ascii=False, indent=4)
        outfile.write(df.to_json(orient='records'))

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
      
    def test_csv2json(self):
        result = csv2json(self.logger, 'trial_data.csv')    
        self.assertEqual('SUCCESS', result)


if __name__ == '__main__':
    unittest.main()

