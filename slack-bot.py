import json
import time
import myql
import requests
from yahoo_oauth import OAuth1

def strip_emojis(string):
        return string[:string.find('/')]

def post_to_slack(message):
	request = requests.post(slackUrl, headers={"Content-type": "application/json"}, json={"text":message})
	respStatus = str(request.status_code) + request.reason
	print(respStatus)
	return respStatus

def get_add_drop_slack_message(data):
	message = '[add/drop]\n'
	for player in data['players']['player']:
		playerName = player['name']['full']
		playerTeam = player['editorial_team_abbr']
		playerPos = player['display_position']
		if player['transaction_data']['type']=="add":
			team = player['transaction_data']['destination_team_name']
			message = message + ':heavy_plus_sign: *{}* added *{}* ({} - {}) \n'.format(team, playerName, playerTeam, playerPos)
		else:
			team = player['transaction_data']['source_team_name']
			message = message + ':heavy_minus_sign: *{}* dropped *{}* ({} - {}) \n'.format(team, playerName, playerTeam, playerPos)
	message = message + '<https://football.fantasysports.yahoo.com/f1/28709/transactions|Check here> if you don\'t believe me \n'
	print('time: {} \n '.format(formattedTime) + message)
	return message

def get_trade_slack_message(data):
	message = '[trade]\n'
	for player in data['players']['player']:
		playerName = player['name']['full']
		playerTeam = player['editorial_team_abbr']
		playerPos = player['display_position']
		sourceTeam = player['transaction_data']['source_team_name']
		destTeam = player['transaction_data']['destination_team_name']
		message = message + ':heavy_exclamation_mark: *{}* traded *{}* ({} - {}) to *{}* \n'.format(sourceTeam, playerName, playerTeam, playerPos, destTeam)
	message = message + '<https://football.fantasysports.yahoo.com/f1/28709/transactions|Check here> if you don\'t believe me \n'
	print('time: {} \n '.format(formattedTime) + message)
	return message

def check_if_new_transaction(data):
	isNew = True
	for oldTransaction in oldTransactions:
		if data['transaction_key'] == str(oldTransaction['transaction_key']):
			isNew = False
			break
	return isNew

def check_if_recent(data):
	compareTime = currentTime - 1800
	isRecent = float(transaction['timestamp']) > compareTime
	return isRecent


if __name__ == '__main__':
	currentTime = time.time()
	formattedTime = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(currentTime))

	# TODO: this needs to be updated with your actual webhook
	#slackUrl = 'put-your-slack-webhook-url-here'

	oauth = OAuth1(None, None, from_file='/home/ec2-user/yahoo-fantasy-football-slack-app/resources/credentials.json')
	if not oauth.token_is_valid():
		oauth.refresh_access_token()
	yql = myql.MYQL(format='json',oauth=oauth)
	resp = yql.raw_query('select * from fantasysports.leagues.transactions where league_key="nfl.l.28709"')
	json_response = json.loads(resp.content.decode(resp.encoding))
	transactions = json_response['query']['results']['league']['transactions']['transaction']

	with open('/home/ec2-user/yahoo-fantasy-football-slack-app/resources/old-transactions.json', 'r') as thefile:
                oldTransactions = json.load(thefile)
	with open('/home/ec2-user/yahoo-fantasy-football-slack-app/resources/old-transactions.json', 'w') as thefile:
        	json.dump(transactions, thefile)

	for transaction in transactions:
		isNew = check_if_new_transaction(transaction)
		#isRecent = check_if_recent(transaction)
		if transaction['type']=="add/drop" and isNew:
			message = get_add_drop_slack_message(transaction)
			post_to_slack(message)
		elif transaction['type']=="trade" and isNew:
			message = get_trade_slack_message(transaction)
			post_to_slack(message)
