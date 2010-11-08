Comcast Bandwidth
=================

As the repo states, it's a script to login to comcast's website and find your current bandwidth usage. I hate using Comcast's website and I haven't seem to found any automatic notifications for when you come near your 250GB limit.

Now you can setup a cronjob and get daily/weekly stats emailed to you.

Requirements
-----
[mechanize library](http://wwwsearch.sourceforge.net/mechanize/)

Usage
-----
You need to edit the SETTINGS at the top of the file to insert your comcast username/password.
Then 'python comcast-bw.py'

Usage: comcastBandwidth [-v[v]] [-w]

Logging:
    -v or -vv       Add more Vs for more verbosity!

Warn Mode
    -w --warn=NUM   Only output if usage above NUM GB (default is 200GB)

Broken?
-------
I've tested this with my username/account. Comcast's website makes extensive use of "preloading" and redirects, which are stupid and why I hate using it, but I may not have caught every possible combination. 

If you run the script with '-v' flag, you can get python logging to figure out where it's broken.

If you run the script with '-vv' flag, you can get mechanize debug for all request/responses and python logging.
