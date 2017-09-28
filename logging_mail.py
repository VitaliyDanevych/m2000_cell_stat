#!/usr/bin/python
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2017 Kiev, Ukraine'
__version__ = "4.0.0"
__status__ = "Production"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""Test harness for the logging module. Tests BufferingSMTPHandler, an alternative implementation
of SMTPHandler.
Copyright (C) 2001-2002 Vinay Sajip. All Rights Reserved.
"""

import string, logging, logging.handlers
from constans import *


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromaddr, string.join(self.toaddrs, ","), self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    print s
                    msg = msg + s + "\r\n"
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []

            
def send(input_text):
    #if severity.lower() == 'critical' or severity.lower()  == 'error' or severity.lower()  == 'warning' or severity.lower() == 'info' or severity.lower() == 'debug':
    logger_mail = logging.getLogger("")
    logger_mail.setLevel(logging.DEBUG)
    logger_mail.addHandler(BufferingSMTPHandler(MAILHOST, FROM, TO, SUBJECT, 10))
    logger_mail.info(input_text)
    logging.shutdown()
