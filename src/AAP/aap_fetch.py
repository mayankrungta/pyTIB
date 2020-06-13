from bs4 import BeautifulSoup
from PIL import Image
from subprocess import check_output

import os
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
REPO_DIR = os.path.dirname(ROOT_DIR)

import sys
sys.path.insert(0, ROOT_DIR)

import errno
import pytesseract
import cv2

import argparse
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import requests
import time
import unittest
import datetime

from wrappers.logger import logger_fetch
from wrappers.sn import driverInitialize, driverFinalize, displayInitialize, displayFinalize

import psutil
import pandas as pd
import json

# For crawler.py

from slugify import slugify
import csv
import urllib.parse as urlparse


# For Google Cloud

use_google_vision = True
use_kannada = False
UPLOAD_ONLY = False

from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format
import re


#######################
# Global Declarations
#######################

timeout = 3
is_mynk = False
is_virtual = True

#############
# Classes
#############

class CEOKarnataka():
    def __init__(self, logger=None, is_selenium=None):
        if logger:
            self.logger = logger
        else:
            logger = self.logger = logger_fetch('info')
        logger.info(f'Constructor({type(self).__name__})')
        #self.url = 'http://ceo.karnataka.gov.in/draftroll_2020/'
        self.url = 'http://ceo.karnataka.gov.in/finalrolls_2020/'
        self.status_file = 'status.csv'
        self.dir = 'BBMP' # 'BBMP_Final'
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.is_selenium = False
        if is_selenium:
            self.is_selenium = is_selenium

        if self.is_selenium:
            self.display = displayInitialize(isDisabled = not is_virtual, isVisible = is_visible)
            self.driver = driverInitialize(timeout=3)
            #self.driver = driverInitialize(path='/opt/firefox/', timeout=3)

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'./aap.bangaluru.json'
        self.project = 'BBMP-OCR'
        self.bucket_name = 'aap_bangaluru' # 'bbmp_bucket' # 'test_aap'
        self.storage_client = storage.Client()
        self.vision_client =  vision.ImageAnnotatorClient()

    def __del__(self):
        if self.is_selenium:
            driverFinalize(self.driver) 
            displayFinalize(self.display)
        self.logger.info(f'Destructor({type(self).__name__})')

    def gcs_delete(self, dirname=None):
        logger = self.logger

        if not dirname:
            dirname = self.dir
        
        logger.info(f'Scanning files in the dir [{dirname}]')
         
        project = self.project
        bucket_name = self.bucket_name

        storage_client = self.storage_client
        bucket = storage_client.get_bucket(self.bucket_name)
        logger.info(f'Listing files in [{dirname}] on {bucket} @ GCS...')
        blobs = bucket.list_blobs(prefix=dirname)
        for blob in blobs:
            logger.debug(blob.name)
            if '.json' in blob.name:
                logger.info(f'To Delete file[{blob.name}]')
                blob.delete()

    def google_vision_scan(self, pdf_file, upload_only=False):
        logger = self.logger
        logger.info(f'Scanning file[{pdf_file}]')
 
        filename = pdf_file.replace('.pdf', '.txt').replace('Karnataka', 'Test')
        if os.path.exists(filename):
            logger.info(f'File already downloaded. Reading [{filename}]...')
            with open(filename) as txt_file:
                text = txt_file.read()
            return text
        
        project = self.project
        bucket_name = self.bucket_name

        storage_client = self.storage_client
        bucket = storage_client.get_bucket(self.bucket_name)
        logger.info(f'Uploading file[{pdf_file}] to {bucket} on GCS...')
        blob = bucket.blob(pdf_file)
        status = blob.exists()
        if not status:
            logger.info(f'File[{pdf_file}] not on GCS[{status}]. Uploading now...')
            blob.upload_from_filename(pdf_file)
        else:
            logger.info(f'File[{pdf_file}] already on GCS[{status}]. Scanning the same.')

        if upload_only:
            logger.info(f'File[{pdf_file}] uploaded on GCS')            
            return

        logger.info(f'Begin scanning file[{pdf_file}]...')
        client = self.vision_client
        
        batch_size = 100
        mime_type = 'application/pdf'
        feature = vision.types.Feature(
            type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
        
        gcs_source_uri = f'gs://{bucket_name}/{pdf_file}'
        gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
        input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
        
        gcs_destination_uri = f'{gcs_source_uri}_'  # gs://aap-bbmp/bbmp-wards-2020.pdf_'
        
        gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
        output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
        async_request = vision.types.AsyncAnnotateFileRequest(
            features=[feature], input_config=input_config, output_config=output_config)
        
        operation = client.async_batch_annotate_files(requests=[async_request])
        operation.result(timeout=180)
        logger.info(f'Done scanning file[{pdf_file}]')
        
        #storage_client = storage.Client()
        match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
        #bucket_name = match.group(1)
        prefix = match.group(2)
        bucket = storage_client.get_bucket(bucket_name)
        
        # List object with the given prefix
        blob_list = list(bucket.list_blobs(prefix=prefix))
        logger.info('Output files:')
        for blob in blob_list:
            logger.info(blob.name)
        
        output = blob_list[0]
        json_string = output.download_as_string()
        response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())
        logger.info(f'Deleting blob[{output.name}]...')
        output.delete()
        
        text = ''
        for page_response in response.responses:
            annotation = page_response.full_text_annotation
            logger.debug('Page text:')
            logger.debug(annotation.text)
            text += annotation.text + '\n'
        
        with open(filename, 'w') as txt_file:
            logger.info(f'Writing file[{filename}]')
            txt_file.write(text)

        return text

    def pdf2text(self, pdf_file, use_google_vision=None):
        logger = self.logger

        if use_google_vision:
            return self.google_vision_scan(pdf_file, upload_only=UPLOAD_ONLY)
        else:
            return self.tesseract_scan(pdf_file)
        
    def tesseract_scan(self, pdf_file):
        logger = self.logger

        filename = pdf_file.replace('.pdf', '.txt')
        if os.path.exists(filename):
            logger.info(f'File already downloaded. Reading [{filename}]...')
            with open(filename) as txt_file:
                text = txt_file.read()
            return text

        if is_mynk:
            aap_location = '/media/mayank/FOOTAGE1/AAP_BBMP_FILEs'
            basename = os.path.basename(filename).strip('.txt')
            dirname = f'{aap_location}/{basename}'
        else:
            dirname = filename.strip('.txt')
        page_file = os.path.join(dirname, 'page') # f'{dirname}/page'
        if False and (not os.path.exists(dirname)):
            #os.makedirs(dirname)
            dest_file = page_file.replace('/page', '_page-01')
            logger.info(dest_file)
            exit(-1)
            # Revisit Added -singlefile to do just first page
            # cmd = f'pdftoppm -png -r 300 -freetype yes {pdf_file} {page_file}'
            cmd = f'pdftoppm -png -singlefile -r 300 -freetype yes {pdf_file} {page_file}'
            logger.info(f'Executing cmd[{cmd}]...')
            os.system(cmd)

        dest_file = page_file.replace('/page', '_page-01')
        logger.info(dest_file)
        img = f'{dest_file}.png'
        logger.debug(img)
        if not os.path.exists(img):
            cmd = f'pdftoppm -png -singlefile -r 300 -freetype yes {pdf_file} {dest_file}'
            logger.info(f'Executing cmd[{cmd}]...')
            os.system(cmd)
        
        cmd = f'tesseract {img} {dest_file} --dpi 300'
        logger.info(f'Executing cmd[{cmd}]...')
        os.system(cmd)

        if False:
            #logger.debug(os.listdir(dirname))
            for png_file in os.listdir(dirname):
                if not png_file.endswith('.png'):  # Only needed during debugging
                    continue
                img = os.path.join(dirname, png_file) # f'{dirname}/{png_file}'
                if not img.endswith('-01.png'):   # Only for now Mynk #FIXME
                    continue
                #if img.endswith('-01.png') or img.endswith('-02.png'):
                if img.endswith('-02.png'):
                    continue
                if os.path.exists(img.replace('.png', '.txt')):
                    continue
                cmd = f'tesseract {img} {img.strip(".png")} --dpi 300'
                logger.info(f'Executing cmd[{cmd}]...')
                os.system(cmd)

        cmd = f'''cat {page_file}-*.txt | grep -v '^$' | 
            grep -v 'Assembly Constituency' | 
            grep -v 'Section No and Name' | 
            grep -v '^Part number : ' | grep -v '^ ' | 
            grep -v 'Available' | grep -v 'Date of Publication:' > \
            {filename}'''
        cmd = f'''cat {page_file}-*.txt > {filename}'''
        cmd = f'''cp {dest_file}.txt {filename}'''
        logger.info(f'Executing cmd[{cmd}]...')
        os.system(cmd)
        return ''
        '''

        #exit(0)

        #cmd = f'rm -rfv {dirname}'
        cmd = f'mv -v {dirname} {aap_location}/'
        logger.info(f'Executing cmd[{cmd}]...')
        os.system(cmd)
        cmd = f'ln -s {aap_location}/{dirname} .'
        logger.info(f'Executing cmd[{cmd}]...')
        os.system(cmd)
        '''
        
        logger.info(f'Reading [{filename}]...')
        with open(filename) as txt_file:
            text = txt_file.read()
        return text

    def fetch_draft_roll(self, district, ac_no, part_no, convert=None, use_google_vision=None, kannada=None):
        logger = self.logger

        if use_kannada:
            kannada = True
        
        filename=os.path.join(f'{self.dir}', f'{district}_{ac_no}_{part_no}.pdf')
        # Discard once done - FIXME
        part_id = int(part_no)
        ac_id = int(ac_no)
        
        if os.path.exists(filename):
            logger.info(f'File already downloaded. Converting [{filename}]...')
            '''
            with open(filename) as html_file:
                html_source = html_file.read()
            '''
        else:
            url = self.url + f'English/MR/AC{ac_no}/S10A{ac_no}P{part_no}.pdf'
            if kannada:
                # url = f'http://ceo.karnataka.gov.in/finalrolls_2020/CodeCaputer1.aspx?field1=./Kannada/MR/AC{ac_no}/S10A{ac_no}P{part_no}.pdf' # &field2={ac_no}&field3=0001'
                # f'http://ceo.karnataka.gov.in/finalrolls_2020/Kannada/MR/AC211/S10A211P1.pdf'
                url = url.replace('/English/', '/Kannada/')
            cmd = f'curl -L -o {filename} {url}'
            logger.info(f'Executing cmd[{cmd}]...')
            os.system(cmd)
            logger.info(f'Fetched the Final Roll [{filename}]')

        if convert:
            self.pdf2text(filename, use_google_vision=use_google_vision)

    def parse_draft_roll(self, district=None, ac_no=None, part_no=None, filename=None):
        logger = self.logger

        if filename:
            search_pattern = f'/media/mayank/FOOTAGE1/AAP_BBMP_FILEs/(\d+)_(\d+)_(\d+)/page-01.txt'
            search_pattern = f'(\d+)_(\d+)_(\d+)'
            match = re.search(search_pattern, filename)
            district = match.group(1)
            ac_no = match.group(2)
            part_no = match.group(3)
            logger.info(f'Attempting file[{filename}]')
        
        filename=os.path.join(f'{self.dir}', f'{district}_{ac_no}_{part_no}/page-01.txt')
        filename = f'/media/mayank/FOOTAGE1/AAP_BBMP_FILEs/{district}_{ac_no}_{part_no}_page-01.txt'
        # Discard once done - FIXME
        district_id = int(district)
        ac_id = int(ac_no)
        part_id = int(part_no)
        logger.info(f'Attempting district[{district_id}] > ac[{ac_id}] > part[{part_id}]')
        row = {
            'District ID': str(district_id),
            'AC ID': str(ac_id),
            'Part ID': str(part_id),
            'Status': 'Done'
        }
        logger.info(f'Attempting for row[{row}]')
        if False:
            if not(part_id < 30 and ac_id == 154):
                logger.info(f'Skipping {filename}...')
                return None
        if os.path.exists(filename):
            logger.info(f'File already downloaded. Parsing [{filename}]...')
            with open(filename, 'r') as file_handle:
                page1 = file_handle.read()

            if len(page1) == 0:
                logger.error(f'Empty file[{filename}]')
                row['Status'] = 'Failed'
                return row

            #search_pattern = 'Constituency is located : (\d+\s*-.*\n*.*)'
            search_pattern = 'Constituency is located\s*:\s*(\d+)\s*-(.*\n*.*)'
            pc_no = re.search(search_pattern, page1).group(1)
            pc_name = re.search(search_pattern, page1).group(2)
            row['Parliamentary Constituency No'] = str(pc_no)
            pc_name = row['Parliamentary Constituency Name'] = re.sub('\n', '', pc_name).strip()
            logger.info(f'Parliamentary Constituency [{pc_no},{pc_name}]')

            #search_pattern = 'No. Name and Reservation Status of Assembly Constituency\s*: (\d+) -(.*\n*.*\n*.*\n*.*)\s*Part'
            search_pattern = 'No. Name and Reservation Status of Assembly Constituency\s*: (\d+) -(.*\n*.*)'
            search_pattern = 'No. Name and Reservation Status of Assembly.*\s*: (\d+) -(.*\n*.*)'
            match = re.search(search_pattern, page1)
            if match:
                ac = row['Assembly Constituency No'] = match.group(1)
                ac_str = match.group(2)
                ac_name = row['Assembly Constituency Name'] = re.sub('\s', '', ac_str)
                logger.info(f'Assembly Constituency [{ac} == {ac_no},{ac_name}]')
                if str(ac_no) != ac:
                    logger.warning(f'{ac} != {ac_no} for file[{filename}]')
                    exit(-1)
            else:
                ac = row['Assembly Constituency No'] = '<MISSED>'
                ac_name = row['Assembly Constituency Name'] = '<MISSED>'
                logger.info(f'Assembly Constituency [{ac} == {ac_no},{ac_name}]')

            if not match:
                search_pattern = 'Name of Polling Station'
                match = re.search(search_pattern, page1)
                if not match:
                    search_pattern = 'Polling Station Details'
                    match = re.search(search_pattern, page1)

            if match:
                part_buffer = page1[match.start():]
                search_pattern = '\(Male/Female/General\)\n*\d+\s*-\s*(.*)'
                match = re.search(search_pattern, part_buffer)

            if not match:
                #search_pattern = 'No. and Name of Polling Station :.*\n*(\d+-.*)'
                #search_pattern = '(\d+-\s*[a-zA-Z\s]+)'
                search_pattern = f'{part_no}\s*-\s*(\d*[a-zA-Z\s]+)'
                search_pattern = f'{part_no}\s*-\s*(.+)'
                logger.info(search_pattern)
                match = re.search(search_pattern, part_buffer)
            row['Part No'] = part_no
            if not match:
                part_name = row['Part Name'] = '<MISSED>'
                row['Status'] = 'Failed'
            else:
                row['Part Name'] = part_name = match.group(1)
            logger.info(f'Part Name[{part_no, part_name}]')

            search_pattern = 'No. and name of sections in the part(.|\n)*999. NRI'
            match = re.search(search_pattern, page1)
            if match:
                sections = row['Section Names'] = match.group()
            else:
                sections = row['Section Names'] = '<MISSED>'
            logger.info(f'Sections [{sections}]')
            
            search_pattern = '(>\s*)(\d+)\s*-(.*)'
            match = re.search(search_pattern, page1)
            if not match:
                search_pattern = 'Ward No( : \s*)(\d+)\s*-(.*)'
                match = re.search(search_pattern, page1)
            if not match:
                #search_pattern = 'Ward No : \s*(\d+)\s*-(.*)'
                search_pattern = 'Ward No(.|\n)*?:\s*(\d+)\s*-(.*)'
                match = re.search(search_pattern, page1)
            if not match:
                ward_no = row['Ward No'] = '<MISSED>'
                ward_name = row['Ward Name'] = '<MISSED>'
                row['Status'] = 'Failed'
            else:
                ward_no = row['Ward No'] = match.group(2)
                ward_name = row['Ward Name'] = match.group(3)
                
            logger.info(f'Ward No [{ward_no}] and Name[{ward_name}]')

            #'Serial No. Serial No. Male Female Third Gender Total\n1 786 398 388 0 786'
            #search_pattern = 'Serial No. Serial No. Male Female Third Gender Total\n(\d+ \d+ \d+ \d+ \d+ \d+)'
            search_pattern = '(\d+ \d+ \d+ \d+ \d+ \d+)'
            match = re.search(search_pattern, page1)
            if not match:
                search_pattern = 'Serial No. Serial No. Male Female Third Gender Total\n(\d+ \d+ \d+ \d+ \d+)'
                match = re.search(search_pattern, page1)
            if not match:
                logger.warning(f'Could not find gender stats for file[{filename}]')
                stats = []
            else:
                stats = match.group(1).split(' ')
            logger.debug(stats)
            if len(stats) < 6:
                men = row['Male'] = '<MISSED>'
                women = row['Female'] = '<MISSED>'
                third = row['Third Gender'] = '<MISSED>'
                TOTAL = row['Total'] = '<MISSED>'
                total = '<MISSED>'
                row['Status'] = 'Failed'
            else:
                men = row['Male'] = stats[2]
                women = row['Female'] = stats[3]
                third = row['Third Gender'] = stats[4]
                TOTAL = row['Total'] = stats[5]
                total = int(men) + int(women) + int(third)
                if stats[1] != stats[-1]:
                    logger.warning(f'Messed gender stats for file[{filename}]')
            logger.info(f'men[{men}] women[{women}] third[{third}] total[{total}] TOTAL[{TOTAL}]')
        return row
        
    def fetch_district_list(self):
        logger = self.logger
        # return ['31', '32', '33', '34']
        return ['31']
        # First four are Mysore district and rest are Kodagu
        # districts = ['217', '218', '216', '215', '210', '211', '212', ]
        # logger.info(f'Districts chosen: [{districts[:1]}]')
        # return districts[:1]
        #return ['28']

    def fetch_draft_rolls(self, convert=None, use_google_vision=None):
        logger = self.logger

        for district in self.fetch_district_list():
            for ac_no in self.fetch_ac_list(district=district):
                for part_no in self.fetch_part_list(district, ac_no):
                    self.fetch_draft_roll(district, ac_no, part_no, convert=convert, use_google_vision=use_google_vision)

    def parse_draft_rolls_brute_force(self):
        logger = self.logger
        buffer = []

        list_filename = '/tmp/files.txt'

        if not os.path.exists(list_filename):
            #cmd = f'ls /media/mayank/FOOTAGE1/AAP_BBMP_FILEs/*/page-01.txt > {list_filename}'
            cmd = f'ls /media/mayank/FOOTAGE1/AAP_BBMP_FILEs/*_page-01.txt > {list_filename}'
            logger.info(f'Executing cmd[{cmd}]...')
            os.system(cmd)

        with open(list_filename, 'r') as file_handle:
            logger.info(f'Reading [{list_filename}]...')
            files = file_handle.read()

        for filename in files.split('\n'):
            if not filename:
                continue
            logger.info(f'Parsing file[{filename}]')
            row = self.parse_draft_roll(filename=filename)
            if not row:
                return buffer
            buffer.append(row)

        return buffer
        
    def parse_draft_rolls_drill_down(self):
        logger = self.logger
        buffer = []
        try:
            '''
            print('Ingore')
        if True:
            '''
            for district in self.fetch_district_list():
                for ac_no in self.fetch_ac_list(district=district):
                    for part_no in self.fetch_part_list(district, ac_no):
                        row = self.parse_draft_roll(district, ac_no, part_no)
                        if not row:
                            raise
                        buffer.append(row)
        except Exception as e:
            logger.warning(f'Parse failed with Exception[{e}]')

        return buffer


    def parse_draft_rolls(self, brute_force=None, filename=None):
        logger = self.logger

        if not filename:
            filename = '/tmp/aggregate.json'             

        if brute_force:
            buffer = self.parse_draft_rolls_brute_force()
        else:
            buffer = self.parse_draft_rolls_drill_down()

        if len(buffer) > 0:
            with open(filename, 'w') as file_handle:
                logger.info(f'Writing file[{filename}]')
                json.dump(buffer, file_handle)

            df = pd.read_json(filename)
            logger.debug(df.head())
            filename = filename.replace('.json', '.csv')
            logger.info(f'Writing file[{filename}]')
            df.to_csv(filename, index=False)

    def fetch_ac_list(self, district=None):
        logger = self.logger        
        filename = os.path.join(self.dir, f'{district}.html')
        url = self.url + f'AC_List_B3.aspx?DistNo={district}'
        type = 'AC NO'
        logger.info(f'Fetching AC list for file[{filename}] and type[{type}]')
        return self.fetch_lookup(url, filename, type)
            
    def fetch_part_list(self, district=None, ac_no=None):
        logger = self.logger        
        filename = os.path.join(f'{self.dir}', f'{district}_{ac_no}.html')
        url = self.url + f'Part_List.aspx?ACNO={ac_no}'
        type = 'Part No'
        logger.info(f'Fetching Part list for file{filename} and type[{type}]')
        return self.fetch_lookup(url, filename, type)

    def fetch_lookup(self, url, filename, type):
        logger = self.logger
        if os.path.exists(filename):
            logger.info(f'File already downloaded. Reading [{filename}]...')
            with open(filename) as html_file:
                html_source = html_file.read()
        else:
            logger.info(f'Fetching URL[{url}]')
            response = requests.get(url)
            html_source = response.content
            with open(filename, 'wb') as html_file:
                logger.info(f'Writing file[{filename}]')
                html_file.write(html_source)

        df = pd.read_html(html_source)[1]
        logger.debug(f'{df}')
        filename = filename.replace('.html', '.csv')
        logger.info(f'Writing [{filename}]') 
        df.to_csv(filename, index=False)
        logger.info(df.head())
        return df[type].to_list()


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = logger_fetch('info')
        self.logger.info('BEGIN PROCESSING...')

    def tearDown(self):
        self.logger.info('...END PROCESSING')

    def test_fetch_draft_rolls(self):
        self.logger.info("TestCase: E2E - fetch_draft_rolls()")
        # Fetch Draft Rolls from http://ceo.karnataka.gov.in/
        ck = CEOKarnataka(logger=self.logger)
        #ck.fetch_draft_rolls(convert=True, use_google_vision=use_google_vision)
        ck.fetch_draft_rolls(convert=True, use_google_vision=use_google_vision)
        del ck
        
    def test_fetch_draft_roll(self):
        self.logger.info("TestCase: UnitTest - fetch_draft_roll(district, ac_no, part_no)")
        # Fetch Draft Rolls from http://ceo.karnataka.gov.in/
        ck = CEOKarnataka(logger=self.logger)
        #ck.fetch_draft_roll(district='32', ac_no='151', part_no='115', convert=True, use_google_vision=use_google_vision)
        #ck.fetch_draft_roll(district='31', ac_no='154', part_no='1', convert=True, use_google_vision=use_google_vision)
        ck.fetch_draft_roll(district='31', ac_no='154', part_no='5', convert=True, use_google_vision=use_google_vision)
        #ck.fetch_draft_roll(district='34', ac_no='155', part_no='232', convert=True, use_google_vision=use_google_vision)
        del ck

    def test_parse_draft_roll(self):
        self.logger.info("TestCase: UnitTest - parse_draft_roll(district, ac_no, part_no)")
        # Parse Draft Rolls from http://ceo.karnataka.gov.in/
        ck = CEOKarnataka(logger=self.logger)
        ck.parse_draft_roll(district='32', ac_no='151', part_no='115', convert=True, use_google_vision=use_google_vision)
        #ck.parse_draft_roll(district='31', ac_no='154', part_no='7')
        del ck

    def test_parse_draft_rolls(self):
        self.logger.info("TestCase: E2E - parse_draft_rolls()")
        # Parse Draft Rolls from http://ceo.karnataka.gov.in/
        ck = CEOKarnataka(logger=self.logger)
        ck.parse_draft_rolls(brute_force=True, filename='/tmp/all.json')
        del ck
        
    def test_gcs_list(self):
        self.logger.info("TestCase: UnitTest - gcs_delete(district, ac_no, part_no)")
        # Parse Draft Rolls from http://ceo.karnataka.gov.in/
        ck = CEOKarnataka(logger=self.logger)
        ck.gcs_delete('BBMP_Final')
        #ck.parse_draft_roll(district='31', ac_no='154', part_no='7')
        del ck

#############
# Functions
#############

if __name__ == '__main__':
    unittest.main()
