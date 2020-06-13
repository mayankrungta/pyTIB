import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)
 
from os import errno
from bs4 import BeautifulSoup

from wrappers.logger import loggerFetch

import unittest
import requests


#######################
# Global Declarations
#######################

timeout = 60
dirname = './reports/'


#############
# Functions
#############

def generate_panchayat_reports(logger, csv_buffer, panchayat_list, prefix):
    for (panchayat_name, panchayat_code) in panchayat_list.items():
        panchayat_buffer = ['Wagelist No,Job card no,Applicant no,Applicant Name,Work Code,Work Name,MSR no,Reference No,Status,Rejection Reason,Proccess Date,Wage list FTO No.,Serial No.\n']

        for row in csv_buffer[1:]:
            jobcode_str = 'JH-06-004-' + panchayat_code[-3:]
            logger.info('Searching %s in ROW[%s]' % (jobcode_str, row))
            if jobcode_str in row:
                panchayat_buffer.append(row)
                
        filename = prefix + panchayat_name + '_' + 'report.csv'
        with open(filename, 'wb') as csv_file:
            logger.info("Writing to [%s]" % filename)
            csv_file.write(''.join(panchayat_buffer).encode('utf-8'))
            #csv_file.write(''.join(panchayat_buffer))
    
def dump_panchayat_reports(logger, csv_buffer, panchayat_lookup, prefix, buffer):
    for (panchayat_code, panchayat_name) in panchayat_lookup.items():
        panchayat_buffer = ['Wagelist No,Job card no,Applicant no,Applicant Name,Work Code,Work Name,MSR no,Reference No,Status,Rejection Reason,Proccess Date,Wage list FTO No.,Serial No.\n']

        panchayat_buffer += buffer[panchayat_name]
                
        filename = prefix + panchayat_name + '_' + 'report.csv'
        with open(filename, 'wb') as csv_file:
            logger.info("Writing to [%s]" % filename)
            csv_file.write(''.join(panchayat_buffer).encode('utf-8'))
            #csv_file.write(''.join(panchayat_buffer))

def populate_panchayat_list(logger, state_name, state_code, district_name, district_code, block_name, block_code, fin_year, cookies):
    panchayat_list = {}

    prefix = dirname + '%s_%s_%s_%s_' % (fin_year, state_name, district_name, block_name)
    filename = prefix + 'panchayat_list.html'
    logger.info('FileName[%s]' % filename)
    
    if os.path.exists(filename):
        with open(filename, 'rb') as html_file:
            logger.info('File already donwnloaded. Reading [%s]' % filename)
            panchayat_list_html = html_file.read()
    else:
        #Reference url = 'http://nregasp2.nic.in/netnrega/Progofficer/PoIndexFrame.aspx?flag_debited=D&lflag=local&District_Code=3406&district_name=LATEHAR&state_name=JHARKHAND&state_Code=34&finyear=2018-2019&check=1&block_name=Manika&Block_Code=3406004'
        url = 'http://nregasp2.nic.in/netnrega/Progofficer/PoIndexFrame.aspx?flag_debited=D&lflag=local&District_Code=%s&district_name=%s&state_name=%s&state_Code=%s&finyear=%s&check=1&block_name=%s&Block_Code=%s' % (district_code, district_name, state_name, state_code, fin_year, block_name, block_code)
    
        try:
            logger.info('Fetching URL[%s]' % url)
            response = requests.get(url, timeout=timeout, cookies=cookies)
        except Exception as e:
            logger.error('Caught Exception[%s]' % e)
            
        panchayat_list_html = response.content
        
        with open(filename, 'wb') as html_file:
            logger.info('Writing [%s]' % filename)
            html_file.write(panchayat_list_html)
    
    bs = BeautifulSoup(panchayat_list_html, 'html.parser')

    table = bs.find(id='ctl00_ContentPlaceHolder1_gvpanch')
    logger.debug(str(table))
    click_list = table.findAll('a')
    logger.debug(str(click_list))

    for anchor in click_list:
        a = str(anchor)
        pos = a.find('Panchayat_name=')
        logger.debug(pos)
        if pos > 0:
            beg = a.find('Panchayat_name=') + len('Panchayat_name=')
            end = a.find('&amp;Panchayat_Code=') 
            panchayat_name = a[beg:end]
            beg = a.find('Panchayat_Code=') + len('Panchayat_Code=')
            end = beg + 10
            panchayat_code = a[beg:end]
            panchayat_list[panchayat_name] = panchayat_code
            logger.info('Found [%s, %s]...' % (panchayat_name, panchayat_code))

    return panchayat_list
        
def populate_panchayat_lookup(logger, state_name, state_code, district_name, district_code, block_name, block_code, fin_year, cookies, buffer):
    panchayat_lookup = {}

    prefix = dirname + '%s_%s_%s_%s_' % (fin_year, state_name, district_name, block_name)
    filename = prefix + 'panchayat_lookup.html'
    logger.info('FileName[%s]' % filename)
    
    if os.path.exists(filename):
        with open(filename, 'rb') as html_file:
            logger.info('File already donwnloaded. Reading [%s]' % filename)
            panchayat_lookup_html = html_file.read()
    else:
        #Reference url = 'http://nregasp2.nic.in/netnrega/Progofficer/PoIndexFrame.aspx?flag_debited=D&lflag=local&District_Code=3406&district_name=LATEHAR&state_name=JHARKHAND&state_Code=34&finyear=2018-2019&check=1&block_name=Manika&Block_Code=3406004'
        url = 'http://nregasp2.nic.in/netnrega/Progofficer/PoIndexFrame.aspx?flag_debited=D&lflag=local&District_Code=%s&district_name=%s&state_name=%s&state_Code=%s&finyear=%s&check=1&block_name=%s&Block_Code=%s' % (district_code, district_name, state_name, state_code, fin_year, block_name, block_code)
    
        try:
            logger.info('Fetching URL[%s]' % url)
            response = requests.get(url, timeout=timeout, cookies=cookies)
        except Exception as e:
            logger.error('Caught Exception[%s]' % e)
            
        panchayat_lookup_html = response.content
        
        with open(filename, 'wb') as html_file:
            logger.info('Writing [%s]' % filename)
            html_file.write(panchayat_lookup_html)
    
    bs = BeautifulSoup(panchayat_lookup_html, 'html.parser')

    table = bs.find(id='ctl00_ContentPlaceHolder1_gvpanch')
    logger.debug(str(table))
    click_list = table.findAll('a')
    logger.debug(str(click_list))

    for anchor in click_list:
        a = str(anchor)
        pos = a.find('Panchayat_name=')
        logger.debug(pos)
        if pos > 0:
            beg = a.find('Panchayat_name=') + len('Panchayat_name=')
            end = a.find('&amp;Panchayat_Code=') 
            panchayat_name = a[beg:end]
            beg = a.find('Panchayat_Code=') + len('Panchayat_Code=')
            end = beg + 10
            panchayat_str = a[beg:end]
            panchayat_code = panchayat_str[-3:]
            panchayat_lookup[panchayat_code] = panchayat_name
            logger.info('Found [%s, %s]...' % (panchayat_code, panchayat_name))
            buffer[panchayat_name] = []

    return panchayat_lookup
        
def populate_reference_no_lookup(logger, url=None, filename=None, cookies=None):
    reference_no_list = []

    if not url:
        url='http://nregasp2.nic.in/netnrega/FTO/ResponseDetailStatusReport.aspx?lflag=eng&flg=W&page=d&state_name=JHARKHAND&state_code=34&district_name=LATEHAR&district_code=3406&block_name=Manika&block_code=3406004&fin_year=2016-2017&typ=R&mode=B&source=&'
    
    if os.path.exists(filename):
        with open(filename, 'rb') as html_file:
            logger.info('File already donwnloaded. Reading [%s]' % filename)
            reference_no_html = html_file.read()
    else:        
        try:
            logger.info('Fetching URL[%s]' % url)
            response = requests.get(url, timeout=timeout, cookies=cookies)
        except Exception as e:
            logger.error('Caught Exception[%s]' % e)
            
        reference_no_html = response.content
    
        with open(filename, 'wb') as html_file:
            logger.info('Writing [%s]' % filename)
            html_file.write(reference_no_html)
        

    
    bs = BeautifulSoup(reference_no_html, 'html.parser')
    span = bs.find(id='ctl00_ContentPlaceHolder1_lbl_head')
    logger.debug('SPAN[%s]' % str(span))

    table = span.findNext('table')
    logger.debug(str(table))

    tr_list = table.select('tr')
    logger.debug(str(tr_list))

    is_first_row = True
    for tr in tr_list:
        if is_first_row:
            is_first_row = False
            continue
        td = tr.findChild('td')
        serial_no = td.text
        logger.debug('Serial_No[%s]' % serial_no)

        td = td.findNext('td')
        fto_no = td.text
        logger.debug('Fto_No[%s]' % fto_no)
        
        td = td.findNext('td')
        reference_no = td.text.strip()
        logger.debug('Reference_No[%s]' % reference_no)

        reference_no_list.append(reference_no)
        
    return reference_no_list
    

def parse_transaction_trail(logger, url=None, filename=None, csv_buffer=None, cookies=None, panchayat_lookup=None, buffer=None):
    if os.path.exists(filename):
        with open(filename, 'rb') as html_file:
            logger.info('File already donwnloaded. Reading [%s]' % filename)
            transaction_trail_html = html_file.read()
    else:        
        # ref_no = '3406004000NRG18010220180328089'
        # ref_no = '3406004000NRG18021120170259332'
        # url = 'http://nregasp2.nic.in/netnrega/FTO/Rejected_ref_no_detail.aspx?panchayat_code=%s&panchayat_name=%sblock_code=%s&block_name=%s&flg=W&state_code=%s&ref_no=%s&fin_year=%s&source=' % (panchayat_code, panchayat_name, block_code, block_name, state_code, ref_no, fin_year)
        try:
            logger.info('Fetching URL[%s]' % url)
            response = requests.get(url, timeout=timeout, cookies=cookies)
        except Exception as e:
            logger.error('Caught Exception[%s]' % e)
    
        transaction_trail_html = response.content
        # filename = dirname + '%s_%s_%s_%s_%s_%s.html' % (state_name, district_name, block_name, panchayat_name, ref_no, fin_year)
        with open(filename, 'wb') as html_file:
            logger.info('Writing [%s]' % filename)
            html_file.write(transaction_trail_html)
            
    bs = BeautifulSoup(transaction_trail_html, 'html.parser')
    table = bs.find(id='ctl00_ContentPlaceHolder1_grid_find_ref')
    logger.debug(str(table))

    try:
        tr_list = table.select('tr')
    except Exception as e:
        if e == "'NoneType' object has no attribute 'select'":
            logger.warning('No Data Found[%s]' % tr_list)
            return
        else:
            logger.error('FIXME[%s]' % e)
            return
    logger.debug(str(tr_list))
    is_first_row = True
    for tr in tr_list:
        logger.debug('ROW[%s]' % str(tr))        
        if is_first_row:
            is_first_row = False
            logger.debug('HEADER[%s]' % str(tr))        
            continue
        td = tr.findChild('td')
        wagelist_no = td.text
        logger.info('Wagelist_No[%s]' % wagelist_no)
    
        td = td.findNext('td')
        jobcard_no = td.text
        logger.info('Jobcard_No[%s]' % jobcard_no)

        jobcard_str = jobcard_no[:13]
        logger.info('Jobcard_Str[%s]' % jobcard_str)

        td = td.findNext('td')
        applicant_no = td.text
        logger.info('Applicant_No[%s]' % applicant_no)
    
        td = td.findNext('td')
        applicant_name = td.text
        logger.info('Applicant_Name[%s]' % applicant_name)
    
        td = td.findNext('td')
        work_code = td.text
        logger.info('Work_Code[%s]' % work_code)
    
        td = td.findNext('td')
        work_name = td.text
        logger.info('Work_Name[%s]' % work_name)
    
        td = td.findNext('td')
        msr_no = td.text
        logger.info('Msr_No[%s]' % msr_no)
    
        td = td.findNext('td')
        reference_no = td.text
        logger.info('Reference_No[%s]' % reference_no)
    
        td = td.findNext('td')
        status = td.text
        logger.info('Status[%s]' % status)
    
        td = td.findNext('td')
        rejection_reason = td.text
        logger.info('Rejection_Reason[%s]' % rejection_reason)
    
        td = td.findNext('td')
        process_date = td.text
        logger.info('Process_Date[%s]' % process_date)
    
        td = td.findNext('td')
        wagelist_fto_no = td.text
        logger.info('Wagelist_Fto_No[%s]' % wagelist_fto_no)
    
        td = td.findNext('td')
        serial_no = td.text
        logger.info('Serial_No[%s]' % serial_no)
    
        row = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (wagelist_no, jobcard_no, applicant_no, applicant_name, work_code, work_name, msr_no, reference_no, status, rejection_reason, process_date, wagelist_fto_no, serial_no)
        logger.info(row)
        csv_buffer.append(row)
        if buffer and jobcard_str in row:
            panchayat_code = jobcard_str[-3:]
            logger.info('Panchayat_Code[%s]' % panchayat_code)
            panchayat_name = panchayat_lookup[panchayat_code] 
            logger.info('panchayat_name[%s]' % panchayat_name)
            buffer[panchayat_name].append(row)


def fetch_efms_report(logger, state_name=None, district_name=None, block_name=None, block_code=None, fin_year=None, cookies=None):
    logger.info('Fetch the Rejected Payments Report')
    if not state_name:
        state_name = 'JHARKHAND'
    if not district_name:
        district_name = 'LATEHAR'
    if not block_name:
        block_name = 'Mahuadanr'
    if not block_code:
        block_code = '3406007'
    if not fin_year:
        fin_year = '2017-2018'

    state_code = '34'
    district_code = '3406'
    panchayat_code = None # '3406004013' # for Namudag

    prefix = dirname + '%s_%s_%s_%s_' % (fin_year, state_name, district_name, block_name)
    logger.info('PREFIX[%s]' % prefix)

    logger.info('Fetching report for State[%s] District[%s] Block[%s] BlockCode[%s] Financial Year[%s]' % (state_name, district_name, block_name, block_code, fin_year))

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise        

    if panchayat_code:
        panchayat_list = { panchayat_name: panchayat_code }
    else:
        panchayat_list = populate_panchayat_list(logger, state_name, state_code, district_name, district_code, block_name, block_code, fin_year, cookies)

    for (panchayat_name, panchayat_code) in panchayat_list.items():
        csv_buffer = ['Wagelist No,Job card no,Applicant no,Applicant Name,Work Code,Work Name,MSR no,Reference No,Status,Rejection Reason,Proccess Date,Wage list FTO No.,Serial No.\n']

        filename = prefix + panchayat_name + '_' + 'rejection_details.html'
        url = 'http://nregasp2.nic.in/netnrega/FTO/ResponseDetailStatusReport.aspx?lflag=eng&flg=W&page=b&state_name=%s&state_code=%s&district_name=%s&district_code=%s&block_name=%s&block_code=%s&panchayat_name=%s&panchayat_code=%s&fin_year=%s&typ=R&mode=B&source=&' % (state_name, state_code, district_name, district_code, block_name, block_code, panchayat_name, panchayat_code, fin_year)
        
        reference_no_list = populate_reference_no_lookup(logger, url=url, filename=filename)
        logger.debug(reference_no_list)
    
        for ref_no in reference_no_list:
            filename = prefix + panchayat_name + '_' + ref_no + '.html'
            # ref_no = '3406004000NRG18010220180328089'
            # ref_no = '3406004000NRG18021120170259332'
            url = 'http://nregasp2.nic.in/netnrega/FTO/Rejected_ref_no_detail.aspx?panchayat_code=%s&panchayat_name=%sblock_code=%s&block_name=%s&flg=W&state_code=%s&ref_no=%s&fin_year=%s&source=' % (panchayat_code, panchayat_name, block_code, block_name, state_code, ref_no, fin_year)
            
            parse_transaction_trail(logger, url=url, filename=filename, csv_buffer=csv_buffer, cookies=cookies)
            logger.debug('The CSV buffer written [%s]' % csv_buffer)
    
        filename = prefix + panchayat_name + '_' + 'report.csv'
        with open(filename, 'wb') as csv_file:
            logger.info("Writing to [%s]" % filename)
            csv_file.write(''.join(csv_buffer).encode('utf-8'))
            #csv_file.write(''.join(csv_buffer))
        
        logger.info('The CSV buffer written [%s]' % csv_buffer)

    dest = './' + prefix.strip('./reports/') + 'reports'
    os.rename(dirname, dest)
    logger.info('Moved to [%s]' % dest)

    return 'SUCCESS'

def fetch_efms_reports(logger):
    url='http://nregasp2.nic.in/netnrega/homestciti.aspx?state_code=34&state_name=JHARKHAND'
    response = requests.get(url, timeout=timeout)
    cookies = response.cookies
        
    result = fetch_efms_report(logger, block_name = 'Manika', block_code = '3406004', fin_year = '2016-2017', cookies=cookies)
    result = fetch_efms_report(logger, block_name = 'Manika', block_code = '3406004', fin_year = '2017-2018', cookies=cookies)
    result = fetch_efms_report(logger, block_name = 'Mahuadanr', block_code = '3406007', fin_year = '2016-2017', cookies=cookies)
    result = fetch_efms_report(logger, block_name = 'Mahuadanr', block_code = '3406007', fin_year = '2017-2018', cookies=cookies)

    return 'SUCCESS'
    

def fetch_rejection_report(logger, state_name=None, district_name=None, block_name=None, block_code=None, fin_year=None, cookies=None):
    logger.info('Fetch the Rejected Payments Report')
    if not state_name:
        state_name = 'JHARKHAND'
    if not district_name:
        district_name = 'LATEHAR'
    if not block_name:
        block_name = 'Mahuadanr'
    if not block_code:
        block_code = '3406007'
    if not fin_year:
        fin_year = '2017-2018'

    state_code = '34'
    district_code = '3406'
    panchayat_code = None # '3406004013' # for Namudag
    panchayat_name = 'Namudag'

    prefix = dirname + '%s_%s_%s_%s_' % (fin_year, state_name, district_name, block_name)
    logger.info('PREFIX[%s]' % prefix)

    logger.info('Fetching report for State[%s] District[%s] Block[%s] BlockCode[%s] Financial Year[%s]' % (state_name, district_name, block_name, block_code, fin_year))

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise        

    buffer = {}
    csv_buffer = ['Wagelist No,Job card no,Applicant no,Applicant Name,Work Code,Work Name,MSR no,Reference No,Status,Rejection Reason,Proccess Date,Wage list FTO No.,Serial No.\n']
    panchayat_lookup = populate_panchayat_lookup(logger, state_name, state_code, district_name, district_code, block_name, block_code, fin_year, cookies, buffer)
    logger.info('panchayat_lookup[%s]' % panchayat_lookup)
    logger.info('buffer[%s]' % buffer)

    filename = prefix + 'rejection_details.html'
    #Refernce url='http://nregasp2.nic.in/netnrega/FTO/ResponseDetailStatusReport.aspx?lflag=eng&flg=W&page=d&state_name=JHARKHAND&state_code=34&district_name=LATEHAR&district_code=3406&block_name=Manika&block_code=3406004&fin_year=2016-2017&typ=R&mode=B&source=&'
    url='http://nregasp2.nic.in/netnrega/FTO/ResponseDetailStatusReport.aspx?lflag=eng&flg=W&page=d&state_name=%s&state_code=%s&district_name=%s&district_code=%s&block_name=%s&block_code=%s&fin_year=%s&typ=R&mode=B&source=&' % (state_name, state_code, district_name, district_code, block_name, block_code, fin_year)
    reference_no_list = populate_reference_no_lookup(logger, url=url, filename=filename, cookies=cookies)
    logger.debug(reference_no_list)

    for ref_no in reference_no_list:
        filename = prefix + ref_no + '.html'
        #Reference url = 'http://nregasp2.nic.in/netnrega/FTO/Rejected_ref_no_detail.aspx?block_code=3406004&block_name=Manika&flg=W&state_code=34&ref_no=3406004000NRG150720160652753&fin_year=2016-2017&source='
        url = 'http://nregasp2.nic.in/netnrega/FTO/Rejected_ref_no_detail.aspx?block_code=%s&block_name=%s&flg=W&state_code=%s&ref_no=%s&fin_year=%s&source=' % (block_code, block_name, state_code, ref_no, fin_year)

        parse_transaction_trail(logger, url=url, filename=filename, csv_buffer=csv_buffer, cookies=cookies, panchayat_lookup=panchayat_lookup, buffer=buffer)
        logger.debug('The CSV buffer written [%s]' % csv_buffer)

    filename = prefix + 'report.csv'
    with open(filename, 'wb') as csv_file:
        logger.info("Writing to [%s]" % filename)
        csv_file.write(''.join(csv_buffer).encode('utf-8'))
        #csv_file.write(''.join(csv_buffer))
    
    logger.debug('The CSV buffer written [%s]' % csv_buffer)

    dump_panchayat_reports(logger, csv_buffer, panchayat_lookup, prefix, buffer)
 
    dest = './' + prefix.strip('./reports/') + 'reports'
    os.rename(dirname, dest)
    logger.info('Moved to [%s]' % dest)

    return 'SUCCESS'

def fetch_rejection_reports(logger):
    url='http://nregasp2.nic.in/netnrega/homestciti.aspx?state_code=34&state_name=JHARKHAND'
    response = requests.get(url, timeout=timeout)
    cookies = response.cookies
    
    result = fetch_rejection_report(logger, block_name = 'Manika', block_code = '3406004', fin_year = '2016-2017', cookies=cookies)
    result = fetch_rejection_report(logger, block_name = 'Manika', block_code = '3406004', fin_year = '2017-2018', cookies=cookies)
    result = fetch_rejection_report(logger, block_name = 'Mahuadanr', block_code = '3406007', fin_year = '2016-2017', cookies=cookies)
    result = fetch_rejection_report(logger, block_name = 'Mahuadanr', block_code = '3406007', fin_year = '2017-2018', cookies=cookies)                
    
    return 'SUCCESS'


##########
# Tests
##########

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = loggerFetch('info')
        self.logger.info('BEGIN PROCESSING...')

    def tearDown(self):
        self.logger.info('...END PROCESSING')

        
    def test_r8_efms_report(self):
        #result = fetch_efms_reports(self.logger)
        result = fetch_rejection_reports(self.logger)
        self.assertEqual('SUCCESS', result)

if __name__ == '__main__':
    unittest.main()
