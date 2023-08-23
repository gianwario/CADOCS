from chatbot.intent_manager import IntentManager
from intent_resolver import IntentResolver
from service.cadocs_messages import build_error_message
from service.utils import CadocsIntents
import json
from os import path
import os
from dotenv import load_dotenv
from service.utils import valid_link, valid_date
load_dotenv('src/.env')

# the Cadocs class contains the logic behind the tool's execution


class Cadocs:

    def __init__(self):
        self.last_repo = ""
        self.asked_user = ""
        # the conversation queue will be used to check whether or not a message has already been answered
        self.conversation_queue = []
        return

    # whenever a message is posted in slack, Cadocs gets a notification through the new_message method
    def new_message(self, exec_data, channel, user):
        print(exec_data)
        text = exec_data["text"]
        # instantiate the manager which will tell us the intent
        manager = IntentManager()
        # detect the intent
        intent, entities, confidence = manager.detect_intent(text)
        # checking whether or not the entities are valid
        if intent == CadocsIntents.GetSmells:
            if not valid_link(entities[0]):
                return self.error_message("url", channel, user.get('profile').get('first_name'))
        if intent == CadocsIntents.GetSmellsDate:
            if not valid_link(entities[0]) and valid_date(entities[1]):
                return self.error_message("url", channel, user.get('profile').get('first_name'))
            elif not valid_date(entities[1]) and valid_link(entities[0]):
                return self.error_message("date", channel, user.get('profile').get('first_name'))
            elif not valid_link(entities[0]) and not valid_date(entities[1]):
                return self.error_message("date_url", channel, user.get('profile').get('first_name'))
        # checking if the message has enough confidence to be executed directly (otherwise active learning mechanism will start)
        if not exec_data["approved"] and confidence < float(os.environ.get('ACTIVE_LEARNING_THRESHOLD', "0.77")) and confidence >= float(os.environ.get('MINIMUM_CONFIDENCE', "0.55")):
            self.conversation_queue.append(exec_data)
            return self.ask_confirm(intent, channel, user.get('id')), None, None, None
        # if the message can be processed directly
        elif (confidence >= float(os.environ.get('ACTIVE_LEARNING_THRESHOLD', "0.77")) or exec_data["approved"]):
            # we instantiate the resolver of the intents
            resolver = IntentResolver()
            entities.append(user["id"])
            # tell the resolver which intent it has to fire
            results = resolver.resolve_intent(intent, entities)
            # if the intent is report, we have to use previously existing info instead of computed ones
            if (intent == CadocsIntents.Report):
                last_ex = self.get_last_execution(user.get('id'))
                results = last_ex.get('results')
                entities = [last_ex.get('repo'), last_ex.get(
                    'date'), last_ex.get('exec_type')]
            # ask a function to create a slack message
            response = resolver.build_message(
                results, user, channel, intent, entities)
            exec_data.update({"executed": True})
            # we update the conversation history
            self.conversation_queue.append(exec_data)
            # build the text of the message based on the results
            return response, results, entities, intent
        # if the confidence is too low, an error message will be displayed
        elif confidence < float(os.environ.get('MINIMUM_CONFIDENCE', "0.55")):
            return build_error_message(channel, user.get('profile').get('first_name')), None, None, None

    # this method builds a message that will ask the user if
    # the intent was correctly predicted
    # this information will be used to retrain the model

    def ask_confirm(self, intent, channel, user):
        self.asked_user = user
        text = ""
        if intent == CadocsIntents.GetSmells:
            text = "Do you want me to predict community smells?"
        elif intent == CadocsIntents.GetSmellsDate:
            text = "Do you want me to predict community smells starting from a specific date?"
        elif intent == CadocsIntents.Report:
            text = "Do you want me to show a report of your last execution?"
        elif intent == CadocsIntents.Info:
            text = "Do you want to know more about community smells?"
        mess = {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Yes",
                                "emoji": True
                            },
                            "value": "yes",
                            "action_id": "action-yes"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "No",
                                "emoji": True
                            },
                            "value": "no",
                            "action_id": "action-no"
                        }
                    ]
                }
            ]
        }

        return mess

    # this method saves execution results to file system
    # in order to retrieve it when needed
    # we chose the json due to the format of the input
    # and basing on the following study
    # http://matthewrocklin.com/blog/work/2015/03/16/Fast-Serialization

    def save_execution(self, results, exec_type, date, repo, user):
        filename = f'src/executions/executions_{user}.json'
        list_obj = []
        # Check if file exists
        if path.isfile(filename) is False:
            with open(filename, 'w'):
                pass

        with open(filename) as fp:
            try:
                list_obj = json.load(fp)
            except:
                pass
            list_obj.append(
                {
                    "user": user,
                    "exec_type": exec_type,
                    "date": date,
                    "repo": repo,
                    "results": results
                }
            )
        with open(filename, 'w') as json_file:
            json.dump(list_obj, json_file,
                      indent=4,
                      separators=(',', ': '))
        # Read JSON file

    # this method will retrieve the last execution of the current user in order to display it

    def get_last_execution(self, user):
        filename = f'src/executions/executions_{user}.json'
        list_obj = []
        # Check if file exists
        if path.isfile(filename) is False:
            raise Exception("File not found")

        # Read JSON file
        with open(filename) as fp:
            list_obj = json.load(fp)
        return list_obj[list_obj.__len__()-1]

    # error message building for bad requests (messages shown before even executing the tool)
    def error_message(self, error_type, channel, username):
        txt = ""
        if (error_type == "url"):
            txt = "Hi "+username+", there was an error processing your request. \n You provided an invalid repository link. Check the availability of the link on GitHub."
        if (error_type == "date"):
            txt = "Hi "+username+", there was an error processing your request. \n You provided an invalid starting date. Remember that the correct format is MM/DD/YYYY."
        if (error_type == "date_url"):
            txt = "Hi "+username + \
                ", there was an error processing your request. \n You provided an invalid repository link and an invalid starting date. Check both the availability of the link on GitHub and the format of the date (MM/DD/YYYY)."

        return {"channel": channel, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}, None, None, None

    def something_wrong(self, channel):
        return {"channel": channel, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Something went wrong with your request. Please try again",
                "emoji": True
            }
        }]}
