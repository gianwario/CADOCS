from intent_manager import IntentManager
from intent_resolver import IntentResolver
from utils import CadocsIntents
import json
from os import path
import os
from dotenv import load_dotenv
load_dotenv('src/.env')

class Cadocs:

    def __init__(self):
        self.last_repo = ""
        self.asked_user= ""
        # the conversation queue will be used to check whether or not a message has already been answered
        self.conversation_queue = []
        return

    def new_message(self, exec_data, channel, user):
        print(exec_data)
        text = exec_data["text"]
        # instantiate the manager which will tell us the intent
        manager = IntentManager()
        # detect the intent
        intent, entities, confidence = manager.detect_intent(text)
        if not exec_data["approved"] and confidence < float(os.environ.get('ACTIVE_LEARNING_THRESHOLD',"0.77")) and confidence >= float(os.environ.get('MINIMUM_CONFIDENCE',"0.55")):
            self.conversation_queue.append(exec_data)
            return self.ask_confirm(intent.value, channel, user.get('id')), None, None, None
        elif not self.is_locked(entities[0], intent) and (confidence >= float(os.environ.get('ACTIVE_LEARNING_THRESHOLD',"0.77")) or exec_data["approved"]):
            # instantiate the resolver
            resolver = IntentResolver()
            # tell the resolver which intent it has to fire
            entities.append(user["id"])
            results = resolver.resolve_intent(intent, entities)
            # ask a function to create a slack message
            if(intent == CadocsIntents.Report):
                last_ex = self.get_last_execution(user.get('id'))
                results = last_ex.get('results')
                entities = [last_ex.get('repo'), last_ex.get('date'), last_ex.get('exec_type')]

            response = resolver.build_message(results, user, channel, intent, entities)
            if(intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate):
                self.last_repo = ""
            exec_data.update({"executed" : True})
            self.conversation_queue.append(exec_data)
            # build the text of the message based on the results
            return response, results, entities, intent
        else:
            return {"channel":channel, "blocks":[{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Wait",
				"emoji": True
			}
		}]}, None, None, None


    # this method build a message that will ask the user if
    # the intent was correctly predicted
    # this information will be used to retrain the model
    def ask_confirm(self, intent, channel, user):
        self.asked_user = user
        mess = {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Was this your intent? "+ intent
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
            print(list_obj)
            list_obj.append(
            {
                "user": user,
                "exec_type": exec_type,
                "date": date,
                "repo": repo,
                "results":results
            }
        )
        with open(filename, 'w') as json_file:
                json.dump(list_obj, json_file, 
                            indent=4,  
                            separators=(',',': '))
        # Read JSON file


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

    def is_locked(self, repo, intent):

        if repo == self.last_repo and (intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate):
            return True
        else:
            self.last_repo = repo
            return False
    
