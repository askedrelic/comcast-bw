#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
comcast-bw.py v1.0
Matt Behrens <askedrelic@gmail.com> http://asktherelic.com

Script to login to comcast's website and find your current bandwidth usage.
"""

import calendar
import cookielib
import datetime
import logging
import mechanize
import os
import sys
import urlparse
import warnings
from optparse import OptionParser

try:
    from pynma import PyNMA
    has_pynma = True
except:
    has_pynma = False

from ConfigParser import SafeConfigParser

class Comcast(object):
    def __init__(self, verbose, username, password):
        self.username = username
        self.password = password
        self.verbose = verbose

    def currentUsage(self):
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Logger
        log = logging.getLogger(__name__)

        # Browser options
        br.set_handle_equiv(True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        if self.verbose:
            console = logging.StreamHandler()
            log.addHandler(console)
            log.setLevel(logging.INFO)
        if self.verbose > 1:
            br.set_debug_http(True)
            br.set_debug_redirects(True)
            br.set_debug_responses(True)

        # Set a reasonably current User-Agent
        br.addheaders = [('User-agent',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US)'
            'AppleWebKit/534.10 (KHTML, like Gecko)'
            'Chrome/8.0.552.11 Safari/534.10')]

        # 1. Head to Login page
        br.open('https://customer.comcast.com/Public/Home.aspx')
        log.info('Loading sign in page')
        sign_link = br.find_link(text="Sign In")
        br.follow_link(sign_link)
        br.select_form(nr=0)
        br["user"] = self.username
        br["passwd"] = self.password
        br.submit()

        # Head to customer homepage, resubmit to get past preloader page
        log.info('Loading redirect to customer homepage')
        br.select_form(nr=0)
        br.submit()

        # 2. Head to customer homepage
        log.info('Skipping loading homepage')
        #br.open('https://customer.comcast.com/Public/Home.aspx')

        # then force preload
        #br.open('https://customer.comcast.com/Secure/Preload.aspx?backTo=%2fSecure%2fHome.aspx&preload=true')


        # 3. Head to users&settings
        log.info('Loading users&settings page')
        br.open('https://customer.comcast.com/Secure/Users.aspx')

        br.open('https://customer.comcast.com/Secure/Preload.aspx?backTo=%2fSecure%2fUsers.aspx&preload=true')

        br.open('https://customer.comcast.com/Secure/Users.aspx')

        log.info('Checking for bandwidth details link')
        # Head to bandwidth details page
        try:
            br.find_link(text="View details")
        except mechanize.LinkNotFoundError:
            import sys
            sys.exit("Looks like you don't have a bandwidth details page. Bummer :(")

        log.info('Loading bandwidth details page')
        details = br.find_link(text="View details")
        resp = br.follow_link(details)

        details_link = resp.geturl()

        # Check if link is a preload page and actually follow the preload url,
        # because this preload url seems unique/generated
        #if(details_link.lower().find('preload') != -1):
            #l = urlparse.urlparse(details_link)
            #url = urlparse.parse_qsl(l.query)[0][1]
            #link = urlparse.urljoin(l.geturl(), url)

        resp = br.open(details_link)
        log.info('Loaded details page')
        details_page = resp.read()
        usage_span = 'UsedForThisDevice'
        span_start = details_page.find(usage_span)
        start = details_page.find('>', span_start) + 1
        end = details_page.find('<', start)

        used_bandwidth = details_page[start:end]

        #strip GB counter and check for 0 usage
        try:
            return int(used_bandwidth[:-2])
        except ValueError:
            return 0

    @staticmethod
    def dateText():
        #current date
        date = datetime.date.today()
        #current day text
        days = str(date.day) + " day"
        #get total days in this month
        days_in_month = str(calendar.monthrange(date.year, date.month)[1] - date.day) + " day"
        if days > 1:
            days += 's'
        if days_in_month > 1:
            days_in_month += 's'
        return days + ", with %s remaining in this month" % days_in_month

def sendAlert(key, usage, date):
    if not has_pynma:
        raise ImportError("No module named PyNMA ")
    global p
    pkey = None

    p = PyNMA()
    p.addkey(key)

    message = "You have used %sGB bandwidth in %s" % (usage,date)
    res = p.push("Comcast Bandwidth Check", 'Daily Update', message, 'http://misfoc.us', batch_mode=False)

if __name__ == '__main__':
    ### Settings ###
    # configure through system variables or config.ini
    if os.environ.has_key('USERNAME') and os.environ.has_key('PASSWORD'):
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        nma_api_key = os.environ.get('NMA_API_KEY', '')
    else:
        parser = SafeConfigParser()
        if os.path.isfile('config.ini'):
            parser.read('config.ini')
        else:
            print "It looks like you are missing a config.ini file!"
            print "Create one using the config.ini.sample"
            raise SystemExit
        username = parser.get('comcast', 'username')
        password = parser.get('comcast', 'password')
        nma_api_key = parser.get('notify_my_android', 'api')

    # Get command line options
    args = sys.argv[1:]

    usage = "Usage: comcastBandwidth [-v[v]] [-w] [--warn-num=NUM] [-a]"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
                    action="store_true",
                    dest="verbose",
                    default=False,
                    help="Print status messages to the display")
    parser.add_option("--vv",
                    action="store_true",
                    dest="really_verbose",
                    default=False,
                    help="Print status messages to the display in more detail")
    parser.add_option("-w",
                    action="store_true",
                    dest="warnMode",
                    default=False,
                    help="Only output if usage above given value"
                         "  [default: 200GB]")
    parser.add_option("--warn-num",
                    dest="warn",
                    default="200",
                    help="Max usage before alerting"
                         " [default: %defaultGB]")
    parser.add_option("-a", "--alert",
                    action="store_true",
                    dest="alert",
                    default=False,
                    help="Sends an alert via Notify My Android")

    (options, args) = parser.parse_args()

    verbose = 0
    if options.verbose:
        verbose = 1
    if options.really_verbose:
        verbose = 2

    warnMode = options.warnMode
    warn = options.warn
    alert = options.alert

    comcast = Comcast(verbose,username,password)
    usage = comcast.currentUsage()

    #Quit if warn flag is set
    if warnMode and (usage < warn):
        raise SystemExit

    print "You have used %sGB bandwidth in %s." % (usage,Comcast.dateText())

    if alert:
        sendAlert(nma_api_key, usage, Comcast.dateText())
