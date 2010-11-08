#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
comcast-bw.py
Matt Behrens <askedrelic@gmail.com> http://asktherelic.com

Script to login to comcast's website and find your current bandwidth usage.
"""

import sys
import urlparse
import cookielib
import warnings
import logging
import datetime
import calendar

import mechanize

## SETTINGS
username = "COMCAST USERNAME (username@comcast.net)"
password = "COMCAST PASSWORD"

help_text = """Usage: comcastBandwidth [-v[v]] [-w]

Logging:
    -v or -vv       Add more Vs for more verbosity!

Warn Mode
    -w --warn=NUM   Only output if usage above NUM GB (default is 200GB)

Misc
    -h --help       This text :<"""

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
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.11 Safari/534.10')]

        # Head to Login page
        br.open('https://customer.comcast.com/Public/Home.aspx')
        log.info('Loading sign in page')
        sign_link = br.find_link(text="Sign In")
        br.follow_link(sign_link)
        br.select_form(nr=0)
        br["user"] = self.username
        br["passwd"] = self.password
        br.submit()

        # Head to customer homepage, resubmit to get past preloader page
        log.info('Loading customer homepage, redirect')
        br.select_form(nr=0)
        br.submit()

        # Head to User information page
        br.open('https://customer.comcast.com/Secure/Users.aspx')
        log.info('Loading customer homepage')

        # Head to
        try:
            br.find_link(text="View details")
        except mechanize.LinkNotFoundError:
            import sys
            sys.exit("Looks like you don't have a bandwidth details page. Bummer :(")
        log.info('loading details page')
        details = br.find_link(text="View details")
        resp = br.follow_link(details)

        details_link = resp.geturl()

        # Check if link is a preload page and actually follow the preload url,
        # because this preload url seems unique/generated
        if(details_link.lower().find('preload') != -1):
            l = urlparse.urlparse(details_link)
            url = urlparse.parse_qsl(l.query)[0][1]
            link = urlparse.urljoin(l.geturl(), url)

        resp = br.open(details_link)
        log.info('Loaded details page')
        details_page = resp.read()
        bandwidthDiv = 'UsedWrapper">'
        start = details_page.find(bandwidthDiv) + len(bandwidthDiv)
        end = details_page.find('<', start)

        used_bandwidth = details_page[start:end]

        #strip GB counter and check for 0 usage
        return int(used_bandwidth[:-2]) or 0

    @staticmethod
    def isoCount(size):
        return (size * 1024) / 700

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

if __name__ == '__main__':
    # Get command line options and args and fuck getopt/optparse :<
    args = sys.argv[1:]

    #verbose: 0 for no opts, 1 -v or 2 -v
    verbose = 0
    warn = 200
    warnMode = False
    if len(args) > 1:
        print "One switch at a time."
        raise SystemExit
    elif len(args) == 1:
        opt = args[0]
        if opt == '-v':
            verbose = 1
        elif opt == '-vv':
            verbose = 2
        elif opt == '-w':
            warnMode = True
        elif opt.count('warn'):
            warnMode = True
            try:
                o, a = opt.split('=')
                warn = int(a)
            except:
                print "Warn needs specific number."
                raise SystemExit
        else:
            print help_text
            raise SystemExit

    comcast = Comcast(verbose,username,password)
    usage = comcast.currentUsage()

    #Quit if warn flag is set
    if warnMode and (usage < warn):
        raise SystemExit

    print "You have used %sGB bandwidth in %s" % (usage,Comcast.dateText())
    if (usage < 250):
        print "You can still download %s linux CDs this month!" % Comcast.isoCount(250 - usage)
