import os
import logging
import requests
import json
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from cadocs import Cadocs
from datetime import date
from utils import CadocsIntents



# TODO: ricreare app slack coi permessi giusti e mettere informazioni confidenziali nell'env 

conversation = []

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
    conversation.append(event)
    #print(conversation)
    # check wether or not the message has been written by the bot (we dont have to answer)
    if event.get('bot_id') is None:
        # get the user's name to print it in answer
        req_user = slack_web_client.users_info(user=event.get('user'))
        user = req_user.get('user')
        # Get the text written in chat
        text = event.get("text")
        # Get the channel used by the writer in order to write back in it
        channel = event.get('channel')
        # ask the chatbot for an answer
        response, results, entities, intent = cadocs.new_message(text, channel, user)
        if(intent == CadocsIntents.GetSmells and results != None):
            cadocs.save_execution(results, "Community Smell Detection", date.today().strftime("%d/%m/%Y"), entities[0], user.get('id'))
        # post the answer message in chat
        return slack_web_client.chat_postMessage(**response)

if __name__ == "__main__":

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(port=5002, threaded=True)