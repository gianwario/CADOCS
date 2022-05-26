from utils import CadocsIntents

# the Intent Manager is used to detect the Intent behind an user's message
class IntentManager:
    def detect_intent(self, text):
        #
        # TODO: intent detection from our nlp model
        # it will return a text that will be transformed into the correspondent enum
        # it could also return the list of entities found in the text (repo link, date, etc)
        #
        entities = ["https://github.com/tensorflow/ranking"]
        
        if text == "report":
            
            return CadocsIntents.Report, []
        elif text == "info":
            return CadocsIntents.Info, []
        else:
            return CadocsIntents.GetSmells, entities

