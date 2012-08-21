#Comcast Bandwidth

This is a script to login to Comcast's website and find your current bandwidth
usage. I hate using Comcast's website and this is an easy way to automate that
process.

Now, you can setup a cronjob and get daily or weekly stats emailed to you.

##
History: As of sometime mid 2012, Comcast appears to have stopped limiting bandwidth usage, see http://www.engadget.com/2012/05/17/comcast-rethinks-bandwidth-caps-trials-two-new-policies-that-in/
There appears to be a "Note:enforcement of the 250GB data consumption threshold is currently suspended" on my page, so you probably don't need to worry about your bandwidth usage anymore.

##Requirements

* Python 2.6/2.7
* [mechanize library](http://wwwsearch.sourceforge.net/mechanize/)
* If using Android notifications, [pynma library](https://github.com/uskr/pynma)

For most OSX/Linux machines, easy_install will install mechanize for you (might require sudo)

    easy_install mechanize

##Usage
First, you need to create a `config.ini` file or copy from the `config.ini.sample` The file should be in following format:

    [comcast]
    username = USER@comcast.net
    password = PASSWORD

    [notify_my_android]
    api = KEY

Then run 'python comcastBandwidth.py' to get your current bandwidth usage.

    Usage: comcastBandwidth [-v[v]] [-w] [--warn-num=NUM] [-a]

	Options:
  	-h, --help       show this help message and exit
  	-v, --verbose    Print status messages to the display
  	--vv             Print status messages to the display in more detail
  	-w               Only output if usage above given value  [default: 200gb]
  	--warn-num=WARN  Max usage before alerting [default: 200gb]
  	-a, --alert      Sends an alert via Notify My Android
        
##Cron Usage
This script can be setup to only output or send an alert if usage is over 200GB
(the -w flag default). Therefore, you can run the script nightly and only get
warnings once you get close to limit, for the month. 

###Warnings

    0 0 * * * /home/askedrelic/code/comcast-bw/comcastBandwidth.py -w

###Warnings With Android Notifications

    0 0 * * * /home/askedrelic/code/comcast-bw/comcastBandwidth.py -w -a

##Heroku Usage
Don't have a server running 24x7? Run this script *for free*, once a day, on a Heroku server. See the [HEROKU_USAGE.md](https://github.com/askedrelic/comcast-bw/blob/master/HEROKU_USAGE.markdown) file

##Anything Broken?
I've tested this with my username/account. Comcast's website makes extensive
use of "preloading" and redirects, which are stupid and why I hate using it,
but I may not have caught every possible combination. 

If you run the script with '-v' flag, you can get python logging to figure out
where it's broken.

If you run the script with '-vv' flag, you can get mechanize debug for all
request/responses and python logging.
