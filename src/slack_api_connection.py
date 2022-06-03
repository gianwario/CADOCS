import os
import logging
import requests
import json
import json
import threading
from flask import Flask, request, jsonify, json, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from cadocs import Cadocs
from datetime import date
from utils import CadocsIntents
from dotenv import load_dotenv



# TODO: ricreare app slack coi permessi giusti e mettere informazioni confidenziali nell'env 

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
    x = threading.Thread(
            target=handle_request,
            args=(payload,)
        )
    x.start()
    response = make_response("", 200)
    response.headers['X-Slack-No-Retry'] = 1
    return response


def handle_request(payload):  
    print(json.dumps(payload, indent=4, sort_keys=True))
    print("\n\n\n\n")
    # Get the onboarding message payload
    event = payload.get("event", {})
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
        response, results, entities, intent = cadocs.new_message(exec_data, channel, user)
        if((intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate) and results != None):
            cadocs.save_execution(results, "Community Smell Detection", date.today().strftime("%d/%m/%Y"), entities[0], user.get('id'))
        # post the answer message in chat
        slack_web_client.chat_postMessage(**response)
        return {"message":"true"}

@app.route("/slack/action-received", methods=["POST"])
def action_received():
    data = json.loads(request.form["payload"])
        # starting a new thread for doing the actual processing    
    x = threading.Thread(
            target=handle_action,
            args=(data,)
        )
    x.start()
    response = make_response("", 200)
    response.headers['X-Slack-No-Retry'] = 1
    return response

def handle_action(data):
    channel = data.get("channel").get("id")
    user_id = data.get("user").get("id")
    req_user = slack_web_client.users_info(user=user_id)
    user = req_user.get('user')
    action = data.get("actions")[0].get("action_id")
    if(user_id == cadocs.asked_user):
        if(action == "action-yes"):
            users_execs = [x for x in cadocs.conversation_queue if x["user"] == user_id]
            exec_data = users_execs[len(users_execs)-1]
            exec_data.update({"approved" : True})
            response, results, entities, intent = cadocs.new_message(exec_data, channel, user)
            if((intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate) and results != None):
                cadocs.save_execution(results, "Community Smell Detection", date.today().strftime("%d/%m/%Y"), entities[0], user_id)
            # post the answer message in chat
            slack_web_client.chat_postMessage(**response)
            return {"message":"true"}
        elif(action == "action-no"):
            print("no")

        
if __name__ == "__main__":
    app.run(port=5002, threaded=True)
