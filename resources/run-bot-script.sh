#!/bin/sh

# Simple script to use as cron job on the server
# Scheduled for every minute so using sleep to run every 30 seconds

/usr/bin/python3.5 /home/ec2-user/yahoo-fantasy-football-slack-app/slack-bot.py
sleep 30
/usr/bin/python3.5 /home/ec2-user/yahoo-fantasy-football-slack-app/slack-bot.py
