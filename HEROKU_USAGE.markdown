#Heroku Usage
Assuming you have a working Heroku account and have the Heroku gem already setup, setting up a free Python server to run this script is easy. Follow the commands below:

	# with this repository checked out, create a new machine
	heroku create --stack cedar

	# push this repo
	git push heroku master

	# add the sendgrid email addon
	heroku addons:add sendgrid:starter

	# now setup your Comcast info, for the comcastBandwidth.py script
	heroku config:add USERNAME="USER@comcast.net"
	heroku config:add PASSWORD="PASSWORD"

	# and the email address you want notifications to go to
	heroku config:add CRON_EMAIL="NOTIFYEMAIL"

	# now test things and you should get an email shortly!
	heroku run fab email_usage

	# assuming the last step worked, add the Scheduler addon
	# to automatically run this script daily
	heroku addons:add scheduler

    # open heroku to configure the Scheduler addon
	heroku addons:open scheduler

From here, you should only have to add the appropriate task:

    task 'fab email_usage' with the 'daily' setting to get daily emails of your usage

or

    task 'fab email_usage_warn` with the 'daily' setting to run the script daily, but
    only get emails once you pass 200GB

I find the email_usage_warn is best because you can forget about your usage until it matters. You can configure the bandwidth limit to whatever you like if you dig into the fabric file.

Welcome to automated bandwidth monitoring!
