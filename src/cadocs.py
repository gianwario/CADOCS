import os
import logging
import requests
import json
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from intent_manager import IntentManager
from intent_resolver import IntentResolver
from utils import CadocsIntents

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter('0d19788edc52c4dabd318fd2f6b0ae2c', "/slack/events", app)
# Create a slack client
SLACK_TOKEN = 'xoxb-3537687436610-3550389206065-Qg2pPAEixOyo15Vy4O3G7xgb'
slack_web_client = WebClient(token=SLACK_TOKEN)


# create our chatbot instance
cadocs = Cadocs()


# This event will fire up every time there is a new message on a chat with the bot invited
@slack_events_adapter.on("message")
def answer(payload):
    # Get the onboarding message payload
    event = payload.get("event", {})
    # check wether or not the message has been written by the bot (we dont have to answer)
    if event.get('bot_id') is None:
        # get the user's name to print it in answer
        user = slack_web_client.users_info(user=event.get('user'))
        username = user.get('user').get('profile').get('first_name')
        # Get the text written in chat
        text = event.get("text")
        print(text)
        # Get the channel used by the writer in order to write back in it
        channel = event.get('channel')
        # ask the chatbot for an answer
        message = cadocs.new_message(text, channel, username)
        # post the answer message in chat
        return slack_web_client.chat_postMessage(**message)


class Cadocs:
    def __init__(self):
        return

    def new_message(self, text, channel, username):
        # instantiate the manager which will tell us the intent
        manager = IntentManager()
        # detect the intent
        intent, entities = manager.detect_intent(text)
        # instantiate the resolver
        resolver = IntentResolver()
        # tell the resolver which intent it has to fire 
        results = resolver.resolve_intent(intent, entities)
        # ask a function to create a slack message
        response = resolver.build_message(results, username, channel, intent, entities)
        # build the text of the message based on the results (TODO: generalize)
        return response

    def save_execution(self, results, exec_type, date, repo):
        self.results = results
        self.exec_type = exec_type
        self.date = date
        self.repo = repo
    
    def get_last_execution(self):
        return self.results, self.exec_type, self.date, self.repo
    
if __name__ == "__main__":

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(port=5000)