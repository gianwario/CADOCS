import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = ''

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter('', "/slack/events", app)

# Create a slack client
slack_web_client = WebClient(token=SLACK_TOKEN)


# Get the onboarding message payload
message = {
   "channel":"conversational-agent",
   "blocks":[
      {
         "type":"section",
         "text":{
            "type":"mrkdwn",
            "text":"Gianmario sei un maestro"
         }
      }
   ]
}

@slack_events_adapter.on("message")
def answer(payload):
    event = payload.get("event", {})
    text = event.get("text")
    if event.get('bot_id') is None:
        return slack_web_client.chat_postMessage(**message)


if __name__ == "__main__":

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)