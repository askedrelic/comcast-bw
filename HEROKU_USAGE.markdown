#Heroku Usage
Assuming you have a working Heroku account and have the Heroku gem already setup, setting up a free Python server to run this script is easy. Follow the commands below:

	#with this repository checked out, create a new machine
	heroku create --stack cedar
	
	#push this repo
	git push heroku master

	#add the sendgrid email addon
	heroku addons:add sendgrid:starter

	#now setup your Comcast info, for the comcastBandwidth.py script
	heroku config:add USERNAME="USER@comcast.net"
	heroku config:add PASSWORD="PASSWORD"

	#and the email address you want notifications to go to
	heroku config:add CRON_EMAIL="NOTIFYEMAIL"
	
	#now test things and you should get an email shortly!
	heroku run rake cron
	
	#assuming the last step worked, add the cron addon to
	#check your bandwidth and get emails once a daily
	heroku addons:add cron:daily

Once everything is in place, you will have to edit the Rakefile manually to set the warning flag and only receive notifications if you are over 200GB.