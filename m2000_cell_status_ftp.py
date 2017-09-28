<<<<<<< HEAD
#!/usr/bin/python
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2015 Kiev, Ukraine'
__version__ = "4.0.0"
__status__ = "Production"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import re
from ftplib import FTP
import datetime
import logging_mail
from constans import *


def connect_ftp(hostname=HOST, username=USER, password=PASSWD):
  '''connect to ftp-server specified in arguments.
  if no arguments specified than uses defaults values from constants '''
  global ftp
  try:
    ftp = FTP(hostname, timeout=15)
  except:
    logger.critical('Cannot reach FTP-server: %s', hostname)
    logging_mail.send('Cannot reach FTP-server: %s %s' % (HOST, EMAIL_TEXT))
    raise
  logger.info('*** Connected to host: %s ***', hostname)
  try:
    ftp.set_pasv(True)
  except:
    logger.critical('Cannot change ftp mode to passive: %s', ftp.set_pasv)
    logging_mail.send('Cannot change ftp mode to passive: %s %s %s' % (HOST, ftp.set_pasv, EMAIL_TEXT))
    raise
  try:
    ftp.login(username, password)
  except: 
    logger.critical('Cannot login to ftp server: %s', hostname)
    logging_mail.send('Cannot login to FTP-server: %s %s' % (HOST, EMAIL_TEXT))
    raise
  return ftp
 
  
def cwd_ftp_dir(dir):
  """ Enter to the folders, calculates needed further folder and executing a download function"""
  global dirname
  dirname = dir 
  try:
      ftp.cwd(dirname)
  except:
      logger.critical('Error changing to ftp directory %s', dirname)
      logging_mail.send('Error changing to ftp directory: %s %s' % (dirname, EMAIL_TEXT))
  logger.info('*** Listed the directory: %s', dirname)
      
  if dirname == '/opt/oss/server/var/fileint/cm/Report':
      logger.info('You are within of: %s', ftp.pwd())
      try:
        list_of_items = ftp.nlst()
      except:
        logger.critical('An exception occurs during list of ftp dir: %s', dirname)
        logging_mail.send('An exception occurs during list of ftp dir: %s %s' % (dirname, EMAIL_TEXT))
        raise

      # to download only 1 GSM file with maximum date at filename
      logger.debug('HOUR: %s', HOUR)
      needed_file_name = get_needed_filename(list_of_items, '2g')
      if needed_file_name is None:
        logger.critical('The function get_needed_filename occurs TypeError exeption')
        logging_mail.send('The function get_needed_filename 2g returns None. GSM/UMTS data will not be updated: %s' % (EMAIL_TEXT))
        exit(1)
        
      logger.info('I will download the 2g file from ftp')
      logger.info('needed_file_name: %s', needed_file_name)
      download_from_ftp(needed_file_name, '2g')
      
      # to download only 1 UMTS file with maximum date at filename
      logger.debug('HOUR: %s', HOUR)
      needed_file_name = get_needed_filename(list_of_items, '3g')
      if needed_file_name is None:
        logger.critical('The function get_needed_filename occurs TypeError exeption')
        logging_mail.send('The function get_needed_filename 2g returns None. GSM/UMTS data will not be updated: %s' % (EMAIL_TEXT))
        exit(1)
      logger.info('I will download the 3g file from ftp')
      logger.info('needed_file_name: %s', needed_file_name)
      download_from_ftp(needed_file_name, '3g')
      
          
def download_from_ftp(needed_file_name, type_of_network):
  """ for downloading max 2g or 3g files and modifies filenames """
  global needed_2g_file_name
  global needed_3g_file_name
  filename = needed_file_name
  if type_of_network == '2g':
     TO_COPY_DIR = TO_COPY_DIR_2G
     needed_2g_file_name = filename.replace(' ', '_')
  elif type_of_network == '3g':  #3g file
       TO_COPY_DIR = TO_COPY_DIR_3G
       needed_3g_file_name = filename.replace(' ', '_')
  else:
       logger.critical('Its matched but I couldt find nighter Report_GSM nor Report_UMTS at filename')
       logging_mail.send('Its matched but I couldt find nighter Report_GSM nor Report_UMTS at filename %s' % (EMAIL_TEXT))
  filename_new = filename.replace(' ', '_')
  ftp.retrbinary('RETR %s' % filename, open(TO_COPY_DIR+filename_new, 'w').write)
  logger.info('file: %s  --> %s %s copied. ', filename, TO_COPY_DIR, filename_new )
         

def get_needed_filename(list_of_items, type_of_network):
    """this function finds the file within of /opt/oss/server/var/fileint/cm/Report'
    where the max date and returns one this file"""
    pattern = HOUR + '_' + YEAR + MONTH + DAY
    logger.info('Pattern is %s', pattern )
    for each_item in list_of_items:
        match = re.findall(pattern, each_item) ##Report_GSM_Cell_Report_gsm_cell_status_report_hour_15_20150722.csv - hours-year-month-day
        if match:
            if type_of_network == '2g':
                match2 = re.match(r'Report_GSM', each_item)
                if match2:
                    needed_file_name = each_item
                    return needed_file_name
            elif type_of_network == '3g':
                match2 = re.match(r'Report_UMTS', each_item)
                if match2:
                    needed_file_name = each_item
                    return needed_file_name
            else:
                logger.critical('There is not set type_of_network to 2g or 3g!!!')
=======
#!/usr/bin/python
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2015 Kiev, Ukraine'
__version__ = "4.0.0"
__status__ = "Testing"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import re
from ftplib import FTP
import datetime
import logging_mail
from constans import *


def connect_ftp(hostname=HOST, username=USER, password=PASSWD):
  '''connect to ftp-server specified in arguments.
  if no arguments specified than uses defaults values from constants '''
  global ftp
  try:
    ftp = FTP(hostname, timeout=15)
  except:
    logger.critical('Cannot reach FTP-server: %s', hostname)
    logging_mail.send('Cannot reach FTP-server: %s %s' % (HOST, EMAIL_TEXT))
    raise
  logger.info('*** Connected to host: %s ***', hostname)
  try:
    ftp.set_pasv(True)
  except:
    logger.critical('Cannot change ftp mode to passive: %s', ftp.set_pasv)
    logging_mail.send('Cannot change ftp mode to passive: %s %s %s' % (HOST, ftp.set_pasv, EMAIL_TEXT))
    raise
  try:
    ftp.login(username, password)
  except: 
    logger.critical('Cannot login to ftp server: %s', hostname)
    logging_mail.send('Cannot login to FTP-server: %s %s' % (HOST, EMAIL_TEXT))
    raise
  return ftp
 
  
def cwd_ftp_dir(dir):
  """ Enter to the folders, calculates needed further folder and executing a download function"""
  global dirname
  dirname = dir 
  try:
      ftp.cwd(dirname)
  except:
      logger.critical('Error changing to ftp directory %s', dirname)
      logging_mail.send('Error changing to ftp directory: %s %s' % (dirname, EMAIL_TEXT))
  logger.info('*** Listed the directory: %s', dirname)
      
  if dirname == '/opt/oss/server/var/fileint/cm/Report':
      logger.info('You are within of: %s', ftp.pwd())
      try:
        list_of_items = ftp.nlst()
      except:
        logger.critical('An exception occurs during list of ftp dir: %s', dirname)
        logging_mail.send('An exception occurs during list of ftp dir: %s %s' % (dirname, EMAIL_TEXT))
        raise

      # to download only 1 GSM file with maximum date at filename
      logger.debug('HOUR: %s', HOUR)
      needed_file_name = get_needed_filename(list_of_items, '2g')
      if needed_file_name is None:
        logger.critical('The function get_needed_filename occurs TypeError exeption')
        logging_mail.send('The function get_needed_filename 2g returns None. GSM/UMTS data will not be updated: %s' % (EMAIL_TEXT))
        exit(1)
        
      logger.info('I will download the 2g file from ftp')
      logger.info('needed_file_name: %s', needed_file_name)
      download_from_ftp(needed_file_name, '2g')
      
      # to download only 1 UMTS file with maximum date at filename
      logger.debug('HOUR: %s', HOUR)
      needed_file_name = get_needed_filename(list_of_items, '3g')
      if needed_file_name is None:
        logger.critical('The function get_needed_filename occurs TypeError exeption')
        logging_mail.send('The function get_needed_filename 2g returns None. GSM/UMTS data will not be updated: %s' % (EMAIL_TEXT))
        exit(1)
      logger.info('I will download the 3g file from ftp')
      logger.info('needed_file_name: %s', needed_file_name)
      download_from_ftp(needed_file_name, '3g')
      
          
def download_from_ftp(needed_file_name, type_of_network):
  """ for downloading max 2g or 3g files and modifies filenames """
  global needed_2g_file_name
  global needed_3g_file_name
  filename = needed_file_name
  if type_of_network == '2g':
     TO_COPY_DIR = TO_COPY_DIR_2G
     needed_2g_file_name = filename.replace(' ', '_')
  elif type_of_network == '3g':  #3g file
       TO_COPY_DIR = TO_COPY_DIR_3G
       needed_3g_file_name = filename.replace(' ', '_')
  else:
       logger.critical('Its matched but I couldt find nighter Report_GSM nor Report_UMTS at filename')
       logging_mail.send('Its matched but I couldt find nighter Report_GSM nor Report_UMTS at filename %s' % (EMAIL_TEXT))
  filename_new = filename.replace(' ', '_')
  ftp.retrbinary('RETR %s' % filename, open(TO_COPY_DIR+filename_new, 'w').write)
  logger.info('file: %s  --> %s %s copied. ', filename, TO_COPY_DIR, filename_new )
         

def get_needed_filename(list_of_items, type_of_network):
    """this function finds the file within of /opt/oss/server/var/fileint/cm/Report'
    where the max date and returns one this file"""
    pattern = HOUR + '_' + YEAR + MONTH + DAY
    logger.info('Pattern is %s', pattern )
    for each_item in list_of_items:
        match = re.findall(pattern, each_item) ##Report_GSM_Cell_Report_gsm_cell_status_report_hour_15_20150722.csv - hours-year-month-day
        if match:
            if type_of_network == '2g':
                match2 = re.match(r'Report_GSM', each_item)
                if match2:
                    needed_file_name = each_item
                    return needed_file_name
            elif type_of_network == '3g':
                match2 = re.match(r'Report_UMTS', each_item)
                if match2:
                    needed_file_name = each_item
                    return needed_file_name
            else:
                logger.critical('There is not set type_of_network to 2g or 3g!!!')
>>>>>>> a01a82db9374aac49ddf36acddfb9faa13eeb2ef
                logging_mail.send('There is not set type_of_network to 2g or 3g!!! %s' % (EMAIL_TEXT))