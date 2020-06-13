import os
dirname = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(dirname)

import sys
sys.path.insert(0, rootdir)

#from os import errno

import time
import unittest

import pandas as pd
import xlsxwriter

from wrappers.logger import loggerFetch

###


#######################
# Global Declarations
#######################

timeout = 10
#dirname = 'BasiaSamples'


#############
# Functions
#############

def get_col_widths(dataframe):
    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]



def printify(logger, filename=None, max_width=None):
    if not filename:
        filename = 'z.csv'
    xlsfile = filename.replace('.csv', '.xlsx')
    logger.info('Printify file [%s]' % filename)

    if not max_width:
        max_width = 25

    fields = ['गांव', 'WorkerID']
    df = pd.read_csv(filename, index_col='WorkerID', header=0, encoding = 'utf-8-sig') # , index_col=fields)

    #logger.info(df)
    print(df.head())
    if 'sample' in filename:
        df = df.sort_values(by=['गांव', 'Category', 'WorkerID'], ascending=[True, False, True])
    else:
        #df = df.sort_values(by=['गांव', df.columns[6], df.columns[0]], ascending=[True, False, True])
        df = df.sort_values(by=['गांव', 'पेमेंट की स्तिथि', 'WorkerID'], ascending=[True, False, True])

    '''
    df.columns[0] = 'Sl No.'
    df['Sl No.'] = df.index
    '''
    df = df.reset_index()
    df.insert(0, 'Sl No.', range(1, len(df)+1))
    df.set_index('Sl No.', inplace=True)
    #df.reset_index(drop = True, inplace = True)

    print(df.head())

    #df.style.set_table_styles([dict(selector="th",props=[('max-width', '50px')])])
    #s.str.wrap(12)
    #print(df.style)
    #logger.info(df)

    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(xlsfile, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    
    ####################################
    ########### Page Setup #############
    ####################################

    worksheet.set_landscape()
    worksheet.set_paper(9)  # A4
    # worksheet.set_zoom(66)
    # worksheet.center_horizontally()
    # worksheet.center_vertically()

    # Set Margins - worksheet.set_margins([left=0.7,] right=0.7,] top=0.75,] bottom=0.75]]])
    # worksheet.set_margins(0.7, 0.7, 0.75, 0.75)
    worksheet.set_margins(0.25, 0.25, 0.25, 0.25)

    # Header - set_header([header='',] options]])
    # e.g worksheet.set_header('&C%s' % filename)
    # worksheet.set_header(filename)  # Default Center Justified
    worksheet.set_header('&C%s' % os.path.basename(filename))
    
    # worksheet.set_header('&CPage &P of &N') # Page 1 of 6
    # worksheet.set_header('&CUpdated at &T') # Updated at 12:30 PM

    # Footer -  set_footer([footer='',] options]])
    worksheet.set_footer('&CPage &P of &N') # Page 1 of 6
    #worksheet.set_header('&CUpdated at &T') # Updated at 12:30 PM

    # Repeat rows -  repeat_rows(first_row[, last_row])
    worksheet.repeat_rows(0) # Header Repeat

    # Grid lines
    '''
    The following values of option are valid:
    
        Don’t hide gridlines.
        Hide printed gridlines only.
        Hide screen and printed gridlines.
    
    '''
    # worksheet.hide_gridlines()
    
    # Row Column Headers - print_row_col_headers()
    # worksheet.print_row_col_headers()

    # Define print area - worksheet.print_area()
    # worksheet1.print_area('A1:H20')     # Cells A1 to H20.
    # worksheet2.print_area(0, 0, 19, 7)  # The same as above.

    # Print Across
    # worksheet.print_across()

    # Fit To Page - worksheet.fit_to_pages()
    # worksheet1.fit_to_pages(1, 1)  # Fit to 1x1 pages.
    # worksheet2.fit_to_pages(2, 1)  # Fit to 2x1 pages.
    # worksheet3.fit_to_pages(1, 2)  # Fit to 1x2 pages.

    # Start print from page 2.
    # worksheet.set_start_page(2)

    # Set Print Scale -  set_print_scale()
    worksheet.set_print_scale(66)

    # Page Breaks - worksheet.set_h_pagebreaks()
    # worksheet.set_h_pagebreaks([20])  # Break between row 20 and 21.
    # worksheet2.set_h_pagebreaks([20, 40, 60, 80, 100])

    # NOTE: replace h with v for vertical breaks - worksheet.set_v_pagebreaks()
    
    
    ####################################
    ########### Formatting #############
    ####################################
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    # Make header bold
    worksheet.set_row(0, None, bold)
    
    # Cell Format approach
    
    cell_format = workbook.add_format()
    # worksheet.set_row(0, None, cell_format.set_bold())

    # Align all centers horizontally and vertically
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_align('vjustify')
    cell_format.set_text_wrap()
    cell_format.set_font_size(10)
    cell_format.set_border(1)

    # Font Family
    cell_format.set_font('Liberation Sans')
    #cell_format.set_font_family('&apos;Liberation Sans&apos;')
    cell_format.set_font_family('Liberation Sans')
    # cell_format.set_font_charset(178)
    '''
    # Set the format but not the column width.
    worksheet.set_column('C:C', None, format2)

    # Set the format but not the column width.
    worksheet.set_column('C:C', None, cell_format)
    '''

    worksheet.set_column('A:Z', None, cell_format)
    
    for i, width in enumerate(get_col_widths(df)):
        if width > max_width:
            width = max_width
        worksheet.set_column(i, i, width)
    # worksheet.set_default_row(20)
    # workbook.close()

    worksheet.set_row(0, None, cell_format)

    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    return 'SUCCESS'
    

    # iter_csv = pd.read_csv(file, iterator=True, chunksize=1000)
    # df = pd.concat([chunk[chunk['field'] > constant] for chunk in iter_csv])    
    '''
    try:
        with open(filename, 'r') as csv_file:
            logger.info('Reading [%s]' % filename)
            csv_source = csv_file.read()
    except Exception as e:
        logger.error('Exception when opening file[%s] - EXCEPT[%s:%s]' % (filenametype(e), e))
        raise e

    data = pd.DataFrame([], columns=['S.No', 'Mandal Name', 'Gram Panchayat', 'Village', 'Job card number/worker ID', 'Name of the wageseeker', 'Credited Date', 'Deposit (INR)', 'Debited Date', 'Withdrawal (INR)', 'Available Balance (INR)', 'Diff. time credit and debit'])
    try:
        df = pd.read_html(filename, attrs = {'id': 'ctl00_MainContent_dgLedgerReport'}, index_col='S.No.', header=0)[0]
    except Exception as e:
        logger.error('Exception when reading transaction table for jobcard[%s] - EXCEPT[%s:%s]' % (filename, type(e), e))
        return data
    logger.info('The transactions table read:\n%s' % df)
    

    df = df.iloc[::-1] # Reverse the order for calculating diff time Debit dates are easier to record in this order
    for index, row in df.iterrows():
        logger.debug('%d: %s' % (index, row))

        serial_no = index
        logger.debug('serial_no[%s]' % serial_no)

        transaction_date = row['Transaction Date']
        logger.debug('transaction_date[%s]' % transaction_date)

        transaction_ref = row['Transaction Reference']
        logger.debug('transaction_ref[%s]' % transaction_ref)

        withdrawn_at = row['Withdrawn at']
        logger.debug('withdrawn_at[%s]' % withdrawn_at)

        deposit_inr = row['Deposit (INR)']
        logger.debug('deposit_inr[%s]' % deposit_inr)

        withdrawal_inr = row['Withdrawal (INR)']
        logger.debug('withdrawal_inr[%s]' % withdrawal_inr)

        availalbe_balance = row['Available Balance (INR)']
        logger.debug('availalbe_balance[%s]' % availalbe_balance)

        if deposit_inr == 0:
            (credited_date, debited_date, diff_time, debit_timestamp) = (transaction_date, 0, 0, pd.to_datetime(transaction_date, dayfirst=True)) #  datetime.strptime(transaction_date, "%d/%m/%Y").timestamp())
        else:
            (credited_date, debited_date, diff_time) = (0, transaction_date, debit_timestamp - pd.to_datetime(transaction_date, dayfirst=True)) # datetime.strptime(transaction_date, "%d/%m/%Y").timestamp())
        logger.debug('credited_date[%s]' % credited_date)
        logger.debug('debited_date[%s]' % debited_date)
        logger.debug('diff_time[%s]' % diff_time)
        
        #csv_buffer.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(serial_no, mandal_name, bo_name, so_name, jobcard_id, account_holder_name, credited_date, debited_date, withdrawal_inr, availalbe_balance, diff_time))
        data = data.append({'S.No': serial_no, 'Mandal Name': mandal_name, 'Gram Panchayat': panchayat_name, 'Village': village_name, 'Job card number/worker ID': jobcard_id, 'Name of the wageseeker': account_holder_name, 'Credited Date': credited_date, 'Deposit (INR)': deposit_inr, 'Debited Date': debited_date, 'Withdrawal (INR)': withdrawal_inr, 'Available Balance (INR)': availalbe_balance, 'Diff. time credit and debit': diff_time}, ignore_index=True)

    data = data.set_index('S.No')
    data = data.iloc[::-1]  # Reverse the order back to normal        
    logger.info('The final table:\n%s' % data)

    return data
    '''

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = loggerFetch('info')
        self.logger.info('BEGIN PROCESSING...')

    def tearDown(self):
        self.logger.info('...END PROCESSING')

    def test_printify(self):
        dirname = 'Jawaja'
        dirname = 'Dewata'
        for filename in os.listdir(dirname):
            result = printify(self.logger, filename=os.path.join(dirname,filename), max_width=30)
        self.assertEqual(result, 'SUCCESS')
        
if __name__ == '__main__':
    unittest.main()
