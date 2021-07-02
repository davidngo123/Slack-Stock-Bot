# Main file that contains majority of the bots functionality 

import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

all_users = []


# list of commands
@ app.route('/help', methods=['POST'])
def print_help():
    client.chat_postMessage(
        channel=channel_id, text="hello")
    return Response(), 200


# Get stock price
@ app.route('/price', methods=['POST'])
def get_stock():
    data = request.form
    stock_id = data.get('text_id')
    client.chat_postMessage(
        channel=channel_id, text="hello")
    return Response(), 200

# Get Stock Info
@ app.route('/info', methods=['POST'])
def get_info():
    data = request.form
    stock_id = data.get('text_id')
    client.chat_postMessage(
        channel=channel_id, text="hello")
    return Response(), 200

# Get graph Info
@ app.route('/graph', methods=['POST'])
def print_graph():
    data = request.form
    stock_id = data.get('text_id')
    client.chat_postMessage(
        channel=channel_id, text="hello")
    return Response(), 200

# Schedule


# Run server if we are using this file
if __name__ == "__main__":
    app.run(debug=True)