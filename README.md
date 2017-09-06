# yahoo-fantasy-football-slack-app

slack-bot.py uses mYQL which is a wrapper for Yahoo!'s YQL API which queries their databases for data such as fantasy football transactions.

Everything is currently hard-coded for my application at this point to pull transactions for my league and posts to my Slack channel.

The plan is to make this more configurable for others to use in the future

This is currently deployed for my use case on an AWS EC2 instance and running as a cron job every minute

# Resources
mYQL: https://github.com/josuebrunel/myql

YQL: https://developer.yahoo.com/yql/

# Pre-Reqs

### YDN
You need to have registered on the Yahoo Developer Network and created an app.  

YDN: https://developer.yahoo.com/

Those credentials should then be added to the resources/credentials.json file.

  #### Example credentials.json file
  
  {
  
    "consumer_key": "my-longer-consumer-key-of-random-characters", 
    "consumer_secret": "my-shorter-consumer-secret"
  
  }
  
The first time the script is ran, you will probably need to do it manually to complete the 2-factor auth

### Slack
You need to create a Slack webhook for your channel

Slack web-hook info: https://api.slack.com/incoming-webhooks

# To Run:
$ pip install myql

$ git clone https://github.com/balsitisdj/yahoo-fantasy-football-slack-app.git

$ cd yahoo-fantasy-football-slack-app

$ python slack-bot.py
