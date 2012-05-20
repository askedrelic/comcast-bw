#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import os

import commands

username = os.environ['SENDGRID_USERNAME']
password = os.environ['SENDGRID_PASSWORD']
to_email = os.environ['CRON_EMAIL']

def send_email(email_msg):
    print "Running cron at %s" % datetime.datetime.now()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Comcast Bandwidth Usage"
    msg['From'] = username
    msg['To'] = to_email
    msg.attach(MIMEText(email_msg, 'plain'))

    s = smtplib.SMTP('smtp.sendgrid.net', 587)
    s.login(username, password)
    s.sendmail(username, to_email, msg.as_string())
    s.quit()                  

@task
def send():
    output = commands.getoutput('python comcastBandwidth.py')
    send_email(output)
