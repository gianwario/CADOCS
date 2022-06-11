import os
import logging
import requests
import json
import threading
from flask import Flask, request, json, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from cadocs import Cadocs
from datetime import date
from utils import CadocsIntents
from dotenv import load_dotenv
import time



# Initialize a Flask app to host the events adapter
app = Flask(__name__)
load_dotenv('src/.env')
# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(os.environ.get('SLACK_EVENT_TOKEN',""), "/slack/events", app)
# Create a slack client
slack_web_client = WebClient(token=os.environ.get('SLACK_TOKEN',""))


# create our chatbot instance
cadocs = Cadocs()

# This event will fire up every time there is a new message on a chat with the bot invited
@slack_events_adapter.on("message")
def answer(payload):
    # starting a new thread for doing the actual processing    
    execution = threading.Thread(
            target=handle_request,
            args=(payload,)
        )
    execution.start()
    response = make_response("", 200)
    response.headers['X-Slack-No-Retry'] = 1
    return response


def handle_request(payload):  
    # Get the onboarding message payload
    event = payload.get("event", {})
    # print(json.dumps(payload, indent=4, sort_keys=True))
    exec_data = {
        "id" : event.get("client_msg_id"),
        "user" : event.get("user"),
        "text" : event.get("text"),
        "executed" : False,
        "approved" : False
    }
    
    '''
    for e in cadocs.conversation_queue:
        if e["id"] == exec_data["id"] and e["executed"]:
            return {"message":"true"}
    '''         
    # print(conversation)
    # check wether or not the message has been written by the bot (we dont have to answer)
    if event.get('bot_id') is None and event.get('user') is not None and exec_data.get("text") is not '' and exec_data.get('id') is not None:
        # get the user's name to print it in answer
        req_user = slack_web_client.users_info(user=event.get('user'))
        user = req_user.get('user')
        # Get the channel used by the writer in order to write back in it
        channel = event.get('channel')
        # we start the progress
        progress = post_waiting_message(channel)
        # ask the chatbot for an answer
        response, results, entities, intent = cadocs.new_message(exec_data, channel, user)
        # we stop the cat-gress
        progress.do_run = False
        if((intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate) and results != None):
            cadocs.save_execution(results, "Community Smell Detection", date.today().strftime("%m/%d/%Y"), entities[0], user.get('id'))
        if(intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate):
            post_attachments(channel, intent)
        # post the answer message in chat
        slack_web_client.chat_postMessage(**response)
        return {"message":"true"}

@app.route("/slack/action-received", methods=["POST"])
def action_received():
    data = json.loads(request.form["payload"])
    # starting a new thread to do the actual processing    
    x = threading.Thread(
            target=handle_action,
            args=(data,)
        )
    x.start()
    blocks = [{
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": data.get("message").get("blocks")[0].get("text").get("text"),
                    "emoji": True
                }
		    }]
    slack_web_client.chat_update(channel=data.get("channel").get("id"), ts=data.get("message").get("ts"), blocks=blocks)
    response = make_response("", 200)
    response.headers['X-Slack-No-Retry'] = 1
    return response

def handle_action(data):
    # retrieving basic info about the message received
    channel = data.get("channel").get("id")
    user_id = data.get("user").get("id")
    req_user = slack_web_client.users_info(user=user_id)
    user = req_user.get('user')
    action = data.get("actions")[0].get("action_id")
    message_ts = data.get("message").get("ts")
    # if the user who clicked the action button is the one who wrote the original message
    if(user_id == cadocs.asked_user):
        # if the answer is yes
        if(action == "action-yes"):
            # we grab the executions asked by the user
            users_execs = [x for x in cadocs.conversation_queue if x["user"] == user_id]
            exec_data = users_execs[len(users_execs)-1]
            exec_data.update({"approved" : True})
            progress = post_waiting_message(channel)
            # we run the tool
            response, results, entities, intent = cadocs.new_message(exec_data, channel, user)
            req = requests.get("http://localhost:5000/update_dataset?message="+exec_data["text"]+"&intent="+intent.value)
            progress.do_run = False
            if((intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate) and results != None):
                cadocs.save_execution(results, "Community Smell Detection", date.today().strftime("%m/%d/%Y"), entities[0], user_id)

            if(intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate):
                post_attachments(channel, intent)
            # update the answer message in chat
            slack_web_client.chat_update(channel=channel, ts=message_ts, blocks=response.get("blocks"))
            return {"message":"true"}
        elif(action == "action-no"):
            slack_web_client.chat_update(channel=channel, ts=message_ts, blocks=[{
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "We are sorry, we couldn't detect your intent. \nPlease try again with a more specific question.\n If you need help, check our advices in the CADOCS app information",
                    "emoji": True
                }
		    }])


def post_waiting_message(channel):
        # we post the waiting message
        message = slack_web_client.chat_postMessage(**{
        "channel":channel,
        "blocks":[{
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "We are handling your request...",
                        "emoji": True
                    }
                }]
        })
        ts = message.get("ts")
        # we start a thread that tells the user we are running the tool 
        progress = threading.Thread(target=update_waiting_message, args=(channel, ts,))
        progress.start()
        return progress

# this method will show the cat-gress of the execution by updating itself until the main thread stops
def update_waiting_message(channel, ts):
    i = 0
    elapsed_time = 0
    t = threading.currentThread()
    # maximum of about 10 minutes
    while getattr(t, "do_run", True):
        i = i + 1
        emojis = ""
        for j in range(i):
            emojis = emojis +":smile_cat:"
        time.sleep(1)
        elapsed_time += 1
        slack_web_client.chat_update(channel=channel, ts=ts, blocks=[
                    {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "We are handling your request...\n" + emojis + "",
                        "emoji": True
                        }
                    }
                ]
            )
        if i == 7:
            i = 0
    slack_web_client.chat_update(channel=channel, ts=ts, blocks=[
                    {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Your request has been processed :smile_cat:",
                        "emoji": True
                        }
                    }
                ]
            )

def post_attachments(channel, intent):
    files = ["commitCentrality_0.pdf", "Issues_0.pdf", "issuesAndPRsCentrality_0.pdf", "PRs_0.pdf"]
    for f in files:
        if os.path.exists('src/attachments/'+f):
            with open('src/attachments/'+f , "rb"):
                response = slack_web_client.files_upload(
                        channels=channel,
                        file='src/attachments/'+f,
                        title=f,
                        filetype='pdf'
                )
                print(response)


if __name__ == "__main__":
    app.run(port=5002, threaded=True)
