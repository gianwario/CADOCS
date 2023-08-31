from src.chatbot.intent_manager import IntentManager
from src.intent_handling.intent_resolver import IntentResolver
from src.chatbot import cadocs_utils
from src.service.cadocs_messages import build_error_message, build_message
from src.intent_handling.cadocs_intents import CadocsIntents
from service.language_handler import LanguageHandler
import os
from dotenv import load_dotenv
from src.service.utils import valid_link, valid_date
load_dotenv('src/.env')

# the Cadocs class contains the logic behind the tool's execution


class CadocsSlack:


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
        # if the confidence is greater than the MINIMUM_CONFIDENCE threshold, the message can be processed directly
        if (confidence > float(os.environ.get('MINIMUM_CONFIDENCE', "0.55"))):
            # we instantiate the resolver of the intents
            resolver = IntentResolver()
            entities.append(user["id"])
            # tell the resolver which intent it has to fire
            results = resolver.resolve_intent(intent, entities)
            # if the intent is report, we have to use previously existing info instead of computed ones
            if (intent == CadocsIntents.Report):
                last_ex = cadocs_utils.get_last_execution(user.get('id'))
                results = last_ex.get('results')
                entities = [last_ex.get('repo'), last_ex.get('date'), last_ex.get('exec_type')]
            # ask a function to create a slack message
            response = build_message(
                results, user, channel, intent, entities)
            exec_data.update({"executed": True})
            # we update the conversation history
            self.conversation_queue.append(exec_data)
            # build the text of the message based on the results
            return response, results, entities, intent
        # if the confidence is too low, an error message will be displayed
        else:
            return build_error_message(channel, user.get('profile').get('first_name')), None, None, None

    # error message building for bad requests (messages shown before even executing the tool)
    def error_message(self, error_type, channel, username):
        lang = LanguageHandler().get_current_language()
        txt = ""
        if lang == "en":           
            if (error_type == "url"):
                txt = "Hi "+username+", there was an error processing your request. \n You provided an invalid repository link. Check the availability of the link on GitHub."
            if (error_type == "date"):
                txt = "Hi "+username+", there was an error processing your request. \n You provided an invalid starting date. Remember that the correct formats are MM/DD/YYYY, MM.DD.YYYY or MM-DD-YYYY."
            if (error_type == "date_url"):
                txt = "Hi "+username + \
                    ", there was an error processing your request. \n You provided an invalid repository link and an invalid starting date. Check both the availability of the link on GitHub and the format of the date (MM/DD/YYYY)."
        elif lang == "it":
            if (error_type == "url"):
                txt = "Ciao "+username+", è stato riscontrato un errore nella elaborazione della sua richiesta. \n È stato fornito un link ad una repository non valido. Verificare la disponibilità del link su GitHub"
            if (error_type == "date"):
                txt = "Ciao "+username+", è stato riscontrato un errore nella elaborazione della sua richiesta. \n È stata fornita una data di inizio non valida. I formati accettati sono: MM/GG/AAAA, MM.GG.AAAA or MM-GG-AAAA."
            if (error_type == "date_url"):
                txt = "Ciao "+username+", è stato riscontrato un errore nella elaborazione della sua richiesta. \
                    \n  Sono stati forniti un link a una repository non valido e una data di inizio non valida. Verificare la disponibilità del link su GitHub e il formato della data (MM/GG/AAAA)."


        return {"channel": channel, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}, None, None, None
    
    def something_wrong(self, channel):

        lang = LanguageHandler().get_current_language()
        txt = ""
        if lang == "en":           
            txt = "Something went wrong with your request. Please try again"
        elif lang == "it":
            txt = "Si è verificato un errore con la sua richiesta. Si prega di riprovare"

        return {"channel": channel, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}
