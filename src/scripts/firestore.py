from google.cloud import firestore
repoDir="/home/orange/repo/src/"
from firebase import firebase
import sys
import os
import json
sys.path.insert(0, repoDir)
from wrappers.logger import loggerFetch
def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='These scripts will initialize the Database for the district and populate relevant details')
  parser.add_argument('-v', '--visible', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-limit', '--limit', help='Limit on the number of results', required=False)
  parser.add_argument('-s', '--stateCode', help='State for which the delayed payment report needs to be crawld', required=False)
  parser.add_argument('-pc', '--panchayatCode', help='Panchayat for which the delayed payment report needs to be crawld', required=False)
  parser.add_argument('-c', '--customer', help='Block for which the data needs to be updated', required=False)
  parser.add_argument('-j', '--jobcard', help='Jobcard for which date needs to be updated', required=False)
  parser.add_argument('-upt', '--updatePanchayatTable', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-dpt', '--deletePanchayatTable', help='Make the browser visible', required=False, action='store_const', const=1)
  parser.add_argument('-ujt', '--updateJobcardTable', help='Update Jobcard Table', required=False, action='store_const', const=1)
  parser.add_argument('-utt', '--updateTransactionTable', help='Update Transaction Table', required=False, action='store_const', const=1)
  parser.add_argument('-djt', '--deleteJobcardTable', help='Update Jobcard Table', required=False, action='store_const', const=1)
  parser.add_argument('-gpt', '--getPanchayatTable', help='Get Panchayat Table', required=False, action='store_const', const=1)
  parser.add_argument('-p', '--populate', help='Get Panchayat Table', required=False, action='store_const', const=1)
  parser.add_argument('-pw', '--populateWeights', help='Get Panchayat Table', required=False, action='store_const', const=1)
  parser.add_argument('-w', '--write', help='Get Panchayat Table', required=False, action='store_const', const=1)

  args = vars(parser.parse_args())
  return args

def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info('args: %s', str(args))
  if args['populateWeights']:
    db = firestore.Client()
    logger.info("Going to Populate the database")
    if args['customer']:
      customer=args['customer']
      jsonName="%s.json" % (customer)
      json_data=open(jsonName,encoding='utf-8-sig').read()
      d = json.loads(json_data)
      i=0
      for item in d:
        i=i+1
        weight=item
        logger.info(weight)
        doc_ref = db.collection(customer).document(str(i))
        doc_ref.set({
          u'weight': weight
        })
  if args['populate']:
    db = firestore.Client()
    logger.info("Going to Populate the database")
    jsonName="sample_data.json"
    json_data=open(jsonName,encoding='utf-8-sig').read()
    d = json.loads(json_data)
    i=0
    for item in d:
      i=i+1
      name=item[0]
      value=item[1]
      logger.info(name)
      doc_ref = db.collection(u'products').document(str(i))
      doc_ref.set({
        u'name': name,
        u'value': value
      })
# Project ID is determined by the GCLOUD_PROJECT environment variable
#
# doc_ref = db.collection(u'users').document(u'alovelace')
# doc_ref.set({
#   u'first': u'Ada',
#   u'last': u'Lovelace',
#   u'born': 1815
# })


  logger.info("...END PROCESSING") 
  exit(0)

if __name__ == '__main__':
  main()
