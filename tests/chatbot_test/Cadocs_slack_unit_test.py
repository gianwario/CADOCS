from src.chatbot import cadocs_slack, intent_manager, cadocs_utils
from src.intent_handling import intent_resolver
from src.chatbot.intent_manager import IntentManager
from src.intent_handling.intent_resolver import IntentResolver
from src.intent_handling.cadocs_intents import CadocsIntents
from src.chatbot.cadocs_slack import CadocsSlack
import pytest


class TestCadocsSlackUT:

    @pytest.fixture
    def cadocs_instance(self):
        cadocs = CadocsSlack()
        yield cadocs

    def test_new_message_get_smells_valid_link_high_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https-://github.com/tensorflow/ranking",
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https://github.com/tensorflow/ranking"]
        mocked_confidence = 0.8

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=True)

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock the build_message method
        mocker.patch('src.chatbot.cadocs_slack.build_message',
                            return_value="get smells")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == "get smells"
        assert results == "Test OK"
        assert entities == ["https://github.com/tensorflow/ranking", 1]
        assert intent == CadocsIntents.GetSmells

    def test_new_message_get_smells_valid_link_low_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking",
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https://github.com/tensorflow/ranking"]
        mocked_confidence = 0.2

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=True)

        # Mock the build_error_message method
        mocked_result = "Error message"
        mocker.patch('src.chatbot.cadocs_slack.build_error_message',
                     return_value=mocked_result)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_not_valid_link(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking",
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmells
        mocked_entities = ["https:github.comtensorflowranking"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid link"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)
        # Assertions
        assert response == "Error: Invalid link"

    def test_new_message_get_smells_date_valid_link_valid_date_high_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 12/12/2022",
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = [
            "https://github.com/tensorflow/ranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('src.chatbot.cadocs_slack.valid_date', return_value=True)

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock the build_message method
        mocker.patch('src.chatbot.cadocs_slack.build_message',
                            return_value="get smells date")

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == "get smells date"
        assert results == "Test OK"
        assert entities == [
            "https://github.com/tensorflow/ranking", "12/12/2022", 1]
        assert intent == CadocsIntents.GetSmellsDate

    def test_new_message_get_smells_date_valid_link_valid_date_low_confidence(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https://github.com/tensorflow/ranking from 12/12/2022",
            "executed": False
        }
        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = [
            "https://github.com/tensorflow/ranking", "12/12/2022"]
        mocked_confidence = 0.2

        # Mock the IntentManager object
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('src.chatbot.cadocs_slack.valid_date', return_value=True)

        # Mock the build_error_message method
        mocked_result = "Error message"
        mocker.patch('src.chatbot.cadocs_slack.build_error_message',
                     return_value=mocked_result)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_result
        assert results == None
        assert entities == None
        assert intent == None

    def test_new_message_get_smells_date_not_valid_link(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 12/12/2022",
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https:github.comtensorflowranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=False)

        # Mock the valid_date method
        mocker.patch('src.chatbot.cadocs_slack.valid_date', return_value=True)

        # Mock error_message method
        msg = "Error: Invalid link"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid link"

    def test_new_message_get_smells_date_not_valid_date(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 1212/2022",
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https://github.comtensorflowranking", "1212/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=True)

        # Mock the valid_date method
        mocker.patch('src.chatbot.cadocs_slack.valid_date', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid date"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid date"

    def test_new_message_get_smells_date_not_valid_link_not_valid_date(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you get community smells for this repo https:github.comtensorflowranking from 12/12/2022",
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.GetSmellsDate
        mocked_entities = ["https:github.comtensorflowranking", "12/12/2022"]
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the valid_link method
        mocker.patch('src.chatbot.cadocs_slack.valid_link', return_value=False)

        # Mock the valid_date method
        mocker.patch('src.chatbot.cadocs_slack.valid_date', return_value=False)

        # Mock error_message method
        msg = "Error: Invalid link and date"
        mocker.patch.object(cadocs_instance, 'error_message', return_value=msg)

        response = cadocs_instance.new_message(exec_data, "channel", user)

        # Assertions
        assert response == "Error: Invalid link and date"

    def test_new_message_report(self, cadocs_instance, mocker):
        exec_data = {
            "text": "can you give me your last report",
            "executed": False
        }

        channel = "channel"

        user = {
            "id": 1,
            "username": "user",
            "profile": {"first_name": "user_test"}
        }

        mocked_intent = CadocsIntents.Report
        mocked_entities = []
        mocked_confidence = 0.8

        # Mock detect_intent method of IntentManager class
        mocker.patch.object(IntentManager, 'detect_intent', return_value=(
            mocked_intent, mocked_entities, mocked_confidence))

        # Mock the IntentResolver object
        mocked_results = "Test OK"
        mocker.patch.object(IntentResolver, 'resolve_intent',
                            return_value=(mocked_results))

        # Mock get_last_execution method
        mocked_last_ex = {"results": "Test OK", "repo": "https://github.com/tensorflow/ranking",
                          "date": "12/12/2022", "exec_type": "get_smells"}
        mocker.patch("src.chatbot.cadocs_utils.get_last_execution", return_value=mocked_last_ex)

        # Mock build_message method
        mocked_response = "Report message"
        mocker.patch('src.chatbot.cadocs_slack.build_message',
                            return_value=mocked_response)

        response, results, entities, intent = cadocs_instance.new_message(
            exec_data, "channel", user)

        # Assertions
        assert response == mocked_response
        assert results == "Test OK"
        assert entities == [
            "https://github.com/tensorflow/ranking", "12/12/2022", "get_smells"]
        assert intent == CadocsIntents.Report

    def test_error_message_url(self, cadocs_instance, mocker):
        error_type = "url"
        username_test = "user_test"
        channel_test = 1

        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="en")

        txt = "Hi "+username_test+", there was an error processing your request. \n You provided an invalid repository link. Check the availability of the link on GitHub."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_error_message_url_it(self, cadocs_instance, mocker):
        error_type = "url"
        username_test = "user_test"
        channel_test = 1

        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="it")

        txt = "Ciao "+username_test+", è stato riscontrato un errore nella elaborazione della sua richiesta. \n È stato fornito un link ad una repository non valido. Verificare la disponibilità del link su GitHub"
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None    

    def test_error_message_date(self, cadocs_instance, mocker):
        error_type = "date"
        username_test = "user_test"
        channel_test = 1
        
        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="en")

        txt = "Hi "+username_test+", there was an error processing your request. \n You provided an invalid starting date. Remember that the correct formats are MM/DD/YYYY, MM.DD.YYYY or MM-DD-YYYY."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_error_message_date_it(self, cadocs_instance, mocker):
        error_type = "date"
        username_test = "user_test"
        channel_test = 1
        
        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="it")

        txt = "Ciao "+username_test+", è stato riscontrato un errore nella elaborazione della sua richiesta. \n È stata fornita una data di inizio non valida. I formati accettati sono: MM/GG/AAAA, MM.GG.AAAA or MM-GG-AAAA."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None    

    def test_error_message_date_url(self, cadocs_instance, mocker):
        error_type = "date_url"
        username_test = "user_test"
        channel_test = 1

        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="en")

        txt = "Hi "+username_test + \
            ", there was an error processing your request. \n You provided an invalid repository link and an invalid starting date. Check both the availability of the link on GitHub and the format of the date (MM/DD/YYYY)."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None

    def test_error_message_date_url_it(self, cadocs_instance, mocker):
        error_type = "date_url"
        username_test = "user_test"
        channel_test = 1

        # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="it")

        txt = "Ciao "+username_test+", è stato riscontrato un errore nella elaborazione della sua richiesta. \
                    \n  Sono stati forniti un link a una repository non valido e una data di inizio non valida. Verificare la disponibilità del link su GitHub e il formato della data (MM/GG/AAAA)."
        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": txt,
                "emoji": True
            }
        }]}

        response1, response2, response3, response4 = cadocs_instance.error_message(
            error_type, channel_test, username_test)

        # Assertions
        assert response1 == expected_response
        assert response2 == None
        assert response3 == None
        assert response4 == None    

    def test_something_wrong(self, cadocs_instance, mocker):
        channel_test = 1

         # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="en")

        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Something went wrong with your request. Please try again",
                "emoji": True
            }
        }]}
        response = cadocs_instance.something_wrong(channel_test)

        # Assertions
        assert response == expected_response

    def test_something_wrong_it(self, cadocs_instance, mocker):
        channel_test = 1

         # Mock of LanguageHandler.get_current_language method of the CadocsSlack module
        mocker.patch('src.chatbot.cadocs_slack.LanguageHandler.get_current_language', return_value="it")

        expected_response = {"channel": channel_test, "blocks": [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Si è verificato un errore con la sua richiesta. Si prega di riprovare",
                "emoji": True
            }
        }]}
        response = cadocs_instance.something_wrong(channel_test)

        # Assertions
        assert response == expected_response