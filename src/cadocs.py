from intent_manager import IntentManager
from intent_resolver import IntentResolver
from utils import CadocsIntents
import json
from os import path

class Cadocs:

    def __init__(self):
        self.last_repo = ""
        return

    def new_message(self, text, channel, user):
        # instantiate the manager which will tell us the intent
        manager = IntentManager()
        # detect the intent
        intent, entities = manager.detect_intent(text)
        if not self.is_locked(entities[0], intent):
            # instantiate the resolver
            resolver = IntentResolver()
            # tell the resolver which intent it has to fire 
            results = resolver.resolve_intent(intent, entities)
            # ask a function to create a slack message
            if(intent == CadocsIntents.Report):
                last_ex = self.get_last_execution(user.get('id'))
                results = last_ex.get('results')
                entities = [last_ex.get('repo'), last_ex.get('date'), last_ex.get('exec_type')]

            response = resolver.build_message(results, user, channel, intent, entities)
            if(intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate):
                self.last_repo = ""
            # build the text of the message based on the results (TODO: generalize)
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

    # this method saves execution results to file system
    # in order to retrieve it when needed
    # we chose the json due to the format of the input
    # and basing on the following study
    # http://matthewrocklin.com/blog/work/2015/03/16/Fast-Serialization
    def save_execution(self, results, exec_type, date, repo, user):
        filename = 'src/executions.json'
        list_obj = []
        # Check if file exists
        if path.isfile(filename) is False:
            raise Exception("File not found")
 
        # Read JSON file
        with open(filename) as fp:
            list_obj = json.load(fp)
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
        


    def get_last_execution(self, user):
        filename = 'src/executions.json'
        list_obj = []
        # Check if file exists
        if path.isfile(filename) is False:
            raise Exception("File not found")
 
        # Read JSON file
        with open(filename) as fp:
            list_obj = json.load(fp)
        user_execs = []
        for ex in list_obj:
            if ex.get('user') == user:
                user_execs.append(ex)
        return user_execs[user_execs.__len__()-1]

    def is_locked(self, repo, intent):

        if repo == self.last_repo and intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
            return True
        else:
            self.last_repo = repo
            return False
    
