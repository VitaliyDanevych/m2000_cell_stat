#!/usr/bin/python
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2015 Kiev, Ukraine'
__version__ = "4.0.0"
__status__ = "Production"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import datetime
import logging
import logging.handlers


HOST = '1.3.1.1'
USER = 'ftpuser'
PASSWD = 'ftppasswd'
TO_COPY_DIR_2G = '/home/na_scripts/m2000_cell_status/version_4_hithub/2g_cell_report/'
TO_COPY_DIR_3G = '/home/na_scripts/m2000_cell_status/version_4_hithub/3g_cell_report/'
HOUR = datetime.datetime.now().strftime("%H")  #14
DAY = datetime.datetime.now().strftime("%d")
MONTH = datetime.datetime.now().strftime("%m")
YEAR = datetime.datetime.now().strftime("%Y")
localtime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

#db_user, db_passwd, db_host_sid = ('configuration','config_pass','10.1.1.2:1521/optimus') # optimus7
db_user, db_passwd, db_host_sid = ('configuration','config_pass','10.1.1.1:1521/optimus') # optimus6

LOG_FILENAME = 'm2000_cell_status.log'
EMAIL_TEXT = """ The script into folder /home/na_scripts/m2000_cell_status/version_3 on 10.1.32.100 host has
                 detected an exception which affect its normal work. The data at configuration.m2000_2g_cell_status@optimus7
                 and configuration.m2000_3g_cell_status@optima7 might be not updated.
                 Please, check debug log %s into mentioned folder and fix this issue
             """ % LOG_FILENAME

MAILHOST = 'smtp.host.ukr'
FROM     = 'm2000_cell_status_script@ora-vx.com'
TO       = ['vitaliy.danevych@test.com.ua']
SUBJECT  = 'The Huawei OSS M2000 script has serious error'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024, backupCount=1)
# Add the log message handler to the logger
#fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.CRITICAL) #ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
