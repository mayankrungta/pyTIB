from __future__ import print_function
import httplib2
import os
import unittest

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

from time import strftime

from wrappers.db import dbInitialize, dbFinalize
from wrappers.logger import loggerFetch

#######################
# Global Declarations
#######################

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets' # .readonly'
CLIENT_SECRET_FILE = '~/.credentials/client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


#############
# Functions
#############

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def download_googlesheet(logger, db, region, spreadsheet_id, revision):
    """ To sync our DB with the corresponding Google Sheet
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    logger.debug(values)

    if not values:
        logger.info('No data found.')
    else:
        # See the column names below for reference
        logger.debug('phone, name, district, block, panchayat, designation, gender, total_calls, success_percentage, updated, cost')
        for row in values:
            ncols = len(row)
            logger.debug("RowCount[%d]" % ncols)
            logger.debug(row)

            if row[0] == 'phone':
                row.append('updated')
                row.append('cost')
                continue
            else:
                while ncols < 11:
                    row.append('')
                    ncols += 1
            logger.debug(row)

            (phone, name, district, block, panchayat, designation, gender, total_calls, success_percentage, timestamp, cost) = row
            timestamp = strftime('%Y-%m-%d %H:%M:%S')
            
            # Print columns A thru J as desired
            # logger.info('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            logger.debug('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (phone, name, district, block, panchayat, designation, gender, total_calls, success_percentage, timestamp))

            query = 'select totalCalls, successPercentage, cost from addressbook where region="%s" and phone="%s"' % (region, phone)
            cur = db.cursor()
            logger.debug('Executing query[%s]' % query)
            cur.execute(query)
            res = cur.fetchall()
            logger.debug(res)

            if res:
                # Update                
                (row[7], row[8], row[10]) = (total_calls, success_percentage, cost) = res[0]
                
                # Add timestamp to the excel
                row[9] = timestamp
                logger.debug('FetchedRow[%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s]' % (phone, name, district, block, panchayat, designation, gender, total_calls, success_percentage, timestamp, cost))

                query = 'update addressbook set name="%s", district="%s", block="%s", panchayat="%s", designation="%s", gender="%s", ts="%s", status="active" where region="%s" and phone="%s"' % (name, district, block, panchayat, designation, gender, timestamp, region, phone)
            else:                
                query = 'insert into addressbook (phone, name, district, block, panchayat, designation , gender, ts, region, status) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "active")' % (phone, name, district, block, panchayat, designation, gender, timestamp, region)

            cur = db.cursor()
            logger.info('Executing query[%s]' % query)
            cur.execute(query)

    logger.debug(values)
    body = {
          'values': values
    }
    range_name = 'Sheet2!A:K'

    logger.info('Updating the Sheet2 for SpreadSheet[%s]' % spreadsheet_id)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()

    query = 'delete from addressbook where region="rscd" and status!="active"'
    cur = db.cursor()
    logger.info('Executing query[%s]' % query)
    # Mynk cur.execute(query)

    return 'SUCCESS'


#############
# Tests
#############


class TestSuite(unittest.TestCase):
  def setUp(self):
    self.logger = loggerFetch('info')
    self.logger.info('BEGIN PROCESSING...')

  def tearDown(self):
    self.logger.info('...END PROCESSING')
    
  def test_fetch(self):
    result = download_googlesheet(self.logger, self.db, 'rscd',  '1UGtgX1goSh-VDY2Sqp0NH5kkxaxgm4IO-3zu9WROnuI', 'Form Responses 1!A:KX')
    
    self.assertEqual('SUCCESS', result)


if __name__ == '__main__':
  unittest.main()

