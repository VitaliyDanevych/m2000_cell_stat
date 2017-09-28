#!/usr/bin/python
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2015 Kiev, Ukraine'
__version__ = "4.0.0"
__status__ = "Production"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import csv
import cx_Oracle
import m2000_cell_status_ftp
import logging_mail
from constans import *


def connection(db_user,db_passwd,db_host_sid):
  global con
  global my_cursor
  logger.info('Start connecting to database')  
  try:
        con = cx_Oracle.connect(db_user, db_passwd, db_host_sid)
  except cx_Oracle.DatabaseError,msg:
        logger.error('The Logon to DB Error occured: %s', msg)
        sys.exit(1) 
  my_cursor = con.cursor()
  try:
        my_cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD.MM.YYYY HH24:MI:SS'")
        my_cursor.execute("ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'DD.MM.YYYY HH24:MI:SS.FF'")
        logger.info("The NLS_DATE_FORMAT and NLS_TIMESTAMP_FORMAT for DB SESSION are SET")
        my_cursor.execute("COMMIT")
  except:
        logger.error('The other error related to DB occured')
        logging_mail.send('There is error ALTER SESSION SET occured!!! %s' % (EMAIL_TEXT))
        my_cursor.execute("ROLLBACK")
        

def insert_sql(filename, type_of_network):
    data_from_db = my_cursor.execute("SELECT TO_TIMESTAMP('09.07.2015 16:30:27') FROM DUAL")
    logger.info('data_from_db: %s', data_from_db)
    logger.info('local_time:  %s', localtime)
    logger.info('the full file path:  %s', filename)
    if type_of_network == '2g':
        s_filename = m2000_cell_status_ftp.needed_2g_file_name
    elif type_of_network == '3g':
        s_filename = m2000_cell_status_ftp.needed_3g_file_name
    else:
        logger.error('There is unknown type of network! not 2G not 3G')
    line_count = 0
    with open(filename, 'rb') as csvfile:  
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            line_count +=1
            if line_count == 1:
                logger.info('I will miss 1st line!')
                continue
            #we need to cut here the lentgh of nodeb_name
            if len(row[2]) > 6:
                temp_row = row[2]
                row[2] = temp_row[:6] # zdes ukorotili do 6 symbols DN2217@DN2217 -> DN2217
            if type_of_network == '2g':
                try:
                    sql = "INSERT INTO m2000_2g_cell_status a (a.insert_time, a.file_name, a.bsc_name, a.site_id, a.site_name, a.cell_id, a.cell_name, a.activity_status, a.ci, a.basei, \
                    a.ni, a.bcchno, a.freqseg, a.blk_status, a.hop_hsn, a.hop_tsc, a.hop_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " \
                    % (localtime, s_filename, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                except:
                     logger.error('The error ocured during 2g sql-statement creation!')
                     logging_mail.send('The error ocured during 2g sql-statement creation! %s %s' % (sql, EMAIL_TEXT))
            elif  type_of_network == '3g':
                try:
                    sql = "INSERT INTO m2000_3g_cell_status a (a.insert_time, a.file_name, a.rnc_name, a.nodeb_id, a.nodeb_name, a.cell_id, a.cell_name, a.activity_status,  a.blk_status, a.lac, \
                    a.sac, a.rac, a.ul_freq, a.dl_freq, a.max_power, a.cellcbsstate, a.cellmbmsstate, a.hsda_opstate, a.hsupa_opstate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " \
                    % (localtime, s_filename, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])
                except:
                    logger.error('The error ocured during 3g sql-statement creation!')
                    logging_mail.send('The error ocured during 3g sql-statement creation! %s %s' % (sql, EMAIL_TEXT))
            else:
                logger.error('There is unknown type of network! not 2G not 3G')
            logger.debug('The number of line: %s', line_count)
            logger.debug('The sql-query: %s', sql)
            try:
                logger.debug('Finish inserting values and commit')
                my_cursor.execute(sql)
                my_cursor.execute("COMMIT")
            except IndexError as msg:
                logger.error('IndexError occured during sql-query ecxecuting: %s %s:' % (msg, sql))
                logging_mail.send('IndexError occured during sql-query ecxecuting: %s %s:' % (msg, EMAIL_TEXT))
                raise
            except cx_Oracle.DatabaseError, msg:
                logger.error('The DB-Error occured during sql-query ecxecuting:  %s' % msg)
                logging_mail.send('The DB-Error occured during sql-query ecxecuting:  %s %s' % (msg, EMAIL_TEXT))
                pass
            except TypeError as msg:
                #except Exception as msg:
                logger.error('The Type-Error occured during sql-query ecxecuting: %s' % msg)
                logging_mail('The Type-Error occured during sql-query ecxecuting: %s %s' % (msg, EMAIL_TEXT))
                my_cursor.execute("ROLLBACK")
            except:
                logger.error('The Unknown Error occured during sql-query ecxecuting:')
                logging_mail('The Unknown Error occured during sql-query ecxecuting: %s' % EMAIL_TEXT)
                my_cursor.execute("ROLLBACK")
                                

def main():
  logger.debug('start program')
  logger.debug('the connect_ftp function has started')  
  m2000_cell_status_ftp.connect_ftp()
  logger.debug('the connect_ftp function has ended') 
  
  logger.debug('the cwd_ftp_dir function has started') 
  m2000_cell_status_ftp.cwd_ftp_dir('/opt/oss/server/var/fileint/cm/Report')
  logger.debug('the cwd_ftp_dir function has ended')
  m2000_cell_status_ftp.ftp.quit()
  
  n2g_path_file = m2000_cell_status_ftp.TO_COPY_DIR_2G + m2000_cell_status_ftp.needed_2g_file_name
  n3g_path_file = m2000_cell_status_ftp.TO_COPY_DIR_3G + m2000_cell_status_ftp.needed_3g_file_name
  logger.info('n2g_path_file: %s, n3g_path_file:  %s', n2g_path_file, n3g_path_file)
  
  logger.debug('the connection function has started') 
  connection(db_user,db_passwd,db_host_sid)
  logger.debug('the connection function has ended') 
  
  logger.debug('the insert_sql function has started 1st time') 
  insert_sql(n2g_path_file, '2g')
  logger.debug('the insert_sql function has ended 1st time')

  logger.debug('the insert_sql function has started 2st time') 
  insert_sql(n3g_path_file, '3g')
  logger.debug('the insert_sql function has ended 2st time')   
  
  logger.info('Close connection to database')  
  con.close()
  logger.debug('end program')
  logging.shutdown()  
  
if __name__ == '__main__':
    main()
