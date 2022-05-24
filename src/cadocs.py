from intent_manager import IntentManager
from intent_resolver import IntentResolver
from utils import CadocsIntents

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
        return response, results, entities, intent

    def save_execution(self, results, exec_type, date, repo):
        self.results = results
        self.exec_type = exec_type
        self.date = date
        self.repo = repo
    
    def get_last_execution(self):
        return self.results, self.exec_type, self.date, self.repo
    
