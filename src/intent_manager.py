from utils import CadocsIntents
import requests

# the Intent Manager is used to detect the Intent behind an user's message
class IntentManager:
    def detect_intent(self, text):
        #
        # intent detection from our nlp model
        # it will return a text that will be transformed into the correspondent enum
        # it could also return the list of entities found in the text (repo link, date, etc)
        #

        req = requests.get('http://localhost:5000/predict?message=' + text)
        results = req.json()
        nlu_intent = results.get('intent').get('intent').get('name')
        nlu_intent_confidence = results.get('intent').get('intent').get('confidence')
        url = results.get('entities').get("url")
        date = results.get("entities").get("date")
        if nlu_intent == "report":
            return CadocsIntents.Report, [], nlu_intent_confidence
        elif nlu_intent == "info":
            return CadocsIntents.Info, [], nlu_intent_confidence
        elif nlu_intent == "get_smells":
            return CadocsIntents.GetSmells, [url], nlu_intent_confidence
        elif nlu_intent == "get_smells_date":
            return CadocsIntents.GetSmellsDate, [url,date], nlu_intent_confidence

