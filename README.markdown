Comcast Bandwidth
=================

As the repo states, it's a script to login to Comcast's website and find your current bandwidth usage. I hate using Comcast's website and I haven't seem to found any automatic notifications for when you come near your 250GB limit.

Now you can setup a cronjob and get daily/weekly stats emailed to you.

Requirements
-----
* Python 2.6/2.7
* [mechanize library](http://wwwsearch.sourceforge.net/mechanize/)

For most OSX/Linux machines, easy_install will install mechanize for you (might require sudo)

    easy_install mechanize

Usage
-----
First, you need to add your Comcast Email and password, by editing the settings at top of the `comcastBandwidth.py` file.

Then run 'python comcastBandwidth.py' to get your current bandwidth usage.

    Usage: comcastBandwidth [-v[v]] [-w]
    
    Logging:
        -v or -vv       Add more Vs for more verbosity!
    
    Warn Mode
        -w --warn=NUM   Only output if usage above NUM GB (default is 200GB)
        
Cron Usage
-----
This script can be setup to only output if usage is over 200GB (the -w flag default). Therefore, you can run the script nightly and only get warnings once you get close to limit, for the month.

    0 0 * * * /home/askedrelic/code/comcast-bw/comcastBandwidth.py -w

Broken?
-------
I've tested this with my username/account. Comcast's website makes extensive use of "preloading" and redirects, which are stupid and why I hate using it, but I may not have caught every possible combination. 

If you run the script with '-v' flag, you can get python logging to figure out where it's broken.

If you run the script with '-vv' flag, you can get mechanize debug for all request/responses and python logging.
