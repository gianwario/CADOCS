from utils import CadocsIntents

class IntentManager:
    def detect_intent(self, text):
        #
        # TODO: intent detection from our nlp model
        # it will return a text that will be transformed into the correspondent enum
        # it could also return the list of entities found in the text (repo link, date, etc)
        #
        entities = ["https://github.com/tensorflow/ranking"]
        # we assume for now the intent is get_smells
        return CadocsIntents.GetSmells, entities

